"""Deterministic Brazilian Portuguese (PT-BR) grapheme-to-viseme mapper and TTS validator."""

from __future__ import annotations

import argparse
import math
import re
import unicodedata
import wave
from pathlib import Path
from typing import Any

import numpy as np

# Viseme vocabulary aligned with assets/personagem/rig/rig.json
VISEME_CODES = ("X", "BMP", "FV", "EI", "A", "OU", "SORRISO")

# Mapping from Microsoft Azure AI Speech 22 standard viseme IDs (0..21) to Rig 2.5D visemes
AZURE_VISEME_MAP: dict[int, str] = {
    0: "X",
    1: "A",
    2: "A",
    3: "OU",
    4: "EI",
    5: "EI",
    6: "EI",
    7: "OU",
    8: "OU",
    9: "A",
    10: "OU",
    11: "A",
    12: "EI",
    13: "EI",
    14: "EI",
    15: "EI",
    16: "EI",
    17: "EI",
    18: "FV",
    19: "EI",
    20: "EI",
    21: "BMP",
}

_VOWEL_BASE = {
    "a": "A",
    "á": "A",
    "à": "A",
    "â": "A",
    "ã": "A",
    "e": "EI",
    "é": "EI",
    "ê": "EI",
    "i": "EI",
    "í": "EI",
    "y": "EI",
    "o": "OU",
    "ó": "OU",
    "ô": "OU",
    "õ": "OU",
    "u": "OU",
    "ú": "OU",
    "ü": "OU",
}


def word_to_visemes_ptbr(word: str) -> list[tuple[str, float]]:
    """Convert a PT-BR word into weighted (viseme, relative_weight) pairs."""
    clean = re.sub(r"[^\wáàâãéêíóôõúüç]", "", word.lower(), flags=re.UNICODE)
    if not clean:
        return [("X", 1.0)]

    # Expand pure digits briefly into vowel-heavy cadence if TTS emitted raw numeric tokens
    if clean.isdigit():
        return [("A", 1.0), ("EI", 1.0), ("OU", 1.0)]

    seq: list[tuple[str, float]] = []
    i = 0
    n = len(clean)
    while i < n:
        ch = clean[i]
        pair = clean[i : i + 2]

        # Handle PT-BR nasal diphthongs and silent 'u' digraphs
        if pair in ("ão", "ãe"):
            seq.append(("A", 1.6))
            seq.append(("OU" if pair == "ão" else "EI", 1.3))
            i += 2
            continue
        if pair == "õe":
            seq.append(("OU", 1.5))
            seq.append(("EI", 1.3))
            i += 2
            continue
        if pair in ("qu", "gu") and i + 2 < n and clean[i + 2] in "eéiíê":
            seq.append(("A", 0.55))
            i += 2
            continue
        if pair in ("ch", "lh", "nh", "rr", "ss", "sc", "sç", "xc"):
            seq.append(("EI", 0.7))
            i += 2
            continue

        if ch in _VOWEL_BASE:
            seq.append((_VOWEL_BASE[ch], 1.85))
            i += 1
            continue

        # In PT-BR, coda '-m' after a vowel nasalizes the vowel rather than closing lips
        if ch == "m" and i == n - 1 and i > 0 and clean[i - 1] in _VOWEL_BASE:
            i += 1
            continue

        if ch in ("p", "b", "m"):
            seq.append(("BMP", 0.95))
        elif ch in ("f", "v"):
            seq.append(("FV", 0.95))
        elif ch in ("o", "u", "w"):
            seq.append(("OU", 1.1))
        else:
            seq.append(("EI" if ch in ("s", "z", "c", "ç", "j", "x", "l") else "A", 0.6))
        i += 1

    # Collapse immediate duplicate visemes summing their weights cleanly
    merged: list[tuple[str, float]] = []
    for v, w in seq:
        if merged and merged[-1][0] == v:
            merged[-1] = (v, merged[-1][1] + w)
        else:
            merged.append((v, w))
    return merged or [("X", 1.0)]


