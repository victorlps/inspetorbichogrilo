"""Local Playwright publisher (Caminho 2) for YouTube Studio, Meta Business Suite (Reels), and TikTok Studio.

Uses a persistent Google Chrome profile (~/.cache/inspetorbichogrilo-pw-profile) outside the repo
so local video files can be uploaded without MCP sandbox restrictions while preserving sessions.
"""

from __future__ import annotations

import argparse
import re
import time
from dataclasses import dataclass
from pathlib import Path

from playwright.sync_api import Page, sync_playwright

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
            lines.append(re.sub(r"^>\s?", "", line.strip()))
    return "\n".join(lines).strip()


def load_pacote_metadata(product_dir: Path) -> PacoteMetadata:
    """Parse platform captions, YouTube title/description, and REQ-007 AI flag from pacote.md."""
    pacote_path = product_dir / "pacote.md"
    if not pacote_path.exists():
        raise FileNotFoundError(f"pacote.md não encontrado em {product_dir}")

    text = pacote_path.read_text(encoding="utf-8")
    video_path = product_dir / "video_final_1080p.mp4"
    if not video_path.exists():
        raise FileNotFoundError(f"Vídeo não encontrado: {video_path}")

    ai_disclosure = "SIM — OBRIGATÓRIO ATIVAR RÓTULO" in text or "REQ-007" in text

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


def _open_context(p):
    PW_PROFILE_DIR.mkdir(parents=True, exist_ok=True)
    return p.chromium.launch_persistent_context(
        user_data_dir=str(PW_PROFILE_DIR),
        channel="chrome",
        headless=False,
        viewport={"width": 1280, "height": 900},
        args=["--disable-blink-features=AutomationControlled"],
    )


def run_login_session() -> None:
    """Open YouTube Studio, Meta Business Suite, and TikTok Studio so user logs in once."""
    with sync_playwright() as p:
        ctx = _open_context(p)
        urls = [
            f"https://studio.youtube.com/channel/{YOUTUBE_CHANNEL_ID}",
            f"https://business.facebook.com/latest/home?asset_id={META_PAGE_ASSET_ID}",
            "https://www.tiktok.com/tiktokstudio/upload",
        ]
        for idx, url in enumerate(urls):
            page = ctx.pages[0] if (idx == 0 and ctx.pages) else ctx.new_page()
            page.goto(url, wait_until="domcontentloaded")
        print("Navegador aberto com perfil persistente. Faça login nas abas necessárias e pressione ENTER aqui para salvar.")
        input()
        ctx.close()


def publish_youtube(page: Page, meta: PacoteMetadata, do_publish: bool = False) -> None:
    """Upload video to YouTube Studio for Inspetor Bicho Grilo channel."""
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
    page.keyboard.type(meta.youtube_title, delay=10)

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
        if show_more.count() > 0:
            show_more.click()
            time.sleep(0.6)
        altered_yes = page.locator('tp-yt-paper-radio-button[name="VIDEO_CONTAINS_SYNTHETIC_MEDIA_YES"], ytcp-altered-content-select tp-yt-paper-radio-button').first
        if altered_yes.count() > 0:
            altered_yes.click()

    for _ in range(3):
        next_btn = page.locator('#next-button').first
        if next_btn.is_visible():
            next_btn.click()
            time.sleep(1.0)

    vis_radio = page.locator(
        'tp-yt-paper-radio-button[name="PUBLIC"]' if do_publish else 'tp-yt-paper-radio-button[name="UNLISTED"]'
    ).first
    if vis_radio.count() > 0:
        vis_radio.click()

    if do_publish:
        done_btn = page.locator('#done-button').first
        if done_btn.is_visible():
            done_btn.click()
            print("[YouTube] Publicado! Aguarde confirmação na tela.")
    else:
        print("[YouTube] Formulário preenchido e pronto para revisão na tela (use --publish para clicar em Publicar).")


def publish_instagram(page: Page, meta: PacoteMetadata, do_publish: bool = False) -> None:
    """Upload Reel via Meta Business Suite for Inspetor Bicho Grilo."""
    url = f"https://business.facebook.com/latest/reels_composer?asset_id={META_PAGE_ASSET_ID}"
    page.goto(url, wait_until="domcontentloaded", timeout=60000)

    file_input = page.locator('input[type="file"][accept*="video"]').first
    file_input.wait_for(state="attached", timeout=30000)
    file_input.set_input_files(str(meta.video_path))
    print("[Instagram/Meta] Vídeo selecionado no Reels Composer...")

    caption_box = page.locator('[contenteditable="true"][role="textbox"]').first
    caption_box.wait_for(state="visible", timeout=30000)
    caption_box.click()
    caption_box.fill(meta.instagram_caption)
    print("[Instagram/Meta] Legenda preenchida. Revise o rótulo de IA (REQ-007) e publique." if not do_publish else "[Instagram/Meta] Pronto para publicar.")


def publish_tiktok(page: Page, meta: PacoteMetadata, do_publish: bool = False) -> None:
    """Upload video via TikTok Studio."""
    page.goto("https://www.tiktok.com/tiktokstudio/upload", wait_until="domcontentloaded", timeout=60000)
    file_input = page.locator('input[type="file"]').first
    file_input.wait_for(state="attached", timeout=30000)
    file_input.set_input_files(str(meta.video_path))
    print("[TikTok] Vídeo selecionado; preenchendo legenda...")

    caption_box = page.locator('[contenteditable="true"]').first
    caption_box.wait_for(state="visible", timeout=45000)
    caption_box.click()
    page.keyboard.press("Meta+A")
    caption_box.fill(meta.tiktok_caption[:2200])
    print("[TikTok] Legenda preenchida. Confira a chave 'Conteúdo gerado por IA' (REQ-007).")


def main() -> None:
    parser = argparse.ArgumentParser(description="Automação local de upload via Playwright (YouTube, Instagram/Meta, TikTok).")
    parser.add_argument("--login", action="store_true", help="Abre as abas no perfil persistente do Chrome para login inicial.")
    parser.add_argument("--product-dir", type=Path, default=REPO_ROOT / "produtos" / "ducha-eletronica-zagonel-nd-7700w")
    parser.add_argument("--platform", choices=["youtube", "instagram", "tiktok", "all"], default="all")
    parser.add_argument("--publish", action="store_true", help="Clica no botão final de publicar (por padrão deixa na tela de revisão).")
    args = parser.parse_args()

    if args.login:
        run_login_session()
        return

    meta = load_pacote_metadata(args.product_dir)
    platforms = ["youtube", "instagram", "tiktok"] if args.platform == "all" else [args.platform]

    with sync_playwright() as p:
        ctx = _open_context(p)
        for idx, plat in enumerate(platforms):
            page = ctx.pages[0] if (idx == 0 and ctx.pages) else ctx.new_page()
            if plat == "youtube":
                publish_youtube(page, meta, do_publish=args.publish)
            elif plat == "instagram":
                publish_instagram(page, meta, do_publish=args.publish)
            elif plat == "tiktok":
                publish_tiktok(page, meta, do_publish=args.publish)
        print("Execução concluída. Pressione ENTER no terminal após conferir as abas abertas para fechar o navegador.")
        input()
        ctx.close()


if __name__ == "__main__":
    main()
