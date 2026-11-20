"""Build clean reusable Rig 2.5D PNG layers and rig.json from referencia-oficial.jpg and draft poses."""

from __future__ import annotations

import argparse
import json
from collections import deque
from pathlib import Path
from typing import Iterable

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

REPO_ROOT = Path(__file__).resolve().parents[2]
REF_IMG_PATH = REPO_ROOT / "assets" / "personagem" / "referencia-oficial.jpg"
DEFAULT_DRAFTS_DIR = Path(
    "/Users/victorsouza/.gemini/antigravity/brain/b63e20dc-1d81-4695-857d-7e8618ed3bb7/scratch/rig_512"
)
OUT_DIR = REPO_ROOT / "assets" / "personagem" / "rig"


def _is_navy_studio_bg(rgb: np.ndarray, bg_ref: np.ndarray, threshold: float = 27.0) -> np.ndarray:
    """Detect dark navy #09111c studio background while strictly protecting green skin and olive cloth shadows."""
    f = rgb.astype(np.float32)
    dist = np.sqrt(np.sum((f - bg_ref) ** 2, axis=2))
    # Studio background always has strong blue dominance over green (B >= G + 2) and low brightness
    return (dist < threshold) & (f[:, :, 2] >= f[:, :, 1] + 2.0) & (f[:, :, 2] < 58.0)


def dilate_mask(mask: np.ndarray, size: int = 5) -> np.ndarray:
    """Dilate a boolean mask cleanly via Pillow MaxFilter."""
    im = Image.fromarray(mask.astype(np.uint8) * 255, mode="L").filter(ImageFilter.MaxFilter(size))
    return np.array(im) > 127


def erode_mask(mask: np.ndarray, size: int = 3) -> np.ndarray:
    """Erode a boolean mask cleanly via Pillow MinFilter."""
    im = Image.fromarray(mask.astype(np.uint8) * 255, mode="L").filter(ImageFilter.MinFilter(size))
    return np.array(im) > 127


