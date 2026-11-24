"""Local Playwright publisher for YouTube Studio, Meta Business Suite (Reels), and TikTok Studio.

Uses a persistent Google Chrome profile (~/.cache/inspetorbichogrilo-pw-profile) outside the repo
so local video files and affiliate link builders operate without MCP sandbox restrictions while preserving sessions.
"""

from __future__ import annotations

import argparse
import json
import re
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from playwright.sync_api import Page, expect, sync_playwright

REPO_ROOT = Path(__file__).resolve().parents[2]
PW_PROFILE_DIR = Path.home() / ".cache" / "inspetorbichogrilo-pw-profile"
YOUTUBE_CHANNEL_ID = "UCgIp02Q0H3rXsNwL-kDdFbA"  # @inspetorbichogrilo
META_PAGE_ASSET_ID = "1492341333956556"  # Inspetor Bicho Grilo


@dataclass
class PacoteMetadata:
    video_path: Path
    ai_disclosure: bool
    instagram_caption: str
    tiktok_caption: str
    youtube_title: str
    youtube_description: str


def _extract_blockquote(section_text: str) -> str:
    lines = []
    for line in section_text.splitlines():
        if line.strip().startswith(">"):
            clean = re.sub(r"^>\s?", "", line.strip())
            clean = clean.replace("**", "").replace("`", "")
            lines.append(clean)
    return "\n".join(lines).strip()


def load_pacote_metadata(product_dir: Path) -> PacoteMetadata:
    """Parse platform captions, YouTube title/description, and REQ-007 AI flag from pacote.md."""
    pacote_path = product_dir / "pacote.md"
    if not pacote_path.exists():
        raise FileNotFoundError(f"pacote.md não encontrado em {product_dir}")

    text = pacote_path.read_text(encoding="utf-8")
    if re.search(r"<LINK_[^>]+>", text):
        raise ValueError(f"pacote.md contém placeholder <LINK_...> não resolvido em {pacote_path}")

    video_path = product_dir / "video_final_1080p.mp4"
    if not video_path.exists():
        raise FileNotFoundError(f"Vídeo não encontrado: {video_path}")

    ai_disclosure = (
        "SIM — ATIVAR RÓTULO" in text
        or "SIM — OBRIGATÓRIO ATIVAR RÓTULO" in text
        or "REQ-007" in text
    )

    ig_match = re.search(r"### 2\.1 Instagram Reels\s+(.*?)(?=\n### |\n---)", text, re.S)
    tt_match = re.search(r"### 2\.2 TikTok\s+(.*?)(?=\n### |\n---)", text, re.S)
    yt_match = re.search(r"### 2\.3 YouTube Shorts\s+(.*?)(?=\n### |\n---)", text, re.S)
    tags_match = re.search(r"- \*\*Hashtags:\*\*\s*`([^`]+)`", text)

    ig_caption = _extract_blockquote(ig_match.group(1)) if ig_match else ""
    tt_base = _extract_blockquote(tt_match.group(1)) if tt_match else ""
    hashtags = tags_match.group(1).strip() if tags_match else ""
    tt_caption = f"{tt_base}\n\n{hashtags}".strip()

    yt_block = yt_match.group(1) if yt_match else ""
    yt_title_m = re.search(r"- \*\*Título sugerido[^\n]*\n\s*`([^`]+)`", yt_block)
    yt_title = yt_title_m.group(1).strip() if yt_title_m else product_dir.name
    yt_desc = _extract_blockquote(yt_block)

    return PacoteMetadata(
        video_path=video_path,
        ai_disclosure=ai_disclosure,
        instagram_caption=ig_caption,
        tiktok_caption=tt_caption,
        youtube_title=yt_title[:100],
        youtube_description=yt_desc,
    )


def _open_context(p, offscreen: bool = False):
    PW_PROFILE_DIR.mkdir(parents=True, exist_ok=True)
    extra_args = ["--disable-blink-features=AutomationControlled"]
    if offscreen:
        extra_args.append("--window-position=-2000,-2000")
    return p.chromium.launch_persistent_context(
        user_data_dir=str(PW_PROFILE_DIR),
        channel="chrome",
        headless=False,
        viewport={"width": 1280, "height": 920},
        args=extra_args,
    )


