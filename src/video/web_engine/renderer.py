"""Parallel Playwright + VideoToolbox renderer for 9:16 episodes (Portao 2 animated animatic + Portao 3 1080p final & ML Clips)."""

from __future__ import annotations

import json
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any

from playwright.sync_api import sync_playwright

REPO_ROOT = Path(__file__).resolve().parents[3]
STAGE_HTML = Path(__file__).resolve().parent / "stage_template.html"
RIG_DIR = REPO_ROOT / "assets" / "personagem" / "rig"
CHROME_PATH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def _make_runtime_payload(
    timeline: dict[str, Any],
    lipsync: dict[str, Any],
    prod_dir: Path,
    theme: dict[str, str],
    transparent_overlay: bool = False,
) -> dict[str, Any]:
    return {
        "fps": int(timeline["fps"]),
        "total_duration": float(timeline["total_duration"]),
        "rig_base_uri": RIG_DIR.as_uri(),
        "assets_base_uri": (prod_dir / "assets").as_uri(),
        "theme": theme,
        "transparent_overlay": transparent_overlay,
        "viseme_frames": lipsync.get("viseme_frames", []),
        "scenes": timeline["scenes"],
    }


def _safe_screenshot(page: Any, **kwargs: Any) -> bytes:
    """Capture screenshot with resilient micro-retry for transient headless compositor hiccups."""
    last_err: Exception | None = None
    for attempt in range(4):
        try:
            return page.screenshot(**kwargs)
        except Exception as err:
            last_err = err
            page.wait_for_timeout(90 * (attempt + 1))
    assert last_err is not None
    raise last_err


def _render_frame_range_jpeg(
    payload: dict[str, Any],
    start_frame: int,
    end_frame: int,
    frame_step: int = 1,
    scale_w: int = 1080,
    jpeg_quality: int = 94,
) -> list[bytes]:
    frames: list[bytes] = []
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=CHROME_PATH, headless=True)
        scale_factor = scale_w / 1080.0
        page = browser.new_page(
            viewport={"width": 1080, "height": 1920},
            device_scale_factor=scale_factor,
        )
        page.goto(STAGE_HTML.as_uri(), wait_until="load")
        page.evaluate("async (ep) => { await window.__initEpisode(ep); }", payload)
        page.evaluate(f"window.__setFrame({start_frame})")
        page.wait_for_timeout(80)
        for f in range(start_frame, end_frame, frame_step):
            page.evaluate(f"window.__setFrame({f})")
            frames.append(_safe_screenshot(page, type="jpeg", quality=jpeg_quality))
        browser.close()
    return frames


def _render_scene_overlay_over_flow(
    payload: dict[str, Any],
    scene_meta: dict[str, Any],
    flow_mp4: Path,
    out_scene_mp4: Path,
    fps: int = 24,
) -> None:
    """Render transparent Canvas simulation + Captions in Playwright and composite over 1080x1920 Flow clip via ffmpeg."""
    s_frame = int(round(float(scene_meta["start"]) * fps))
    e_frame = int(round(float(scene_meta["end"]) * fps))
    dur = (e_frame - s_frame) / float(fps)
    slowmo = float(scene_meta.get("flow_slowmo", 1.0))
    pts_expr = f",setpts={slowmo:.3f}*PTS" if slowmo > 1.01 else ""

    proc = subprocess.Popen(
        [
            "ffmpeg",
            "-y",
            "-stream_loop",
            "-1",
            "-i",
            str(flow_mp4),
            "-f",
            "image2pipe",
            "-vcodec",
            "png",
            "-r",
            str(fps),
            "-i",
            "-",
            "-t",
            f"{dur:.3f}",
            "-filter_complex",
            f"[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920{pts_expr},eq=brightness=-0.02:contrast=1.05:saturation=1.06[bg];[bg][1:v]overlay=0:0:format=auto[outv]",
            "-map",
            "[outv]",
            "-an",
            "-r",
            str(fps),
            "-c:v",
            "h264_videotoolbox",
            "-b:v",
            "8M",
            "-pix_fmt",
            "yuv420p",
            str(out_scene_mp4),
        ],
        stdin=subprocess.PIPE,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    assert proc.stdin is not None

    overlay_payload = {**payload, "transparent_overlay": True}
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=CHROME_PATH, headless=True)
        page = browser.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=1)
        page.goto(STAGE_HTML.as_uri(), wait_until="load")
        page.evaluate("async (ep) => { await window.__initEpisode(ep); }", overlay_payload)
        page.evaluate(f"window.__setFrame({s_frame})")
        page.wait_for_timeout(80)
        for f in range(s_frame, e_frame):
            page.evaluate(f"window.__setFrame({f})")
            png_bytes = _safe_screenshot(page, type="png", omit_background=True)
            proc.stdin.write(png_bytes)
        browser.close()

    proc.stdin.close()
    rc = proc.wait()
    if rc != 0:
        raise RuntimeError(f"Falha ao compor overlay sobre Flow clip {flow_mp4}")


