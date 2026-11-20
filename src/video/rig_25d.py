"""Reusable Rig 2.5D renderer for the Inspetor Bicho Grilo character."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFont

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_RIG_DIR = REPO_ROOT / "assets" / "personagem" / "rig"
ARTIFACT_SHEET_PATH = Path(
    "/Users/victorsouza/.gemini/antigravity/brain/b63e20dc-1d81-4695-857d-7e8618ed3bb7/prancha_validacao_rig.png"
)


def _load_font(size: int, bold: bool = True) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for p in (
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ):
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def _transform_layer(
    im: Image.Image,
    angle_deg: float = 0.0,
    pivot: tuple[float, float] | None = None,
    dx: float = 0.0,
    dy: float = 0.0,
) -> Image.Image:
    """Rotate image smoothly around pivot and translate by (dx, dy) preserving canvas size."""
    out = im
    if abs(angle_deg) > 1e-3:
        out = out.rotate(
            angle_deg,
            resample=Image.Resampling.BICUBIC,
            expand=False,
            center=pivot,
        )
    if abs(dx) > 1e-3 or abs(dy) > 1e-3:
        out = ImageChops.offset(out, int(round(dx)), int(round(dy)))
    return out


class InspectorRig:
    """Layered 2.5D character rig supporting PT-BR visemes, blinks, gaze, and hat gadgets."""

    def __init__(self, rig_dir: Path = DEFAULT_RIG_DIR) -> None:
        self.rig_dir = Path(rig_dir)
        manifest_path = self.rig_dir / "rig.json"
        self.manifest = json.loads(manifest_path.read_text())
        self.base_w, self.base_h = self.manifest["base_size"]
        self.pivots: dict[str, tuple[float, float]] = {
            k: (float(v[0]), float(v[1])) for k, v in self.manifest["pivots"].items()
        }
        self.actions: dict[str, dict] = self.manifest["actions"]
        self.layers: dict[str, Image.Image] = {
            k: Image.open(self.rig_dir / rel).convert("RGBA")
            for k, rel in self.manifest["layers"].items()
        }
        self.visemas: dict[str, Image.Image] = {
            k: Image.open(self.rig_dir / rel).convert("RGBA")
            for k, rel in self.manifest["visemas"].items()
        }

    def _blink_state(self, t: float, blink_override: str | None) -> str | None:
        if blink_override in ("meio", "fechado"):
            return blink_override
        if blink_override == "aberto":
            return None
        phase = t % 3.4
        if phase < 0.05:
            return "meio"
        if phase < 0.14:
            return "fechado"
        if phase < 0.19:
            return "meio"
        return None

    def render_frame(
        self,
        t: float = 0.0,
        viseme: str | None = None,
        action: str = "neutro",
        look_at: str | None = None,
        lanterna_on: bool | None = None,
        lupa_deg_offset: float = 0.0,
        eyebrow_mode: str | None = None,
        blink_override: str | None = None,
        target_height: int | None = None,
    ) -> Image.Image:
        """Render a single RGBA character frame at timestamp t."""
        cfg = self.actions.get(action, self.actions["neutro"])
        use_look = look_at if look_at is not None else cfg.get("look_at", "camera")
        use_lantern = cfg.get("lanterna_on", False) if lanterna_on is None else lanterna_on
        use_brow = eyebrow_mode if eyebrow_mode is not None else cfg.get("eyebrow", "neutro")
        use_viseme = viseme if viseme in self.visemas else cfg.get("visema_rest", "X")

        # Gentle organic breathing & sway (freeze rotation when fingers clasp hat brim)
        hat_pinned = action == "toque_chapeu"
        breath_y = math.sin(t * 2.2) * 2.5
        head_y = math.sin(t * 2.2 + 0.3) * 3.0
        head_tilt = 0.0 if hat_pinned else math.sin(t * 1.15) * 1.1
        ant_sway = math.sin(t * 3.1) * 3.2

        canvas = Image.new("RGBA", (self.base_w, self.base_h), (0, 0, 0, 0))

        # 1. Torso base (breathing offset)
        torso_key = cfg.get("torso", "torso_neutro")
        canvas.alpha_composite(_transform_layer(self.layers[torso_key], dy=breath_y))

        # 2. Build Head + Facial Features + Hat Gadgets group
        head_grp = Image.new("RGBA", (self.base_w, self.base_h), (0, 0, 0, 0))
        head_grp.alpha_composite(self.layers["cabeca_base"])

        if use_look in ("direita", "produto"):
            head_grp.alpha_composite(self.layers["olhos_direita"])

        b_state = self._blink_state(t, blink_override)
        if b_state == "meio":
            head_grp.alpha_composite(self.layers["olhos_meio"])
        elif b_state == "fechado":
            head_grp.alpha_composite(self.layers["olhos_fechado"])

        # Eyebrows (expression presets)
        brow_l = self.layers["sobrancelha_esq"]
        brow_r = self.layers["sobrancelha_dir"]
        if use_brow == "analitico":
            brow_l = _transform_layer(brow_l, angle_deg=6.0, pivot=(295, 315), dy=-9)
            brow_r = _transform_layer(brow_r, angle_deg=-5.0, pivot=(490, 315), dy=3)
        elif use_brow == "alerta":
            brow_l = _transform_layer(brow_l, angle_deg=4.0, pivot=(295, 315), dy=-10)
            brow_r = _transform_layer(brow_r, angle_deg=-4.0, pivot=(490, 315), dy=-10)
        head_grp.alpha_composite(brow_l)
        head_grp.alpha_composite(brow_r)

        # Mouth viseme
        head_grp.alpha_composite(self.visemas[use_viseme])

        # Antennae swaying gently from hat crown pivots
        head_grp.alpha_composite(_transform_layer(self.layers["antena_esq"], angle_deg=ant_sway, pivot=self.pivots["antena_esq"]))
        head_grp.alpha_composite(_transform_layer(self.layers["antena_dir"], angle_deg=-ant_sway * 0.85, pivot=self.pivots["antena_dir"]))

        # Mechanical flashlight arm (+ warm beam when lanterna_on=True)
        lanterna_deg = float(cfg.get("lanterna_deg", 0.0)) + math.sin(t * 2.0) * 1.4
        if use_lantern:
            beam = _transform_layer(self.layers["feixe_lanterna"], angle_deg=lanterna_deg, pivot=self.pivots["haste_lanterna"])
            head_grp.alpha_composite(beam)
        head_grp.alpha_composite(_transform_layer(self.layers["haste_lanterna"], angle_deg=lanterna_deg, pivot=self.pivots["haste_lanterna"]))

        # Mechanical magnifying glass arm
        lupa_deg = float(cfg.get("lupa_deg", 0.0)) + lupa_deg_offset + math.sin(t * 1.7 + 0.8) * 1.4
        head_grp.alpha_composite(_transform_layer(self.layers["haste_lupa"], angle_deg=lupa_deg, pivot=self.pivots["haste_lupa"]))

        # Composite Head group over Torso
        canvas.alpha_composite(_transform_layer(head_grp, angle_deg=head_tilt, pivot=self.pivots["cabeca"], dy=head_y))

        # 3. Optional Foreground Arm (hat tip clasps brim smoothly tracking head vertical motion)
        fg_arm_key = cfg.get("foreground_arm")
        if fg_arm_key and fg_arm_key in self.layers:
            canvas.alpha_composite(_transform_layer(self.layers[fg_arm_key], dy=head_y))

        if target_height is not None and target_height != self.base_h:
            tw = int(round(self.base_w * (target_height / self.base_h)))
            canvas = canvas.resize((tw, target_height), Image.Resampling.LANCZOS)
        return canvas


def render_contact_sheet(rig: InspectorRig, out_paths: list[Path]) -> None:
    """Render visual validation contact sheet over split dark/light backdrops to verify zero halo & seams."""
    f_title = _load_font(26, bold=True)
    f_label = _load_font(18, bold=True)
    f_sub = _load_font(14, bold=False)

    actions_list = ["neutro", "inspecao_lupa", "lanterna_on", "analitico", "apontar_produto", "toque_chapeu"]
    viseme_list = [
        ("X (Repouso)", "X", "aberto"),
        ("BMP (M/B/P)", "BMP", "aberto"),
        ("FV (F/V)", "FV", "aberto"),
        ("EI (E/I)", "EI", "aberto"),
        ("A (Aberto)", "A", "aberto"),
        ("OU (Arred.)", "OU", "aberto"),
        ("Piscando", "SORRISO", "fechado"),
    ]

    sheet_w = 1880
    sheet_h = 980
    sheet = Image.new("RGBA", (sheet_w, sheet_h), (18, 24, 38, 255))
    draw = ImageDraw.Draw(sheet)

    draw.text((32, 20), "RIG 2.5D INSPETOR BICHO GRILO — PRANCHA DE VALIDAÇÃO VISUAL", font=f_title, fill=(248, 250, 252))
    draw.text(
        (32, 54),
        "Linha 1: Ações e gestos em fundo misto escuro/claro (verificação anti-halo e vidro translúcido) | Linha 2: 6 Visemas PT-BR + Piscada",
        font=f_sub,
        fill=(148, 163, 184),
    )

    # Row 1: 6 Full-body Actions
    card_w, card_h = 292, 415
    gap = 14
    x_start = 28
    y_row1 = 92
    for idx, act in enumerate(actions_list):
        cx = x_start + idx * (card_w + gap)
        # Split backdrop: left half dark #0f172a, right half light #e2e8f0
        draw.rectangle([cx, y_row1, cx + card_w // 2, y_row1 + card_h - 38], fill=(15, 23, 42, 255))
        draw.rectangle([cx + card_w // 2, y_row1, cx + card_w, y_row1 + card_h - 38], fill=(226, 232, 240, 255))
        draw.rectangle([cx, y_row1, cx + card_w, y_row1 + card_h], outline=(71, 85, 105, 255), width=2)

        pose_img = rig.render_frame(t=0.4, action=act, blink_override="aberto", target_height=card_h - 46)
        px = cx + (card_w - pose_img.width) // 2
        py = y_row1 + 6
        sheet.alpha_composite(pose_img, (px, py))

        draw.rectangle([cx, y_row1 + card_h - 38, cx + card_w, y_row1 + card_h], fill=(30, 41, 59, 255))
        draw.text((cx + 12, y_row1 + card_h - 30), act, font=f_label, fill=(241, 245, 249))

    # Row 2: 7 Tight Facial Viseme & Blink Crops
    cw2, ch2 = 248, 390
    gap2 = 14
    x_start2 = 28
    y_row2 = 540
    for idx, (label, vis, blink_ovr) in enumerate(viseme_list):
        cx = x_start2 + idx * (cw2 + gap2)
        bg_col = (24, 34, 52, 255) if idx % 2 == 0 else (203, 213, 225, 255)
        draw.rectangle([cx, y_row2, cx + cw2, y_row2 + ch2 - 36], fill=bg_col)
        draw.rectangle([cx, y_row2, cx + cw2, y_row2 + ch2], outline=(71, 85, 105, 255), width=2)

        full = rig.render_frame(t=0.4, viseme=vis, action="neutro", blink_override=blink_ovr)
        # Tight face crop centered around eyes + mouth (x=235..585, y=260..635)
        face_crop = full.crop((235, 255, 585, 635))
        face_crop.thumbnail((cw2 - 12, ch2 - 48), Image.Resampling.LANCZOS)
        fx = cx + (cw2 - face_crop.width) // 2
        fy = y_row2 + (ch2 - 36 - face_crop.height) // 2
        sheet.alpha_composite(face_crop, (fx, fy))

        draw.rectangle([cx, y_row2 + ch2 - 36, cx + cw2, y_row2 + ch2], fill=(30, 41, 59, 255))
        draw.text((cx + 12, y_row2 + ch2 - 28), label, font=f_label, fill=(241, 245, 249))

    for out_p in out_paths:
        out_p.parent.mkdir(parents=True, exist_ok=True)
        sheet.convert("RGB").save(out_p, quality=94)
        print(f"Prancha salva em {out_p}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Inspect and validate the Rig 2.5D character layers.")
    parser.add_argument("--rig-dir", type=Path, default=DEFAULT_RIG_DIR)
    parser.add_argument("--sheet", action="store_true", help="Render validation contact sheet.")
    args = parser.parse_args()
    r = InspectorRig(args.rig_dir)
    if args.sheet:
        render_contact_sheet(r, [args.rig_dir / "prancha_validacao_rig.png", ARTIFACT_SHEET_PATH])