def validate_tts_audio(
    audio_path: Path,
    word_events: list[dict[str, Any]] | None = None,
    require_word_boundaries: bool = False,
    min_bytes: int = 1024,
) -> tuple[bool, str]:
    """Deterministically validate generated TTS audio integrity (REQ-014)."""
    if not audio_path.exists():
        return False, f"Arquivo de áudio ausente: {audio_path}"
    size = audio_path.stat().st_size
    if size < min_bytes:
        return False, f"Arquivo de áudio vazio ou truncado ({size} bytes < {min_bytes}): {audio_path}"
    if require_word_boundaries and not word_events:
        return False, f"Eventos WordBoundary ausentes para áudio {audio_path.name}"
    return True, f"Áudio válido ({size} bytes, {len(word_events or [])} palavras)"


def wav_rms_envelope(wav_path: Path, fps: int = 24) -> list[float]:
    """Compute normalized per-frame RMS energy envelope [0..1] from a mono/stereo 16-bit WAV."""
    with wave.open(str(wav_path), "rb") as wf:
        n_channels = wf.getnchannels()
        sampwidth = wf.getsampwidth()
        framerate = wf.getframerate()
        raw = wf.readframes(wf.getnframes())
    if sampwidth != 2:
        raise ValueError(f"WAV deve ser 16-bit PCM (recebido {sampwidth * 8}-bit)")
    samples = np.frombuffer(raw, dtype=np.int16).astype(np.float32)
    if n_channels > 1:
        samples = samples.reshape(-1, n_channels).mean(axis=1)
    samples /= 32768.0

    step = max(1, int(round(framerate / fps)))
    n_frames = int(math.ceil(len(samples) / step))
    rms_vals: list[float] = []
    for idx in range(n_frames):
        seg = samples[idx * step : (idx + 1) * step]
        rms_vals.append(float(np.sqrt(np.mean(seg * seg))) if len(seg) else 0.0)
    peak = max(rms_vals) if rms_vals else 0.0
    if peak > 1e-6:
        rms_vals = [v / peak for v in rms_vals]
    return rms_vals


def build_frame_visemes_from_words(
    word_events: list[dict[str, Any]],
    total_duration: float,
    fps: int = 24,
    wav_path: Path | None = None,
    silence_threshold: float = 0.035,
) -> list[str]:
    """Build per-frame viseme list using WordBoundary timestamps + optional WAV RMS silence gate."""
    n_frames = max(1, int(math.ceil(total_duration * fps)))
    cues: list[tuple[float, float, str]] = []

    for w in word_events:
        start = float(w["start"])
        dur = max(0.04, float(w["duration"]))
        parts = word_to_visemes_ptbr(str(w["text"]))
        total_w = sum(weight for _, weight in parts)
        cursor = start
        for vis, weight in parts:
            span = dur * (weight / total_w)
            cues.append((cursor, cursor + span, vis))
            cursor += span

    rms_env = wav_rms_envelope(wav_path, fps=fps) if wav_path and wav_path.exists() else None

    frames: list[str] = ["X"] * n_frames
    cue_idx = 0
    for f_idx in range(n_frames):
        t = (f_idx + 0.5) / fps
        while cue_idx + 1 < len(cues) and cues[cue_idx][1] < t:
            cue_idx += 1
        vis = "X"
        if cue_idx < len(cues) and cues[cue_idx][0] <= t <= cues[cue_idx][1]:
            vis = cues[cue_idx][2]
        if rms_env is not None and f_idx < len(rms_env) and rms_env[f_idx] < silence_threshold:
            vis = "X"
        frames[f_idx] = vis
    return frames