def run_login_session() -> None:
    """Open social studios AND affiliate portals so one login session covers the whole pipeline."""
    with sync_playwright() as p:
        ctx = _open_context(p, offscreen=False)
        urls = [
            f"https://studio.youtube.com/channel/{YOUTUBE_CHANNEL_ID}",
            f"https://business.facebook.com/latest/home?asset_id={META_PAGE_ASSET_ID}",
            "https://www.tiktok.com/tiktokstudio/upload",
            "https://www.mercadolivre.com.br/afiliados/linkbuilder",
            "https://associados.amazon.com.br/",
        ]
        for idx, url in enumerate(urls):
            page = ctx.pages[0] if (idx == 0 and ctx.pages) else ctx.new_page()
            page.goto(url, wait_until="domcontentloaded")
        print(
            "Navegador aberto com as 5 abas (YouTube, Meta, TikTok, Mercado Livre Afiliados e Amazon Associados). "
            "Faça login nas abas necessárias e pressione ENTER aqui para salvar."
        )
        input()
        ctx.close()


def publish_youtube(page: Page, meta: PacoteMetadata, do_publish: bool = False) -> dict[str, Any]:
    """Upload video to YouTube Studio for Inspetor Bicho Grilo channel and return status."""
    url = f"https://studio.youtube.com/channel/{YOUTUBE_CHANNEL_ID}/videos/upload?d=ud"
    page.goto(url, wait_until="domcontentloaded", timeout=60000)

    file_input = page.locator('input[type="file"]').first
    file_input.wait_for(state="attached", timeout=30000)
    file_input.set_input_files(str(meta.video_path))
    print("[YouTube] Arquivo selecionado; aguardando formulário de detalhes...")

    title_box = page.locator('#textbox[aria-label*="título"], #textbox[aria-label*="title"]').first
    title_box.wait_for(state="visible", timeout=60000)
    title_box.click()
    page.keyboard.press("Meta+A")
    page.keyboard.press("Backspace")
    title_box.fill(meta.youtube_title)

    desc_box = page.locator('#textbox[aria-label*="Fale"], #textbox[aria-label*="Tell viewers"]').first
    if desc_box.count() > 0:
        desc_box.click()
        page.keyboard.press("Meta+A")
        desc_box.fill(meta.youtube_description)

    not_for_kids = page.locator('tp-yt-paper-radio-button[name="VIDEO_MADE_FOR_KIDS_NOT_MFK"]').first
    if not_for_kids.count() > 0:
        not_for_kids.click()

    if meta.ai_disclosure:
        show_more = page.locator('#toggle-button:has-text("Mostrar mais"), #toggle-button:has-text("Show more")').first
        if show_more.count() > 0 and show_more.is_visible():
            show_more.click()
            time.sleep(0.8)
        altered_yes = page.locator(
            'tp-yt-paper-radio-button[name="VIDEO_CONTAINS_SYNTHETIC_MEDIA_YES"], '
            'ytcp-altered-content-select tp-yt-paper-radio-button[name*="YES"]'
        ).first
        if altered_yes.count() > 0:
            altered_yes.scroll_into_view_if_needed()
            altered_yes.click()

    # Extract video short link from wizard if already assigned
    short_url = ""
    link_el = page.locator('a[href*="youtube.com/shorts/"], a[href*="youtu.be/"]').first
    if link_el.count() > 0:
        short_url = link_el.get_attribute("href") or ""

    for _ in range(3):
        next_btn = page.locator('#next-button').first
        if next_btn.is_visible():
            next_btn.click()
            time.sleep(1.2)

    vis_radio = page.locator(
        'tp-yt-paper-radio-button[name="PUBLIC"]' if do_publish else 'tp-yt-paper-radio-button[name="UNLISTED"]'
    ).first
    vis_radio.wait_for(state="visible", timeout=30000)
    vis_radio.click()

    if not short_url:
        link_el2 = page.locator('a[href*="youtube.com/shorts/"], a[href*="youtu.be/"]').first
        if link_el2.count() > 0:
            short_url = link_el2.get_attribute("href") or ""

    if do_publish:
        done_btn = page.locator('#done-button').first
        done_btn.wait_for(state="visible", timeout=60000)
        expect(done_btn).to_be_enabled(timeout=180000)
        done_btn.click()
        print(f"[YouTube] Clique em Publicar enviado ({short_url or 'aguardando URL'})...")
        # Wait until upload/publish confirmation dialog finishes so upload is never cut off
        for _ in range(36):
            time.sleep(2.5)
            dialog_txt = page.locator("body").inner_text()
            if (
                "Vídeo publicado" in dialog_txt
                or "Video published" in dialog_txt
                or "processamento" in dialog_txt.lower()
                or "fechar" in dialog_txt.lower()
            ):
                if "enviando" not in dialog_txt.lower() and "uploading" not in dialog_txt.lower():
                    break
        page.screenshot(path="/tmp/publish_youtube_status.png")
        print(f"[YouTube] Publicação concluída: {short_url}")
        return {"platform": "youtube", "published": True, "url": short_url}

    print("[YouTube] Formulário preenchido na tela de revisão.")
    return {"platform": "youtube", "published": False, "url": short_url}


