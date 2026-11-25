"""End-to-end post-approval publisher (ADR 0011):
1. Deterministically validates Portao 3 + platform syntax + vitrine entry.
2. Enforces 100% monetized short affiliate links (meli.la / amzn.to / tag=) BEFORE pushing or uploading any video.
3. Activates card in vitrine/catalogo.json, pushes lightweight metadata to GitHub Pages, and confirms 100% affiliate links live on the public CDN.
4. Dispatches uploads using Official HTTP APIs first when configured and eligible (YouTube Data API v3, Instagram Graph API <=90s), falling back seamlessly to hardened Playwright studio flows (Meta Business Suite FB+IG cross-post / >90s / REQ-007, and TikTok Studio).
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
import urllib.request
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.publish.affiliate_links import _is_already_short_affiliate, sync_affiliate_links  # noqa: E402
from src.publish.meta_graph_upload import has_ig_graph_ready, upload_reel_graph_api  # noqa: E402
from src.publish.playwright_publish import load_pacote_metadata, run_publish  # noqa: E402
from src.publish.youtube_upload import has_youtube_oauth_ready, upload_short  # noqa: E402
from src.video.validate_gates import _ffprobe_streams, validate_portao_3  # noqa: E402

VITRINE_LIVE_JSON = "https://victorlps.github.io/inspetorbichogrilo/catalogo.json"
CATALOGO_PATH = REPO_ROOT / "vitrine" / "catalogo.json"


def _resilient_git_push() -> None:
    """Push unpushed commits incrementally over HTTP/1.1."""
    revs_out = subprocess.check_output(
        ["git", "rev-list", "--reverse", "origin/master..HEAD"],
        cwd=REPO_ROOT,
        text=True,
    ).strip()
    commits = [c.strip() for c in revs_out.splitlines() if c.strip()]
    if not commits:
        print("  Nenhum commit pendente para enviar.")
        return

    for sha in commits:
        for attempt in range(3):
            res = subprocess.run(
                [
                    "git",
                    "-c",
                    "http.version=HTTP/1.1",
                    "-c",
                    "http.lowSpeedLimit=1000",
                    "-c",
                    "http.lowSpeedTime=180",
                    "push",
                    "origin",
                    f"{sha}:refs/heads/master",
                ],
                cwd=REPO_ROOT,
            )
            if res.returncode == 0:
                break
            time.sleep(3.0 * (attempt + 1))
        else:
            raise RuntimeError(f"Falha ao enviar commit {sha} após 3 tentativas.")


def _extract_vitrine_code(product_dir: Path) -> str:
    pacote = (product_dir / "pacote.md").read_text(encoding="utf-8")
    m = re.search(r"\b(IBG-\d{3,})\b", pacote)
    if not m:
        raise ValueError(f"Código curto IBG-XXX ausente em {product_dir / 'pacote.md'}")
    return m.group(1)


def _activate_and_verify_local_catalogo(code: str) -> tuple[bool, list[str]]:
    """Ensure card is marked ativo=True and 100% of its variations have monetized affiliate links."""
    data = json.loads(CATALOGO_PATH.read_text(encoding="utf-8"))
    card = next((p for p in data.get("produtos", []) if p.get("codigo") == code), None)
    if card is None:
        return False, [f"Card {code} ausente em vitrine/catalogo.json"]

    changed = False
    if not card.get("ativo"):
        card["ativo"] = True
        changed = True
    if changed:
        CATALOGO_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    variacoes = card.get("variacoes", [])
    if not variacoes:
        return changed, [f"Card {code} sem variações em vitrine/catalogo.json"]

    bad = [
        f"{v.get('rotulo', '?')}: {v.get('url', '')}"
        for v in variacoes
        if not _is_already_short_affiliate(str(v.get("url", "")))
    ]
    return changed, bad


def _wait_for_vitrine_live_monetized(code: str, timeout_s: int = 120) -> bool:
    """Confirm card is active on live GitHub Pages AND 100% of its live URLs are monetized affiliate links."""
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        try:
            req = urllib.request.Request(
                f"{VITRINE_LIVE_JSON}?t={int(time.time())}",
                headers={"Cache-Control": "no-cache"},
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            card = next((p for p in data.get("produtos", []) if p.get("codigo") == code and p.get("ativo")), None)
            if card:
                vars_live = card.get("variacoes", [])
                if vars_live and all(_is_already_short_affiliate(str(v.get("url", ""))) for v in vars_live):
                    return True
        except Exception:
            pass
        time.sleep(5.0)
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description="Orquestrador híbrido de publicação pós-aceite com trava 100% de afiliados.")
    parser.add_argument("--product-dir", type=Path, required=True, help="Caminho para produtos/<slug>")
    parser.add_argument("--platform", choices=["youtube", "instagram", "tiktok", "all", "none"], default="all")
    parser.add_argument("--login-timeout", type=int, default=300, help="Segundos aguardando login único quando necessário")
    parser.add_argument("--skip-push", action="store_true", help="Pula git push caso já sincronizado no remoto")
    args = parser.parse_args()

    prod_dir = args.product_dir.resolve()
    code = _extract_vitrine_code(prod_dir)

    print(f"[1/5] Sincronizando links curtos de afiliado para {code} antes da validação final...")
    aff_res = sync_affiliate_links(code=code, product_dir=prod_dir, wait_for_login_s=args.login_timeout, include_inactive=True)
    print("  Afiliados:", json.dumps(aff_res, ensure_ascii=False))

    activated, bad_links = _activate_and_verify_local_catalogo(code)
    if bad_links:
        print(
            "BLOQUEIO PRÉ-PUBLICAÇÃO: existem variações sem link de afiliado comissionado em vitrine/catalogo.json:\n  - "
            + "\n  - ".join(bad_links),
            file=sys.stderr,
        )
        return 2

    print(f"[2/5] Validando Portão 3 completo (vídeo + sintaxe de plataformas + vitrine 100% afiliada) para {code}...")
    ok, errs, _ = validate_portao_3(prod_dir, require_vitrine_entry=True)
    if not ok:
        for e in errs:
            print("  ERRO:", e, file=sys.stderr)
        return 1

    # Commit catalogo.json / pacote.md updates if changed
    status_out = subprocess.check_output(
        ["git", "status", "--porcelain", "vitrine/catalogo.json", str(prod_dir / "pacote.md")],
        cwd=REPO_ROOT,
        text=True,
    ).strip()
    if status_out:
        subprocess.run(["git", "add", "vitrine/catalogo.json", str(prod_dir / "pacote.md")], cwd=REPO_ROOT, check=True)
        subprocess.run(
            ["git", "commit", "-m", f"chore(vitrine): ativa {code} com 100% links de afiliado verificados"],
            cwd=REPO_ROOT,
            check=True,
        )

    if not args.skip_push:
        print("[3/5] Publicando vitrine no GitHub Pages...")
        _resilient_git_push()

    print(f"[4/5] Confirmando {code} ativo e 100% comissionado em {VITRINE_LIVE_JSON}...")
    is_live = _wait_for_vitrine_live_monetized(code, timeout_s=120)
    if not is_live:
        print(f"ERRO: {code} ainda não consta 100% ativo/comissionado no GitHub Pages — abortando antes do envio de vídeos.", file=sys.stderr)
        return 3
    print(f"  Vitrine pública {code} 100% verificada no ar!")

    if args.platform == "none":
        print("[5/5] Upload em redes ignorado (--platform none).")
        return 0

    requested = ["youtube", "instagram", "tiktok"] if args.platform == "all" else [args.platform]
    meta = load_pacote_metadata(prod_dir)
    probe = _ffprobe_streams(meta.video_path)
    duration_s = float(probe.get("format", {}).get("duration", 0.0))

    api_results: list[dict[str, Any]] = []
    pw_platforms: list[str] = []

    for plat in requested:
        if plat == "youtube" and has_youtube_oauth_ready():
            try:
                print("[5/5] Enviando YouTube Shorts via API oficial (YouTube Data API v3)...")
                yt_resp = upload_short(
                    video_path=meta.video_path,
                    title=meta.youtube_title,
                    description=meta.youtube_description,
                    tags=["ComoFunciona", "Ciencia", "InspetorBichoGrilo", "Shorts"],
                    privacy="public",
                    contains_synthetic_media=meta.ai_disclosure,
                )
                vid_id = yt_resp.get("id", "")
                api_results.append({"platform": "youtube", "method": "youtube_data_api_v3", "published": True, "url": f"https://youtube.com/shorts/{vid_id}"})
                continue
            except Exception as exc:
                print(f"[YouTube API] Falha ({exc}); acionando fallback Playwright...")
                pw_platforms.append("youtube")
        elif plat == "instagram" and has_ig_graph_ready() and duration_s <= 90.0 and not meta.ai_disclosure:
            try:
                print("[5/5] Enviando Instagram Reel via API oficial (Meta Graph API Resumable)...")
                ig_resp = upload_reel_graph_api(meta.video_path, meta.instagram_caption)
                api_results.append(ig_resp)
                continue
            except Exception as exc:
                print(f"[Meta Graph API] Falha ({exc}); acionando fallback Meta Business Suite...")
                pw_platforms.append("instagram")
        else:
            pw_platforms.append(plat)

    pw_results: list[dict[str, Any]] = []
    if pw_platforms:
        print(f"[5/5] Publicando via perfil autenticado Playwright em: {', '.join(pw_platforms)}...")
        pw_results = run_publish(product_dir=prod_dir, platforms=pw_platforms, do_publish=True, no_wait=True, offscreen=False)

    all_res = api_results + pw_results
    print("RESUMO_FINAL:", json.dumps({"code": code, "vitrine_live": is_live, "affiliates": aff_res, "platforms": all_res}, ensure_ascii=False))
    return 0 if all(r.get("published") for r in all_res) else 4


if __name__ == "__main__":
    raise SystemExit(main())
