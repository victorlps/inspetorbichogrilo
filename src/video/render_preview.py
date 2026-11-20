"""Render lightweight Portao 3 preview.mp4 using Rig 2.5D + Rhubarb + ffmpeg."""

from __future__ import annotations

import json
import math
import subprocess
from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

REPO_ROOT = Path(__file__).resolve().parents[2]
REF_IMG = REPO_ROOT / "assets" / "personagem" / "referencia-oficial.jpg"
PROD_DIR = REPO_ROOT / "produtos" / "ducha-eletronica-zagonel-nd-7700w"
BUILD_DIR = PROD_DIR / "_preview_build"
OUT_MP4 = PROD_DIR / "preview.mp4"

W, H = 540, 960
FPS = 24


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    """Load a clean macOS sans-serif font with fallback."""
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]
    for p in candidates:
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def remove_studio_bg(im: Image.Image) -> Image.Image:
    """Flood-fill remove dark #0f172a studio background from image borders with soft feather."""
    rgb = np.array(im.convert("RGB"), dtype=np.float32)
    h, w, _ = rgb.shape
    bg_ref = rgb[10, 10]  # Top-left studio background sample
    dist = np.sqrt(np.sum((rgb - bg_ref) ** 2, axis=2))

    # Flood fill from borders where color is close to studio backdrop
    mask_bg = np.zeros((h, w), dtype=bool)
    visited = np.zeros((h, w), dtype=bool)
    q: deque[tuple[int, int]] = deque()
    for x in range(w):
        q.append((0, x))
        q.append((h - 1, x))
    for y in range(h):
        q.append((y, 0))
        q.append((y, w - 1))

    thresh = 30.0
    while q:
        y, x = q.popleft()
        if visited[y, x]:
            continue
        visited[y, x] = True
        if dist[y, x] <= thresh:
            mask_bg[y, x] = True
            if y > 0 and not visited[y - 1, x]:
                q.append((y - 1, x))
            if y + 1 < h and not visited[y + 1, x]:
                q.append((y + 1, x))
            if x > 0 and not visited[y, x - 1]:
                q.append((y, x - 1))
            if x + 1 < w and not visited[y, x + 1]:
                q.append((y, x + 1))

    alpha = np.where(mask_bg, 0, 255).astype(np.uint8)
    alpha_img = Image.fromarray(alpha, mode="L").filter(ImageFilter.GaussianBlur(radius=1.3))
    rgba = im.convert("RGBA")
    rgba.putalpha(alpha_img)
    return rgba


