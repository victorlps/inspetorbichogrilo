"""End-to-end post-approval orchestrator: validate Portao 3, sync affiliate short links, deploy GitHub Pages vitrine, verify live URL, and publish to YouTube + Instagram + TikTok."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.publish.affiliate_links import sync_affiliate_links  # noqa: E402
from src.publish.playwright_publish import run_publish  # noqa: E402
from src.video.validate_gates import validate_portao_3  # noqa: E402

VITRINE_LIVE_JSON = "https://victorlps.github.io/inspetorbichogrilo/catalogo.json"


def _resilient_git_push() -> None:
    """Push unpushed commits incrementally with 500MB http.postBuffer to avoid GitHub HTTP 408 on video packs."""
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
                    "http.postBuffer=524288000",
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
        raise ValueError(f"Código curto IBG-XXX não encontrado em {product_dir / 'pacote.md'}")
    return m.group(1)


def _wait_for_vitrine_live(code: str, timeout_s: int = 120) -> bool:
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        try:
            req = urllib.request.Request(
                f"{VITRINE_LIVE_JSON}?t={int(time.time())}",
                headers={"Cache-Control": "no-cache"},
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            if any(p.get("codigo") == code and p.get("ativo") for p in data.get("produtos", [])):
                return True
        except Exception:
            pass
        time.sleep(5.0)
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description="Fluxo autônomo completo de publicação pós-aceite (Portão 3 -> Vitrine -> Redes).")
    parser.add_argument("--product-dir", type=Path, required=True, help="Caminho para produtos/<slug>")
    parser.add_argument("--platform", choices=["youtube", "instagram", "tiktok", "all", "none"], default="all")
    parser.add_argument("--skip-push", action="store_true", help="Pula git push caso já publicado no remoto")
    parser.add_argument("--offscreen", action="store_true", help="Executa navegador fora da área visível")
    args = parser.parse_args()

    prod_dir = args.product_dir.resolve()
    code = _extract_vitrine_code(prod_dir)
    print(f"[1/5] Validando Portão 3 e catálogo local para {prod_dir.name} ({code})...")
    ok, errs, stats = validate_portao_3(prod_dir)
    if not ok:
        for e in errs:
            print("  ERRO:", e, file=sys.stderr)
        return 1
    json.loads((REPO_ROOT / "vitrine" / "catalogo.json").read_text(encoding="utf-8"))

    print(f"[2/5] Sincronizando links curtos de afiliado para {code}...")
    aff_res = sync_affiliate_links(code=code, product_dir=prod_dir)
    print("  Afiliados:", json.dumps(aff_res, ensure_ascii=False))
    if aff_res.get("converted", 0) > 0:
        subprocess.run(
            ["git", "add", "vitrine/catalogo.json", str(prod_dir / "pacote.md")],
            cwd=REPO_ROOT,
            check=True,
        )
        subprocess.run(
            ["git", "commit", "-m", f"chore(vitrine): atualiza links curtos de afiliado de {code}"],
            cwd=REPO_ROOT,
            check=True,
        )

    if not args.skip_push:
        print("[3/5] Publicando vitrine no GitHub Pages (git push incremental)...")
        _resilient_git_push()
    else:
        print("[3/5] git push ignorado (--skip-push).")

    print(f"[4/5] Aguardando {code} ficar ativo em {VITRINE_LIVE_JSON}...")
    is_live = _wait_for_vitrine_live(code, timeout_s=110)
    print(f"  Vitrine pública {code} online: {is_live}")

    if args.platform == "none":
        print("[5/5] Upload em plataformas ignorado (--platform none).")
        return 0

    platforms = ["youtube", "instagram", "tiktok"] if args.platform == "all" else [args.platform]
    print(f"[5/5] Publicando {prod_dir.name} em {', '.join(platforms)}...")
    pub_res = run_publish(
        product_dir=prod_dir,
        platforms=platforms,
        do_publish=True,
        no_wait=True,
        offscreen=args.offscreen,
    )
    print("RESUMO_FINAL:", json.dumps({"code": code, "vitrine_live": is_live, "affiliates": aff_res, "platforms": pub_res}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
