"""Automated Affiliate Short-Link Generator & Eligibility Verifier for Mercado Livre Afiliados & Amazon Associados.

Architecture:
1. Probes sessions invisibly first (--headless=new with standard desktop Chrome User-Agent) in ~/.cache/inspetorbichogrilo-pw-profile.
2. Supports --verify-urls in Portao 1 so @Curador confirms 100% affiliate eligibility before selecting SKUs in ficha.md, and --include-inactive in Portao 3 so vitrine/catalogo.json has 100% meli.la/amzn.to links ready while 'ativo': false (REQ-008).
3. When initial authentication is needed, opens one visible Chrome window with dedicated tabs per marketplace, preserving each tab until login completes.
"""

from __future__ import annotations

import argparse
import json
import re
import time
from pathlib import Path
from typing import Any

from playwright.sync_api import BrowserContext, Page, sync_playwright

REPO_ROOT = Path(__file__).resolve().parents[2]
PW_PROFILE_DIR = Path.home() / ".cache" / "inspetorbichogrilo-pw-profile"
CATALOGO_PATH = REPO_ROOT / "vitrine" / "catalogo.json"
ML_LINKBUILDER_URL = "https://www.mercadolivre.com.br/afiliados/linkbuilder"
AMZ_ASSOCIATES_URL = "https://associados.amazon.com.br/"

SHORT_DOMAINS = (
    "https://meli.la/",
    "https://mercadolivre.com/sec/",
    "https://www.mercadolivre.com.br/sec/",
    "https://amzn.to/",
)


def _is_already_short_affiliate(url: str) -> bool:
    u = url.strip()
    return u.startswith(SHORT_DOMAINS) or "tag=" in u or "matt_tool=" in u


def _launch_profile(p: Any, headless_new: bool) -> BrowserContext:
    PW_PROFILE_DIR.mkdir(parents=True, exist_ok=True)
    args = ["--disable-blink-features=AutomationControlled"]
    kwargs: dict[str, Any] = {}
    if headless_new:
        args.append("--headless=new")
        kwargs["user_agent"] = (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        )
    return p.chromium.launch_persistent_context(
        user_data_dir=str(PW_PROFILE_DIR),
        channel="chrome",
        headless=False,
        viewport={"width": 1280, "height": 900},
        args=args,
        **kwargs,
    )


def _is_ml_logged_in(page: Page) -> bool:
    u = page.url.lower()
    if "/login" in u or "jms/mlb/lgz" in u or "identification" in u:
        return False
    return "/afiliados/linkbuilder" in u and page.locator("textarea#url-0").count() > 0


def _is_amz_sitestripe_ready(page: Page) -> bool:
    return page.locator("#amzn-ss-text-link, #AssociatesBar, [id*='sitestripe']").count() > 0


def _generate_ml_short_link_on_page(page: Page, target_url: str) -> str | None:
    # Always load clean Linkbuilder state so 'Gerar' button is fresh for every URL
    page.goto(ML_LINKBUILDER_URL, wait_until="domcontentloaded", timeout=60000)
    time.sleep(2.5)
    if not _is_ml_logged_in(page):
        return None

    # Paste target URL specifically into Linkbuilder's #url-0 textarea firing React input events
    box = page.locator("textarea#url-0").first
    box.wait_for(state="visible", timeout=20000)
    box.click()
    page.keyboard.press("Meta+A")
    page.keyboard.press("Backspace")
    page.keyboard.insert_text(target_url)
    time.sleep(1.0)

    before_vals = set(
        re.findall(
            r"https://(?:meli\.la/[A-Za-z0-9_-]+|(?:www\.)?mercadolivre\.com(?:\.br)?/sec/[A-Za-z0-9_-]+)",
            page.evaluate("() => Array.from(document.querySelectorAll('textarea,input')).map(e=>e.value||'').join('\\n') + '\\n' + document.body.innerText"),
        )
    )

    gen_btn = page.locator("button:has-text('Gerar'):not([disabled])").first
    try:
        gen_btn.wait_for(state="visible", timeout=10000)
        gen_btn.click()
    except Exception:
        return None

    for _ in range(20):
        time.sleep(0.8)
        after_txt = page.evaluate(
            "() => Array.from(document.querySelectorAll('textarea,input')).map(e=>e.value||'').join('\\n') + '\\n' + document.body.innerText"
        )
        found = re.findall(
            r"https://(?:meli\.la/[A-Za-z0-9_-]+|(?:www\.)?mercadolivre\.com(?:\.br)?/sec/[A-Za-z0-9_-]+)",
            after_txt,
        )
        new_links = [lk for lk in found if lk not in before_vals]
        if new_links:
            return new_links[-1]
        if found:
            return found[-1]
    return None