def capture_styleframes_and_audit(
    payload: dict[str, Any],
    prod_dir: Path,
    build_dir: Path,
    is_final: bool = False,
    ml_clips: bool = False,
) -> tuple[list[str], list[dict[str, Any]], dict[str, int]]:
    """Capture representative frames + multi-moment transformation keyframes AND measure DOM safe-zone boxes & screen word density."""
    fps = int(payload["fps"])
    folder_name = "keyframes_ml_clips" if (is_final and ml_clips) else ("keyframes_final" if is_final else "styleframes")
    sub_dir = build_dir / folder_name
    sub_dir.mkdir(parents=True, exist_ok=True)
    prefix = "keyframe" if is_final else "styleframe"

    rel_paths: list[str] = []
    all_boxes: list[dict[str, Any]] = []
    screen_words: dict[str, int] = {}

    det_payload = {**payload, "transparent_overlay": False}
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=CHROME_PATH, headless=True)
        page = browser.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=1)
        page.goto(STAGE_HTML.as_uri(), wait_until="load")
        page.evaluate("async (ep) => { await window.__initEpisode(ep); }", det_payload)
        page.wait_for_timeout(80)

        for sc in payload["scenes"]:
            sc_id = str(sc["scene"])
            dur = float(sc["duration"])
            start_s = float(sc["start"])

            # Check early (20%), middle (55%), and late (82%) moments to verify transformation & peak word count
            max_wc = 0
            for tag_suf, frac in (("inicio", 0.20), ("meio", 0.55), ("fim", 0.82)):
                t_sample = start_s + dur * frac
                f_sample = int(round(t_sample * fps))
                page.evaluate(f"window.__setFrame({f_sample})")
                page.wait_for_timeout(30)
                wc = int(page.evaluate("window.__countScreenWords()"))
                if wc > max_wc:
                    max_wc = wc
                if tag_suf == "meio":
                    out_png = sub_dir / f"{prefix}_cena{sc_id}.png"
                    _safe_screenshot(page, path=str(out_png), type="png")
                    rel_paths.append(str(out_png.relative_to(prod_dir)))
                    boxes = page.evaluate(f"window.__auditBoxes('{sc_id}')")
                    all_boxes.extend(boxes)
                elif is_final and not ml_clips and tag_suf == "fim":
                    out_end = sub_dir / f"{prefix}_cena{sc_id}_fim.png"
                    _safe_screenshot(page, path=str(out_end), type="png")
                    rel_paths.append(str(out_end.relative_to(prod_dir)))

            screen_words[sc_id] = max_wc

        browser.close()

    return rel_paths, all_boxes, screen_words


