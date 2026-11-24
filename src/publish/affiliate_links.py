"""Automated Affiliate Short-Link Generator for Mercado Livre Afiliados & Amazon Associados.

Uses the shared persistent Playwright Chrome profile (~/.cache/inspetorbichogrilo-pw-profile)
to convert canonical marketplace URLs in vitrine/catalogo.json (and pacote.md) into official
affiliate short links (https://meli.la/... and https://amzn.to/...) whenever the affiliate
session is authenticated in the profile.
"""

from __future__ import annotations

import argparse
import json
import re
import time
from pathlib import Path
from typing import Any

from playwright.sync_api import BrowserContext, sync_playwright

REPO_ROOT = Path(__file__).resolve().parents[2]
PW_PROFILE_DIR = Path.home() / ".cache" / "inspetorbichogrilo-pw-profile"
CATALOGO_PATH = REPO_ROOT / "vitrine" / "catalogo.json"
ML_LINKBUILDER_URL = "https://www.mercadolivre.com.br/afiliados/linkbuilder"

SHORT_DOMAINS = ("https://meli.la/", "https://mercadolivre.com/sec/", "https://www.mercadolivre.com.br/sec/", "https://amzn.to/")


def _is_already_short_affiliate(url: str) -> bool:
    u = url.strip()
    return u.startswith(SHORT_DOMAINS) or "tag=" in u or "matt_tool=" in u


def _shorten_ml_url_in_linkbuilder(ctx: BrowserContext, target_url: str) -> str | None:
    """Shorten a canonical Mercado Livre URL via /afiliados/linkbuilder if logged in."""
    page = ctx.new_page()
    try:
        page.goto(ML_LINKBUILDER_URL, wait_until="domcontentloaded", timeout=30000)
        time.sleep(3.0)
        if "/login" in page.url or "jms/mlb/lgz" in page.url:
            return None

        # Locate URL input/textarea in Mercado Livre Linkbuilder
        box = page.locator("textarea, input[type='text'], input[type='url']").first
        if box.count() == 0:
            return None
        box.click()
        box.fill(target_url)
        time.sleep(0.5)

        gen_btn = page.locator(
            "button:has-text('Gerar'), button:has-text('Criar'), button[type='submit']"
        ).first
        if gen_btn.count() == 0:
            return None
        gen_btn.click()
        time.sleep(3.0)

        # Extract generated meli.la or /sec/ short link from page text or inputs
        html_and_vals = page.evaluate(
            """() => {
                const vals = Array.from(document.querySelectorAll('textarea, input')).map(e => e.value || '');
                return document.body.innerText + '\\n' + vals.join('\\n');
            }"""
        )
        m = re.search(r"https://(?:meli\.la/[A-Za-z0-9_-]+|(?:www\.)?mercadolivre\.com(?:\.br)?/sec/[A-Za-z0-9_-]+)", html_and_vals)
        return m.group(0) if m else None
    finally:
        page.close()


def _shorten_amazon_sitestripe(ctx: BrowserContext, target_url: str) -> str | None:
    """Extract Amazon Associates SiteStripe short link if logged into Associates account."""
    page = ctx.new_page()
    try:
        page.goto(target_url, wait_until="domcontentloaded", timeout=30000)
        time.sleep(2.5)
        txt_btn = page.locator("#amzn-ss-text-link a, [data-action*='sitestripe-text'], a:has-text('Texto')").first
        if txt_btn.count() == 0 or not txt_btn.is_visible():
            return None
        txt_btn.click()
        time.sleep(1.8)
        short_input = page.locator("#amzn-ss-text-shortlink-textarea, textarea[id*='shortlink'], input[id*='shortlink']").first
        if short_input.count() > 0:
            val = short_input.input_value().strip()
            if val.startswith("https://amzn.to/") or "tag=" in val:
                return val
        return None
    finally:
        page.close()


def sync_affiliate_links(
    code: str | None = None,
    catalogo_path: Path = CATALOGO_PATH,
    product_dir: Path | None = None,
    ctx: BrowserContext | None = None,
) -> dict[str, Any]:
    """Convert canonical URLs in vitrine/catalogo.json (and optional pacote.md) to short affiliate links."""
    data = json.loads(catalogo_path.read_text(encoding="utf-8"))
    own_ctx = False
    p_mgr = None

    candidates: list[tuple[dict[str, Any], str]] = []
    for prod in data.get("produtos", []):
        if code and prod.get("codigo") != code:
            continue
        if not prod.get("ativo"):
            continue
        for var in prod.get("variacoes", []):
            url = str(var.get("url", "")).strip()
            if url and not _is_already_short_affiliate(url):
                candidates.append((var, url))

    if not candidates:
        return {"checked": 0, "converted": 0, "session_missing": []}

    converted: dict[str, str] = {}
    session_missing: set[str] = set()

    try:
        if ctx is None:
            PW_PROFILE_DIR.mkdir(parents=True, exist_ok=True)
            p_mgr = sync_playwright().start()
            ctx = p_mgr.chromium.launch_persistent_context(
                user_data_dir=str(PW_PROFILE_DIR),
                channel="chrome",
                headless=False,
                viewport={"width": 1280, "height": 900},
                args=["--disable-blink-features=AutomationControlled", "--window-position=-2000,-2000"],
            )
            own_ctx = True

        ml_auth_checked = True
        amz_auth_checked = True

        for var_obj, orig_url in candidates:
            if orig_url in converted:
                var_obj["url"] = converted[orig_url]
                continue

            short_url: str | None = None
            if "mercadolivre.com.br" in orig_url and ml_auth_checked:
                short_url = _shorten_ml_url_in_linkbuilder(ctx, orig_url)
                if short_url is None:
                    ml_auth_checked = False
                    session_missing.add("mercado_livre_afiliados")
            elif "amazon.com.br" in orig_url and amz_auth_checked:
                short_url = _shorten_amazon_sitestripe(ctx, orig_url)
                if short_url is None:
                    amz_auth_checked = False
                    session_missing.add("amazon_associados")

            if short_url:
                converted[orig_url] = short_url
                var_obj["url"] = short_url
    finally:
        if own_ctx and ctx is not None:
            ctx.close()
        if p_mgr is not None:
            p_mgr.stop()

    if converted:
        catalogo_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        if product_dir and (product_dir / "pacote.md").exists():
            p_txt = (product_dir / "pacote.md").read_text(encoding="utf-8")
            for orig_u, short_u in converted.items():
                p_txt = p_txt.replace(orig_u, short_u)
            (product_dir / "pacote.md").write_text(p_txt, encoding="utf-8")

    return {
        "checked": len(candidates),
        "converted": len(converted),
        "mapping": converted,
        "session_missing": sorted(session_missing),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Converte URLs canônicas em links curtos de afiliado no catalogo.json.")
    parser.add_argument("--code", type=str, default=None, help="Código curto do produto (ex.: IBG-002)")
    parser.add_argument("--product-dir", type=Path, default=None, help="Pasta opcional produtos/<slug> para sincronizar pacote.md")
    args = parser.parse_args()

    res = sync_affiliate_links(code=args.code, product_dir=args.product_dir)
    print(json.dumps(res, ensure_ascii=False, indent=2))
    if res["session_missing"]:
        print(
            "[affiliate_links] Aviso: sessões ainda não autenticadas no perfil Playwright: "
            + ", ".join(res["session_missing"])
            + ". Execute 'PYTHONPATH=. .venv/bin/python src/publish/playwright_publish.py --login' uma única vez para salvar o login de afiliados."
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