def build_viseme_sprites(base_rgba: Image.Image) -> dict[str, Image.Image]:
    """Generate 9 Rhubarb mouth-warped character sprites preserving 3D skin shading."""
    # Exact mouth box in 896x1200 reference: x=310..495, y=525..595
    arr_orig = np.array(base_rgba)
    # Viseme params: (jaw_drop_px, corner_spread_px, mouth_open_darkness)
    params = {
        "X": (-10, 0, 0.0),    # Closed rest
        "A": (-12, 2, 0.0),    # Closed pressed (M, B, P)
        "B": (-2, 4, 0.35),    # Slightly open
        "C": (8, 6, 0.70),     # Mid open
        "D": (18, 3, 1.00),    # Wide open
        "E": (11, -7, 0.80),   # Rounded O
        "F": (-5, -3, 0.25),   # F / V lip tuck
        "G": (4, -12, 0.55),   # Pursed W / OO
        "H": (6, 2, 0.60),     # L / tongue
    }

    sprites: dict[str, Image.Image] = {}
    mx0, mx1 = 305, 505
    my0, my1 = 515, 625
    cy = 556
    cx = 400

    for code, (jaw_dy, spread_dx, dark_amt) in params.items():
        arr = arr_orig.copy()
        # Local vertical/horizontal warp in mouth/chin patch
        patch = arr[my0:my1, mx0:mx1].copy()
        ph, pw, _ = patch.shape
        yy, xx = np.mgrid[0:ph, 0:pw]
        gx = xx + mx0
        gy = yy + my0

        # Smooth horizontal Gaussian falloff around mouth center
        wx = np.exp(-(((gx - cx) / 72.0) ** 2))
        # Lower jaw mask (below mouth center line)
        mouth_line = cy + 0.0014 * ((gx - cx) ** 2) - 4.0
        wy_lower = np.clip((gy - mouth_line) / 28.0, 0.0, 1.0) * np.exp(-(((gy - (cy + 34)) / 42.0) ** 2))

        src_y = np.clip(yy - (jaw_dy * wx * wy_lower), 0, ph - 1).astype(np.int32)
        src_x = np.clip(xx - (spread_dx * ((gx - cx) / 80.0) * wx * np.exp(-(((gy - cy) / 30.0) ** 2))), 0, pw - 1).astype(np.int32)

        warped = patch[src_y, src_x]

        # Darken mouth cavity when opening wider, or blend skin when closing (X/A)
        cavity_dist = np.abs(gy - (mouth_line + max(jaw_dy, 0) * 0.35))
        if jaw_dy < 0:
            # Close gap smoothly by pulling lower lip up to upper lip
            close_band = (gy >= mouth_line - 3) & (gy <= mouth_line + 14) & (wx > 0.25)
            sample_y = np.clip(mouth_line.astype(np.int32) - my0 + 18, 0, ph - 1)
            for c in range(3):
                warped[:, :, c] = np.where(close_band, patch[sample_y, xx, c], warped[:, :, c])
        elif dark_amt > 0.3:
            open_r = max(4.0, jaw_dy * 0.65)
            in_cavity = (cavity_dist < open_r * wx) & (wx > 0.22)
            for c, val in enumerate((38, 16, 20)):
                warped[:, :, c] = np.where(in_cavity, int(val), warped[:, :, c])

        arr[my0:my1, mx0:mx1] = warped
        sprites[code] = Image.fromarray(arr, mode="RGBA")

    return sprites


def make_blink_mask(base_rgba: Image.Image) -> Image.Image:
    """Create eyelid-closed overlay for natural blinking."""
    arr = np.array(base_rgba.copy())
    # Sample upper eyelid skin color near (310, 345) and (490, 345)
    for ex0, ex1, ey0, ey1 in ((272, 355, 350, 418), (435, 545, 348, 422)):
        skin_row = arr[ey0 - 6 : ey0 - 2, ex0 + 15 : ex1 - 15].mean(axis=(0, 1)).astype(np.uint8)
        for y in range(ey0, ey1):
            t = (y - ey0) / max(1, (ey1 - ey0))
            shade = 0.88 + 0.12 * math.sin(t * math.pi)
            arr[y, ex0:ex1, :3] = (skin_row[:3] * shade).astype(np.uint8)
    return Image.fromarray(arr, mode="RGBA")


def draw_wrapped_caption(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont, y_center: int) -> None:
    """Draw bold centered caption with dark outline at the bottom."""
    words = text.split()
    lines: list[str] = []
    cur = ""
    for w in words:
        test = f"{cur} {w}".strip()
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] <= W - 64:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)

    line_h = 30
    y = y_center - (len(lines) * line_h) // 2
    for ln in lines:
        bbox = draw.textbbox((0, 0), ln, font=font)
        lw = bbox[2] - bbox[0]
        x = (W - lw) // 2
        draw.text((x, y), ln, font=font, fill=(255, 255, 255), stroke_width=3, stroke_fill=(10, 14, 24))
        y += line_h