def render_animatic_from_styleframes(
    timeline: dict[str, Any],
    styleframe_rels: list[str],
    prod_dir: Path,
    build_dir: Path,
    out_mp4: Path,
    lipsync: dict[str, Any] | None = None,
    theme: dict[str, str] | None = None,
) -> None:
    """Render real moving Portao 2 animatic MP4 at 12fps (scaled 540x960 -> 1080x1920, 0 Flow credits) so visual animations are testable."""
    fps_src = int(timeline["fps"])
    anim_fps = 12
    step = max(1, fps_src // anim_fps)
    total_frames = max(1, int(round(float(timeline["total_duration"]) * fps_src)))
    payload = _make_runtime_payload(timeline, lipsync or {}, prod_dir, theme or {}, transparent_overlay=False)

    mid = (total_frames // (2 * step)) * step
    with ThreadPoolExecutor(max_workers=2) as ex:
        f1 = ex.submit(_render_frame_range_jpeg, payload, 0, mid, step, 540, 86)
        f2 = ex.submit(_render_frame_range_jpeg, payload, mid, total_frames, step, 540, 86)
        anim_frames = f1.result() + f2.result()

    tmp_vid = build_dir / "_anim_vid_only.mp4"
    proc = subprocess.Popen(
        [
            "ffmpeg",
            "-y",
            "-f",
            "image2pipe",
            "-vcodec",
            "mjpeg",
            "-r",
            str(anim_fps),
            "-i",
            "-",
            "-vf",
            "scale=1080:1920:flags=lanczos",
            "-r",
            str(fps_src),
            "-c:v",
            "h264_videotoolbox",
            "-b:v",
            "4M",
            "-pix_fmt",
            "yuv420p",
            str(tmp_vid),
        ],
        stdin=subprocess.PIPE,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    assert proc.stdin is not None
    for buf in anim_frames:
        proc.stdin.write(buf)
    proc.stdin.close()
    if proc.wait() != 0:
        raise RuntimeError("Falha ao codificar animatic em movimento.")

    master_wav = build_dir / str(timeline["master_audio"])
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(tmp_vid),
            "-i",
            str(master_wav),
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-movflags",
            "+faststart",
            "-shortest",
            str(out_mp4),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    tmp_vid.unlink(missing_ok=True)


def render_episode_mp4(
    timeline: dict[str, Any],
    lipsync: dict[str, Any],
    theme: dict[str, str],
    prod_dir: Path,
    build_dir: Path,
    out_mp4: Path,
    ml_clips: bool = False,
    concurrency: int = 2,
) -> dict[str, Any]:
    """Render full 1080x1920 @ 24fps episode using 2-tab Playwright + h264_videotoolbox (+ Flow 1080p overlay when enabled)."""
    t0 = time.perf_counter()
    fps = int(timeline["fps"])
    payload = _make_runtime_payload(timeline, lipsync, prod_dir, theme, transparent_overlay=False)

    sf_rels, _, _ = capture_styleframes_and_audit(payload, prod_dir, build_dir, is_final=False)
    kf_rels, layout_boxes, screen_words = capture_styleframes_and_audit(
        payload, prod_dir, build_dir, is_final=True, ml_clips=ml_clips
    )

    scene_mp4s: list[Path] = []
    for sc in timeline["scenes"]:
        sc_id = str(sc["scene"])
        s_frame = int(round(float(sc["start"]) * fps))
        e_frame = max(s_frame + 1, int(round(float(sc["end"]) * fps)))
        sc_out = build_dir / f"_render_sc_{sc_id}{'_ml' if ml_clips else ''}.mp4"

        flow_rel = sc.get("flow_video_1080p")
        use_flow = bool(flow_rel and sc.get("use_flow_bg") and not ml_clips and (prod_dir / flow_rel).exists())

        if use_flow:
            print(f"[Render] Cena {sc_id}: compondo simulação Canvas transparente sobre Flow 1080p ({flow_rel})...")
            _render_scene_overlay_over_flow(payload, sc, prod_dir / flow_rel, sc_out, fps=fps)
            for tag_suf, frac in (("", 0.55), ("_fim", 0.82)):
                kf_p = build_dir / "keyframes_final" / f"keyframe_cena{sc_id}{tag_suf}.png"
                subprocess.run(
                    [
                        "ffmpeg",
                        "-y",
                        "-ss",
                        f"{float(sc['duration']) * frac:.2f}",
                        "-i",
                        str(sc_out),
                        "-frames:v",
                        "1",
                        str(kf_p),
                    ],
                    check=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
        else:
            total_sc_frames = e_frame - s_frame
            print(f"[Render] Cena {sc_id}: renderizando {total_sc_frames} quadros Canvas 2D (concurrency={concurrency})...")
            mid = s_frame + total_sc_frames // 2
            if concurrency >= 2 and total_sc_frames >= 16:
                with ThreadPoolExecutor(max_workers=2) as ex:
                    f1 = ex.submit(_render_frame_range_jpeg, payload, s_frame, mid)
                    f2 = ex.submit(_render_frame_range_jpeg, payload, mid, e_frame)
                    sc_frames = f1.result() + f2.result()
            else:
                sc_frames = _render_frame_range_jpeg(payload, s_frame, e_frame)

            proc = subprocess.Popen(
                [
                    "ffmpeg",
                    "-y",
                    "-f",
                    "image2pipe",
                    "-vcodec",
                    "mjpeg",
                    "-r",
                    str(fps),
                    "-i",
                    "-",
                    "-c:v",
                    "h264_videotoolbox",
                    "-b:v",
                    "8M",
                    "-pix_fmt",
                    "yuv420p",
                    str(sc_out),
                ],
                stdin=subprocess.PIPE,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            assert proc.stdin is not None
            for buf in sc_frames:
                proc.stdin.write(buf)
            proc.stdin.close()
            if proc.wait() != 0:
                raise RuntimeError(f"FFmpeg falhou na Cena {sc_id}")

        scene_mp4s.append(sc_out)

    concat_file = build_dir / f"_sc_concat{'_ml' if ml_clips else ''}.txt"
    concat_file.write_text("".join(f"file '{p.resolve()}'\n" for p in scene_mp4s), encoding="utf-8")
    master_wav = build_dir / str(timeline["master_audio"])

    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat_file),
            "-i",
            str(master_wav),
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-movflags",
            "+faststart",
            "-shortest",
            str(out_mp4),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    for p in scene_mp4s:
        p.unlink(missing_ok=True)
    concat_file.unlink(missing_ok=True)

    elapsed = round(time.perf_counter() - t0, 2)
    audit_data = {
        "engine": "web_motion_engine (Canvas 2D Procedural + Playwright 2-tab + h264_videotoolbox)",
        "render_elapsed_s": elapsed,
        "styleframes": sf_rels,
        "keyframes": kf_rels,
        "scene_screen_words": screen_words,
        "layout_boxes_1080": layout_boxes,
    }
    if not ml_clips:
        (build_dir / "render_audit.json").write_text(
            json.dumps(audit_data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
    print(f"[Render] Concluído: {out_mp4.name} em {elapsed}s")
    return audit_data
