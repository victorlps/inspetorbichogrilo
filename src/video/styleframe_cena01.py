"""Generate zero-cost Art Direction styleframes for Cena 01 (brand zoom + realistic newspaper clippings)."""

from __future__ import annotations

import math
import random
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

REPO_ROOT = Path(__file__).resolve().parents[2]
PROD_DIR = REPO_ROOT / "produtos" / "ducha-eletronica-zagonel-nd-7700w"
ZAGONEL_PNG = PROD_DIR / "assets" / "zagonel_oficial_nd.png"
REF_CHAR = REPO_ROOT / "assets" / "personagem" / "referencia-oficial.jpg"
SCRATCH_DIR = Path("/Users/victorsouza/.gemini/antigravity/brain/b63e20dc-1d81-4695-857d-7e8618ed3bb7/scratch")

W, H = 540, 960


def load_font(size: int, serif: bool = False, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    """Load serif newspaper or clean sans-serif font."""
    if serif:
        candidates = [
            "/System/Library/Fonts/Supplemental/Georgia Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Georgia.ttf",
            "/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Times New Roman.ttf",
        ]
    else:
        candidates = [
            "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
            "/System/Library/Fonts/Helvetica.ttc",
        ]
    for p in candidates:
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def remove_studio_bg_fast(im: Image.Image) -> Image.Image:
    """Quick edge-flood removal of #0f172a studio backdrop."""
    from collections import deque
    rgb = np.array(im.convert("RGB"), dtype=np.float32)
    h, w, _ = rgb.shape
    bg_ref = rgb[10, 10]
    dist = np.sqrt(np.sum((rgb - bg_ref) ** 2, axis=2))
    mask_bg = np.zeros((h, w), dtype=bool)
    visited = np.zeros((h, w), dtype=bool)
    q: deque[tuple[int, int]] = deque()
    for x in range(w):
        q.append((0, x))
        q.append((h - 1, x))
    for y in range(h):
        q.append((y, 0))
        q.append((y, w - 1))
    while q:
        y, x = q.popleft()
        if visited[y, x]:
            continue
        visited[y, x] = True
        if dist[y, x] <= 30.0:
            mask_bg[y, x] = True
            for ny, nx in ((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)):
                if 0 <= ny < h and 0 <= nx < w and not visited[ny, nx]:
                    q.append((ny, nx))
    alpha = Image.fromarray(np.where(mask_bg, 0, 255).astype(np.uint8), mode="L").filter(ImageFilter.GaussianBlur(1.2))
    out = im.convert("RGBA")
    out.putalpha(alpha)
    return out


def make_branded_shower(brand_mode: str) -> Image.Image:
    """Return Zagonel ND 1200x1200 RGBA with logo swapped to Thermosystem, Hydra, or original Zagonel."""
    base = Image.open(ZAGONEL_PNG).convert("RGBA")
    if brand_mode == "Zagonel":
        return base

    arr = np.array(base)
    # Cleanly patch over original logo box (x=435..518, y=268..318) by interpolating surrounding white plastic
    x0, x1, y0, y1 = 435, 518, 268, 318
    top_row = arr[y0 - 4 : y0, x0:x1, :3].mean(axis=0)
    bot_row = arr[y1 : y1 + 4, x0:x1, :3].mean(axis=0)
    for y in range(y0, y1):
        t = (y - y0) / max(1, y1 - y0 - 1)
        arr[y, x0:x1, :3] = ((1.0 - t) * top_row + t * bot_row).astype(np.uint8)
    patched = Image.fromarray(arr, mode="RGBA")

    # Stamp new brand text with matching subtle rotation
    txt_layer = Image.new("RGBA", (180, 60), (0, 0, 0, 0))
    td = ImageDraw.Draw(txt_layer)
    if brand_mode == "Thermosystem":
        f_main = load_font(17, serif=False, bold=True)
        td.text((14, 16), "Thermosystem", font=f_main, fill=(28, 62, 130, 235))
        td.text((58, 36), "ND", font=load_font(11, bold=True), fill=(70, 80, 95, 220))
    elif brand_mode == "Hydra":
        f_main = load_font(22, serif=False, bold=True)
        td.text((40, 14), "hydra", font=f_main, fill=(35, 38, 44, 240))
        td.text((62, 39), "ND", font=load_font(11, bold=True), fill=(85, 90, 98, 220))

    rot_txt = txt_layer.rotate(-11.5, expand=True, resample=Image.Resampling.BICUBIC)
    patched.alpha_composite(rot_txt, (388, 260))
    return patched


def make_newspaper_clipping(
    paper_name: str,
    date_label: str,
    headline: str,
    subline: str,
    highlight_text: str | None = None,
    seed: int = 42,
) -> Image.Image:
    """Create a realistic torn-edge aged newspaper clipping with grain, rules, columns, and highlighter."""
    cw, ch = 350, 165
    rng = random.Random(seed)

    # Aged newsprint base with subtle paper grain
    noise = np.random.default_rng(seed).normal(0, 5.5, (ch, cw, 1))
    base_col = np.array([[[240, 234, 220]]], dtype=np.float32) + noise
    paper_rgb = np.clip(base_col, 210, 248).astype(np.uint8)
    paper = Image.fromarray(paper_rgb, mode="RGB").convert("RGBA")

    # Jagged torn-paper alpha polygon
    pts: list[tuple[int, int]] = []
    for x in range(8, cw - 8, 9):
        pts.append((x, rng.randint(4, 9)))
    for y in range(8, ch - 8, 9):
        pts.append((cw - rng.randint(4, 10), y))
    for x in range(cw - 8, 8, -9):
        pts.append((x, ch - rng.randint(4, 10)))
    for y in range(ch - 8, 8, -9):
        pts.append((rng.randint(4, 10), y))

    mask = Image.new("L", (cw, ch), 0)
    ImageDraw.Draw(mask).polygon(pts, fill=255)
    paper.putalpha(mask)

    d = ImageDraw.Draw(paper)
    f_paper = load_font(11, serif=True, bold=True)
    f_date = load_font(10, serif=False, bold=True)
    f_head = load_font(18, serif=True, bold=True)
    f_body = load_font(11, serif=True, bold=False)

    # Newspaper masthead & double rule
    d.text((18, 13), paper_name.upper(), font=f_paper, fill=(32, 30, 28, 255))
    d.text((cw - 78, 14), date_label, font=f_date, fill=(110, 35, 30, 240))
    d.line([(18, 29), (cw - 18, 29)], fill=(30, 28, 26, 230), width=2)
    d.line([(18, 32), (cw - 18, 32)], fill=(30, 28, 26, 160), width=1)

    # Wrap headline
    words = headline.split()
    h_lines: list[str] = []
    cur = ""
    for w in words:
        test = f"{cur} {w}".strip()
        if d.textbbox((0, 0), test, font=f_head)[2] <= cw - 40:
            cur = test
        else:
            h_lines.append(cur)
            cur = w
    if cur:
        h_lines.append(cur)

    # Highlighter streak under headline if requested
    hy = 38
    if highlight_text:
        hl_layer = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
        hd = ImageDraw.Draw(hl_layer)
        for idx_l, ln in enumerate(h_lines[:2]):
            lw = d.textbbox((0, 0), ln, font=f_head)[2]
            ly = hy + idx_l * 22
            hd.rectangle([16, ly + 2, 22 + lw, ly + 20], fill=(250, 224, 72, 145))
        paper = Image.alpha_composite(paper, hl_layer)
        d = ImageDraw.Draw(paper)

    for ln in h_lines[:2]:
        d.text((18, hy), ln, font=f_head, fill=(22, 20, 18, 255))
        hy += 22

    # Subline + real tiny two-column newsprint text (not gray bars)
    d.text((18, hy + 4), subline, font=f_body, fill=(55, 50, 45, 240))
    f_micro = load_font(7, serif=True, bold=False)
    col_left = [
        "A transação envolve unidades fabris",
        "e centros de distribuição estratégicos",
        "mantendo o padrão técnico da linha ND.",
    ]
    col_right = [
        "Especialistas apontam continuidade",
        "na compatibilidade de resistências",
        "e peças de reposição desde 2012.",
    ]
    col_y = hy + 22
    for row in range(3):
        yy = col_y + row * 10
        if yy < ch - 14:
            d.text((18, yy), col_left[row], font=f_micro, fill=(95, 90, 82, 215))
            d.text((182, yy), col_right[row], font=f_micro, fill=(95, 90, 82, 215))

    # Add soft drop shadow behind clipping
    shadow_pad = 16
    out = Image.new("RGBA", (cw + shadow_pad * 2, ch + shadow_pad * 2), (0, 0, 0, 0))
    sh_alpha = mask.point(lambda a: int(a * 0.48))
    sh = Image.new("RGBA", (cw, ch), (0, 0, 0, 255))
    sh.putalpha(sh_alpha)
    out.alpha_composite(sh, (shadow_pad + 4, shadow_pad + 6))
    out = out.filter(ImageFilter.GaussianBlur(5))
    out.alpha_composite(paper, (shadow_pad, shadow_pad))
    return out


def build_styleframes() -> None:
    """Create 2 Art Direction styleframes for Cena 01 at zero cost."""
    SCRATCH_DIR.mkdir(parents=True, exist_ok=True)
    char_rgba = remove_studio_bg_fast(Image.open(REF_CHAR))
    char_h = 355
    char_w = int(char_h * (896 / 1200))
    char_scaled = char_rgba.resize((char_w, char_h), Image.Resampling.LANCZOS)

    font_cap = load_font(22, serif=False, bold=True)

    configs = [
        (
            "styleframe_cena01_thermosystem.png",
            "Thermosystem",
            ("JORNAL SETORIAL", "2012 · 2015", "Duratex assume Thermosystem e Corona", "Linha ND mantém projeto original sob Hydra Corona", True),
            "Em 2012 eu comprei um chuveiro da Thermosystem...",
            0.0,
        ),
        (
            "styleframe_cena01_zagonel.png",
            "Zagonel",
            ("FIESC · EXAME · ANAMACO", "OUT / 2024", "Dexco vende Thermosystem e Corona à Zagonel", "Projeto da Ducha ND segue intacto na Zagonel", True),
            "...e o mesmo projeto reapareceu na Zagonel ND.",
            -2.5,
        ),
    ]

    for fname, brand, paper_args, caption, tilt in configs:
        canvas = Image.new("RGBA", (W, H), (14, 21, 38, 255))
        # Subtle warm studio spotlight behind shower stage
        glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        gd = ImageDraw.Draw(glow)
        gd.ellipse([70, 50, 520, 500], fill=(42, 68, 110, 120))
        glow = glow.filter(ImageFilter.GaussianBlur(55))
        canvas = Image.alpha_composite(canvas, glow)

        # Zoomed-in Zagonel ND shower inside top-middle safe zone (below Y=144px top UI)
        shower = make_branded_shower(brand)
        crop_box = (210, 15, 920, 620)
        shower_zoom = shower.crop(crop_box)
        shower_zoom.thumbnail((370, 370), Image.Resampling.LANCZOS)
        # Soft fade on bottom 18% of shower water crop
        sa = np.array(shower_zoom.getchannel("A"), dtype=np.float32)
        sh_h = sa.shape[0]
        fade_start = int(sh_h * 0.80)
        for ry in range(fade_start, sh_h):
            sa[ry, :] *= max(0.0, 1.0 - (ry - fade_start) / max(1, sh_h - fade_start))
        shower_zoom.putalpha(Image.fromarray(sa.astype(np.uint8), mode="L"))
        canvas.alpha_composite(shower_zoom, (95, 115))

        # Newspaper clipping angled cleanly to the right of character hat (zero overlap)
        pname, pdate, phead, psub, phighlight = paper_args
        clip = make_newspaper_clipping(pname, pdate, phead, psub, highlight_text="yes" if phighlight else None)
        clip_rot = clip.rotate(tilt if tilt != 0 else -2.5, expand=True, resample=Image.Resampling.BICUBIC)
        clip_rot.thumbnail((295, 185), Image.Resampling.LANCZOS)
        canvas.alpha_composite(clip_rot, (180, 345))

        # Inspetor Bicho Grilo in lower-left (face uncovered at Y=490..565)
        canvas.alpha_composite(char_scaled, (-25, 405))

        # Dynamic short-phrase caption right below character chin inside universal safe zone (Y=580..624, i.e. 1160..1248 in 1080p)
        draw = ImageDraw.Draw(canvas)
        safe_cx = 240  # shifted slightly left to clear 96px right UI stack
        words = caption.split()
        lines, cur = [], ""
        for w in words:
            t = f"{cur} {w}".strip()
            if draw.textbbox((0, 0), t, font=font_cap)[2] <= 370:
                cur = t
            else:
                lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
        y = 588 - (len(lines) * 26) // 2
        for idx_ln, ln in enumerate(lines):
            lw = draw.textbbox((0, 0), ln, font=font_cap)[2]
            lx = safe_cx - lw // 2
            draw.rounded_rectangle([lx - 10, y - 2, lx + lw + 10, y + 25], radius=8, fill=(10, 14, 24, 200))
            col = (250, 204, 21) if idx_ln == len(lines) - 1 else (255, 255, 255)
            draw.text((lx, y), ln, font=font_cap, fill=col, stroke_width=2, stroke_fill=(10, 14, 24))
            y += 28

        out_path = SCRATCH_DIR / fname
        canvas.convert("RGB").save(out_path)
        print("Saved:", out_path)


if __name__ == "__main__":
    build_styleframes()