def _generate_amz_short_link_on_page(page: Page, target_url: str) -> str | None:
    page.goto(target_url, wait_until="domcontentloaded", timeout=30000)
    time.sleep(2.5)
    if not _is_amz_sitestripe_ready(page):
        return None
    txt_btn = page.locator("#amzn-ss-text-link a, [data-action*='sitestripe-text'], a:has-text('Texto')").first
    if txt_btn.count() > 0 and txt_btn.is_visible():
        txt_btn.click()
        time.sleep(1.8)
    short_input = page.locator(
        "#amzn-ss-text-shortlink-textarea, textarea[id*='shortlink'], input[id*='shortlink']"
    ).first
    if short_input.count() > 0:
        val = short_input.input_value().strip()
        if val.startswith("https://amzn.to/") or "tag=" in val:
            return val
    return None


def verify_candidate_urls(urls: list[str]) -> dict[str, str | None]:
    """Verify and convert candidate marketplace URLs invisibly during Portao 1 / Portao 3 curation."""
    results: dict[str, str | None] = {}
    with sync_playwright() as p:
        ctx = _launch_profile(p, headless_new=True)
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        for raw_u in urls:
            u = raw_u.strip()
            if _is_already_short_affiliate(u):
                results[u] = u
            elif "mercadolivre.com.br" in u:
                results[u] = _generate_ml_short_link_on_page(page, u)
            elif "amazon.com.br" in u:
                results[u] = _generate_amz_short_link_on_page(page, u)
            else:
                results[u] = None
        ctx.close()
    return results