def remove_backdrop_rgba(rgb: np.ndarray, threshold: float = 27.5) -> Image.Image:
    """Remove border-connected and enclosed trapped studio backdrop with anti-halo interior color bleed."""
    h, w, _ = rgb.shape
    bg_ref = np.array([rgb[12, 12], rgb[12, w - 12], rgb[h // 2, 10]], dtype=np.float32).mean(axis=0)
    bg_cand = _is_navy_studio_bg(rgb, bg_ref, threshold=threshold)

    visited = np.zeros((h, w), dtype=bool)
    bg_mask = np.zeros((h, w), dtype=bool)
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
        if bg_cand[y, x]:
            bg_mask[y, x] = True
            if y > 0 and not visited[y - 1, x]:
                q.append((y - 1, x))
            if y + 1 < h and not visited[y + 1, x]:
                q.append((y + 1, x))
            if x > 0 and not visited[y, x - 1]:
                q.append((y, x - 1))
            if x + 1 < w and not visited[y, x + 1]:
                q.append((y, x + 1))

    # Also remove enclosed trapped studio-navy pockets between torso, raised arm, collar, and rear legs (y >= 540, outside face/mouth)
    yy_g, xx_g = np.mgrid[0:h, 0:w]
    not_mouth_face = ~((xx_g >= 320) & (xx_g <= 500) & (yy_g <= 615))
    lower_pockets = bg_cand & (~bg_mask) & (yy_g >= 540) & not_mouth_face
    p_visited = np.zeros((h, w), dtype=bool)
    py_idxs, px_idxs = np.where(lower_pockets)
    for sy, sx in zip(py_idxs, px_idxs):
        if p_visited[sy, sx]:
            continue
        comp: list[tuple[int, int]] = []
        pq: deque[tuple[int, int]] = deque([(int(sy), int(sx))])
        p_visited[sy, sx] = True
        while pq:
            cy, cx = pq.popleft()
            comp.append((cy, cx))
            for ny, nx in ((cy - 1, cx), (cy + 1, cx), (cy, cx - 1), (cy, cx + 1)):
                if 540 <= ny < h and 0 <= nx < w and lower_pockets[ny, nx] and not p_visited[ny, nx]:
                    p_visited[ny, nx] = True
                    pq.append((ny, nx))
        if len(comp) >= 40:
            for cy, cx in comp:
                bg_mask[cy, cx] = True

    # Preserve delicate bezels/antennae via 1px inward erosion + interior color bleed outward over the rim
    fg_raw = ~bg_mask
    fg_eroded = erode_mask(fg_raw, 3)
    soft_alpha = Image.fromarray(fg_eroded.astype(np.uint8) * 255, mode="L").filter(ImageFilter.GaussianBlur(0.85))
    alpha_arr = np.array(soft_alpha, dtype=np.uint8)
    safe_core = erode_mask(fg_eroded, 5)
    alpha_arr = np.where(safe_core, 255, alpha_arr)
    alpha_arr = np.where(bg_mask, 0, alpha_arr)

    # Anti-halo bleed: push safe_core RGB outward over the outer rim & feathered edge pixels (5 passes)
    clean_rgb = rgb.copy()
    rim = (alpha_arr > 0) & (~safe_core)
    if np.any(rim):
        src_rgb = np.where(safe_core[:, :, None], clean_rgb, 0).astype(np.float32)
        solid = safe_core.copy()
        for _ in range(5):
            solid_f = solid.astype(np.float32)
            num = np.zeros_like(src_rgb)
            den = np.zeros((h, w), dtype=np.float32)
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    num += np.roll(src_rgb, shift=(dy, dx), axis=(0, 1))
                    den += np.roll(solid_f, shift=(dy, dx), axis=(0, 1))
            valid = den > 0
            avg = np.zeros_like(src_rgb)
            avg[valid] = num[valid] / den[valid, None]
            fill_now = rim & (~solid) & valid
            clean_rgb[fill_now] = np.clip(avg[fill_now], 0, 255).astype(np.uint8)
            solid = solid | fill_now
            src_rgb = np.where(solid[:, :, None], clean_rgb, 0).astype(np.float32)

    out = Image.fromarray(clean_rgb, mode="RGB").convert("RGBA")
    out.putalpha(Image.fromarray(alpha_arr, mode="L"))
    return out


def align_to_reference(
    draft_rgb: np.ndarray,
    ref_rgb: np.ndarray,
    patch_box: tuple[int, int, int, int] = (335, 480, 265, 555),
) -> np.ndarray:
    """Shift draft image to align cleanly with reference anchor region."""
    h, w, _ = ref_rgb.shape
    if draft_rgb.shape[:2] != (h, w):
        draft_rgb = np.array(Image.fromarray(draft_rgb).resize((w, h), Image.Resampling.LANCZOS))

    y0, y1, x0, x1 = patch_box
    ref_patch = ref_rgb[y0:y1, x0:x1].astype(np.float32)
    draft_f = draft_rgb.astype(np.float32)
    best_err, best_dx, best_dy = 1e12, 0, 0
    for dy in range(-8, 9):
        for dx in range(-8, 9):
            cand = draft_f[y0 + dy : y1 + dy, x0 + dx : x1 + dx]
            err = float(np.mean(np.abs(cand - ref_patch)))
            if err < best_err:
                best_err, best_dx, best_dy = err, dx, dy

    if best_dx == 0 and best_dy == 0:
        return draft_rgb
    shifted = np.zeros_like(draft_rgb)
    sx0, sx1 = max(0, best_dx), min(w, w + best_dx)
    sy0, sy1 = max(0, best_dy), min(h, h + best_dy)
    shifted[sy0 - best_dy : sy1 - best_dy, sx0 - best_dx : sx1 - best_dx] = draft_rgb[sy0:sy1, sx0:sx1]
    return shifted


def extract_eyelids_from_draft(
    ref_rgb: np.ndarray,
    cabeca_alpha: np.ndarray,
    draft_path: Path,
) -> tuple[Image.Image, Image.Image]:
    """Slice natural 3D half/closed eyelid overlays per eye from real 3D blink draft."""
    dr_raw = np.array(Image.open(draft_path).convert("RGB"), dtype=np.uint8)
    # Align by nose/smile/chin so closed eyes do not bias alignment
    aligned = align_to_reference(dr_raw, ref_rgb, patch_box=(460, 600, 315, 515))

    h, w, _ = ref_rgb.shape
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    brow_guard = np.clip((yy - 344.0) / 14.0, 0.0, 1.0)
    safe_face_eye = cabeca_alpha >= 160

    closed_rgba = np.zeros((h, w, 4), dtype=np.uint8)
    half_rgba = np.zeros((h, w, 4), dtype=np.uint8)

    for ecx, ecy, erx, ery in ((305.0, 397.0, 52.0, 36.0), (497.0, 394.0, 65.0, 35.0)):
        nr = np.sqrt(((xx - ecx) / erx) ** 2 + ((yy - ecy) / ery) ** 2)
        ring = safe_face_eye & (nr >= 0.78) & (nr <= 0.98) & (yy >= 352.0)
        matched = match_ring_color(aligned, ref_rgb, ring)

        a_closed = np.where(safe_face_eye, np.clip((1.0 - nr) / 0.22, 0.0, 1.0) * brow_guard, 0.0)
        a_half = a_closed * np.clip((ecy + 2.0 - yy) / 5.0, 0.0, 1.0)

        mc = a_closed > 0.002
        closed_rgba[mc, :3] = matched[mc]
        closed_rgba[mc, 3] = np.maximum(
            closed_rgba[mc, 3], np.clip(a_closed[mc] * 255.0, 0, 255).astype(np.uint8)
        )

        mh = a_half > 0.002
        half_rgba[mh, :3] = matched[mh]
        half_rgba[mh, 3] = np.maximum(
            half_rgba[mh, 3], np.clip(a_half[mh] * 255.0, 0, 255).astype(np.uint8)
        )

    return Image.fromarray(half_rgba, mode="RGBA"), Image.fromarray(closed_rgba, mode="RGBA")


def match_ring_color(draft_rgb: np.ndarray, ref_rgb: np.ndarray, ring_mask: np.ndarray) -> np.ndarray:
    """Scale draft RGB channels to match reference skin tone precisely along the mouth feather perimeter."""
    ref_mean = ref_rgb[ring_mask].astype(np.float32).mean(axis=0)
    dr_mean = draft_rgb[ring_mask].astype(np.float32).mean(axis=0)
    gain = np.clip(ref_mean / np.maximum(dr_mean, 1.0), 0.85, 1.18)
    return np.clip(draft_rgb.astype(np.float32) * gain[None, None, :], 0, 255).astype(np.uint8)


def connected_component_from_seeds(mask: np.ndarray, seeds: Iterable[tuple[int, int]]) -> np.ndarray:
    """Return 4-connected True pixels in mask reachable from given seeds (searching r<=14 if off by px)."""
    h, w = mask.shape
    out = np.zeros((h, w), dtype=bool)
    q: deque[tuple[int, int]] = deque()
    for sy, sx in seeds:
        if 0 <= sy < h and 0 <= sx < w and mask[sy, sx]:
            q.append((sy, sx))
            out[sy, sx] = True
        else:
            found = False
            for r in range(1, 15):
                for yy in range(max(0, sy - r), min(h, sy + r + 1)):
                    for xx in range(max(0, sx - r), min(w, sx + r + 1)):
                        if mask[yy, xx]:
                            q.append((yy, xx))
                            out[yy, xx] = True
                            found = True
                            break
                    if found:
                        break
                if found:
                    break
    while q:
        y, x = q.popleft()
        for ny, nx in ((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)):
            if 0 <= ny < h and 0 <= nx < w and mask[ny, nx] and not out[ny, nx]:
                out[ny, nx] = True
                q.append((ny, nx))
    return out


def horizontal_inpaint_rgb(rgb: np.ndarray, mask: np.ndarray) -> np.ndarray:
    """Interpolate vertical structures smoothly from pixels horizontally adjacent on each scanline."""
    out = rgb.copy().astype(np.float32)
    h, w, _ = out.shape
    for y in range(h):
        xs = np.where(mask[y])[0]
        if len(xs) == 0:
            continue
        splits = np.where(np.diff(xs) > 1)[0]
        starts = np.r_[xs[0], xs[splits + 1]]
        ends = np.r_[xs[splits], xs[-1]]
        for x0, x1 in zip(starts, ends):
            ls = out[y, max(0, x0 - 6) : x0]
            rs = out[y, x1 + 1 : min(w, x1 + 7)]
            if len(ls) and len(rs):
                c0, c1 = ls.mean(axis=0), rs.mean(axis=0)
                span = max(1, x1 - x0 + 2)
                for x in range(x0, x1 + 1):
                    t = (x - x0 + 1) / span
                    out[y, x] = (1.0 - t) * c0 + t * c1
            elif len(ls):
                out[y, x0 : x1 + 1] = ls.mean(axis=0)
            elif len(rs):
                out[y, x0 : x1 + 1] = rs.mean(axis=0)
    return np.clip(out, 0, 255).astype(np.uint8)


def harmonic_skin_inpaint(rgb: np.ndarray, mask: np.ndarray, valid_skin: np.ndarray, n_iters: int = 80) -> np.ndarray:
    """Smoothly diffuse valid green skin colors across masked brow pixels without sampling dark hat brim."""
    out = rgb.copy().astype(np.float32)
    h, w, _ = out.shape
    ys, xs = np.where(mask)
    if len(ys) == 0:
        return rgb
    y0, y1 = max(1, int(ys.min()) - 6), min(h - 1, int(ys.max()) + 6)
    x0, x1 = max(1, int(xs.min()) - 6), min(w - 1, int(xs.max()) + 6)
    sub_m = mask[y0:y1, x0:x1]
    sub_v = valid_skin[y0:y1, x0:x1] & (~sub_m)
    buf = out[y0:y1, x0:x1].copy()
    # Initialize mask pixels with mean valid neighboring green skin
    mean_skin = buf[sub_v].mean(axis=0) if np.any(sub_v) else np.array([105.0, 152.0, 48.0])
    buf[sub_m] = mean_skin

    fixed = sub_v
    for _ in range(n_iters):
        up = np.roll(buf, 1, axis=0)
        dn = np.roll(buf, -1, axis=0)
        lf = np.roll(buf, 1, axis=1)
        rt = np.roll(buf, -1, axis=1)
        avg = 0.25 * (up + dn + lf + rt)
        buf[sub_m & (~fixed)] = avg[sub_m & (~fixed)]
    out[y0:y1, x0:x1] = buf
    return np.clip(out, 0, 255).astype(np.uint8)


def make_translucent_magnifier_glass(rgba: np.ndarray) -> np.ndarray:
    """Replace cool dark studio glass inside the true elliptical bezel (737, 549) without touching silver rim."""
    h, w, _ = rgba.shape
    rgb = rgba[:, :, :3].astype(np.float32)
    a = rgba[:, :, 3].copy()
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    dx = xx - 737.0
    dy = yy - 549.0
    u = dx * 0.9975 + dy * 0.07
    v = -dx * 0.07 + dy * 0.9975
    dist_norm = np.sqrt((u / 49.5) ** 2 + (v / 62.5) ** 2)
    bright = rgb.mean(axis=2)
    blue_excess = rgb[:, :, 2] - rgb[:, :, 0]
    inside_glass = (
        ((dist_norm < 0.78) & (bright < 98.0) & (blue_excess >= 2.0))
        | ((dist_norm >= 0.78) & (dist_norm < 1.0) & (bright < 90.0) & (blue_excess >= 6.0))
    ) & (a > 0)

    out = rgba.copy()
    out[inside_glass, 0] = 238
    out[inside_glass, 1] = 248
    out[inside_glass, 2] = 255
    out[inside_glass, 3] = np.clip(14.0 + dist_norm[inside_glass] * 14.0, 12, 32).astype(np.uint8)

    diag = np.abs((xx - 722.0) * 0.74 + (yy - 534.0) * 0.67) < 8.5
    streak = inside_glass & diag & (dist_norm < 0.78)
    out[streak, :3] = [255, 255, 255]
    out[streak, 3] = 48
    return out


def make_lantern_beam_sprite(w: int = 896, h: int = 1200) -> Image.Image:
    """Generate soft warm volumetric light cone originating at flashlight lens (84, 515)."""
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    ox, oy = 84.0, 515.0
    dx, dy = xx - ox, yy - oy
    ux, uy = -0.74, 0.67
    proj = dx * ux + dy * uy
    perp = np.abs(dx * (-uy) + dy * ux)
    cone_r = 22.0 + np.maximum(proj, 0.0) * 0.66
    in_cone = (proj >= -8.0) & (proj <= 310.0) & (perp <= cone_r)
    radial = np.clip(1.0 - (perp / np.maximum(cone_r, 1.0)) ** 2, 0.0, 1.0)
    axial = np.clip(1.0 - np.maximum(proj, 0.0) / 310.0, 0.0, 1.0) ** 1.35
    alpha = np.where(in_cone, radial * axial * 120.0, 0.0)
    beam = np.zeros((h, w, 4), dtype=np.uint8)
    beam[:, :, 0] = 255
    beam[:, :, 1] = 242
    beam[:, :, 2] = 185
    beam[:, :, 3] = np.clip(alpha, 0, 255).astype(np.uint8)
    return Image.fromarray(beam, mode="RGBA").filter(ImageFilter.GaussianBlur(4.0))


def make_smooth_eyelids(
    w: int,
    h: int,
    ref_rgb: np.ndarray,
    fg_mask: np.ndarray,
    eye_masks: list[np.ndarray],
) -> tuple[Image.Image, Image.Image]:
    """Generate smooth harmonically-shaded Pixar eyelids with feathered edges and interior lash arcs."""
    eyes_union = np.zeros((h, w), dtype=bool)
    for emask in eye_masks:
        eyes_union |= dilate_mask(emask, 3)

    # Include shaded olive skin on outer left corner (G>=40) so lid seamlessly gradient-matches the brim shadow
    valid_eye_skin = (
        fg_mask
        & (~eyes_union)
        & ((ref_rgb[:, :, 1].astype(np.int16) - ref_rgb[:, :, 0].astype(np.int16)) >= 8)
        & (ref_rgb[:, :, 1] >= 40)
    )

    # Keep left-eye feather strictly right of temple/brim shadow (x >= 269) so no light green haze bleeds onto dark temple
    xx_grid_e = np.broadcast_to(np.arange(w)[None, :], (h, w))
    smooth_eyes: list[np.ndarray] = []
    outer_eyes: list[np.ndarray] = []
    combined_mask = np.zeros((h, w), dtype=bool)
    for idx_e, emask in enumerate(eye_masks):
        blurred = Image.fromarray((dilate_mask(emask, 3).astype(np.uint8) * 255), mode="L").filter(
            ImageFilter.GaussianBlur(2.8)
        )
        sm = (np.array(blurred) > 110) | emask
        out_m = dilate_mask(sm, 7)
        if idx_e == 0:
            sm = sm & (xx_grid_e >= 270)
            out_m = out_m & (xx_grid_e >= 269)
        smooth_eyes.append(sm)
        outer_eyes.append(out_m)
        combined_mask |= dilate_mask(out_m, 3)

    inpainted_skin = harmonic_skin_inpaint(ref_rgb, combined_mask, valid_eye_skin, n_iters=160).astype(np.float32)
    yy_g, _ = np.mgrid[0:h, 0:w]

    skin_mid = ref_rgb[360:405, 370:425].astype(np.float32).mean(axis=(0, 1))
    lash_col = tuple(int(v) for v in np.clip(skin_mid * 0.24, 0, 255)) + (230,)

    results: list[Image.Image] = []
    scale = 2
    for level_frac, is_closed in ((0.50, False), (1.03, True)):
        lid_full = np.zeros((h, w, 4), dtype=np.uint8)
        lash_canvas_2x = Image.new("RGBA", (w * scale, h * scale), (0, 0, 0, 0))
        d2 = ImageDraw.Draw(lash_canvas_2x)

        for sm, out_m in zip(smooth_eyes, outer_eyes):
            eys, exs = np.where(sm)
            ex0, ex1 = int(exs.min()), int(exs.max())
            ey0, ey1 = int(eys.min()), int(eys.max())
            eh = max(1, ey1 - ey0)

            y_cut = ey0 + eh * level_frac
            soft_orbit = (
                np.array(Image.fromarray((out_m.astype(np.uint8) * 255), mode="L").filter(ImageFilter.GaussianBlur(2.4)))
                / 255.0
            )
            if is_closed:
                # Guarantee 100% opaque coverage over dilated sclera/iris opening; feather smoothly outward!
                solid_core = dilate_mask(sm, 3)
                v_alpha = np.where(solid_core, 1.0, soft_orbit)
            else:
                v_alpha = np.minimum(soft_orbit, np.where(out_m, np.clip((y_cut + 2.0 - yy_g) / 3.5, 0.0, 1.0), 0.0))

            alpha_m = np.clip(v_alpha * 255.0, 0, 255).astype(np.uint8)

            # Subtle 3D upper-dome shading (soft 0.90 crease -> 1.00 lid dome -> 0.89 lower groove)
            t = np.clip((yy_g - ey0) / float(eh), 0.0, 1.0)
            vol_gain = (0.89 + 0.11 * np.sin(t * np.pi))[:, :, None]
            shaded = np.clip(inpainted_skin * vol_gain, 0, 255).astype(np.uint8)

            patch_mask = alpha_m > 0
            lid_full[patch_mask, :3] = shaded[patch_mask]
            lid_full[patch_mask, 3] = np.maximum(lid_full[patch_mask, 3], alpha_m[patch_mask])

            # Curved lash crease strictly inside shrunken interior so ends never touch outer border
            lx0 = (ex0 + 7) * scale
            lx1 = (ex1 - 7) * scale
            lx_mid = (lx0 + lx1) // 2
            y_lash = int((ey0 + eh * (0.62 if is_closed else level_frac * 0.90)) * scale)
            y_dip = y_lash + (13 if is_closed else 6)
            pts = []
            for s_idx in range(25):
                u = s_idx / 24.0
                px = int((1 - u) ** 2 * lx0 + 2 * (1 - u) * u * lx_mid + u ** 2 * lx1)
                py = int((1 - u) ** 2 * (y_lash - 6) + 2 * (1 - u) * u * y_dip + u ** 2 * (y_lash - 7))
                pts.append((px, py))
            d2.line(pts, fill=lash_col, width=7 if is_closed else 6, joint="curve")

        lash_1x = np.array(lash_canvas_2x.resize((w, h), Image.Resampling.LANCZOS))
        # Composite lash stroke ONLY where lid_full alpha is solidly inside the orbit
        inner_clip = np.clip(lid_full[:, :, 3].astype(np.float32) / 255.0, 0.0, 1.0)
        lash_a = (lash_1x[:, :, 3].astype(np.float32) * inner_clip) / 255.0
        out_img = Image.fromarray(lid_full, mode="RGBA")
        clipped_lash = lash_1x.copy()
        clipped_lash[:, :, 3] = np.clip(lash_a * 255.0, 0, 255).astype(np.uint8)
        out_img.alpha_composite(Image.fromarray(clipped_lash, mode="RGBA"))
        results.append(out_img)
    return results[0], results[1]


def build_rig(drafts_dir: Path, out_dir: Path) -> None:
    """Build all cleanly separated character layers, visemes, poses, and rig.json manifest."""
    out_dir.mkdir(parents=True, exist_ok=True)
    vis_dir = out_dir / "visemas"
    vis_dir.mkdir(parents=True, exist_ok=True)

    ref_rgb = np.array(Image.open(REF_IMG_PATH).convert("RGB"), dtype=np.uint8)
    h, w, _ = ref_rgb.shape
    ref_rgba_img = remove_backdrop_rgba(ref_rgb)
    ref_rgba = np.array(ref_rgba_img)
    fg = ref_rgba[:, :, 3] > 20
    yy_idx, xx_idx = np.mgrid[0:h, 0:w]

    # 1. Isolate Torso Neutro starting UP at y >= 584 behind chin shadow (prevents any neck gap during head bob!)
    torso_mask = (yy_idx >= 584) & fg & ~((yy_idx >= 435) & (yy_idx <= 645) & (xx_idx >= 638) & (xx_idx <= 822))
    torso_neutro = ref_rgba.copy()
    torso_neutro[~torso_mask, 3] = 0
    fade_row = np.clip((yy_idx - 582) / 10.0, 0.0, 1.0)
    torso_neutro[:, :, 3] = np.where(torso_mask, (torso_neutro[:, :, 3] * fade_row).astype(np.uint8), 0)
    Image.fromarray(torso_neutro, mode="RGBA").save(out_dir / "torso_neutro.png")

    # 2. Separate Antennae & Mechanical Hat Gadgets cleanly by Color + Connectivity
    green_fg = fg & (ref_rgb[:, :, 1].astype(np.int16) - ref_rgb[:, :, 0].astype(np.int16) > 10)
    ant_l_raw = connected_component_from_seeds(
        green_fg & (yy_idx <= 232) & (xx_idx <= 355), [(120, 145), (160, 290), (200, 330)]
    )
    ant_r_raw = connected_component_from_seeds(
        green_fg & (yy_idx <= 228) & (xx_idx >= 365) & (xx_idx <= 515), [(80, 440), (150, 485)]
    )

    for name, raw_m in [("antena_esq", ant_l_raw), ("antena_dir", ant_r_raw)]:
        ant_arr = ref_rgba.copy()
        keep = dilate_mask(raw_m, 3) & fg
        ant_arr[~keep, 3] = 0
        Image.fromarray(ant_arr, mode="RGBA").save(out_dir / f"{name}.png")

    # Neutral/metallic mask cleanly isolates rods & gadgets without biting khaki hat felt!
    neutral_fg = fg & (np.abs(ref_rgb[:, :, 1].astype(np.int16) - ref_rgb[:, :, 0].astype(np.int16)) < 20) & (
        np.abs(ref_rgb[:, :, 2].astype(np.int16) - ref_rgb[:, :, 1].astype(np.int16)) < 24
    )
    # Lantern arm + warm bulb glow (exclude left antenna & face/hat brim)
    lantern_base = fg & (~dilate_mask(ant_l_raw, 5)) & (
        ((xx_idx <= 336) & (yy_idx <= 224) & neutral_fg)
        | ((xx_idx <= 185) & (yy_idx > 224) & (yy_idx <= 365))
        | ((xx_idx <= 245) & (yy_idx > 365) & (yy_idx <= 565))
    )
    lantern_mask = connected_component_from_seeds(lantern_base, [(165, 250), (350, 130), (490, 95), (195, 315)])
    lantern_arr = ref_rgba.copy()
    lantern_arr[~(dilate_mask(lantern_mask, 3) & fg & (~dilate_mask(ant_l_raw, 3))), 3] = 0
    Image.fromarray(lantern_arr, mode="RGBA").save(out_dir / "haste_lanterna.png")
    make_lantern_beam_sprite(w, h).save(out_dir / "feixe_lanterna.png")

    # Magnifier metal arm + glass ring isolated purely by metal neutrality/gap (exclude left crown olive felt!)
    not_crown_felt = ~((xx_idx <= 592) & ((ref_rgb[:, :, 1].astype(np.int16) - ref_rgb[:, :, 2].astype(np.int16)) >= 14))
    lupa_base = fg & (
        ((xx_idx >= 566) & (xx_idx <= 630) & (yy_idx >= 135) & (yy_idx <= 220) & neutral_fg & not_crown_felt)
        | ((xx_idx >= 615) & (yy_idx <= 245) & (neutral_fg | (xx_idx >= 680)))
        | ((xx_idx >= 755) & (yy_idx > 245) & (yy_idx <= 375))
        | ((xx_idx >= 642) & (yy_idx > 375) & (yy_idx <= 645))
    )
    lupa_mask = connected_component_from_seeds(lupa_base, [(115, 645), (168, 602), (300, 815), (540, 795)])
    lupa_arr = ref_rgba.copy()
    lupa_arr[~(dilate_mask(lupa_mask, 3) & fg), 3] = 0
    lupa_arr = make_translucent_magnifier_glass(lupa_arr)
    Image.fromarray(lupa_arr, mode="RGBA").save(out_dir / "haste_lupa.png")

    # 3. Extract Eyebrows cleanly & Smooth-Inpaint Cabeca Base (zero ghost brows / continuous hat crown)
    brown_mask = (
        (ref_rgb[:, :, 0].astype(np.int16) > ref_rgb[:, :, 1].astype(np.int16) + 4)
        & (ref_rgb[:, :, 0] < 130)
        & (ref_rgb[:, :, 1] < 90)
        & (ref_rgb[:, :, 2] < 55)
        & (yy_idx >= 294)
        & (yy_idx <= 345)
    )
    brow_l_mask = connected_component_from_seeds(brown_mask & (xx_idx >= 250) & (xx_idx <= 360), [(312, 300)])
    brow_r_mask = connected_component_from_seeds(brown_mask & (xx_idx >= 415) & (xx_idx <= 565), [(315, 480)])

    for bname, bmask in [("sobrancelha_esq", brow_l_mask), ("sobrancelha_dir", brow_r_mask)]:
        b_soft = dilate_mask(bmask, 5)
        b_arr = ref_rgba.copy()
        b_alpha = Image.fromarray((b_soft.astype(np.uint8) * 255), mode="L").filter(ImageFilter.GaussianBlur(1.1))
        b_arr[:, :, 3] = np.where(bmask, 255, np.array(b_alpha))
        b_arr[~b_soft, 3] = 0
        Image.fromarray(b_arr, mode="RGBA").save(out_dir / f"{bname}.png")

    # Build clean cabeca_base (keep continuous crown felt behind pivot sockets; remove sky wedge under right antenna)
    head_mask = fg.copy() & (yy_idx <= 630)
    sky_arch = (
        (yy_idx <= 135)
        & (xx_idx >= 360)
        & (xx_idx <= 475)
        & (ref_rgb[:, :, 2].astype(np.int16) >= np.minimum(ref_rgb[:, :, 0], ref_rgb[:, :, 1]).astype(np.int16) + 1)
        & (ref_rgb.max(axis=2) < 75)
    )
    head_mask &= ~(dilate_mask(sky_arch, 7) & (ref_rgb.max(axis=2) < 88) & (ref_rgb[:, :, 1] < 65) & (ref_rgb[:, :, 2] >= np.minimum(ref_rgb[:, :, 0], ref_rgb[:, :, 1])))

    x_crown_r = 535.0 + (yy_idx - 135.0) * 0.72
    in_crown_r = (yy_idx >= 135) & (yy_idx <= 235) & (xx_idx <= x_crown_r)
    x_crown_l = 338.0 - (yy_idx - 160.0) * 0.55
    in_crown_l = (yy_idx >= 160) & (yy_idx <= 230) & (xx_idx >= x_crown_l)

    head_mask &= ~dilate_mask(ant_l_raw, 11)
    head_mask &= ~(dilate_mask(ant_r_raw, 11) & (yy_idx <= 116))
    head_mask &= ~(dilate_mask(lantern_mask, 7) & (~in_crown_l))
    head_mask &= ~(dilate_mask(lupa_mask, 7) & (~in_crown_r))
    top_crown = connected_component_from_seeds(head_mask, [(250, 420), (450, 400)])
    head_mask &= top_crown

    cabeca_rgb = ref_rgb.copy()
    # Harmonic olive-felt inpaint behind antenna roots AND socket overlaps (never sample dark sky!)
    crown_inpaint = (ant_r_raw & (yy_idx >= 110) & (yy_idx <= 228)) | (ant_l_raw & (yy_idx >= 182) & (yy_idx <= 232))
    socket_overlap = dilate_mask(
        ((lupa_mask & in_crown_r) | (lantern_mask & in_crown_l) | crown_inpaint), 5
    ) & head_mask
    valid_hat_felt = (
        head_mask
        & (~socket_overlap)
        & ((ref_rgb[:, :, 1].astype(np.int16) - ref_rgb[:, :, 2].astype(np.int16)) >= 10)
        & (ref_rgb.mean(axis=2) > 45)
    )
    cabeca_rgb = harmonic_skin_inpaint(cabeca_rgb, socket_overlap, valid_hat_felt, n_iters=140)

    # Harmonic green-skin-only diffusion across expanded eyebrow masks (eliminates brow shadow ghost in analitico)
    valid_green_skin = (
        fg
        & (ref_rgb[:, :, 1].astype(np.int16) - ref_rgb[:, :, 0].astype(np.int16) >= 14)
        & (ref_rgb[:, :, 1] >= 95)
        & (yy_idx >= 292)
    )
    cabeca_rgb = harmonic_skin_inpaint(cabeca_rgb, dilate_mask(brow_l_mask | brow_r_mask, 9), valid_green_skin, n_iters=110)

    cabeca_arr = np.dstack([cabeca_rgb, ref_rgba[:, :, 3]]).astype(np.uint8)
    cabeca_arr[~head_mask, 3] = 0
    chin_fade = np.where(yy_idx >= 616, np.clip((630 - yy_idx) / 14.0, 0.0, 1.0), 1.0)
    cabeca_arr[:, :, 3] = (cabeca_arr[:, :, 3] * chin_fade).astype(np.uint8)
    Image.fromarray(cabeca_arr, mode="RGBA").save(out_dir / "cabeca_base.png")

    # 4. Curved Smooth Eyelids & Subtle Right Gaze (rounded almond aperture so left lid has no flat edges)
    non_green = (ref_rgb[:, :, 1].astype(np.int16) - ref_rgb[:, :, 0].astype(np.int16) < 14) & fg
    eye_l_almond = (((xx_idx - 306.0) / 40.5) ** 2 + ((yy_idx - 396.0) / 27.5) ** 2) <= 1.0
    eye_l_raw = connected_component_from_seeds(
        non_green & eye_l_almond, [(395, 306)]
    )
    eye_r_raw = connected_component_from_seeds(
        non_green & (xx_idx >= 446) & (xx_idx <= 552) & (yy_idx >= 364) & (yy_idx <= 420), [(392, 495)]
    )
    eyelid_draft = drafts_dir / "olhos_fechados.jpg"
    if eyelid_draft.exists():
        olhos_meio, olhos_fechado = extract_eyelids_from_draft(ref_rgb, cabeca_arr[:, :, 3], eyelid_draft)
    else:
        olhos_meio, olhos_fechado = make_smooth_eyelids(w, h, ref_rgb, fg, [eye_l_raw, eye_r_raw])
    olhos_meio.save(out_dir / "olhos_meio.png")
    olhos_fechado.save(out_dir / "olhos_fechado.png")

    gaze_arr = np.zeros((h, w, 4), dtype=np.uint8)
    for emask in (eye_l_raw, eye_r_raw):
        sclera_px = ref_rgb[emask & (ref_rgb.mean(axis=2) > 155)]
        sclera_col = sclera_px.mean(axis=0) if len(sclera_px) else np.array([220.0, 224.0, 225.0])
        iris_m = emask & (ref_rgb.mean(axis=2) < 130)
        ys_i, xs_i = np.where(iris_m)
        if not len(xs_i):
            continue
        gaze_arr[emask, :3] = np.clip(sclera_col, 0, 255).astype(np.uint8)
        gaze_arr[emask, 3] = 255
        for y, x in zip(ys_i, xs_i):
            nx = min(w - 1, x + 5)
            if emask[y, nx]:
                gaze_arr[y, nx, :3] = ref_rgb[y, x]
                gaze_arr[y, nx, 3] = 255
    Image.fromarray(gaze_arr, mode="RGBA").save(out_dir / "olhos_direita.png")

    # 5. Extract Seam-Free Viseme Sprites covering full right smile corner so no smile ghost leaks in OU
    cx, cy = 412.0, 560.0
    rx, ry = 98.0, 64.0
    norm_r = np.sqrt(((xx_idx - cx) / rx) ** 2 + ((yy_idx - cy) / ry) ** 2)
    mouth_alpha = np.clip((1.0 - norm_r) / 0.28, 0.0, 1.0)
    nose_guard = np.clip((yy_idx - 496.0) / 18.0, 0.0, 1.0)
    safe_face = erode_mask(cabeca_arr[:, :, 3] >= 245, 7)
    mouth_alpha_u8 = np.where(safe_face, (np.minimum(mouth_alpha, nose_guard) * 255).astype(np.uint8), 0)
    perimeter_ring = safe_face & (norm_r >= 0.72) & (norm_r <= 0.98) & (yy_idx >= 510)

    viseme_files = {
        "BMP": drafts_dir / "visema_BMP.jpg",
        "FV": drafts_dir / "visema_FV.jpg",
        "A": drafts_dir / "visema_A.jpg",
        "EI": drafts_dir / "visema_EI.jpg",
        "OU": drafts_dir / "visema_OU.jpg",
    }
    vis_paths_json = {}
    matched_visemes: dict[str, np.ndarray] = {}
    for vcode, vpath in viseme_files.items():
        dr_raw = np.array(Image.open(vpath).convert("RGB"), dtype=np.uint8)
        dr_aligned = align_to_reference(dr_raw, ref_rgb)
        matched_visemes[vcode] = match_ring_color(dr_aligned, ref_rgb, perimeter_ring)

    # Blend OU smoothly onto BMP cheek base starting at x=432..448 so zero diagonal dimple crease remains
    bmp_base = matched_visemes["BMP"].astype(np.float32)
    ou_src = matched_visemes["OU"].astype(np.float32)
    ou_w = (1.0 - np.clip((xx_idx - 432.0) / 16.0, 0.0, 1.0))[:, :, None]
    matched_visemes["OU"] = np.clip(bmp_base * (1.0 - ou_w) + ou_src * ou_w, 0, 255).astype(np.uint8)

    for vcode, dr_matched in matched_visemes.items():
        v_rgba = np.dstack([dr_matched, mouth_alpha_u8]).astype(np.uint8)
        out_p = vis_dir / f"visema_{vcode}.png"
        Image.fromarray(v_rgba, mode="RGBA").save(out_p)
        vis_paths_json[vcode] = f"visemas/visema_{vcode}.png"
        if vcode == "BMP":
            Image.fromarray(v_rgba, mode="RGBA").save(vis_dir / "visema_X.png")
            vis_paths_json["X"] = "visemas/visema_X.png"

    sorriso_rgba = np.dstack([ref_rgb, mouth_alpha_u8]).astype(np.uint8)
    Image.fromarray(sorriso_rgba, mode="RGBA").save(vis_dir / "visema_SORRISO.png")
    vis_paths_json["SORRISO"] = "visemas/visema_SORRISO.png"

    # 6. Extract Extra Arm Pose Layers (keep full neck collar at x<638 so torso_apontar has zero slit)
    ap_raw = align_to_reference(np.array(Image.open(drafts_dir / "pose_apontar.jpg").convert("RGB"), dtype=np.uint8), ref_rgb)
    ap_rgba = np.array(remove_backdrop_rgba(ap_raw))
    diff_ap = np.mean(np.abs(ap_raw.astype(np.float32) - ref_rgb.astype(np.float32)), axis=2)
    lupa_unchanged_in_overlap = (xx_idx >= 638) & (xx_idx <= 814) & (yy_idx >= 435) & (yy_idx <= 645) & (diff_ap < 18)
    ap_mask = ((yy_idx >= 584) | ((xx_idx >= 742) & (yy_idx >= 515) & (yy_idx <= 645))) & (ap_rgba[:, :, 3] > 20) & (~lupa_unchanged_in_overlap)
    torso_ap = ap_rgba.copy()
    torso_ap[~ap_mask, 3] = 0
    torso_ap[:, :, 3] = np.where((yy_idx < 600) & (xx_idx < 740), (torso_ap[:, :, 3] * fade_row).astype(np.uint8), torso_ap[:, :, 3])
    Image.fromarray(torso_ap, mode="RGBA").save(out_dir / "torso_apontar.png")

    tc_raw = align_to_reference(np.array(Image.open(drafts_dir / "pose_toque_chapeu.jpg").convert("RGB"), dtype=np.uint8), ref_rgb)
    tc_rgba = np.array(remove_backdrop_rgba(tc_raw))
    diff_tc = np.mean(np.abs(tc_raw.astype(np.float32) - ref_rgb.astype(np.float32)), axis=2)
    tc_torso_mask = (yy_idx >= 584) & (tc_rgba[:, :, 3] > 20) & ~((yy_idx <= 645) & (xx_idx >= 640) & (xx_idx <= 780) & (diff_tc < 18))
    torso_tc = tc_rgba.copy()
    torso_tc[~tc_torso_mask, 3] = 0
    torso_tc[:, :, 3] = np.where(tc_torso_mask, (torso_tc[:, :, 3] * fade_row).astype(np.uint8), 0)
    Image.fromarray(torso_tc, mode="RGBA").save(out_dir / "torso_toque_chapeu.png")

    raised_arm_cand = (diff_tc > 20) & (xx_idx >= 555) & (xx_idx <= 855) & (yy_idx >= 245) & (yy_idx <= 665) & (tc_rgba[:, :, 3] > 20)
    raised_arm_mask = connected_component_from_seeds(raised_arm_cand, [(350, 730), (310, 680), (500, 795), (600, 795)])
    arm_alpha = Image.fromarray((dilate_mask(raised_arm_mask, 3).astype(np.uint8) * 255), mode="L").filter(ImageFilter.GaussianBlur(0.65))
    braco_tc = tc_rgba.copy()
    braco_tc[:, :, 3] = np.minimum(braco_tc[:, :, 3], np.array(arm_alpha))
    braco_tc[~dilate_mask(raised_arm_mask, 5), 3] = 0
    Image.fromarray(braco_tc, mode="RGBA").save(out_dir / "braco_toque_chapeu.png")

    # 7. Write Rig Manifest (rig.json)
    manifest = {
        "name": "Inspetor Bicho Grilo Rig 2.5D",
        "base_size": [w, h],
        "layers": {
            "cabeca_base": "cabeca_base.png",
            "torso_neutro": "torso_neutro.png",
            "torso_apontar": "torso_apontar.png",
            "torso_toque_chapeu": "torso_toque_chapeu.png",
            "braco_toque_chapeu": "braco_toque_chapeu.png",
            "antena_esq": "antena_esq.png",
            "antena_dir": "antena_dir.png",
            "haste_lanterna": "haste_lanterna.png",
            "feixe_lanterna": "feixe_lanterna.png",
            "haste_lupa": "haste_lupa.png",
            "sobrancelha_esq": "sobrancelha_esq.png",
            "sobrancelha_dir": "sobrancelha_dir.png",
            "olhos_meio": "olhos_meio.png",
            "olhos_fechado": "olhos_fechado.png",
            "olhos_direita": "olhos_direita.png",
        },
        "visemas": vis_paths_json,
        "pivots": {
            "antena_esq": [336, 218],
            "antena_dir": [492, 218],
            "haste_lanterna": [332, 198],
            "haste_lupa": [572, 180],
            "cabeca": [430, 595],
        },
        "actions": {
            "neutro": {"torso": "torso_neutro", "lupa_deg": 0.0, "lanterna_deg": 0.0, "lanterna_on": False, "eyebrow": "neutro", "look_at": "camera", "visema_rest": "X"},
            "inspecao_lupa": {"torso": "torso_apontar", "lupa_deg": 18.0, "lanterna_deg": 4.0, "lanterna_on": False, "eyebrow": "analitico", "look_at": "direita", "visema_rest": "X"},
            "lanterna_on": {"torso": "torso_neutro", "lupa_deg": -4.0, "lanterna_deg": -10.0, "lanterna_on": True, "eyebrow": "alerta", "look_at": "camera", "visema_rest": "X"},
            "analitico": {"torso": "torso_neutro", "lupa_deg": -15.0, "lanterna_deg": 5.0, "lanterna_on": False, "eyebrow": "analitico", "look_at": "direita", "visema_rest": "X"},
            "apontar_produto": {"torso": "torso_apontar", "lupa_deg": -10.0, "lanterna_deg": 2.0, "lanterna_on": False, "eyebrow": "neutro", "look_at": "direita", "visema_rest": "SORRISO"},
            "toque_chapeu": {"torso": "torso_toque_chapeu", "foreground_arm": "braco_toque_chapeu", "lupa_deg": 8.0, "lanterna_deg": 6.0, "lanterna_on": False, "eyebrow": "neutro", "look_at": "camera", "visema_rest": "SORRISO"},
        },
    }
    (out_dir / "rig.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2))
    print(f"Rig 2.5D reconstruído (v3) em {out_dir}: {len(manifest['layers'])} camadas + {len(vis_paths_json)} visemas")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Slice and assemble reusable Rig 2.5D PNG layers.")
    parser.add_argument("--drafts-dir", type=Path, default=DEFAULT_DRAFTS_DIR)
    parser.add_argument("--out-dir", type=Path, default=OUT_DIR)
    args = parser.parse_args()
    build_rig(args.drafts_dir, args.out_dir)
