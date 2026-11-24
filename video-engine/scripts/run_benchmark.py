"""Orchestrate empirical 5s (120 frames @ 24fps, 1080x1920) benchmark on Intel Core i7-5557U."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
VE_DIR = REPO_ROOT / "video-engine"
OUT_DIR = VE_DIR / "_bench_out"
PUBLIC_DIR = VE_DIR / "public"
CHROME_PATH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def _probe(mp4: Path) -> dict:
    out = subprocess.check_output(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration,size:stream=codec_name,width,height,nb_frames",
            "-of",
            "json",
            str(mp4),
        ],
        text=True,
    )
    return json.loads(out)


def _extract_frame(mp4: Path, png_out: Path, sec: float = 2.0) -> None:
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-ss",
            f"{sec:.2f}",
            "-i",
            str(mp4),
            "-frames:v",
            "1",
            str(png_out),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def _run_timed(cmd: list[str], cwd: Path) -> tuple[float, float, str]:
    """Run command via /usr/bin/time -l on macOS to capture wall time and peak RSS MB."""
    t0 = time.perf_counter()
    res = subprocess.run(
        ["/usr/bin/time", "-l"] + cmd,
        cwd=str(cwd),
        capture_output=True,
        text=True,
        check=True,
    )
    elapsed = time.perf_counter() - t0
    peak_mb = 0.0
    for line in res.stderr.splitlines():
        if "maximum resident set size" in line:
            try:
                raw = int(line.strip().split()[0])
                peak_mb = round(raw / (1024 * 1024), 1)
            except ValueError:
                pass
    return round(elapsed, 2), peak_mb, res.stdout


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    PUBLIC_DIR.mkdir(parents=True, exist_ok=True)
    rig_link = PUBLIC_DIR / "rig"
    if not rig_link.exists():
        os.symlink(REPO_ROOT / "assets" / "personagem" / "rig", rig_link)

    results: dict[str, dict] = {}

    # 1. Baseline: Pillow + InspectorRig + h264_videotoolbox
    print("[1/3] Running Pillow baseline...")
    el_pil, rss_pil, _ = _run_timed(
        [str(REPO_ROOT / ".venv" / "bin" / "python"), "scripts/bench_pillow_baseline.py"],
        cwd=VE_DIR,
    )
    mp4_pil = OUT_DIR / "pillow_bench.mp4"
    _extract_frame(mp4_pil, OUT_DIR / "frame_pillow.png")
    results["pillow_baseline"] = {
        "engine": "Python Pillow + numpy + ffmpeg (h264_videotoolbox)",
        "clip_duration_s": 5.0,
        "frames": 120,
        "resolution": "1080x1920",
        "concurrency": 1,
        "wall_time_s": el_pil,
        "realtime_factor_x": round(el_pil / 5.0, 2),
        "projected_50s_video_s": round(el_pil * 10.0, 1),
        "peak_rss_mb": rss_pil,
        "file_size_kb": round(mp4_pil.stat().st_size / 1024, 1),
        "probe": _probe(mp4_pil),
    }

    # 2. Candidato B: Playwright + HTML5/CSS/SVG (2 workers) + h264_videotoolbox
    print("[2/3] Running Playwright + HTML/CSS/SVG deterministic...")
    el_pw, rss_pw, _ = _run_timed(
        [str(REPO_ROOT / ".venv" / "bin" / "python"), "scripts/bench_playwright_html.py"],
        cwd=VE_DIR,
    )
    mp4_pw = OUT_DIR / "playwright_bench.mp4"
    _extract_frame(mp4_pw, OUT_DIR / "frame_playwright.png")
    results["playwright_html_svg"] = {
        "engine": "Playwright Headless Chrome + HTML5/CSS/SVG (2 tabs) + ffmpeg (h264_videotoolbox)",
        "clip_duration_s": 5.0,
        "frames": 120,
        "resolution": "1080x1920",
        "concurrency": 2,
        "wall_time_s": el_pw,
        "realtime_factor_x": round(el_pw / 5.0, 2),
        "projected_50s_video_s": round(el_pw * 10.0, 1),
        "peak_rss_mb": rss_pw,
        "file_size_kb": round(mp4_pw.stat().st_size / 1024, 1),
        "probe": _probe(mp4_pw),
    }

    # 3. Candidato A: Remotion 4.0 (React + TypeScript + System Chrome, concurrency=2)
    print("[3/3] Running Remotion 4.0 (concurrency=2)...")
    mp4_rem = OUT_DIR / "remotion_bench.mp4"
    el_rem, rss_rem, _ = _run_timed(
        [
            "npx",
            "remotion",
            "render",
            "src/index.ts",
            "BenchScene",
            str(mp4_rem),
            "--concurrency=2",
            f"--browser-executable={CHROME_PATH}",
            "--jpeg-quality=94",
        ],
        cwd=VE_DIR,
    )
    _extract_frame(mp4_rem, OUT_DIR / "frame_remotion.png")
    results["remotion_react"] = {
        "engine": "Remotion 4.0.546 (React 18 + TypeScript + System Chrome, concurrency=2)",
        "clip_duration_s": 5.0,
        "frames": 120,
        "resolution": "1080x1920",
        "concurrency": 2,
        "wall_time_s": el_rem,
        "realtime_factor_x": round(el_rem / 5.0, 2),
        "projected_50s_video_s": round(el_rem * 10.0, 1),
        "peak_rss_mb": rss_rem,
        "file_size_kb": round(mp4_rem.stat().st_size / 1024, 1),
        "probe": _probe(mp4_rem),
    }

    out_json = VE_DIR / "benchmark_results.json"
    out_json.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    print("BENCHMARK_COMPLETE:", out_json)
    for k, v in results.items():
        print(
            f"  {k}: {v['wall_time_s']}s ({v['realtime_factor_x']}x RT) | "
            f"50s proj ~{v['projected_50s_video_s']}s | RSS {v['peak_rss_mb']} MB"
        )


if __name__ == "__main__":
    main()