def publish_instagram(page: Page, meta: PacoteMetadata, do_publish: bool = False) -> dict[str, Any]:
    """Upload Reel via Meta Business Suite for Inspetor Bicho Grilo."""
    url = f"https://business.facebook.com/latest/reels_composer?asset_id={META_PAGE_ASSET_ID}"
    page.goto(url, wait_until="domcontentloaded", timeout=60000)
    time.sleep(4.0)

    file_input = page.locator('input[type="file"]').first
    if file_input.count() > 0:
        file_input.set_input_files(str(meta.video_path))
    else:
        add_btn = page.locator(
            'div[role="button"]:has-text("Adicionar vídeo"), button:has-text("Adicionar vídeo"), '
            'div[role="button"]:has-text("Add video"), button:has-text("Add video")'
        ).first
        add_btn.wait_for(state="visible", timeout=30000)
        with page.expect_file_chooser(timeout=15000) as fc_info:
            add_btn.click()
        fc_info.value.set_files(str(meta.video_path))
    print("[Instagram/Meta] Vídeo selecionado no Reels Composer...")

    caption_box = page.locator('[contenteditable="true"][role="textbox"]').first
    caption_box.wait_for(state="visible", timeout=45000)
    caption_box.click()
    caption_box.fill(meta.instagram_caption)

    if do_publish:
        # Wait for video upload to reach 100% before clicking Next/Share
        for _ in range(45):
            body_t = page.locator("body").inner_text()
            if "100%" in body_t or "Concluído" in body_t or "Uploaded" in body_t:
                break
            time.sleep(2.0)

        for _ in range(2):
            next_btn = page.locator(
                'div[role="button"]:has-text("Avançar"):not([aria-disabled="true"]), '
                'button:has-text("Avançar"):not([disabled]), '
                'div[role="button"]:has-text("Next"):not([aria-disabled="true"]), '
                'button:has-text("Next"):not([disabled])'
            ).first
            try:
                next_btn.wait_for(state="visible", timeout=45000)
                next_btn.click()
                time.sleep(2.5)
            except Exception:
                break

        # Attempt to toggle AI info label if exposed in Meta Business Suite composer
        if meta.ai_disclosure:
            ai_switch = page.locator(
                'input[aria-label*="IA"], input[aria-label*="AI"], [role="switch"][aria-label*="IA"], [role="switch"][aria-label*="AI"]'
            ).first
            if ai_switch.count() > 0 and ai_switch.is_visible():
                checked = ai_switch.get_attribute("aria-checked")
                if checked == "false":
                    ai_switch.click()
                    time.sleep(0.8)

        share_btn = page.locator(
            'div[role="button"]:has-text("Compartilhar"):not([aria-disabled="true"]), '
            'button:has-text("Compartilhar"):not([disabled]), '
            'div[role="button"]:has-text("Publicar"):not([aria-disabled="true"]), '
            'button:has-text("Publicar"):not([disabled]), '
            'div[role="button"]:has-text("Share"):not([aria-disabled="true"]), '
            'button:has-text("Share"):not([disabled])'
        ).last
        share_btn.wait_for(state="visible", timeout=120000)
        share_btn.click()
        print("[Instagram/Meta] Clique em Compartilhar/Publicar enviado! Aguardando processamento...")
        time.sleep(18.0)
        page.screenshot(path="/tmp/publish_instagram_status.png")
        return {"platform": "instagram", "published": True, "url": page.url}

    print("[Instagram/Meta] Legenda preenchida na tela de revisão.")
    return {"platform": "instagram", "published": False, "url": page.url}


def _dismiss_tiktok_overlays(page: Page) -> None:
    """Dismiss TikTok tutorial/cookie/joyride overlays that intercept pointer events."""
    for _ in range(4):
        page.keyboard.press("Escape")
        page.evaluate(
            """() => {
                document.querySelectorAll('#react-joyride-portal, .react-joyride__overlay, [data-floating-ui-portal]').forEach(el => {
                    if (el.querySelector('.react-joyride__overlay') || el.id === 'react-joyride-portal' || el.querySelector('.TUXModal-overlay')) {
                        el.remove();
                    }
                });
            }"""
        )
        time.sleep(0.5)


