"""CLI entrypoint to build and render any product episode from a declarative episode_spec.json manifest."""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.video.web_engine.renderer import (  # noqa: E402
    _make_runtime_payload,
    capture_styleframes_and_audit,
    render_animatic_from_styleframes,
    render_episode_mp4,
)
from src.video.web_engine.tts_audio import synthesize_episode_audio  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Build and render a 9:16 product episode from episode_spec.json.")
    parser.add_argument("product_dir", type=Path, help="Path to produtos/<slug>")
    parser.add_argument("--spec", type=Path, default=None, help="Optional path to episode_spec.json")
    parser.add_argument("--mode", choices=["animatic", "final"], default="final")
    parser.add_argument("--tts-engine", choices=["auto", "azure", "edge"], default="auto")
    parser.add_argument("--skip-tts", action="store_true", help="Reuse existing timeline.json and lipsync.json")
    parser.add_argument("--ml-clips", action="store_true", help="Render clean deterministic variant without flow_ia")
    parser.add_argument("--concurrency", type=int, default=2, help="Parallel Chrome worker tabs (default: 2)")
    args = parser.parse_args()

    prod_dir = args.product_dir.resolve()
    spec_path = (args.spec or (prod_dir / "episode_spec.json")).resolve()
    if not spec_path.exists():
        print(f"ERRO: Manifesto não encontrado em {spec_path}", file=sys.stderr)
        return 1

    episode_spec = json.loads(spec_path.read_text(encoding="utf-8"))
    build_dir = prod_dir / "_preview_build"
    build_dir.mkdir(parents=True, exist_ok=True)
    theme = episode_spec.get("theme", {})

    effective_tts = "edge" if (args.mode == "animatic" and args.tts_engine == "auto") else args.tts_engine

    if args.skip_tts and (build_dir / "timeline.json").exists() and (build_dir / "lipsync.json").exists():
        timeline = json.loads((build_dir / "timeline.json").read_text(encoding="utf-8"))
        lipsync = json.loads((build_dir / "lipsync.json").read_text(encoding="utf-8"))
        if args.ml_clips:
            from src.video.web_engine.tts_audio import _build_master_audio_mix
            ml_wav = build_dir / "master_audio_ml_clips.wav"
            _build_master_audio_mix(
                narration_wav=build_dir / "narration.wav",
                scenes_meta=timeline["scenes"],
                prod_dir=prod_dir,
                out_wav=ml_wav,
                ml_clips=True,
            )
            timeline = {
                **timeline,
                "req_007_ai_disclosure": False,
                "master_audio": ml_wav.name,
            }
            (build_dir / "timeline_ml_clips.json").write_text(
                json.dumps(timeline, ensure_ascii=False, indent=2), encoding="utf-8"
            )
    else:
        timeline = asyncio.run(
            synthesize_episode_audio(
                episode_spec=episode_spec,
                prod_dir=prod_dir,
                build_dir=build_dir,
                tts_engine=effective_tts,
                ml_clips=args.ml_clips,
            )
        )
        lipsync = json.loads((build_dir / "lipsync.json").read_text(encoding="utf-8"))

    if args.mode == "animatic":
        payload = _make_runtime_payload(timeline, lipsync, prod_dir, theme, transparent_overlay=False)
        sf_rels, boxes, screen_words = capture_styleframes_and_audit(payload, prod_dir, build_dir, is_final=False)
        out_anim = prod_dir / "animatic_portao2.mp4"
        render_animatic_from_styleframes(timeline, sf_rels, prod_dir, build_dir, out_anim, lipsync=lipsync, theme=theme)
        audit_data = {
            "engine": "web_motion_engine_animatic",
            "styleframes": sf_rels,
            "keyframes": sf_rels,
            "scene_screen_words": screen_words,
            "layout_boxes_1080": boxes,
        }
        (build_dir / "render_audit.json").write_text(json.dumps(audit_data, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"[Animatic] Pronto: {out_anim} ({len(sf_rels)} styleframes)")
        return 0

    out_name = "video_final_ml_clips_1080p.mp4" if args.ml_clips else "video_final_1080p.mp4"
    out_mp4 = prod_dir / out_name
    render_episode_mp4(
        timeline=timeline,
        lipsync=lipsync,
        theme=theme,
        prod_dir=prod_dir,
        build_dir=build_dir,
        out_mp4=out_mp4,
        ml_clips=args.ml_clips,
        concurrency=args.concurrency,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