def render_preview() -> None:
    """Render full preview.mp4 piping RGB frames directly to ffmpeg."""
    timeline = json.loads((BUILD_DIR / "timeline.json").read_text())
    lipsync = json.loads((BUILD_DIR / "lipsync.json").read_text())
    total_dur = timeline["total_duration"]
    cues = lipsync["mouthCues"]

    base_raw = Image.open(REF_IMG)
    base_rgba = remove_studio_bg(base_raw)
    visemes = build_viseme_sprites(base_rgba)
    blink_sprite = make_blink_mask(base_rgba)

    # Pre-scale sprites for 540x960 preview (height ~460px in foreground)
    char_h = 460
    char_w = int(char_h * (896 / 1200))
    visemes_scaled = {k: v.resize((char_w, char_h), Image.Resampling.BILINEAR) for k, v in visemes.items()}
    blink_scaled = blink_sprite.resize((char_w, char_h), Image.Resampling.BILINEAR)

    prod_img = Image.open(PROD_DIR / "assets" / "zagonel_oficial_nd.png").convert("RGBA")
    prod_img.thumbnail((330, 330), Image.Resampling.BILINEAR)

    font_title = load_font(22, bold=True)
    font_sub = load_font(16, bold=False)
    font_cap = load_font(22, bold=True)
    font_badge = load_font(15, bold=True)

    # Active caption segments (chunk words every ~6 words)
    word_chunks: list[tuple[float, float, str]] = []
    for sc in timeline["scenes"]:
        ws = sc["words"]
        for i in range(0, len(ws), 6):
            grp = ws[i : i + 6]
            s_t = grp[0]["start"]
            e_t = grp[-1]["start"] + grp[-1]["duration"] + 0.15
            word_chunks.append((s_t, e_t, " ".join(w["text"] for w in grp)))

    n_frames = int(math.ceil(total_dur * FPS))
    wav_path = BUILD_DIR / "narration.wav"

    cmd = [
        "ffmpeg",
        "-y",
        "-f",
        "rawvideo",
        "-pix_fmt",
        "rgb24",
        "-s",
        f"{W}x{H}",
        "-r",
        str(FPS),
        "-i",
        "-",
        "-i",
        str(wav_path),
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        "-preset",
        "veryfast",
        "-crf",
        "24",
        "-c:a",
        "aac",
        "-b:a",
        "128k",
        "-shortest",
        str(OUT_MP4),
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    assert proc.stdin is not None

    cue_idx = 0
    for f_idx in range(n_frames):
        t = f_idx / FPS
        while cue_idx + 1 < len(cues) and cues[cue_idx]["end"] < t:
            cue_idx += 1
        viseme = cues[cue_idx]["value"] if cue_idx < len(cues) else "X"

        # Determine active scene
        active_sc = timeline["scenes"][-1]
        for sc in timeline["scenes"]:
            if sc["start"] <= t <= sc["end"]:
                active_sc = sc
                break
        sc_id = active_sc["scene"]
        sc_prog = (t - active_sc["start"]) / max(0.01, active_sc["duration"])

        # Base dark slate canvas (#0f172a)
        canvas = Image.new("RGBA", (W, H), (15, 23, 42, 255))
        draw = ImageDraw.Draw(canvas)

        # Top subtle header bar
        draw.rectangle([0, 0, W, 56], fill=(10, 16, 30, 220))
        draw.text((22, 16), "INSPETOR BICHO GRILO · PREVIEW PORTÃO 3", font=font_badge, fill=(148, 163, 184))

        if sc_id == "01":
            # Magazine/press clipping cards sliding in + Zagonel ND
            papers = [
                ("FIESC", "Zagonel compra Thermosystem e Corona", 40, 110, -4),
                ("EXAME", "Dexco sai de chuveiros elétricos em 2024", 150, 180, 3),
                ("REVISTA ANAMACO", "Projeto da linha ND segue intacto", 80, 255, -2),
            ]
            for idx_p, (pub, headline, px, py, rot) in enumerate(papers):
                enter = min(1.0, max(0.0, (sc_prog - idx_p * 0.16) * 3.2))
                if enter > 0:
                    y_off = int((1.0 - enter) * 40)
                    card = Image.new("RGBA", (340, 72), (241, 245, 249, int(235 * enter)))
                    cd = ImageDraw.Draw(card)
                    cd.rectangle([0, 0, 339, 71], outline=(203, 213, 225, 255), width=2)
                    cd.text((14, 10), pub, font=font_badge, fill=(185, 28, 28))
                    cd.text((14, 34), headline, font=font_sub, fill=(15, 23, 42))
                    card_r = card.rotate(rot, expand=True, resample=Image.Resampling.BILINEAR)
                    canvas.alpha_composite(card_r, (px, py + y_off))

            if sc_prog > 0.45:
                fade = min(1.0, (sc_prog - 0.45) * 3.0)
                px = (W - prod_img.width) // 2 + 75
                py = 260
                p_copy = prod_img.copy()
                p_copy.putalpha(p_copy.getchannel("A").point(lambda a: int(a * fade)))
                canvas.alpha_composite(p_copy, (px, py))

        elif sc_id == "02":
            # Zagonel ND + rising animated steam/vapor puffs
            px = (W - prod_img.width) // 2 + 70
            py = 165
            canvas.alpha_composite(prod_img, (px, py))
            # Rising vapor circles
            for k in range(12):
                phase = (t * 0.9 + k * 0.27) % 1.0
                vx = px + 95 + int(math.sin(t * 2.5 + k) * 28) + (k % 3 - 1) * 22
                vy = py + 235 - int(phase * 155)
                vr = int(12 + phase * 22)
                va = int((1.0 - phase) * 110)
                vapor_layer = Image.new("RGBA", (vr * 2 + 4, vr * 2 + 4), (0, 0, 0, 0))
                vd = ImageDraw.Draw(vapor_layer)
                vd.ellipse([2, 2, vr * 2 + 2, vr * 2 + 2], fill=(226, 232, 240, va))
                canvas.alpha_composite(vapor_layer, (vx - vr, vy - vr))

        elif sc_id == "03":
            # Visual action 1: Cold water chamber filling; Action 2: Thin wire vs 6mm2 wire
            if sc_prog < 0.52:
                # Chamber filling with cold blue water
                fill_lvl = min(1.0, sc_prog / 0.45)
                bx, by, bw, bh = 165, 130, 260, 210
                draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=18, outline=(148, 163, 184), width=3, fill=(30, 41, 59))
                wh = int((bh - 12) * fill_lvl)
                if wh > 0:
                    draw.rounded_rectangle([bx + 6, by + bh - 6 - wh, bx + bw - 6, by + bh - 6], radius=12, fill=(56, 189, 248))
                draw.text((bx + 28, by + bh + 14), "CÂMARA ENCHENDO COM ÁGUA FRIA", font=font_badge, fill=(125, 211, 252))
            else:
                # Thin wire glowing red vs 6mm2 cool green
                pulse = 0.5 + 0.5 * math.sin(t * 10.0)
                # Thin wire
                draw.rounded_rectangle([120, 145, 420, 215], radius=12, fill=(45, 20, 25), outline=(239, 68, 68), width=2)
                draw.line([(145, 180), (395, 180)], fill=(255, int(70 + 80 * pulse), 40), width=4)
                draw.text((145, 152), "FIO FINO · SUPERAQUECE (7700W)", font=font_badge, fill=(252, 165, 165))
                # 6 mm2 wire
                draw.rounded_rectangle([120, 240, 420, 315], radius=12, fill=(20, 40, 30), outline=(34, 197, 94), width=2)
                draw.line([(145, 282), (395, 282)], fill=(74, 222, 128), width=14)
                draw.text((145, 248), "CABO 6 mm² · ESTÁVEL", font=font_badge, fill=(134, 239, 172))

        else:
            # Cena 04: Hero Zagonel ND + CTA
            px = (W - prod_img.width) // 2 + 65
            py = 140
            canvas.alpha_composite(prod_img, (px, py))
            draw.rounded_rectangle([140, 455, 460, 505], radius=12, fill=(22, 163, 74))
            draw.text((168, 468), "COMENTE: ZAGONEL", font=font_title, fill=(255, 255, 255))

        # Character 2.5D foreground (gentle breathing + blink every 3.5s)
        is_blink = (t % 3.5) < 0.14
        char_img = blink_scaled if is_blink else visemes_scaled.get(viseme, visemes_scaled["X"])
        bob_y = int(math.sin(t * 2.4) * 5)
        char_x = -25
        char_y = H - char_h + 10 + bob_y
        canvas.alpha_composite(char_img, (char_x, char_y))

        # Dynamic word-chunk caption at bottom
        for cs, ce, ctext in word_chunks:
            if cs <= t <= ce:
                draw_wrapped_caption(draw, ctext, font_cap, H - 82)
                break

        proc.stdin.write(canvas.convert("RGB").tobytes())

    proc.stdin.close()
    rc = proc.wait()
    if rc != 0:
        raise RuntimeError(f"ffmpeg failed with exit code {rc}")
    print(f"Rendered preview.mp4: {OUT_MP4} ({n_frames} frames, {total_dur:.2f}s)")


if __name__ == "__main__":
    render_preview()