def update_tiktok_avatar(page: Page, avatar_path: Path) -> None:
    """Update TikTok profile picture without MCP sandbox restrictions."""
    page.goto("https://www.tiktok.com/@inspetorbichogrilo", wait_until="domcontentloaded", timeout=60000)
    time.sleep(3.0)
    _dismiss_tiktok_overlays(page)
    edit_btn = page.locator('button[data-e2e="edit-profile-entrance"], button:has-text("Editar perfil"), button:has-text("Edit profile")').first
    edit_btn.wait_for(state="visible", timeout=20000)
    edit_btn.click(force=True)
    time.sleep(1.5)
    file_input = page.locator('input[type="file"]').first
    file_input.wait_for(state="attached", timeout=15000)
    file_input.set_input_files(str(avatar_path))
    time.sleep(2.0)
    apply_btn = page.locator('button:has-text("Aplicar"), button:has-text("Apply")').first
    if apply_btn.count() > 0 and apply_btn.is_visible():
        apply_btn.click()
        time.sleep(1.0)
    save_btn = page.locator('button:has-text("Salvar"), button:has-text("Save")').first
    if save_btn.count() > 0 and save_btn.is_visible():
        save_btn.click()
        time.sleep(1.5)
    print("[TikTok] Foto de perfil atualizada com avatar-perfil-1024.png!")


def _enable_tiktok_ai_disclosure(page: Page) -> bool:
    """Toggle TikTok Studio 'Conteúdo gerado por IA' / 'AI-generated content' switch (REQ-007)."""
    try:
        more_btn = page.locator(
            'div:has-text("Mostrar mais"), span:has-text("Mostrar mais"), button:has-text("Mostrar mais"), '
            'div:has-text("Show more"), span:has-text("Show more"), button:has-text("Show more")'
        ).last
        if more_btn.count() > 0 and more_btn.is_visible():
            more_btn.scroll_into_view_if_needed()
            more_btn.click(force=True)
            time.sleep(1.0)

        toggled = page.evaluate(
            """() => {
                const labels = ['Conteúdo gerado por IA', 'AI-generated content', 'gerado por IA'];
                const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_ELEMENT);
                let node;
                while ((node = walker.nextNode())) {
                    const txt = (node.textContent || '').trim();
                    if (labels.some(l => txt.includes(l)) && txt.length < 180) {
                        const sw = node.querySelector('[role="switch"], input[type="checkbox"]')
                            || (node.parentElement && node.parentElement.querySelector('[role="switch"], input[type="checkbox"]'));
                        if (sw) {
                            const checked = sw.getAttribute('aria-checked') === 'true' || sw.checked === true;
                            if (!checked) sw.click();
                            return true;
                        }
                    }
                }
                return false;
            }"""
        )
        if toggled:
            time.sleep(1.2)
            # Confirm TikTok AI label modal if shown ("Ativar" / "Turn on")
            turn_on = page.locator('button:has-text("Ativar"), button:has-text("Turn on"), button:has-text("Confirmar")').last
            if turn_on.count() > 0 and turn_on.is_visible():
                turn_on.click()
                time.sleep(0.8)
        return bool(toggled)
    except Exception:
        return False


def publish_tiktok(page: Page, meta: PacoteMetadata, do_publish: bool = False) -> dict[str, Any]:
    """Upload video via TikTok Studio with REQ-007 AI disclosure toggle."""
    page.goto("https://www.tiktok.com/tiktokstudio/upload", wait_until="domcontentloaded", timeout=60000)
    file_input = page.locator('input[type="file"]').first
    file_input.wait_for(state="attached", timeout=30000)
    file_input.set_input_files(str(meta.video_path))
    print("[TikTok] Vídeo selecionado; aguardando editor...")
    time.sleep(5.0)
    _dismiss_tiktok_overlays(page)

    caption_box = page.locator('[contenteditable="true"]').first
    caption_box.wait_for(state="visible", timeout=60000)
    caption_box.click()
    page.keyboard.press("Meta+A")
    caption_box.fill(meta.tiktok_caption[:2200])

    ai_toggled = False
    if meta.ai_disclosure:
        ai_toggled = _enable_tiktok_ai_disclosure(page)
        print(f"[TikTok] Rótulo REQ-007 ('Conteúdo gerado por IA'): toggled={ai_toggled}")

    if do_publish:
        post_btn = page.locator('button[data-e2e="post_video_button"], button:has-text("Publicar"), button:has-text("Post")').last
        post_btn.wait_for(state="visible", timeout=90000)
        expect(post_btn).to_be_enabled(timeout=180000)
        post_btn.scroll_into_view_if_needed()
        post_btn.click()
        time.sleep(3.0)
        confirm_btn = page.locator(
            'button:has-text("Publicar agora"), button:has-text("Post now"), button:has-text("Continuar")'
        ).last
        if confirm_btn.count() > 0 and confirm_btn.is_visible():
            confirm_btn.click()
        print("[TikTok] Clique em Publicar enviado! Aguardando confirmação...")
        for _ in range(15):
            time.sleep(2.0)
            if "/content" in page.url or "Publicado" in page.locator("body").inner_text():
                break
        page.screenshot(path="/tmp/publish_tiktok_status.png")
        return {"platform": "tiktok", "published": True, "ai_toggled": ai_toggled, "url": page.url}

    print("[TikTok] Legenda preenchida na tela de revisão.")
    return {"platform": "tiktok", "published": False, "ai_toggled": ai_toggled, "url": page.url}