def sync_affiliate_links(
    code: str | None = None,
    catalogo_path: Path = CATALOGO_PATH,
    product_dir: Path | None = None,
    wait_for_login_s: int = 300,
    include_inactive: bool = True,
) -> dict[str, Any]:
    """Convert canonical URLs in vitrine/catalogo.json to short affiliate links (including pre-publish 'ativo': false cards)."""
    data = json.loads(catalogo_path.read_text(encoding="utf-8"))

    ml_candidates: list[tuple[dict[str, Any], str]] = []
    amz_candidates: list[tuple[dict[str, Any], str]] = []

    for prod in data.get("produtos", []):
        if code and prod.get("codigo") != code:
            continue
        if not include_inactive and not prod.get("ativo"):
            continue
        for var in prod.get("variacoes", []):
            url = str(var.get("url", "")).strip()
            if not url or _is_already_short_affiliate(url):
                continue
            if "mercadolivre.com.br" in url:
                ml_candidates.append((var, url))
            elif "amazon.com.br" in url:
                amz_candidates.append((var, url))

    total_candidates = len(ml_candidates) + len(amz_candidates)
    if total_candidates == 0:
        return {"checked": 0, "converted": 0, "mapping": {}, "session_missing": []}

    converted: dict[str, str] = {}
    need_ml_login = False
    need_amz_login = False

    # Phase 1: Invisible probe (--headless=new) — zero windows on desktop if already logged in!
    with sync_playwright() as p:
        ctx = _launch_profile(p, headless_new=True)
        if ml_candidates:
            pg_ml = ctx.pages[0] if ctx.pages else ctx.new_page()
            pg_ml.goto(ML_LINKBUILDER_URL, wait_until="domcontentloaded", timeout=30000)
            time.sleep(3.0)
            if _is_ml_logged_in(pg_ml):
                for var_obj, orig_url in ml_candidates:
                    s = converted.get(orig_url) or _generate_ml_short_link_on_page(pg_ml, orig_url)
                    if s:
                        converted[orig_url] = s
                        var_obj["url"] = s
            else:
                need_ml_login = True

        if amz_candidates:
            pg_amz = ctx.new_page()
            pg_amz.goto(amz_candidates[0][1], wait_until="domcontentloaded", timeout=30000)
            time.sleep(2.5)
            if _is_amz_sitestripe_ready(pg_amz):
                for var_obj, orig_url in amz_candidates:
                    s = converted.get(orig_url) or _generate_amz_short_link_on_page(pg_amz, orig_url)
                    if s:
                        converted[orig_url] = s
                        var_obj["url"] = s
            else:
                need_amz_login = True
        ctx.close()

    # Phase 2: When initial login is needed and wait_for_login_s > 0, open one visible window with dedicated tabs per marketplace
    session_missing: list[str] = []
    if (need_ml_login or need_amz_login) and wait_for_login_s > 0:
        print(
            f"[affiliate_links] Abrindo janela visível em abas separadas para login único "
            f"(ML={need_ml_login}, Amazon={need_amz_login}) — aguardando até {wait_for_login_s}s..."
        )
        with sync_playwright() as p:
            ctx = _launch_profile(p, headless_new=False)
            ml_tab: Page | None = None
            amz_tab: Page | None = None

            if need_ml_login:
                ml_tab = ctx.pages[0] if ctx.pages else ctx.new_page()
                ml_tab.goto(ML_LINKBUILDER_URL, wait_until="domcontentloaded", timeout=45000)
            if need_amz_login:
                amz_tab = ctx.new_page() if (need_ml_login or not ctx.pages) else ctx.pages[0]
                amz_tab.goto(amz_candidates[0][1], wait_until="domcontentloaded", timeout=45000)
            if ml_tab is not None:
                ml_tab.bring_to_front()

            deadline = time.time() + wait_for_login_s
            ml_done = not need_ml_login
            amz_done = not need_amz_login

            while time.time() < deadline and not (ml_done and amz_done):
                time.sleep(2.5)
                if not ml_done and ml_tab is not None:
                    if ml_tab.is_closed():
                        break
                    try:
                        if _is_ml_logged_in(ml_tab):
                            print("[affiliate_links] Login do Mercado Livre detectado! Gerando links meli.la...")
                            for var_obj, orig_url in ml_candidates:
                                s = converted.get(orig_url) or _generate_ml_short_link_on_page(ml_tab, orig_url)
                                if s:
                                    converted[orig_url] = s
                                    var_obj["url"] = s
                            ml_done = True
                    except Exception:
                        pass

                if not amz_done and amz_tab is not None:
                    if amz_tab.is_closed():
                        amz_done = True
                        continue
                    try:
                        if _is_amz_sitestripe_ready(amz_tab):
                            print("[affiliate_links] Barra SiteStripe da Amazon detectada! Gerando link amzn.to...")
                            for var_obj, orig_url in amz_candidates:
                                s = converted.get(orig_url) or _generate_amz_short_link_on_page(amz_tab, orig_url)
                                if s:
                                    converted[orig_url] = s
                                    var_obj["url"] = s
                            amz_done = True
                    except Exception:
                        pass

            if not ml_done:
                session_missing.append("mercado_livre_afiliados")
            if not amz_done:
                session_missing.append("amazon_associados")
            ctx.close()
    else:
        if need_ml_login:
            session_missing.append("mercado_livre_afiliados")
        if need_amz_login:
            session_missing.append("amazon_associados")

    if converted:
        catalogo_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        if product_dir and (product_dir / "pacote.md").exists():
            p_txt = (product_dir / "pacote.md").read_text(encoding="utf-8")
            for orig_u, short_u in converted.items():
                p_txt = p_txt.replace(orig_u, short_u)
            (product_dir / "pacote.md").write_text(p_txt, encoding="utf-8")

    failed_urls = [
        orig_u
        for _, orig_u in (ml_candidates + amz_candidates)
        if orig_u not in converted
    ]
    return {
        "checked": total_candidates,
        "converted": len(converted),
        "failed_urls": failed_urls,
        "mapping": converted,
        "session_missing": session_missing,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Valida elegibilidade e converte URLs canônicas em links curtos de afiliado.")
    parser.add_argument("--code", type=str, default=None, help="Código curto do produto (ex.: IBG-002)")
    parser.add_argument("--product-dir", type=Path, default=None, help="Pasta opcional produtos/<slug>")
    parser.add_argument("--login-timeout", type=int, default=300, help="Segundos aguardando login único em abas dedicadas")
    parser.add_argument("--verify-urls", nargs="*", default=None, help="Testa elegibilidade de URLs candidatas no Portão 1 sem alterar arquivos")
    args = parser.parse_args()

    if args.verify_urls is not None:
        v_res = verify_candidate_urls(args.verify_urls)
        print(json.dumps(v_res, ensure_ascii=False, indent=2))
        return 0 if all(v_res.values()) else 1

    res = sync_affiliate_links(code=args.code, product_dir=args.product_dir, wait_for_login_s=args.login_timeout)
    print(json.dumps(res, ensure_ascii=False, indent=2))
    if res["session_missing"] or res["failed_urls"]:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
