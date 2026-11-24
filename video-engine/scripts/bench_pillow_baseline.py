"""Benchmark Candidato C (Baseline): Pillow + InspectorRig + ffmpeg (h264_videotoolbox) for 120 frames at 1080x1920."""

from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from src.video.rig_25d import InspectorRig  # noqa: E402

OUT_DIR = REPO_ROOT / "video-engine" / "_bench_out"


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_mp4 = OUT_DIR / "pillow_bench.mp4"
    t0 = time.perf_counter()

    rig = InspectorRig()
    font_lg = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 42)
    font_md = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 26)
    visemas = ["X", "A", "OU", "EI", "BMP", "FV", "SORRISO"]

    proc = subprocess.Popen(
        [
            "ffmpeg",
            "-y",
            "-f",
            "rawvideo",
            "-vcodec",
            "rawvideo",
            "-s",
            "1080x1920",
            "-pix_fmt",
            "rgb24",
            "-r",
            "24",
            "-i",
            "-",
            "-c:v",
            "h264_videotoolbox",
            "-b:v",
            "6M",
            "-pix_fmt",
            "yuv420p",
            str(out_mp4),
        ],
        stdin=subprocess.PIPE,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    assert proc.stdin is not None

    bg = Image.new("RGBA", (1080, 1920), (15, 31, 28, 255))
    for frame in range(120):
        t = frame / 24.0
        canvas = bg.copy()
        draw = ImageDraw.Draw(canvas)
        draw.rounded_rectangle((65, 296, 740, 356), radius=28, fill=(15, 23, 42, 220), outline=(52, 211, 153, 255), width=2)
        draw.text((92, 312), "TRILHA LEVE: 90% MENOS PESO NA MOCHILA", font=font_md, fill=(236, 253, 245, 255))

        draw.rounded_rectangle((65, 380, 887, 880), radius=32, fill=(15, 23, 42, 210), outline=(255, 255, 255, 60), width=2)
        draw.text((98, 412), "COMO A LIOFILIZACAO FUNCIONA", font=font_md, fill=(251, 191, 36, 255))
        for idx, title in enumerate(("1. Gelo Rapido", "2. Alto Vacuo", "3. Crocante")):
            x0 = 98 + idx * 255
            draw.rounded_rectangle((x0, 470, x0 + 235, 610), radius=20, fill=(30, 41, 59, 230), outline=(52, 211, 153, 255), width=2)
            draw.text((x0 + 16, 515), title, font=font_md, fill=(255, 255, 255, 255))

        w_fresh = int(min(1.0, max(0.0, (frame - 10) / 35.0)) * 750)
        w_freeze = int(min(0.12, max(0.0, (frame - 28) / 37.0) * 0.12) * 750)
        draw.rounded_rectangle((98, 690, 98 + max(10, w_fresh), 714), radius=10, fill=(239, 68, 68, 255))
        draw.rounded_rectangle((98, 780, 98 + max(10, w_freeze), 804), radius=10, fill=(16, 185, 129, 255))

        rig_img = rig.render_frame(t=t, action="inspecao_lupa", viseme=visemas[(frame // 4) % len(visemas)], target_height=308)
        canvas.alpha_composite(rig_img, (65, 935))

        draw.rounded_rectangle((310, 1080, 887, 1185), radius=22, fill=(9, 13, 22, 230), outline=(250, 204, 21, 180), width=2)
        draw.text((350, 1110), "90% menos peso!", font=font_lg, fill=(250, 204, 21, 255))

        proc.stdin.write(canvas.convert("RGB").tobytes())

    proc.stdin.close()
    proc.wait()
    elapsed = time.perf_counter() - t0
    print(f"PILLOW_ELAPSED={elapsed:.3f}")


if __name__ == "__main__":
    main()