def run_publish(
    product_dir: Path,
    platforms: list[str],
    do_publish: bool = False,
    no_wait: bool = True,
    offscreen: bool = False,
    do_update_tiktok_avatar: bool = False,
) -> list[dict[str, Any]]:
    meta = load_pacote_metadata(product_dir)
    results: list[dict[str, Any]] = []
    with sync_playwright() as p:
        ctx = _open_context(p, offscreen=offscreen)
        if do_update_tiktok_avatar:
            try:
                av_page = ctx.pages[0] if ctx.pages else ctx.new_page()
                update_tiktok_avatar(av_page, REPO_ROOT / "assets" / "personagem" / "avatar-perfil-1024.png")
            except Exception as exc:
                print(f"[tiktok-avatar] Erro ao atualizar foto: {exc}")
        for idx, plat in enumerate(platforms):
            page = ctx.new_page() if (idx > 0 or do_update_tiktok_avatar or not ctx.pages) else ctx.pages[0]
            try:
                if plat == "youtube":
                    results.append(publish_youtube(page, meta, do_publish=do_publish))
                elif plat == "instagram":
                    results.append(publish_instagram(page, meta, do_publish=do_publish))
                elif plat == "tiktok":
                    results.append(publish_tiktok(page, meta, do_publish=do_publish))
            except Exception as exc:
                page.screenshot(path=f"/tmp/publish_{plat}_error.png")
                print(f"[{plat}] Erro durante automação: {exc}")
                results.append({"platform": plat, "published": False, "error": str(exc)})
        if no_wait:
            time.sleep(4.0)
            print("Execução concluída (--no-wait).")
        else:
            print("Execução concluída. Pressione ENTER no terminal após conferir as abas abertas para fechar o navegador.")
            input()
        ctx.close()
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description="Automação local de upload via Playwright (YouTube, Instagram/Meta, TikTok).")
    parser.add_argument("--login", action="store_true", help="Abre as 5 abas no perfil persistente do Chrome para login único.")
    parser.add_argument("--product-dir", type=Path, default=REPO_ROOT / "produtos" / "ducha-eletronica-zagonel-nd-7700w")
    parser.add_argument("--platform", choices=["youtube", "instagram", "tiktok", "none", "all"], default="all")
    parser.add_argument("--publish", action="store_true", help="Clica no botão final de publicar.")
    parser.add_argument("--offscreen", action="store_true", help="Posiciona a janela fora da tela principal durante o envio.")
    parser.add_argument("--update-tiktok-avatar", action="store_true", help="Atualiza a foto de perfil do TikTok.")
    parser.add_argument("--no-wait", action="store_true", help="Fecha automaticamente ao terminar sem esperar ENTER.")
    args = parser.parse_args()

    if args.login:
        run_login_session()
        return

    if args.platform == "none":
        platforms: list[str] = []
    elif args.platform == "all":
        platforms = ["youtube", "instagram", "tiktok"]
    else:
        platforms = [args.platform]

    res = run_publish(
        product_dir=args.product_dir,
        platforms=platforms,
        do_publish=args.publish,
        no_wait=args.no_wait,
        offscreen=args.offscreen,
        do_update_tiktok_avatar=args.update_tiktok_avatar,
    )
    print("RESULTADO_PUBLICACAO:", json.dumps(res, ensure_ascii=False))


if __name__ == "__main__":
    main()
