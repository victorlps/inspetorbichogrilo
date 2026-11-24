"""Reusable PT-BR TTS synthesis (Azure AI Speech F0 / edge-tts), WordBoundary punctuation cleaning, and stereo audio mixer."""

from __future__ import annotations

import os
import html
import json
import subprocess
import time
import wave
from pathlib import Path
from typing import Any

import edge_tts
import numpy as np

from src.video.lipsync_ptbr import (
    build_frame_visemes_from_azure_visemes,
    build_frame_visemes_from_words,
    validate_tts_audio,
)

REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_VOICE = "pt-BR-AntonioNeural"


def ffprobe_duration(path: Path) -> float:
    out = subprocess.check_output(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(path),
        ],
        text=True,
    ).strip()
    return float(out)


def load_azure_speech_creds() -> tuple[str, str] | None:
    """Load AZURE_SPEECH_KEY and AZURE_SPEECH_REGION from env or .env without logging or exposing secrets."""
    key = os.environ.get("AZURE_SPEECH_KEY", "").strip()
    region = os.environ.get("AZURE_SPEECH_REGION", "").strip()
    if key and region:
        return key, region
    env_path = REPO_ROOT / ".env"
    if env_path.exists():
        for raw_line in env_path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            k = k.strip()
            v = v.strip().strip('"').strip("'")
            if k == "AZURE_SPEECH_KEY" and not key:
                key = v
            elif k == "AZURE_SPEECH_REGION" and not region:
                region = v
    if key and region:
        return key, region
    return None


def collapse_phonetic_words(
    raw_words: list[dict[str, Any]],
    replacements: list[tuple[str, str]],
) -> list[dict[str, Any]]:
    """Map phonetic TTS words back to clean display tokens and sanitize isolated Azure WordBoundary punctuation."""
    collapsed: list[dict[str, Any]] = []
    i = 0
    n = len(raw_words)
    rep_seqs: list[tuple[list[str], str]] = [
        ([tok.lower() for tok in src.split()], dst) for src, dst in replacements
    ]
    rep_seqs.sort(key=lambda item: len(item[0]), reverse=True)

    while i < n:
        tok_raw = str(raw_words[i]["text"]).strip()
        if tok_raw and all(ch in ".,!?:;-…" for ch in tok_raw):
            if collapsed:
                if any(ch in "?!.;" for ch in tok_raw):
                    collapsed[-1]["sentence_end"] = True
                    if any(ch in "?!" for ch in tok_raw):
                        punct = "?" if "?" in tok_raw else "!"
                        if not collapsed[-1]["text"].endswith(("?", "!")):
                            collapsed[-1]["text"] = collapsed[-1]["text"].rstrip(".,:;") + punct
                elif "," in tok_raw and not collapsed[-1]["text"].endswith(("?", "!", ",")):
                    collapsed[-1]["text"] = collapsed[-1]["text"].rstrip(".:;") + ","
            i += 1
            continue

        matched = False
        for seq_tokens, display_tok in rep_seqs:
            k = len(seq_tokens)
            if i + k <= n:
                window = [str(raw_words[i + j]["text"]).lower().strip(".,!?:;") for j in range(k)]
                if window == seq_tokens:
                    start_t = float(raw_words[i]["start"])
                    end_t = float(raw_words[i + k - 1]["start"]) + float(raw_words[i + k - 1]["duration"])
                    collapsed.append(
                        {
                            "text": display_tok,
                            "tts_text": " ".join(str(raw_words[i + j]["text"]) for j in range(k)),
                            "start": round(start_t, 4),
                            "duration": round(max(0.05, end_t - start_t), 4),
                        }
                    )
                    i += k
                    matched = True
                    break
        if not matched:
            w = raw_words[i]
            ends_sent = tok_raw.endswith((".", "!", "?"))
            clean_tok = tok_raw.rstrip(".:;")
            if not clean_tok:
                clean_tok = tok_raw
            collapsed.append(
                {
                    "text": clean_tok,
                    "tts_text": str(w["text"]),
                    "start": round(float(w["start"]), 4),
                    "duration": round(float(w["duration"]), 4),
                    "sentence_end": ends_sent,
                }
            )
            i += 1
    return collapsed