def build_frame_visemes_from_azure_visemes(
    viseme_events: list[dict[str, Any]],
    total_duration: float,
    fps: int = 24,
) -> list[str]:
    """Map native Azure AI Speech viseme events ({audio_offset_sec, viseme_id}) to per-frame visemes."""
    n_frames = max(1, int(math.ceil(total_duration * fps)))
    if not viseme_events:
        return ["X"] * n_frames

    ordered = sorted(viseme_events, key=lambda e: float(e["audio_offset_sec"]))
    frames: list[str] = ["X"] * n_frames
    ev_idx = 0
    for f_idx in range(n_frames):
        t = (f_idx + 0.5) / fps
        while ev_idx + 1 < len(ordered) and float(ordered[ev_idx + 1]["audio_offset_sec"]) <= t:
            ev_idx += 1
        if float(ordered[ev_idx]["audio_offset_sec"]) <= t:
            vid = int(ordered[ev_idx]["viseme_id"])
            frames[f_idx] = AZURE_VISEME_MAP.get(vid, "EI")
    return frames


def build_frame_visemes_fallback_phrase(
    phrase_segments: list[dict[str, Any]],
    total_duration: float,
    fps: int = 24,
    wav_path: Path | None = None,
) -> list[str]:
    """Fallback aligner for TTS engines without WordBoundary (e.g., offline Piper pt_BR)."""
    synthetic_words: list[dict[str, Any]] = []
    for seg in phrase_segments:
        s0 = float(seg["start"])
        dur = max(0.1, float(seg["end"]) - s0)
        tokens = [tok for tok in str(seg["text"]).split() if re.search(r"\w", tok)]
        if not tokens:
            continue
        char_weights = [max(1, len(re.sub(r"\W", "", t))) for t in tokens]
        tot = sum(char_weights)
        cur = s0
        for tok, cw in zip(tokens, char_weights):
            wd = dur * (cw / tot)
            synthetic_words.append({"text": tok, "start": cur, "duration": wd})
            cur += wd
    return build_frame_visemes_from_words(synthetic_words, total_duration, fps=fps, wav_path=wav_path)


def _normalize_ascii(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def self_test() -> None:
    """Run deterministic self-checks on PT-BR phoneme-to-viseme rules and frame timing."""
    samples = {
        "bom": ("BMP", "OU"),
        "vapor": ("FV", "A", "BMP", "OU"),
        "frio": ("FV", "A", "EI", "OU"),
        "água": ("A", "OU", "A"),
        "ferramenta": ("FV", "EI", "A", "BMP", "EI"),
        "cabo": ("A", "BMP", "OU"),
        "inspeção": ("EI", "BMP", "EI", "A", "OU"),
    }
    for word, expected_subset in samples.items():
        got = [v for v, _ in word_to_visemes_ptbr(word)]
        # Verify final nasal '-m' in "bom" does NOT emit trailing BMP
        if word == "bom":
            assert got[-1] != "BMP", f"Final '-m' in 'bom' closed prematurely: {got}"
        for req_v in expected_subset:
            assert req_v in got, f"Word '{word}' missing viseme '{req_v}' (got {got})"
        assert all(v in VISEME_CODES for v in got)

    # Verify frame generation & Azure viseme mapping
    events = [
        {"text": "bom", "start": 0.1, "duration": 0.35},
        {"text": "cabo", "start": 0.55, "duration": 0.4},
    ]
    frames = build_frame_visemes_from_words(events, total_duration=1.2, fps=24)
    assert len(frames) == 29
    assert frames[0] == "X" and frames[-1] == "X"
    assert "BMP" in frames and "OU" in frames

    az_frames = build_frame_visemes_from_azure_visemes(
        [{"audio_offset_sec": 0.0, "viseme_id": 0}, {"audio_offset_sec": 0.2, "viseme_id": 21}],
        total_duration=0.5,
        fps=24,
    )
    assert az_frames[0] == "X" and az_frames[-1] == "BMP"

    fb_frames = build_frame_visemes_fallback_phrase(
        [{"start": 0.0, "end": 0.8, "text": "teste rápido"}],
        total_duration=0.9,
        fps=24,
    )
    assert len(fb_frames) == 22 and any(v != "X" for v in fb_frames)
    print(f"OK: lipsync_ptbr self-test passed ({len(samples)} palavras PT-BR, {_normalize_ascii('validacao OK')})")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Deterministic PT-BR lipsync helper.")
    parser.add_argument("--self-test", action="store_true", help="Run built-in unit checks.")
    args = parser.parse_args()
    if args.self_test:
        self_test()