def build_caption_beats(display_words: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Group display words into readable beats of 1 to 3 words, breaking cleanly at sentence boundaries."""
    beats: list[dict[str, Any]] = []
    n = len(display_words)
    i = 0
    while i < n:
        grp: list[dict[str, Any]] = []
        while i < n and len(grp) < 3:
            w = display_words[i]
            grp.append(w)
            i += 1
            if w.get("sentence_end") or str(w.get("text", "")).endswith(("?", "!", ",")):
                break
        s_t = float(grp[0]["start"])
        e_t = float(grp[-1]["start"]) + float(grp[-1]["duration"]) + 0.16
        beats.append(
            {
                "start": round(s_t, 4),
                "end": round(e_t, 4),
                "words": grp,
                "word_count": len(grp),
            }
        )
    for b_idx in range(len(beats) - 1):
        if beats[b_idx]["end"] > beats[b_idx + 1]["start"]:
            beats[b_idx]["end"] = beats[b_idx + 1]["start"]
    return beats


def _synth_scene_azure(
    text: str,
    voice: str,
    rate: str,
    out_wav: Path,
    key: str,
    region: str,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    import azure.cognitiveservices.speech as speechsdk  # type: ignore

    speech_config = speechsdk.SpeechConfig(subscription=key, region=region)
    speech_config.set_speech_synthesis_output_format(
        speechsdk.SpeechSynthesisOutputFormat.Riff48Khz16BitMonoPcm
    )
    audio_config = speechsdk.audio.AudioOutputConfig(filename=str(out_wav))
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    raw_words: list[dict[str, Any]] = []
    raw_visemes: list[dict[str, Any]] = []

    def on_word(evt: Any) -> None:
        raw_words.append(
            {
                "text": str(evt.text),
                "start": float(evt.audio_offset) / 10_000_000.0,
                "duration": float(evt.duration.total_seconds()) if evt.duration else 0.12,
            }
        )

    def on_viseme(evt: Any) -> None:
        raw_visemes.append(
            {
                "audio_offset_sec": float(evt.audio_offset) / 10_000_000.0,
                "viseme_id": int(evt.viseme_id),
            }
        )

    synthesizer.synthesis_word_boundary.connect(on_word)
    synthesizer.viseme_received.connect(on_viseme)

    escaped_text = html.escape(text)
    ssml = (
        f'<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="pt-BR">'
        f'<voice name="{voice}"><prosody rate="{rate}">{escaped_text}</prosody></voice></speak>'
    )
    last_reason: Any = None
    for attempt in range(4):
        raw_words.clear()
        raw_visemes.clear()
        if attempt > 0:
            time.sleep(1.8 * attempt)
        result = synthesizer.speak_ssml_async(ssml).get()
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            time.sleep(0.45)
            return raw_words, raw_visemes
        details = getattr(result, "cancellation_details", None)
        last_reason = getattr(details, "reason", result.reason)
    raise RuntimeError(f"Azure AI Speech falhou após tentativas ({last_reason})")


def _build_master_audio_mix(
    narration_wav: Path,
    scenes_meta: list[dict[str, Any]],
    prod_dir: Path,
    out_wav: Path,
    ml_clips: bool = False,
) -> None:
    """Create stereo 48kHz master audio mixing TTS narration, subtle procedural chimes (CC0), and optional Flow scene audio (-20dB)."""
    sr = 48000
    tmp_narr48 = out_wav.parent / "_tmp_narr48.wav"
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(narration_wav),
            "-ar",
            str(sr),
            "-ac",
            "2",
            "-c:a",
            "pcm_s16le",
            str(tmp_narr48),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    with wave.open(str(tmp_narr48), "rb") as wf:
        raw = wf.readframes(wf.getnframes())
    tmp_narr48.unlink(missing_ok=True)

    audio = np.frombuffer(raw, dtype=np.int16).astype(np.float32).reshape(-1, 2) / 32768.0
    n_samples = audio.shape[0]

    # Subtle original transition chimes (sine harmonics, 100% own commercial domain)
    for idx, sc in enumerate(scenes_meta):
        t_start = float(sc["start"])
        s0 = int(t_start * sr)
        dur_chime = 0.22
        n_c = min(int(dur_chime * sr), n_samples - s0)
        if n_c > 100:
            t_arr = np.arange(n_c, dtype=np.float32) / sr
            f1 = 587.33 if idx % 2 == 0 else 523.25
            f2 = f1 * 1.5
            env = np.sin(np.pi * (t_arr / dur_chime)) ** 2
            chime = 0.032 * env * (0.65 * np.sin(2 * np.pi * f1 * t_arr) + 0.35 * np.sin(2 * np.pi * f2 * t_arr))
            audio[s0 : s0 + n_c, 0] += chime
            audio[s0 : s0 + n_c, 1] += chime

        # Optional ambient audio from Flow scene clip (-20dB = 0.10 amplitude) when not ml_clips
        flow_rel = sc.get("flow_audio_source")
        if flow_rel and not ml_clips:
            flow_path = prod_dir / flow_rel
            if flow_path.exists():
                tmp_fl = out_wav.parent / f"_tmp_flow_{sc['scene']}.wav"
                res = subprocess.run(
                    [
                        "ffmpeg",
                        "-y",
                        "-i",
                        str(flow_path),
                        "-t",
                        f"{float(sc['duration']):.3f}",
                        "-ar",
                        str(sr),
                        "-ac",
                        "2",
                        "-c:a",
                        "pcm_s16le",
                        str(tmp_fl),
                    ],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
                if res.returncode == 0 and tmp_fl.exists() and tmp_fl.stat().st_size > 1024:
                    with wave.open(str(tmp_fl), "rb") as fwf:
                        fraw = fwf.readframes(fwf.getnframes())
                    tmp_fl.unlink(missing_ok=True)
                    fl_arr = np.frombuffer(fraw, dtype=np.int16).astype(np.float32).reshape(-1, 2) / 32768.0
                    n_mix = min(fl_arr.shape[0], n_samples - s0)
                    if n_mix > sr // 4:
                        fade = min(int(0.25 * sr), n_mix // 3)
                        f_env = np.ones((n_mix, 1), dtype=np.float32) * 0.09
                        f_env[:fade, 0] *= np.linspace(0.0, 1.0, fade, dtype=np.float32)
                        f_env[-fade:, 0] *= np.linspace(1.0, 0.0, fade, dtype=np.float32)
                        audio[s0 : s0 + n_mix] += fl_arr[:n_mix] * f_env
                else:
                    tmp_fl.unlink(missing_ok=True)

    audio = np.clip(audio, -0.98, 0.98)
    pcm16 = (audio * 32767.0).astype(np.int16)
    with wave.open(str(out_wav), "wb") as out_wf:
        out_wf.setnchannels(2)
        out_wf.setsampwidth(2)
        out_wf.setframerate(sr)
        out_wf.writeframes(pcm16.tobytes())


async def synthesize_episode_audio(
    episode_spec: dict[str, Any],
    prod_dir: Path,
    build_dir: Path,
    tts_engine: str = "auto",
    ml_clips: bool = False,
) -> dict[str, Any]:
    """Synthesize per-scene narration, compute WordBoundary beats + viseme frames, and write timeline.json & lipsync.json."""
    build_dir.mkdir(parents=True, exist_ok=True)
    fps = int(episode_spec.get("fps", 24))
    voice = str(episode_spec.get("voice", DEFAULT_VOICE))
    replacements = [tuple(pair) for pair in episode_spec.get("phonetic_replacements", [])]

    azure_creds = load_azure_speech_creds()
    if tts_engine == "azure" and not azure_creds:
        raise RuntimeError("AZURE_SPEECH_KEY e AZURE_SPEECH_REGION não configurados no .env ou ambiente.")
    use_azure = (tts_engine == "azure") or (tts_engine == "auto" and azure_creds is not None)
    engine_label = "azure-f0" if use_azure else "edge-tts"
    print(f"[TTS] Motor selecionado: {engine_label}")

    scenes_meta: list[dict[str, Any]] = []
    all_raw_words: list[dict[str, Any]] = []
    all_azure_visemes: list[dict[str, Any]] = []
    trimmed_wavs: list[Path] = []
    t_cursor = 0.0

    for spec in episode_spec["scenes"]:
        sc_id = str(spec["id"])
        rate = str(spec.get("rate", "+16%"))
        tts_text = str(spec["tts_text"])
        raw_words: list[dict[str, Any]] = []
        raw_visemes: list[dict[str, Any]] = []

        if use_azure and azure_creds is not None:
            audio_path = build_dir / f"audio_{sc_id}.wav"
            raw_words, raw_visemes = _synth_scene_azure(
                text=tts_text,
                voice=voice,
                rate=rate,
                out_wav=audio_path,
                key=azure_creds[0],
                region=azure_creds[1],
            )
        else:
            audio_path = build_dir / f"audio_{sc_id}.mp3"
            comm = edge_tts.Communicate(tts_text, voice, rate=rate, boundary="WordBoundary")
            with open(audio_path, "wb") as f:
                async for chunk in comm.stream():
                    if chunk["type"] == "audio":
                        f.write(chunk["data"])
                    elif chunk["type"] == "WordBoundary":
                        raw_words.append(
                            {
                                "text": chunk["text"],
                                "start": chunk["offset"] / 10_000_000.0,
                                "duration": chunk["duration"] / 10_000_000.0,
                            }
                        )

        ok, msg = validate_tts_audio(audio_path, raw_words, require_word_boundaries=True)
        if not ok:
            raise RuntimeError(f"Falha na validação TTS da Cena {sc_id}: {msg}")

        raw_dur = ffprobe_duration(audio_path)
        last_word_end = (raw_words[-1]["start"] + raw_words[-1]["duration"]) if raw_words else raw_dur
        pad_tail = float(spec.get("tail_pad_s", 0.24))
        sc_dur = min(raw_dur, last_word_end + pad_tail)
        if spec.get("max_dur_s") is not None:
            sc_dur = min(sc_dur, float(spec["max_dur_s"]))

        sc_wav = build_dir / f"scene_{sc_id}.wav"
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i",
                str(audio_path),
                "-t",
                f"{sc_dur:.3f}",
                "-ar",
                "48000",
                "-ac",
                "2",
                "-c:a",
                "pcm_s16le",
                str(sc_wav),
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        actual_dur = ffprobe_duration(sc_wav)
        trimmed_wavs.append(sc_wav)

        shifted_raw: list[dict[str, Any]] = []
        for w in raw_words:
            sw = {
                "text": w["text"],
                "start": round(t_cursor + float(w["start"]), 4),
                "duration": round(float(w["duration"]), 4),
            }
            shifted_raw.append(sw)
            all_raw_words.append(sw)

        sc_reps = [tuple(p) for p in spec.get("phrase_replacements", [])] + replacements
        disp_words = collapse_phonetic_words(shifted_raw, sc_reps)
        beats = build_caption_beats(disp_words)

        scenes_meta.append(
            {
                **spec,
                "scene": sc_id,
                "start": round(t_cursor, 4),
                "end": round(t_cursor + actual_dur, 4),
                "duration": round(actual_dur, 4),
                "raw_words": shifted_raw,
                "display_words": disp_words,
                "caption_beats": beats,
                "audio_file": audio_path.name,
                "audio_bytes": audio_path.stat().st_size,
            }
        )
        for rv in raw_visemes:
            if float(rv["audio_offset_sec"]) <= actual_dur:
                all_azure_visemes.append(
                    {
                        "audio_offset_sec": float(rv["audio_offset_sec"]) + t_cursor,
                        "viseme_id": int(rv["viseme_id"]),
                    }
                )
        t_cursor += actual_dur

    concat_txt = build_dir / "concat.txt"
    with open(concat_txt, "w", encoding="utf-8") as cf:
        for w_p in trimmed_wavs:
            cf.write(f"file '{w_p.resolve()}'\n")

    narration_wav = build_dir / "narration.wav"
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat_txt),
            "-ar",
            "16000",
            "-ac",
            "1",
            "-c:a",
            "pcm_s16le",
            str(narration_wav),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    master_wav = build_dir / ("master_audio_ml_clips.wav" if ml_clips else "master_audio.wav")
    _build_master_audio_mix(
        narration_wav=narration_wav,
        scenes_meta=scenes_meta,
        prod_dir=prod_dir,
        out_wav=master_wav,
        ml_clips=ml_clips,
    )

    if use_azure and all_azure_visemes:
        viseme_frames = build_frame_visemes_from_azure_visemes(
            viseme_events=all_azure_visemes,
            total_duration=t_cursor,
            fps=fps,
        )
    else:
        viseme_frames = build_frame_visemes_from_words(
            word_events=all_raw_words,
            total_duration=t_cursor,
            fps=fps,
            wav_path=narration_wav,
            silence_threshold=0.03,
        )

    lipsync_data = {
        "fps": fps,
        "tts_engine": engine_label,
        "total_duration": round(t_cursor, 4),
        "total_frames": len(viseme_frames),
        "viseme_frames": viseme_frames,
    }
    (build_dir / "lipsync.json").write_text(json.dumps(lipsync_data, ensure_ascii=False, indent=2), encoding="utf-8")

    has_flow = any("flow_ia" in str(s.get("motor", "")).lower() for s in scenes_meta) and not ml_clips
    timeline_data = {
        "total_duration": round(t_cursor, 4),
        "fps": fps,
        "voice": voice,
        "tts_engine": engine_label,
        "req_007_ai_disclosure": has_flow,
        "master_audio": master_wav.name,
        "scenes": scenes_meta,
    }
    tl_filename = "timeline_ml_clips.json" if ml_clips else "timeline.json"
    (build_dir / tl_filename).write_text(json.dumps(timeline_data, ensure_ascii=False, indent=2), encoding="utf-8")
    return timeline_data
