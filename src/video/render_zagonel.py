"""Portao 2 (styleframes + animatic_portao2.mp4 / preview.mp4) and Portao 3 (video_final_1080p.mp4) 3D X-Ray Engineering Renderer for Zagonel ND."""

from __future__ import annotations

import argparse
import asyncio
import html
import json
import math
import os
import shutil
import subprocess
import wave
from pathlib import Path
from typing import Any

import edge_tts
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

from src.video.lipsync_ptbr import (
    build_frame_visemes_from_azure_visemes,
    build_frame_visemes_from_words,
    validate_tts_audio,
)
from src.video.rig_25d import InspectorRig

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PROD_DIR = REPO_ROOT / "produtos" / "ducha-eletronica-zagonel-nd-7700w"
FPS = 24
VOICE = "pt-BR-AntonioNeural"

# Canonical 1080x1920 safe zone (ADR 0006 & .agents/formato/biblia.md)
SAFE_X_HARD_MIN = 48
SAFE_X_REC_MIN = 65
SAFE_X_MAX = 887
SAFE_Y_MIN = 288
SAFE_Y_MAX = 1247
CAP_Y_MIN = 1040
CAP_Y_MAX = 1220

SCENES_SPEC: list[dict[str, Any]] = [
    {
        "id": "01",
        "title": "Gancho das 3 Posições, Costura com o Benefício & Transição Foto Real -> Raio-X 3D",
        "motor": "Rig 2.5D + Determinístico",
        "rate": "+22%",
        "max_dur_s": None,
        "show_rig": True,
        "actions": [(0.0, "inspecao_lupa"), (0.45, "analitico")],
        "top_bar": ("DUCHA ZAGONEL ND (REAL -> RAIO-X)", "ilustrativo"),
        "status_pill": ("#22c55e", "BENEFÍCIO: AJUSTE FINO COM JATO 100% ABERTO"),
        "display_text": (
            "Por que chuveiro comum de três estalos nunca fica na temperatura certa? "
            "Ou a água ferve, ou você fecha o registro e perde metade do jato! "
            "Abri em raio-x a clássica ND, da Thermosystem e Hydra, hoje da Zagonel!"
        ),
        "tts_text": (
            "Por que chuveiro comum de três estalos nunca fica na temperatura certa? "
            "Ou a água ferve, ou você fecha o registro e perde metade do jato! "
            "Abri em raio-x a clássica êne dê, da térmosístem e ídra, hoje da zagonél!"
        ),
        "phrase_replacements": [
            ("êne dê", "ND"),
            ("térmosístem", "Thermosystem"),
            ("ídra", "Hydra"),
            ("zagonél", "Zagonel"),
        ],
    },
    {
        "id": "02",
        "title": "A Costura do Dimmer de Calor (TRIAC para o Leigo) + Vídeo Real no Banho",
        "motor": "Determinístico + Flow Omni 360p -> 1080p (flow_ia)",
        "rate": "+22%",
        "max_dur_s": None,
        "show_rig": False,
        "actions": [(0.0, "lanterna_on")],
        "top_bar": ("REGULADOR GRADUAL (COMO UM DIMMER)", "uso real + 3D"),
        "status_pill": ("#22c55e", "JATO 100% FORTE · CALOR NO PONTO CERTO"),
        "display_text": (
            "Em vez de três chaves fixas, a haste gira um regulador eletrônico no compartimento seco! "
            "Essa peça se chama TRIAC e funciona como um dimmer de luz. "
            "Você escolhe o calor exato no banho sem mexer na pressão da água!"
        ),
        "tts_text": (
            "Em vez de três chaves fixas, a haste gira um regulador eletrônico no compartimento seco! "
            "Essa peça se chama triáque e funciona como um dímer de luz. "
            "Você escolhe o calor exato no banho sem mexer na pressão da água!"
        ),
        "phrase_replacements": [
            ("triáque", "TRIAC"),
            ("dímer", "dimmer"),
        ],
    },
    {
        "id": "03",
        "title": "Tubo Hidráulico Fechado, Diafragma Anti-Queima a Seco e Regra nº 1 do Manual",
        "motor": "Determinístico",
        "rate": "+22%",
        "max_dur_s": None,
        "show_rig": False,
        "actions": [(0.0, "analitico")],
        "top_bar": ("SEGURANÇA CONTRA QUEIMA A SECO", "corte 3D"),
        "status_pill": ("#38bdf8", "ÁGUA NO DUTO FECHADO · PARTIDA SEGURA"),
        "display_text": (
            "E por onde a água passa? "
            "Ela sobe por um tubo fechado e levanta essa borracha chamada diafragma! "
            "Ele só liga a energia com a câmara cheia. "
            "Por isso, na instalação, deixe correr água fria antes de ligar o disjuntor!"
        ),
        "tts_text": (
            "E por onde a água passa? "
            "Ela sobe por um tubo fechado e levanta essa borracha chamada diafragma! "
            "Ele só liga a energia com a câmara cheia. "
            "Por isso, na instalação, deixe correr água fria antes de ligar o disjuntor!"
        ),
        "phrase_replacements": [],
    },
    {
        "id": "04",
        "title": "Câmara Quente, Mesma Resistência (ND e Turbo!), 127V vs 220V e Haste Branca",
        "motor": "Determinístico",
        "rate": "+22%",
        "max_dur_s": None,
        "show_rig": False,
        "actions": [(0.0, "analitico")],
        "top_bar": ("MESMA RESISTÊNCIA ND/TURBO · 127V VS 220V", "peça real + 3D"),
        "status_pill": ("#f97316", "220V (7700W): ESQUENTA MAIS · 127V (5500W): FIO 10 mm²"),
        "display_text": (
            "No pescoço curvo, a resistência continua a mesma da antiga ND e Turbo! "
            "Em 220V ela esquenta mais que em 127. "
            "Use o cabo certo e repare: a Zagonel deixou a haste toda branca!"
        ),
        "tts_text": (
            "No pescoço curvo, a resistência continua a mesma da antiga êne dê e Turbo! "
            "Em duzentos e vinte volts ela esquenta mais que em cento e vinte e sete. "
            "Use o cabo certo e repare: a zagonél deixou a haste toda branca!"
        ),
        "phrase_replacements": [
            ("êne dê", "ND"),
            ("duzentos e vinte volts", "220V"),
            ("cento e vinte e sete", "127"),
            ("zagonél", "Zagonel"),
        ],
    },
    {
        "id": "05",
        "title": "Fechamento com Produto Real Funcionando e CTA (127V e 220V)",
        "motor": "Rig 2.5D + Determinístico",
        "rate": "+22%",
        "max_dur_s": None,
        "show_rig": True,
        "actions": [(0.0, "toque_chapeu"), (0.45, "apontar_produto")],
        "top_bar": ("ZAGONEL ND OFICIAL · 4,8/5 (3.152 AVAL.)", "produto real"),
        "status_pill": ("#22c55e", "LINK NA BIO · OU COMENTE: ZAGONEL"),
        "display_text": (
            "É o projeto clássico com mais de três mil avaliações positivas e banho sem aperto! "
            "Quer a versão 127 ou 220V? "
            "Os links separados estão na bio, ou comente ZAGONEL!"
        ),
        "tts_text": (
            "É o projeto clássico com mais de três mil avaliações positivas e banho sem aperto! "
            "Quer a versão cento e vinte e sete ou duzentos e vinte volts? "
            "Os links separados estão na bío, ou comente zagonél!"
        ),
        "phrase_replacements": [
            ("cento e vinte e sete", "127"),
            ("duzentos e vinte volts", "220V"),
            ("bío", "bio"),
            ("zagonél", "ZAGONEL"),
        ],
    },
]


def load_font(size: int, bold: bool = True, mono: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    if mono:
        candidates = [
            "/System/Library/Fonts/Supplemental/Courier New Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Courier New.ttf",
            "/System/Library/Fonts/Menlo.ttc",
            "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        ]
    else:
        candidates = [
            "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
            "/System/Library/Fonts/Helvetica.ttc",
        ]
    for p in candidates:
        if Path(p).exists():
            return ImageFont.truetype(p, max(8, size))
    return ImageFont.load_default()


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
    )
    return float(out.strip())


def collapse_phonetic_words(
    raw_words: list[dict[str, Any]],
    replacements: list[tuple[str, str]],
) -> list[dict[str, Any]]:
    """Collapse multi-word phonetic expansions back into clean technical display tokens and normalize punctuation."""
    collapsed: list[dict[str, Any]] = []
    n = len(raw_words)
    i = 0

    rep_seqs: list[tuple[list[str], str]] = [
        ([tok.lower() for tok in src.split()], dst) for src, dst in replacements
    ]
    rep_seqs.sort(key=lambda item: len(item[0]), reverse=True)

    while i < n:
        tok_raw = str(raw_words[i]["text"]).strip()
        # Handle isolated punctuation tokens emitted by Azure Speech WordBoundary
        if tok_raw and all(ch in ".,!?:;-…" for ch in tok_raw):
            if any(ch in "?!" for ch in tok_raw) and collapsed:
                punct = "?" if "?" in tok_raw else "!"
                if not collapsed[-1]["text"].endswith(("?", "!")):
                    collapsed[-1]["text"] = collapsed[-1]["text"].rstrip(".,:;") + punct
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
            clean_tok = tok_raw.rstrip(".,:;")
            if not clean_tok:
                clean_tok = tok_raw
            collapsed.append(
                {
                    "text": clean_tok,
                    "tts_text": str(w["text"]),
                    "start": round(float(w["start"]), 4),
                    "duration": round(float(w["duration"]), 4),
                }
            )
            i += 1
    return collapsed


def build_caption_beats(display_words: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Group display words into beats of 1 to 3 words (strictly <= 3 words per beat)."""
    beats: list[dict[str, Any]] = []
    n = len(display_words)
    i = 0
    while i < n:
        rem = n - i
        chunk_len = 2 if rem == 4 else min(3, rem)
        grp = display_words[i : i + chunk_len]
        s_t = float(grp[0]["start"])
        e_t = float(grp[-1]["start"]) + float(grp[-1]["duration"]) + 0.14
        beats.append(
            {
                "start": round(s_t, 4),
                "end": round(e_t, 4),
                "words": grp,
                "word_count": len(grp),
            }
        )
        i += chunk_len
    for b_idx in range(len(beats) - 1):
        if beats[b_idx]["end"] > beats[b_idx + 1]["start"]:
            beats[b_idx]["end"] = beats[b_idx + 1]["start"]
    return beats


def _load_azure_speech_creds() -> tuple[str, str] | None:
    """Load AZURE_SPEECH_KEY and AZURE_SPEECH_REGION from env or .env without logging secrets."""
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


def _synth_scene_azure(
    text: str,
    voice: str,
    rate: str,
    out_wav: Path,
    key: str,
    region: str,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Synthesize scene audio via official Azure AI Speech API with WordBoundary and Viseme events."""
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
    result = synthesizer.speak_ssml_async(ssml).get()
    if result.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
        details = getattr(result, "cancellation_details", None)
        reason_msg = getattr(details, "reason", result.reason)
        raise RuntimeError(f"Azure AI Speech falhou ({reason_msg})")
    return raw_words, raw_visemes


async def synth_all_scenes(
    build_dir: Path,
    prod_dir: Path,
    tts_engine: str = "auto",
    ml_clips: bool = False,
) -> dict[str, Any]:
    """Synthesize PT-BR TTS audio per scene, trim trailing silence, mix SFX + Cena 02 Flow water audio."""
    build_dir.mkdir(parents=True, exist_ok=True)
    scenes_meta: list[dict[str, Any]] = []
    all_raw_words: list[dict[str, Any]] = []
    all_azure_visemes: list[dict[str, Any]] = []
    t_cursor = 0.0
    trimmed_wavs: list[Path] = []

    azure_creds = _load_azure_speech_creds()
    if tts_engine == "azure" and not azure_creds:
        raise RuntimeError("AZURE_SPEECH_KEY e AZURE_SPEECH_REGION não configurados no .env ou ambiente.")
    use_azure = (tts_engine == "azure") or (tts_engine == "auto" and azure_creds is not None)
    engine_label = "azure-f0" if use_azure else "edge-tts"
    print(f"TTS engine selecionado: {engine_label}")

    for spec in SCENES_SPEC:
        sc_id = spec["id"]
        raw_words: list[dict[str, Any]] = []
        raw_visemes: list[dict[str, Any]] = []
        if use_azure and azure_creds is not None:
            audio_path = build_dir / f"audio_{sc_id}.wav"
            raw_words, raw_visemes = _synth_scene_azure(
                text=spec["tts_text"],
                voice=VOICE,
                rate=spec["rate"],
                out_wav=audio_path,
                key=azure_creds[0],
                region=azure_creds[1],
            )
        else:
            audio_path = build_dir / f"audio_{sc_id}.mp3"
            comm = edge_tts.Communicate(spec["tts_text"], VOICE, rate=spec["rate"], boundary="WordBoundary")
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
        sc_dur = min(raw_dur, last_word_end + 0.24)
        if spec["max_dur_s"] is not None:
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

        disp_words = collapse_phonetic_words(shifted_raw, spec["phrase_replacements"])
        beats = build_caption_beats(disp_words)

        scenes_meta.append(
            {
                "scene": sc_id,
                "title": spec["title"],
                "motor": spec["motor"],
                "start": round(t_cursor, 4),
                "end": round(t_cursor + actual_dur, 4),
                "duration": round(actual_dur, 4),
                "show_rig": spec["show_rig"],
                "top_bar": spec["top_bar"],
                "status_pill": spec["status_pill"],
                "display_text": spec["display_text"],
                "tts_text": spec["tts_text"],
                "actions": spec["actions"],
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

    mixed_wav = build_dir / "master_audio.wav"
    _build_master_audio_mix(
        narration_wav=narration_wav,
        flow_mp4=Path("__disabled__") if ml_clips else (prod_dir / "assets" / "flow_cena02_360p.mp4"),
        scenes_meta=scenes_meta,
        out_wav=mixed_wav,
    )

    if use_azure and all_azure_visemes:
        viseme_frames = build_frame_visemes_from_azure_visemes(
            viseme_events=all_azure_visemes,
            total_duration=t_cursor,
            fps=FPS,
        )
    else:
        viseme_frames = build_frame_visemes_from_words(
            word_events=all_raw_words,
            total_duration=t_cursor,
            fps=FPS,
            wav_path=narration_wav,
            silence_threshold=0.03,
        )

    lipsync_data = {
        "fps": FPS,
        "total_duration": round(t_cursor, 4),
        "total_frames": len(viseme_frames),
        "viseme_frames": viseme_frames,
    }
    (build_dir / "lipsync.json").write_text(json.dumps(lipsync_data, ensure_ascii=False, indent=2), encoding="utf-8")

    timeline_data = {
        "total_duration": round(t_cursor, 4),
        "fps": FPS,
        "voice": VOICE,
        "req_007_ai_disclosure": True,
        "scenes": scenes_meta,
    }
    (build_dir / "timeline.json").write_text(json.dumps(timeline_data, ensure_ascii=False, indent=2), encoding="utf-8")
    return timeline_data


def _build_master_audio_mix(
    narration_wav: Path,
    flow_mp4: Path,
    scenes_meta: list[dict[str, Any]],
    out_wav: Path,
) -> None:
    """Create stereo 48kHz master audio mixing TTS narration, Cena 02 Flow water audio (-20dB) and subtle transitions."""
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
            "1",
            "-c:a",
            "pcm_s16le",
            str(tmp_narr48),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    with wave.open(str(tmp_narr48), "rb") as wf:
        narr_pcm = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0
    tmp_narr48.unlink(missing_ok=True)

    n_samples = len(narr_pcm)
    mix = narr_pcm.copy()

    sc02 = next((s for s in scenes_meta if s["scene"] == "02"), None)
    if sc02 and flow_mp4.exists():
        tmp_flow_wav = out_wav.parent / "_tmp_flow_water.wav"
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i",
                str(flow_mp4),
                "-vn",
                "-ar",
                str(sr),
                "-ac",
                "1",
                "-c:a",
                "pcm_s16le",
                str(tmp_flow_wav),
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        if tmp_flow_wav.exists():
            with wave.open(str(tmp_flow_wav), "rb") as wf:
                water_pcm = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0
            tmp_flow_wav.unlink(missing_ok=True)
            # Play water sound during Cena 02 (especially prominent in the 2nd half where Flow video runs)
            s_idx = int((sc02["start"] + sc02["duration"] * 0.35) * sr)
            e_idx = min(n_samples, int(sc02["end"] * sr))
            span = max(0, e_idx - s_idx)
            if span > 0 and len(water_pcm) > 0:
                seg = water_pcm[:span].copy()
                if len(seg) < span:
                    seg = np.pad(seg, (0, span - len(seg)), mode="wrap")
                fade_n = min(int(0.35 * sr), span // 3)
                if fade_n > 0:
                    seg[:fade_n] *= np.linspace(0.0, 1.0, fade_n, dtype=np.float32)
                    seg[-fade_n:] *= np.linspace(1.0, 0.0, fade_n, dtype=np.float32)
                mix[s_idx:e_idx] += seg * 0.11  # -19 dB

    for sc in scenes_meta[1:]:
        b_idx = int(sc["start"] * sr)
        dur_s = 0.14
        k_len = int(dur_s * sr)
        if b_idx + k_len < n_samples:
            t_arr = np.linspace(0.0, dur_s, k_len, dtype=np.float32)
            env = np.sin(np.pi * t_arr / dur_s) ** 2
            tone = (np.sin(2.0 * np.pi * 520.0 * t_arr) + 0.5 * np.sin(2.0 * np.pi * 780.0 * t_arr)) * env * 0.022
            mix[b_idx : b_idx + k_len] += tone

    mix = np.clip(mix, -0.98, 0.98)
    pcm16 = (mix * 32767.0).astype(np.int16)
    stereo = np.column_stack([pcm16, pcm16]).ravel()
    with wave.open(str(out_wav), "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(stereo.tobytes())


def _smoothstep(edge0: float, edge1: float, x: float) -> float:
    t = max(0.0, min(1.0, (x - edge0) / max(1e-6, edge1 - edge0)))
    return t * t * (3.0 - 2.0 * t)


def _lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def _lerp_vec(a: tuple[float, float, float], b: tuple[float, float, float], t: float) -> tuple[float, float, float]:
    return (_lerp(a[0], b[0], t), _lerp(a[1], b[1], t), _lerp(a[2], b[2], t))


def _lerp_color(c1: tuple[int, int, int], c2: tuple[int, int, int], t: float) -> tuple[int, int, int]:
    t_c = max(0.0, min(1.0, t))
    return (
        int(round(c1[0] + (c2[0] - c1[0]) * t_c)),
        int(round(c1[1] + (c2[1] - c1[1]) * t_c)),
        int(round(c1[2] + (c2[2] - c1[2]) * t_c)),
    )


class ND3DRayXEngine:
    """Vectorized 3D X-Ray Engineering Rasterizer for the Zagonel ND Shower with 100% Watertight Compartmentation."""

    def __init__(self, width: int, height: int) -> None:
        self.W = width
        self.H = height
        self.scale = width / 1080.0

        # Precompute dark studio backdrop (#090a0f) with subtle radial engineering glow
        self.studio_bg = self._build_studio_backdrop()

        # Build 3D Mesh Quads for the true Zagonel ND morphology:
        self.mesh_rear_body = self._build_rear_body_mesh()
        self.mesh_top_cap = self._build_top_cap_mesh()
        self.mesh_inlet_pipe = self._build_inlet_pipe_mesh()
        self.mesh_curved_neck = self._build_curved_neck_mesh()
        self.mesh_spreader_head, self.nozzle_pts_local = self._build_spreader_head_mesh()
        # Closed internal water pipe inside the upper rear body (strictly y >= +0.20, above watertight bulkhead y = +0.08)
        self.mesh_closed_water_tube = self._build_closed_water_tube_mesh()

        # Deterministic 3D particle seeds (420 particles strictly confined inside upper tube & hot chamber)
        rng = np.random.default_rng(42)
        self.p_count = 420
        self.p_phase0 = rng.random(self.p_count, dtype=np.float32)
        self.p_ang = rng.uniform(0.0, 2.0 * np.pi, self.p_count).astype(np.float32)
        self.p_rad = np.sqrt(rng.random(self.p_count, dtype=np.float32))
        self.p_spd = rng.uniform(0.85, 1.18, self.p_count).astype(np.float32)

    def s(self, val_1080: float) -> int:
        return int(round(val_1080 * self.scale))

    def _build_studio_backdrop(self) -> Image.Image:
        yy, xx = np.mgrid[0 : self.H, 0 : self.W].astype(np.float32)
        cx = self.W * 0.46
        cy = self.H * 0.35
        rx = self.W * 0.52
        ry = self.H * 0.28
        dist2 = ((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2
        glow = np.exp(-dist2 * 1.35)

        r = np.clip(9.0 + glow * 10.0, 0, 255).astype(np.uint8)
        g = np.clip(10.0 + glow * 28.0, 0, 255).astype(np.uint8)
        b = np.clip(15.0 + glow * 48.0, 0, 255).astype(np.uint8)
        a = np.full((self.H, self.W), 255, dtype=np.uint8)
        bg = Image.fromarray(np.dstack([r, g, b, a]), mode="RGBA")
        return bg

    @staticmethod
    def _quads_from_rings(rings: list[np.ndarray]) -> dict[str, np.ndarray]:
        """Build (N, 4, 3) quads, face centers, and unit normals from a list of 3D rings (M, 3)."""
        quads_list: list[np.ndarray] = []
        for r_idx in range(len(rings) - 1):
            r0 = rings[r_idx]
            r1 = rings[r_idx + 1]
            m = len(r0)
            for j in range(m):
                jn = (j + 1) % m
                q = np.array([r0[j], r0[jn], r1[jn], r1[j]], dtype=np.float32)
                quads_list.append(q)
        quads = np.stack(quads_list, axis=0)
        centers = quads.mean(axis=1)
        v1 = quads[:, 1] - quads[:, 0]
        v2 = quads[:, 3] - quads[:, 0]
        norms = np.cross(v1, v2)
        lens = np.linalg.norm(norms, axis=1, keepdims=True)
        norms = norms / np.maximum(lens, 1e-6)
        return {"quads": quads, "centers": centers, "normals": norms}

    def _build_rear_body_mesh(self) -> dict[str, np.ndarray]:
        """Subconjunto A: Bojo Traseiro Vertical Ovalado (204 mm altura, encostado na parede em z ≈ -0.68)."""
        profile = [
            (-0.88, 0.08, 0.08, -0.68),
            (-0.82, 0.14, 0.13, -0.68),
            (-0.62, 0.26, 0.22, -0.66),
            (-0.32, 0.38, 0.31, -0.64),
            (0.08, 0.45, 0.36, -0.62),
            (0.38, 0.46, 0.36, -0.62),
            (0.64, 0.43, 0.34, -0.64),
            (0.78, 0.38, 0.30, -0.66),
        ]
        n_seg = 24
        thetas = np.linspace(0.0, 2.0 * np.pi, n_seg, endpoint=False, dtype=np.float32)
        rings: list[np.ndarray] = []
        for y_val, rx, rz, z_off in profile:
            xs = np.cos(thetas) * rx
            zs = z_off + np.sin(thetas) * rz
            zs = np.maximum(zs, -0.98)
            ys = np.full_like(xs, y_val)
            rings.append(np.column_stack([xs, ys, zs]))
        return self._quads_from_rings(rings)

    def _build_top_cap_mesh(self) -> dict[str, np.ndarray]:
        """Tampa superior do bojo traseiro (sobe em +Y quando explode > 0)."""
        profile = [
            (0.78, 0.38, 0.30, -0.66),
            (0.84, 0.32, 0.25, -0.66),
            (0.89, 0.16, 0.13, -0.67),
            (0.91, 0.02, 0.02, -0.68),
        ]
        n_seg = 20
        thetas = np.linspace(0.0, 2.0 * np.pi, n_seg, endpoint=False, dtype=np.float32)
        rings: list[np.ndarray] = []
        for y_val, rx, rz, z_off in profile:
            xs = np.cos(thetas) * rx
            zs = np.maximum(z_off + np.sin(thetas) * rz, -0.98)
            ys = np.full_like(xs, y_val)
            rings.append(np.column_stack([xs, ys, zs]))
        return self._quads_from_rings(rings)

    def _build_inlet_pipe_mesh(self) -> dict[str, np.ndarray]:
        """Nipple traseiro horizontal de entrada d'água 1/2" BSP na Zona Superior Úmida (y = +0.34)."""
        z_vals = [-1.52, -1.42, -1.40, -0.96]
        r_vals = [0.22, 0.22, 0.12, 0.12]
        n_seg = 16
        thetas = np.linspace(0.0, 2.0 * np.pi, n_seg, endpoint=False, dtype=np.float32)
        rings: list[np.ndarray] = []
        for zv, rv in zip(z_vals, r_vals):
            xs = np.cos(thetas) * rv
            ys = 0.34 + np.sin(thetas) * rv
            zs = np.full_like(xs, zv)
            rings.append(np.column_stack([xs, ys, zs]))
        return self._quads_from_rings(rings)

    def _build_closed_water_tube_mesh(self) -> dict[str, np.ndarray]:
        """Tubo/duto hidráulico interno fechado na Zona Superior Úmida (y = +0.20..+0.54, acima da parede divisória y = +0.08)."""
        y_vals = np.linspace(0.20, 0.54, 6, dtype=np.float32)
        n_seg = 18
        thetas = np.linspace(0.0, 2.0 * np.pi, n_seg, endpoint=False, dtype=np.float32)
        rings: list[np.ndarray] = []
        for yv in y_vals:
            xs = np.cos(thetas) * 0.23
            zs = -0.66 + np.sin(thetas) * 0.19
            ys = np.full_like(xs, yv)
            rings.append(np.column_stack([xs, ys, zs]))
        return self._quads_from_rings(rings)

    @staticmethod
    def _neck_spine(u: float) -> tuple[float, float, float, float, float]:
        """Return (x, y, z, rx, ry) along the curved upper neck (Câmara Quente 700 ml) to frontal spreader head."""
        z = -0.44 + u * 1.52
        y = 0.46 + math.sin(u * math.pi * 0.78) * 0.14 - (u ** 1.7) * 0.34
        rx = 0.31 + (u ** 1.5) * 0.26
        ry = 0.21 + math.sin(u * math.pi) * 0.04 - (u ** 1.8) * 0.08
        return (0.0, y, z, rx, ry)

    def _build_curved_neck_mesh(self) -> dict[str, np.ndarray]:
        """Subconjunto C (parte 1): Braço/Pescoço Superior Curvo — Câmara Quente 700 ml (324 mm de avanço)."""
        n_steps = 14
        n_seg = 20
        thetas = np.linspace(0.0, 2.0 * np.pi, n_seg, endpoint=False, dtype=np.float32)
        rings: list[np.ndarray] = []
        for i in range(n_steps):
            u = i / (n_steps - 1)
            cx, cy, cz, rx, ry = self._neck_spine(u)
            xs = cx + np.cos(thetas) * rx
            ys = cy + np.sin(thetas) * ry
            zs = np.full_like(xs, cz) + np.sin(thetas) * (0.08 * u)
            rings.append(np.column_stack([xs, ys, zs]))
        return self._quads_from_rings(rings)

    def _build_spreader_head_mesh(self) -> tuple[dict[str, np.ndarray], np.ndarray]:
        """Subconjunto C (parte 2): Cabeça Circular do Espalhador Frontal (Ø 120 mm, inclinada 18°, 78 furos)."""
        tilt = math.radians(18.0)
        cos_t, sin_t = math.cos(tilt), math.sin(tilt)
        center = np.array([0.0, 0.04, 1.06], dtype=np.float32)

        profile = [
            (0.14, 0.54),
            (0.06, 0.60),
            (-0.04, 0.62),
            (-0.10, 0.58),
            (-0.11, 0.04),
        ]
        n_seg = 24
        thetas = np.linspace(0.0, 2.0 * np.pi, n_seg, endpoint=False, dtype=np.float32)
        rings: list[np.ndarray] = []
        for ly, r in profile:
            lx = np.cos(thetas) * r
            lz = np.sin(thetas) * r
            ry = ly * cos_t - lz * sin_t
            rz = ly * sin_t + lz * cos_t
            rings.append(np.column_stack([lx + center[0], ry + center[1], rz + center[2]]))

        # 78 nozzles in 4 concentric rings: 8 + 14 + 22 + 34 = 78
        nozzle_rings = [(0.13, 8), (0.26, 14), (0.40, 22), (0.53, 34)]
        noz_list: list[list[float]] = []
        ly = -0.105
        for nr, count in nozzle_rings:
            for k in range(count):
                ang = (k / count) * 2.0 * math.pi
                lx = math.cos(ang) * nr
                lz = math.sin(ang) * nr
                ry = ly * cos_t - lz * sin_t
                rz = ly * sin_t + lz * cos_t
                noz_list.append([lx + float(center[0]), ry + float(center[1]), rz + float(center[2])])

        return self._quads_from_rings(rings), np.array(noz_list, dtype=np.float32)

    def _make_camera(
        self,
        cam_pos: tuple[float, float, float],
        cam_tgt: tuple[float, float, float],
        fov_deg: float,
        stage_cx: float,
        stage_cy: float,
    ) -> dict[str, Any]:
        eye = np.array(cam_pos, dtype=np.float32)
        target = np.array(cam_tgt, dtype=np.float32)
        up = np.array([0.0, 1.0, 0.0], dtype=np.float32)

        fwd = target - eye
        fwd = fwd / max(float(np.linalg.norm(fwd)), 1e-6)
        right = np.cross(fwd, up)
        right = right / max(float(np.linalg.norm(right)), 1e-6)
        true_up = np.cross(right, fwd)

        focal = (self.W * 0.37) / math.tan(math.radians(fov_deg) * 0.5)
        return {
            "eye": eye,
            "fwd": fwd,
            "right": right,
            "up": true_up,
            "focal": focal,
            "cx": stage_cx,
            "cy": stage_cy,
        }

    @staticmethod
    def _project_points(pts: np.ndarray, cam: dict[str, Any]) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Project (N, 3) world points to 2D screen coordinates (u, v) and view depth z_view."""
        rel = pts - cam["eye"]
        x_cam = rel @ cam["right"]
        y_cam = rel @ cam["up"]
        z_cam = np.maximum(rel @ cam["fwd"], 0.15)
        scale = cam["focal"] / z_cam
        u = cam["cx"] + x_cam * scale
        v = cam["cy"] - y_cam * scale
        return u, v, z_cam

    def _draw_mesh_pass(
        self,
        draw: ImageDraw.ImageDraw,
        mesh: dict[str, np.ndarray],
        offset: tuple[float, float, float],
        cam: dict[str, Any],
        base_rgb: tuple[int, int, int],
        rim_rgb: tuple[int, int, int],
        shell_opacity: float,
        front_pass: bool,
        wire_alpha: int = 0,
    ) -> None:
        off = np.array(offset, dtype=np.float32)
        quads = mesh["quads"] + off
        centers = mesh["centers"] + off
        normals = mesh["normals"]

        view_dirs = cam["eye"] - centers
        v_lens = np.linalg.norm(view_dirs, axis=1, keepdims=True)
        view_dirs = view_dirs / np.maximum(v_lens, 1e-6)
        dot_nv = np.sum(normals * view_dirs, axis=1)

        if front_pass:
            mask = dot_nv >= -0.05
        else:
            mask = dot_nv < -0.05

        if not np.any(mask):
            return

        sel_quads = quads[mask]
        sel_centers = centers[mask]
        sel_normals = normals[mask]
        sel_dot = np.abs(dot_nv[mask])

        _, _, z_depths = self._project_points(sel_centers, cam)
        order = np.argsort(-z_depths)
        sel_quads = sel_quads[order]
        sel_normals = sel_normals[order]
        sel_dot = sel_dot[order]

        m = len(sel_quads)
        flat_pts = sel_quads.reshape(-1, 3)
        u_flat, v_flat, _ = self._project_points(flat_pts, cam)
        u_q = u_flat.reshape(m, 4)
        v_q = v_flat.reshape(m, 4)

        light_dir = np.array([0.55, 0.65, 0.52], dtype=np.float32)
        diff = np.clip(sel_normals @ light_dir, 0.0, 1.0)
        fresnel = np.power(1.0 - np.clip(sel_dot, 0.0, 1.0), 1.75)

        xray_factor = 1.0 - max(0.0, min(1.0, (shell_opacity - 0.14) / 0.78))

        for i in range(m):
            f_val = float(fresnel[i])
            d_val = float(diff[i])
            rim_mix = min(1.0, f_val * (0.55 + 0.45 * xray_factor) + d_val * 0.18)
            r = int(round(base_rgb[0] * (0.45 + 0.55 * d_val) * (1.0 - rim_mix) + rim_rgb[0] * rim_mix))
            g = int(round(base_rgb[1] * (0.45 + 0.55 * d_val) * (1.0 - rim_mix) + rim_rgb[1] * rim_mix))
            b = int(round(base_rgb[2] * (0.45 + 0.55 * d_val) * (1.0 - rim_mix) + rim_rgb[2] * rim_mix))

            if front_pass:
                alpha_base = shell_opacity * 235.0
                alpha_xray = 6.0 + (f_val ** 1.35) * 95.0
                a = int(round(_lerp(alpha_base, alpha_xray, xray_factor)))
            else:
                alpha_base = shell_opacity * 155.0
                alpha_xray = 14.0 + f_val * 65.0
                a = int(round(_lerp(alpha_base, alpha_xray, xray_factor)))

            pts_2d = [
                (float(u_q[i, 0]), float(v_q[i, 0])),
                (float(u_q[i, 1]), float(v_q[i, 1])),
                (float(u_q[i, 2]), float(v_q[i, 2])),
                (float(u_q[i, 3]), float(v_q[i, 3])),
            ]
            draw.polygon(pts_2d, fill=(max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)), max(0, min(255, a))))
            if wire_alpha > 0 and (i % 2 == 0 or f_val > 0.48):
                wa = int(round(wire_alpha * (0.35 + 0.65 * f_val)))
                draw.line(pts_2d + [pts_2d[0]], fill=(0, 229, 255, max(0, min(255, wa))), width=1)

    def _draw_3d_tube(
        self,
        draw: ImageDraw.ImageDraw,
        pts_3d: np.ndarray,
        cam: dict[str, Any],
        radius_world: float,
        color_rgba: tuple[int, int, int, int],
        highlight_rgba: tuple[int, int, int, int] | None = None,
    ) -> None:
        u, v, z = self._project_points(pts_3d, cam)
        n = len(pts_3d)
        for i in range(n - 1):
            z_mid = 0.5 * (float(z[i]) + float(z[i + 1]))
            w_px = max(1, int(round(radius_world * cam["focal"] / z_mid)))
            p0 = (float(u[i]), float(v[i]))
            p1 = (float(u[i + 1]), float(v[i + 1]))
            draw.line([p0, p1], fill=color_rgba, width=w_px)
            if highlight_rgba and w_px >= 3:
                draw.line([p0, p1], fill=highlight_rgba, width=max(1, w_px // 2))

    def _draw_3d_disc(
        self,
        draw: ImageDraw.ImageDraw,
        center_3d: tuple[float, float, float],
        radius_x: float,
        radius_z: float,
        cam: dict[str, Any],
        fill_rgba: tuple[int, int, int, int],
        outline_rgba: tuple[int, int, int, int] | None = None,
        n_pts: int = 24,
        outline_width: int = 1,
    ) -> None:
        ang = np.linspace(0.0, 2.0 * np.pi, n_pts, endpoint=False, dtype=np.float32)
        pts = np.column_stack(
            [
                center_3d[0] + np.cos(ang) * radius_x,
                np.full_like(ang, center_3d[1]),
                center_3d[2] + np.sin(ang) * radius_z,
            ]
        )
        u, v, _ = self._project_points(pts, cam)
        poly = [(float(u[i]), float(v[i])) for i in range(n_pts)]
        draw.polygon(poly, fill=fill_rgba)
        if outline_rgba is not None:
            draw.line(poly + [poly[0]], fill=outline_rgba, width=max(1, outline_width))

    def _draw_3d_box(
        self,
        draw: ImageDraw.ImageDraw,
        center_3d: tuple[float, float, float],
        size_3d: tuple[float, float, float],
        cam: dict[str, Any],
        fill_rgba: tuple[int, int, int, int],
        outline_rgba: tuple[int, int, int, int] | None = None,
    ) -> None:
        cx, cy, cz = center_3d
        hx, hy, hz = size_3d[0] * 0.5, size_3d[1] * 0.5, size_3d[2] * 0.5
        corners = np.array(
            [
                [cx - hx, cy - hy, cz - hz],
                [cx + hx, cy - hy, cz - hz],
                [cx + hx, cy + hy, cz - hz],
                [cx - hx, cy + hy, cz - hz],
                [cx - hx, cy - hy, cz + hz],
                [cx + hx, cy - hy, cz + hz],
                [cx + hx, cy + hy, cz + hz],
                [cx - hx, cy + hy, cz + hz],
            ],
            dtype=np.float32,
        )
        faces_idx = [
            (0, 1, 2, 3),
            (4, 5, 6, 7),
            (0, 4, 7, 3),
            (1, 5, 6, 2),
            (3, 2, 6, 7),
            (0, 1, 5, 4),
        ]
        u, v, z = self._project_points(corners, cam)
        face_depths = [(f, float(np.mean([z[idx] for idx in f]))) for f in faces_idx]
        face_depths.sort(key=lambda item: -item[1])
        for f, _ in face_depths[:4]:
            poly = [(float(u[idx]), float(v[idx])) for idx in f]
            draw.polygon(poly, fill=fill_rgba, outline=outline_rgba)

    def render_3d_stage(
        self,
        t: float,
        state: dict[str, Any],
    ) -> tuple[Image.Image, dict[str, tuple[int, int]]]:
        """Render the 3D X-Ray Zagonel ND with 100% Watertight Compartmentation and return projected 2D anchor points."""
        canvas = self.studio_bg.copy()
        back_shell_layer = Image.new("RGBA", (self.W, self.H), (0, 0, 0, 0))
        organs_layer = Image.new("RGBA", (self.W, self.H), (0, 0, 0, 0))
        front_shell_layer = Image.new("RGBA", (self.W, self.H), (0, 0, 0, 0))
        glow_layer = Image.new("RGBA", (self.W, self.H), (0, 0, 0, 0))

        b_draw = ImageDraw.Draw(back_shell_layer)
        draw = ImageDraw.Draw(organs_layer)
        f_draw = ImageDraw.Draw(front_shell_layer)
        g_draw = ImageDraw.Draw(glow_layer)

        cam = self._make_camera(
            cam_pos=state["cam_pos"],
            cam_tgt=state["cam_tgt"],
            fov_deg=state.get("fov", 36.0),
            stage_cx=self.W * state.get("stage_cx_ratio", 0.50),
            stage_cy=self.H * state.get("stage_cy_ratio", 0.35),
        )

        # Draw subtle 3D perspective studio floor grid (#0f172a / cyan tint)
        grid_y = -2.85
        for gz in np.linspace(-2.2, 2.2, 9):
            pts = np.array([[-1.8, grid_y, gz], [1.8, grid_y, gz]], dtype=np.float32)
            u, v, _ = self._project_points(pts, cam)
            b_draw.line([(float(u[0]), float(v[0])), (float(u[1]), float(v[1]))], fill=(30, 58, 95, 55), width=1)
        for gx in np.linspace(-1.8, 1.8, 9):
            pts = np.array([[gx, grid_y, -2.2], [gx, grid_y, 2.2]], dtype=np.float32)
            u, v, _ = self._project_points(pts, cam)
            b_draw.line([(float(u[0]), float(v[0])), (float(u[1]), float(v[1]))], fill=(30, 58, 95, 55), width=1)

        op = float(state["shell_opacity"])
        ex = float(state["explode"])
        wf = float(state["water_flow"])
        pw = float(state["power_level"])
        dl = float(state["diaphragm_lift"])
        closed = dl > 0.72
        heat = pw if closed else 0.0
        xray = 1.0 - max(0.0, min(1.0, (op - 0.14) / 0.78))
        wire_a = int(round(xray * 110))

        # Offsets for Exploded View (Vista Explodida)
        off_rear = (0.0, 0.0, 0.0)
        off_top_cap = (0.0, ex * 0.45, 0.0)
        off_neck = (0.0, ex * 0.12, ex * 0.05)
        off_spreader = (0.0, -ex * 0.28, ex * 0.16)
        off_diaph_y = ex * 0.16

        shell_rgb = (224, 236, 248)
        rim_rgb = (0, 229, 255)

        # PASS 1: Back-facing translucent shell faces
        self._draw_mesh_pass(b_draw, self.mesh_inlet_pipe, off_rear, cam, shell_rgb, rim_rgb, op, front_pass=False)
        self._draw_mesh_pass(b_draw, self.mesh_rear_body, off_rear, cam, shell_rgb, rim_rgb, op, front_pass=False)
        self._draw_mesh_pass(b_draw, self.mesh_curved_neck, off_neck, cam, shell_rgb, rim_rgb, op, front_pass=False)
        self._draw_mesh_pass(b_draw, self.mesh_spreader_head, off_spreader, cam, shell_rgb, rim_rgb, op, front_pass=False)
        self._draw_mesh_pass(b_draw, self.mesh_top_cap, off_top_cap, cam, shell_rgb, rim_rgb, op, front_pass=False)

        # PASS 2: Closed Internal Water Tube Wall in Upper Rear Body (y = +0.20..+0.54)
        self._draw_mesh_pass(
            b_draw,
            self.mesh_closed_water_tube,
            off_rear,
            cam,
            base_rgb=(14, 165, 233),
            rim_rgb=(0, 229, 255),
            shell_opacity=0.30 + wf * 0.18,
            front_pass=True,
            wire_alpha=int(round(75 * xray)),
        )
        # Inlet horizontal internal pipe connecting rear nipple (z=-1.45) to vertical closed tube (z=-0.66) at y=+0.34
        inlet_internal_pts = np.array([[0.0, 0.34, -1.45], [0.0, 0.34, -0.66]], dtype=np.float32)
        self._draw_3d_tube(b_draw, inlet_internal_pts, cam, 0.095, (14, 165, 233, 120), (0, 229, 255, 190))

        # PASS 3: Watertight Bulkhead Wall (Parede Divisória Estanque Horizontal + Anel O-Ring em y = +0.08)
        # Separates Upper Wet Zone (y >= +0.20) from Lower Dry Zone (y < +0.04)
        self._draw_3d_disc(
            draw,
            (0.0, 0.08, -0.64),
            0.44,
            0.35,
            cam,
            fill_rgba=(30, 41, 59, 248),
            outline_rgba=(250, 204, 21, 255),
            n_pts=32,
            outline_width=max(2, self.s(3)),
        )
        self._draw_3d_disc(
            draw,
            (0.0, 0.11, -0.64),
            0.42,
            0.33,
            cam,
            fill_rgba=(51, 65, 85, 240),
            outline_rgba=(0, 229, 255, 235),
            n_pts=32,
            outline_width=max(1, self.s(2)),
        )
        # Solid bottom base of the closed water tube at y = +0.20
        self._draw_3d_disc(
            draw,
            (0.0, 0.20, -0.66),
            0.24,
            0.20,
            cam,
            fill_rgba=(14, 116, 144, 235),
            outline_rgba=(0, 229, 255, 255),
            n_pts=24,
            outline_width=max(1, self.s(2)),
        )

        # PASS 4: Subconjunto B — Haste Seletora Vertical Inferior (493 mm, saindo do bico inferior do bojo traseiro!)
        collar_pts = np.array([[0.0, -0.86, -0.68], [0.0, -1.10, -0.68]], dtype=np.float32)
        shaft_pts = np.array([[0.0, -1.10, -0.68], [0.0, -2.54, -0.68]], dtype=np.float32)
        tip_pts = np.array([[0.0, -2.54, -0.68], [0.0, -2.74, -0.68]], dtype=np.float32)
        self._draw_3d_tube(draw, shaft_pts, cam, 0.042, (238, 244, 252, 245), (255, 255, 255, 255))
        self._draw_3d_tube(draw, collar_pts, cam, 0.115, (245, 250, 255, 255), (255, 255, 255, 255))
        self._draw_3d_tube(draw, tip_pts, cam, 0.072, (240, 248, 255, 255), (0, 229, 255, 180))

        # PASS 5: Zona Inferior 100% Seca (y = -0.58..-0.14) — Placa PCB Verde + Regulador Dimmer TRIAC + Potenciômetro
        triac_z = -0.64
        # Placa PCB Verde/Cobre isolada abaixo da parede divisória estanque (y = -0.38)
        self._draw_3d_box(
            draw,
            (0.0, -0.38, triac_z),
            (0.32, 0.36, 0.035),
            cam,
            fill_rgba=(16, 85, 58, 250),
            outline_rgba=(34, 197, 94, 245),
        )
        # Potenciômetro acoplado ao eixo vertical da haste (y = -0.50)
        self._draw_3d_box(
            draw,
            (0.0, -0.50, triac_z + 0.03),
            (0.13, 0.13, 0.08),
            cam,
            fill_rgba=(203, 213, 225, 250),
            outline_rgba=(56, 189, 248, 220),
        )
        # Semicondutor TRIAC (regulador tipo dimmer, em y = -0.26)
        pulse_60hz = 0.5 + 0.5 * abs(math.sin(t * 22.0))
        triac_col = _lerp_color((30, 41, 59), (249, 115, 22), heat * (0.45 + 0.55 * pulse_60hz))
        self._draw_3d_box(
            draw,
            (0.05, -0.26, triac_z + 0.04),
            (0.13, 0.14, 0.055),
            cam,
            fill_rgba=(*triac_col, 255),
            outline_rgba=(250, 204, 21, 245),
        )
        # Aba metálica selada do dissipador que sobe encostada apenas por fora na base do tubo frio (sem contato com água!)
        heatsink_tab_pts = np.array([[0.05, -0.20, triac_z + 0.02], [0.05, 0.18, -0.66]], dtype=np.float32)
        self._draw_3d_tube(draw, heatsink_tab_pts, cam, 0.024, (148, 163, 184, 240), (226, 232, 240, 255))

        if heat > 0.05:
            self._draw_3d_box(
                g_draw,
                (0.05, -0.26, triac_z + 0.04),
                (0.18, 0.18, 0.08),
                cam,
                fill_rgba=(249, 115, 22, int(round(150 * heat * pulse_60hz))),
            )

        # PASS 6: Órgão Interno Superior — Diafragma de Borracha + Mola + Ponte de Contatos de Cobre/Prata (y >= +0.54)
        diaph_base_y = 0.54 + off_diaph_y
        lift_y = dl * 0.09
        self._draw_3d_disc(
            draw,
            (0.0, diaph_base_y + lift_y * 0.5, -0.66),
            0.26,
            0.21,
            cam,
            fill_rgba=(30, 41, 59, 250),
            outline_rgba=(6, 182, 212, 255),
            n_pts=24,
            outline_width=max(1, self.s(2)),
        )
        spring_t = np.linspace(0.0, 1.0, 42, dtype=np.float32)
        spring_ang = spring_t * (4.5 * 2.0 * np.pi)
        spring_h = 0.19 * (1.0 - dl * 0.28)
        spring_pts = np.column_stack(
            [
                np.cos(spring_ang) * 0.09,
                (diaph_base_y + 0.03 + lift_y) + spring_t * spring_h,
                -0.66 + np.sin(spring_ang) * 0.07,
            ]
        )
        self._draw_3d_tube(draw, spring_pts, cam, 0.014, (148, 163, 184, 240), (226, 232, 240, 255))

        bridge_y = diaph_base_y + 0.17 + lift_y
        fixed_y = diaph_base_y + 0.27
        self._draw_3d_box(
            draw,
            (0.0, bridge_y, -0.66),
            (0.36, 0.032, 0.09),
            cam,
            fill_rgba=(217, 119, 54, 255),
            outline_rgba=(251, 191, 36, 240),
        )
        self._draw_3d_box(
            draw,
            (-0.14, fixed_y, -0.66),
            (0.13, 0.035, 0.10),
            cam,
            fill_rgba=(180, 83, 9, 255),
            outline_rgba=(251, 191, 36, 220),
        )
        self._draw_3d_box(
            draw,
            (0.14, fixed_y, -0.66),
            (0.13, 0.035, 0.10),
            cam,
            fill_rgba=(180, 83, 9, 255),
            outline_rgba=(251, 191, 36, 220),
        )
        if closed:
            for cx_pad in (-0.13, 0.13):
                self._draw_3d_disc(
                    g_draw,
                    (cx_pad, fixed_y - 0.01, -0.66),
                    0.065,
                    0.065,
                    cam,
                    fill_rgba=(0, 229, 255, 220),
                )
                self._draw_3d_disc(
                    draw,
                    (cx_pad, fixed_y - 0.01, -0.66),
                    0.038,
                    0.038,
                    cam,
                    fill_rgba=(255, 255, 255, 255),
                    outline_rgba=(0, 229, 255, 255),
                )

        # PASS 7: Órgão Interno 3 — Resistência Espiral Dupla Hélice de Níquel-Cromo (NiCr) na Câmara Quente (700 ml, Pescoço Curvo)
        n_coil = 140
        u_arr = np.linspace(0.06, 0.88, n_coil, dtype=np.float32)
        spine_pts: list[list[float]] = []
        coil_pts: list[list[float]] = []
        for u_val in u_arr:
            sx, sy, sz, rx, ry = self._neck_spine(float(u_val))
            sy += off_neck[1] * 0.5
            sz += off_neck[2] * 0.5
            spine_pts.append([sx, sy, sz])
            ang = float(u_val) * 16.0 * 2.0 * math.pi
            cr = 0.13 + math.sin(float(u_val) * math.pi) * 0.03
            coil_pts.append(
                [
                    sx + math.cos(ang) * cr,
                    sy + math.sin(ang) * cr * 0.68,
                    sz,
                ]
            )
        spine_arr = np.array(spine_pts, dtype=np.float32)
        coil_arr = np.array(coil_pts, dtype=np.float32)

        # Suporte termoplástico isolante comprido de encaixe rápido padrão ND/Turbo
        self._draw_3d_tube(draw, spine_arr, cam, 0.038, (203, 213, 225, 225), (248, 250, 252, 245))

        coil_rgb = _lerp_color((113, 113, 122), (255, 85, 0), min(1.0, heat * 1.15))
        coil_hi = _lerp_color((161, 161, 170), (255, 215, 100), heat)
        if heat > 0.08:
            self._draw_3d_tube(
                g_draw,
                coil_arr,
                cam,
                0.050,
                (255, 95, 15, int(round(195 * heat))),
            )
        self._draw_3d_tube(
            draw,
            coil_arr,
            cam,
            0.020,
            (*coil_rgb, 255),
            (*coil_hi, 255),
        )

        # PASS 8: Continuous Streamlines (Fitas de Fluxo Hidráulico Contínuas) + Confinamento Estrito da Água (y >= +0.22 no bojo!)
        if wf > 0.02:
            # 8A. Continuous Water Streamlines inside the closed upper pipe and curved hot chamber
            stream_offsets = [(-0.07, 0.0), (0.0, 0.04), (0.07, -0.02)]
            for ox, oy in stream_offsets:
                st_pts: list[list[float]] = [
                    [ox * 0.5, 0.34 + oy * 0.5, -1.45],
                    [ox * 0.6, 0.34 + oy * 0.5, -0.70],
                    [ox * 0.7, 0.48 + lift_y * 0.4, -0.64],
                ]
                for u_s in np.linspace(0.05, 0.94, 18):
                    sx, sy, sz, _, _ = self._neck_spine(float(u_s))
                    st_pts.append([sx + ox, sy + off_neck[1] * 0.5 + oy, sz + off_neck[2] * 0.5])
                st_arr = np.array(st_pts, dtype=np.float32)
                st_col = _lerp_color((0, 229, 255), (255, 140, 45), heat * 0.75)
                self._draw_3d_tube(
                    draw,
                    st_arr,
                    cam,
                    0.015,
                    (*st_col, int(round(165 * wf))),
                    (224, 242, 254, int(round(210 * wf))),
                )

            # 8B. Continuous Water Jets streaming down from the 78 frontal nozzles
            jet_col = _lerp_color((0, 229, 255), (255, 155, 65), heat * 0.85)
            for n_idx in range(0, len(self.nozzle_pts_local), 3):
                n_pt = self.nozzle_pts_local[n_idx]
                j_start = [float(n_pt[0]), float(n_pt[1]) + off_spreader[1], float(n_pt[2]) + off_spreader[2]]
                j_end = [
                    float(n_pt[0]) * 1.24,
                    float(n_pt[1]) + off_spreader[1] - 1.65,
                    float(n_pt[2]) + off_spreader[2] + 0.44,
                ]
                j_arr = np.array([j_start, j_end], dtype=np.float32)
                self._draw_3d_tube(
                    b_draw,
                    j_arr,
                    cam,
                    0.008,
                    (*jet_col, int(round(95 * wf))),
                )

            # 8C. Confined Fluid Particles (NEVER below y = +0.22 in the rear body!)
            flow_speed = 0.22 + wf * 0.85
            phases = (self.p_phase0 + t * 0.48 * self.p_spd * flow_speed) % 1.0
            p_xyz = np.zeros((self.p_count, 3), dtype=np.float32)
            p_heat = np.zeros(self.p_count, dtype=np.float32)

            for i in range(self.p_count):
                ph = float(phases[i])
                ang = float(self.p_ang[i])
                rad = float(self.p_rad[i])
                if ph < 0.20:
                    # 1. Entrada pelo nipple superior (y = +0.34, z = -1.48..-0.68)
                    s = ph / 0.20
                    r = rad * 0.065
                    p_xyz[i, 0] = math.cos(ang) * r
                    p_xyz[i, 1] = 0.34 + math.sin(ang) * r * 0.7
                    p_xyz[i, 2] = _lerp(-1.48, -0.68, s)
                    p_heat[i] = 0.0
                elif ph < 0.42:
                    # 2. Subindo EXCLUSIVAMENTE dentro do tubo fechado superior (y = +0.26..+0.52) até o diafragma
                    s = (ph - 0.20) / 0.22
                    sw = ang + s * 2.4
                    r = 0.04 + rad * 0.14
                    p_xyz[i, 0] = math.cos(sw) * r
                    p_xyz[i, 1] = _lerp(0.26, 0.51 + lift_y, s)
                    p_xyz[i, 2] = -0.66 + math.sin(sw) * r * 0.75
                    p_heat[i] = 0.0
                elif ph < 0.76:
                    # 3. Percorrendo a Câmara Quente (700 ml) no pescoço curvo ao redor da resistência espiral NiCr
                    s = (ph - 0.42) / 0.34
                    sx, sy, sz, _, _ = self._neck_spine(s)
                    sw = ang + s * 5.2
                    r = 0.03 + rad * 0.14
                    p_xyz[i, 0] = sx + math.cos(sw) * r
                    p_xyz[i, 1] = sy + off_neck[1] * 0.5 + math.sin(sw) * r * 0.65
                    p_xyz[i, 2] = sz + off_neck[2] * 0.5
                    p_heat[i] = heat * (s ** 0.80)
                else:
                    # 4. Jorrando em feixe cônico pelos 78 furos do espalhador frontal Ø 120 mm (z >= +1.05)
                    s = (ph - 0.76) / 0.24
                    noz_idx = i % len(self.nozzle_pts_local)
                    n_pt = self.nozzle_pts_local[noz_idx]
                    p_xyz[i, 0] = float(n_pt[0]) * (1.0 + s * 0.26)
                    p_xyz[i, 1] = float(n_pt[1]) + off_spreader[1] - s * 1.85
                    p_xyz[i, 2] = float(n_pt[2]) + off_spreader[2] + s * 0.50
                    p_heat[i] = heat

            pu, pv, pz = self._project_points(p_xyz, cam)
            p_alpha = int(round(min(1.0, wf * 1.15) * 235))
            for i in range(self.p_count):
                ux, vy = float(pu[i]), float(pv[i])
                if not (40 <= ux <= self.W - 40 and 250 <= vy <= self.H - 250):
                    continue
                hm = float(p_heat[i])
                if hm < 0.5:
                    p_rgb = _lerp_color((0, 229, 255), (255, 107, 26), hm * 2.0)
                else:
                    p_rgb = _lerp_color((255, 107, 26), (255, 195, 95), (hm - 0.5) * 2.0)
                pr = max(1, int(round((0.018 * cam["focal"]) / float(pz[i]))))
                g_draw.ellipse([ux - pr * 1.6, vy - pr * 1.6, ux + pr * 1.6, vy + pr * 1.6], fill=(*p_rgb, p_alpha // 3))
                draw.ellipse([ux - pr, vy - pr, ux + pr, vy + pr], fill=(*p_rgb, p_alpha))

        # PASS 9: 78 Bicos do Espalhador Frontal (Ø 120 mm)
        noz_world = self.nozzle_pts_local + np.array(off_spreader, dtype=np.float32)
        nu, nv, nz = self._project_points(noz_world, cam)
        noz_col = _lerp_color((0, 229, 255), (255, 140, 40), heat)
        for i in range(len(noz_world)):
            nr = max(1, int(round((0.012 * cam["focal"]) / float(nz[i]))))
            draw.ellipse(
                [float(nu[i]) - nr, float(nv[i]) - nr, float(nu[i]) + nr, float(nv[i]) + nr],
                fill=(*noz_col, 210),
            )

        # PASS 10: Front-facing Translucent X-Ray Glass Shell + Fresnel Cyan Rim + Subtle Wireframe
        self._draw_mesh_pass(f_draw, self.mesh_inlet_pipe, off_rear, cam, shell_rgb, rim_rgb, op, front_pass=True, wire_alpha=wire_a)
        self._draw_mesh_pass(f_draw, self.mesh_rear_body, off_rear, cam, shell_rgb, rim_rgb, op, front_pass=True, wire_alpha=wire_a)
        self._draw_mesh_pass(f_draw, self.mesh_curved_neck, off_neck, cam, shell_rgb, rim_rgb, op, front_pass=True, wire_alpha=wire_a)
        self._draw_mesh_pass(f_draw, self.mesh_spreader_head, off_spreader, cam, shell_rgb, rim_rgb, op, front_pass=True, wire_alpha=wire_a)
        self._draw_mesh_pass(f_draw, self.mesh_top_cap, off_top_cap, cam, shell_rgb, rim_rgb, op, front_pass=True, wire_alpha=wire_a)

        blurred_glow = glow_layer.filter(ImageFilter.GaussianBlur(radius=max(2, self.s(6))))
        canvas.alpha_composite(back_shell_layer)
        canvas.alpha_composite(blurred_glow)
        canvas.alpha_composite(organs_layer)
        canvas.alpha_composite(front_shell_layer)

        # Project 3D anchor vertices to 2D screen coordinates for HUD Leader Lines
        anchors_3d = {
            "camara_vedada": (0.0, 0.36, -0.66),
            "tubo_vedado": (0.0, 0.34, -0.66),
            "parede_estanque": (0.0, 0.09, -0.64),
            "compartimento_seco": (0.0, -0.40, triac_z),
            "regulador_dimmer": (0.05, -0.26, triac_z),
            "haste_493mm": (0.0, -1.00, -0.68),
            "diafragma": (0.0, diaph_base_y + 0.10 + lift_y, -0.66),
            "espiral_nicr": (0.0, 0.44 + off_neck[1] * 0.5, 0.32 + off_neck[2] * 0.5),
            "espalhador_78": (0.0, -0.05 + off_spreader[1], 1.10 + off_spreader[2]),
        }
        anchor_names = list(anchors_3d.keys())
        anchor_pts = np.array([anchors_3d[k] for k in anchor_names], dtype=np.float32)
        au, av, _ = self._project_points(anchor_pts, cam)
        anchors_2d: dict[str, tuple[int, int]] = {}
        for idx, k in enumerate(anchor_names):
            anchors_2d[k] = (int(round(float(au[idx]))), int(round(float(av[idx]))))

        return canvas, anchors_2d


class ZagonelStageComposer:
    """9:16 Stage Composer integrating Real Product Photos, ND3DRayXEngine, Minimalist HUD, Flow clip, and InspectorRig."""

    def __init__(self, prod_dir: Path, width: int, height: int, ml_clips: bool = False) -> None:
        self.prod_dir = prod_dir
        self.assets_dir = prod_dir / "assets"
        self.W = width
        self.H = height
        self.scale = width / 1080.0
        self.ml_clips = ml_clips

        self.engine_3d = ND3DRayXEngine(width=width, height=height)

        self.rig = InspectorRig()
        self.rig_target_h = self.s(285)

        self.img_era1 = Image.open(self.assets_dir / "era1_thermosystem.jpg").convert("RGBA")
        self.img_era2 = Image.open(self.assets_dir / "era2_hydra_nd.jpg").convert("RGBA")
        self.img_zagonel = Image.open(self.assets_dir / "zagonel_oficial_nd.png").convert("RGBA")
        self.img_uso_real = Image.open(self.assets_dir / "zagonel_nd_uso_real.png").convert("RGBA")
        self.img_resistencia = Image.open(self.assets_dir / "resistencia_tse0277_cut.png").convert("RGBA")

        self.f_top = load_font(self.s(19), bold=True, mono=True)
        self.f_badge = load_font(self.s(17), bold=True, mono=False)
        self.f_leader = load_font(self.s(22), bold=True, mono=True)
        self.f_pill = load_font(self.s(19), bold=True, mono=True)
        self.f_card_lbl = load_font(self.s(17), bold=True, mono=True)
        self.f_thumb_lbl = load_font(self.s(13), bold=True, mono=True)
        self.f_cap = load_font(self.s(40), bold=True, mono=False)

        self.layout_boxes_1080: list[dict[str, Any]] = []

        # Pre-cache Rig 2.5D sprites (used in Scene 01 opening and Scene 05 closing)
        self.rig_cache: dict[tuple[str, str, str], Image.Image] = {}
        self._build_rig_cache()

        # Pre-build Real Product Showcase Cards for Scenes 01, 02, 04, and 05
        self.card_zagonel_hero = self._build_real_product_hero_card(
            w=self.s(490),
            h=self.s(570),
            title="FOTO REAL · ZAGONEL ND OFICIAL",
        )
        self.card_era1_thumb = self._build_photo_thumb_card(
            self.img_era1,
            w=self.s(164),
            h=self.s(144),
            caption="2012 · THERMOSYSTEM",
            border_col=(148, 163, 184, 220),
        )
        self.card_era2_thumb = self._build_photo_thumb_card(
            self.img_era2,
            w=self.s(164),
            h=self.s(144),
            caption="2015 · HYDRA ND",
            border_col=(56, 189, 248, 220),
        )
        self.card_uso_real_side = self._build_photo_thumb_card(
            self.img_uso_real,
            w=self.s(306),
            h=self.s(310),
            caption="INSTALADA NO BANHEIRO",
            border_col=(34, 197, 94, 235),
        )
        self.card_dimmer_wave = self._build_dimmer_explainer_card(
            w=self.s(330),
            h=self.s(210),
        )
        self.card_resistencia_real = self._build_resistance_card(
            w=self.s(244),
            h=self.s(520),
        )
        self.card_closing_real = self._build_closing_dual_real_card(
            w=self.s(530),
            h=self.s(540),
        )
        self.card_haste_zagonel_real = self._build_photo_thumb_card(
            self.img_zagonel,
            w=self.s(404),
            h=self.s(510),
            caption="ATUAL ZAGONEL · HASTE 100% BRANCA",
            border_col=(0, 229, 255, 240),
        )
        self.card_haste_hydra_real = self._build_photo_thumb_card(
            self.img_era2,
            w=self.s(364),
            h=self.s(460),
            caption="ANTIGA HYDRA · ANEL COLORIDO",
            border_col=(250, 204, 21, 235),
        )

        # Pre-build circular optical loupes for Scene 04 part 2 (white collar vs old colored ring)
        self.loupe_white_collar = self._make_circular_loupe(
            self.img_zagonel,
            crop_box=(310, 360, 540, 600),
            diameter=self.s(154),
            border_col=(0, 229, 255, 245),
        )
        self.loupe_old_hydra = self._make_circular_loupe(
            self.img_era2,
            crop_box=(205, 290, 420, 520),
            diameter=self.s(134),
            border_col=(250, 204, 21, 235),
        )

        # Pre-extract Flow frames for Scene 02 Part 2 (or deterministic official photo for ML Clips)
        self.flow_window_pos = (self.s(392), self.s(374))
        self.flow_window_size = (self.s(472), self.s(560))
        if self.ml_clips:
            self.flow_source_name = "deterministic_photo_real_no_flow_ia"
            self.flow_frames = [
                self._build_photo_thumb_card(
                    self.img_zagonel,
                    w=self.flow_window_size[0],
                    h=self.flow_window_size[1],
                    caption="ZAGONEL ND OFICIAL · JATO ABERTO",
                    border_col=(0, 229, 255, 235),
                )
            ]
        else:
            flow_1080 = self.assets_dir / "flow_cena02_1080p.mp4"
            flow_src = flow_1080 if (self.W >= 1080 and flow_1080.exists()) else (self.assets_dir / "flow_cena02_360p.mp4")
            self.flow_source_name = flow_src.name
            self.flow_frames = self._load_flow_clip_frames(flow_src)

    def s(self, val_1080: float) -> int:
        return int(round(val_1080 * self.scale))

    def record_box_1080(self, scene_id: str, label: str, x0: int, y0: int, x1: int, y1: int, kind: str = "element") -> None:
        inv = 1080.0 / self.W
        self.layout_boxes_1080.append(
            {
                "scene": scene_id,
                "label": label,
                "kind": kind,
                "bbox_1080": [
                    int(round(x0 * inv)),
                    int(round(y0 * inv)),
                    int(round(x1 * inv)),
                    int(round(y1 * inv)),
                ],
            }
        )

    def _build_rig_cache(self) -> None:
        actions = ("neutro", "inspecao_lupa", "lanterna_on", "analitico", "apontar_produto", "toque_chapeu")
        visemes = ("X", "BMP", "FV", "EI", "A", "OU", "SORRISO")
        blinks = ("aberto", "fechado")
        for act in actions:
            for vis in visemes:
                for b_state in blinks:
                    im = self.rig.render_frame(
                        t=0.35,
                        viseme=vis,
                        action=act,
                        blink_override=b_state,
                        target_height=self.rig_target_h,
                    )
                    self.rig_cache[(act, vis, b_state)] = im

    def _build_real_product_hero_card(self, w: int, h: int, title: str) -> Image.Image:
        """Build a high-contrast showcase card displaying the real Zagonel ND showering water (zagonel_oficial_nd.png)."""
        card = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        d = ImageDraw.Draw(card)
        d.rounded_rectangle(
            [0, 0, w - 1, h - 1],
            radius=self.s(22),
            fill=(15, 23, 42, 238),
            outline=(0, 229, 255, 235),
            width=max(2, self.s(3)),
        )
        # Soft dark-blue gradient studio plate inside card so the white Zagonel ND shower body + transparent water jets pop with crisp contrast
        inner_pad = self.s(10)
        iw = w - inner_pad * 2
        ih = h - self.s(54)
        yy, xx = np.mgrid[0:ih, 0:iw].astype(np.float32)
        g_norm = yy / max(1.0, float(ih))
        pr = np.clip(18.0 + (1.0 - g_norm) * 16.0, 0, 255).astype(np.uint8)
        pg = np.clip(32.0 + (1.0 - g_norm) * 26.0, 0, 255).astype(np.uint8)
        pb = np.clip(58.0 + (1.0 - g_norm) * 38.0, 0, 255).astype(np.uint8)
        pa = np.full((ih, iw), 255, dtype=np.uint8)
        studio_plate = Image.fromarray(np.dstack([pr, pg, pb, pa]), mode="RGBA")
        # Fit zagonel_oficial_nd.png nicely
        prod_im = self.img_zagonel.copy()
        prod_im.thumbnail((int(iw * 0.96), int(ih * 0.96)), Image.Resampling.LANCZOS)
        px = (iw - prod_im.width) // 2
        py = (ih - prod_im.height) // 2
        studio_plate.alpha_composite(prod_im, (px, py))

        mask = Image.new("L", (iw, ih), 0)
        ImageDraw.Draw(mask).rounded_rectangle([0, 0, iw - 1, ih - 1], radius=self.s(16), fill=255)
        card.paste(studio_plate, (inner_pad, inner_pad), mask)

        # Bottom label strip
        d.text(
            (self.s(18), h - self.s(34)),
            title,
            font=self.f_card_lbl,
            fill=(0, 229, 255, 255),
        )
        return card

    def _build_photo_thumb_card(
        self,
        src_img: Image.Image,
        w: int,
        h: int,
        caption: str,
        border_col: tuple[int, int, int, int],
    ) -> Image.Image:
        card = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        d = ImageDraw.Draw(card)
        d.rounded_rectangle(
            [0, 0, w - 1, h - 1],
            radius=self.s(16),
            fill=(13, 18, 30, 238),
            outline=border_col,
            width=max(1, self.s(2)),
        )
        pad = self.s(6)
        iw = w - pad * 2
        ih = h - self.s(34)
        im = src_img.copy()
        # Center-crop to aspect ratio iw/ih
        src_w, src_h = im.size
        target_ratio = iw / max(1, ih)
        src_ratio = src_w / max(1, src_h)
        if src_ratio > target_ratio:
            new_w = int(src_h * target_ratio)
            x_off = (src_w - new_w) // 2
            im = im.crop((x_off, 0, x_off + new_w, src_h))
        else:
            new_h = int(src_w / target_ratio)
            y_off = (src_h - new_h) // 2
            im = im.crop((0, y_off, src_w, y_off + new_h))
        im = im.resize((iw, ih), Image.Resampling.LANCZOS)

        plate = Image.new("RGBA", (iw, ih), (245, 248, 252, 255))
        plate.alpha_composite(im)
        mask = Image.new("L", (iw, ih), 0)
        ImageDraw.Draw(mask).rounded_rectangle([0, 0, iw - 1, ih - 1], radius=self.s(12), fill=255)
        card.paste(plate, (pad, pad), mask)

        use_font = self.f_thumb_lbl if w <= self.s(200) else self.f_card_lbl
        tb = d.textbbox((0, 0), caption, font=use_font)
        tw = tb[2] - tb[0]
        d.text(
            (max(self.s(4), (w - tw) // 2), h - self.s(24)),
            caption,
            font=use_font,
            fill=(241, 245, 249, 255),
        )
        return card

    def _build_dimmer_explainer_card(self, w: int, h: int) -> Image.Image:
        """Build a layperson-friendly visual card contrasting 3 fixed steps vs continuous dimmer regulation."""
        card = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        d = ImageDraw.Draw(card)
        d.rounded_rectangle(
            [0, 0, w - 1, h - 1],
            radius=self.s(18),
            fill=(11, 16, 28, 232),
            outline=(34, 197, 94, 225),
            width=max(1, self.s(2)),
        )
        d.text((self.s(16), self.s(12)), "COMO UM DIMMER DE LUZ", font=self.f_card_lbl, fill=(34, 197, 94, 255))
        d.text((self.s(16), self.s(36)), "100% de água · calor gradual", font=self.f_badge, fill=(226, 232, 240, 245))

        # Draw smooth gradient temperature ramp bar
        bar_x0, bar_y0 = self.s(18), self.s(76)
        bar_w, bar_h = w - self.s(36), self.s(36)
        steps = 40
        for i in range(steps):
            t_s = i / (steps - 1)
            c_rgb = _lerp_color((0, 229, 255), (255, 95, 20), t_s)
            sx0 = bar_x0 + int(bar_w * (i / steps))
            sx1 = bar_x0 + int(bar_w * ((i + 1) / steps))
            d.rectangle([sx0, bar_y0, sx1, bar_y0 + bar_h], fill=(*c_rgb, 245))
        d.rounded_rectangle(
            [bar_x0, bar_y0, bar_x0 + bar_w, bar_y0 + bar_h],
            radius=self.s(10),
            outline=(248, 250, 252, 210),
            width=max(1, self.s(2)),
        )
        # Slider indicator knob at optimal comfort point (72%)
        kx = bar_x0 + int(bar_w * 0.72)
        d.ellipse(
            [kx - self.s(12), bar_y0 - self.s(6), kx + self.s(12), bar_y0 + bar_h + self.s(6)],
            fill=(250, 204, 21, 255),
            outline=(9, 10, 15, 255),
            width=max(1, self.s(2)),
        )
        d.text((bar_x0, bar_y0 + bar_h + self.s(16)), "FRIO", font=self.f_card_lbl, fill=(56, 189, 248, 255))
        d.text((bar_x0 + self.s(98), bar_y0 + bar_h + self.s(16)), "PONTO CERTO", font=self.f_card_lbl, fill=(250, 204, 21, 255))
        d.text((bar_x0 + bar_w - self.s(66), bar_y0 + bar_h + self.s(16)), "QUENTE", font=self.f_card_lbl, fill=(249, 115, 22, 255))
        return card

    def _build_resistance_card(self, w: int, h: int) -> Image.Image:
        """Build a card showcasing the real longitudinal ND/Turbo quick-fit resistance photo (resistencia_tse0277_cut.png)."""
        card = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        d = ImageDraw.Draw(card)
        d.rounded_rectangle(
            [0, 0, w - 1, h - 1],
            radius=self.s(18),
            fill=(13, 18, 30, 238),
            outline=(249, 115, 22, 235),
            width=max(2, self.s(3)),
        )
        pad = self.s(8)
        iw = w - pad * 2
        ih = h - self.s(64)
        plate = Image.new("RGBA", (iw, ih), (242, 246, 252, 250))

        res_im = self.img_resistencia.copy()
        res_im.thumbnail((int(iw * 0.90), int(ih * 0.94)), Image.Resampling.LANCZOS)
        rx = (iw - res_im.width) // 2
        ry = (ih - res_im.height) // 2
        plate.alpha_composite(res_im, (rx, ry))

        mask = Image.new("L", (iw, ih), 0)
        ImageDraw.Draw(mask).rounded_rectangle([0, 0, iw - 1, ih - 1], radius=self.s(14), fill=255)
        card.paste(plate, (pad, pad), mask)

        d.text((self.s(12), h - self.s(50)), "PEÇA REAL · ENCAIXE", font=self.f_card_lbl, fill=(250, 204, 21, 255))
        d.text((self.s(12), h - self.s(28)), "IGUAL ND E TURBO!", font=self.f_card_lbl, fill=(248, 250, 252, 255))
        return card

    def _build_closing_dual_real_card(self, w: int, h: int) -> Image.Image:
        """Build closing showcase card pairing the official Zagonel ND showering photo + real bathroom installation photo."""
        card = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        d = ImageDraw.Draw(card)
        d.rounded_rectangle(
            [0, 0, w - 1, h - 1],
            radius=self.s(22),
            fill=(13, 18, 30, 242),
            outline=(34, 197, 94, 240),
            width=max(2, self.s(3)),
        )
        pad = self.s(10)
        col_w = (w - pad * 3) // 2
        img_h = h - self.s(54)

        # Left column: zagonel_oficial_nd.png on dark-blue studio plate for high contrast of white body + water jets
        yy, xx = np.mgrid[0:img_h, 0:col_w].astype(np.float32)
        g_norm = yy / max(1.0, float(img_h))
        pr = np.clip(18.0 + (1.0 - g_norm) * 16.0, 0, 255).astype(np.uint8)
        pg = np.clip(32.0 + (1.0 - g_norm) * 26.0, 0, 255).astype(np.uint8)
        pb = np.clip(58.0 + (1.0 - g_norm) * 38.0, 0, 255).astype(np.uint8)
        pa = np.full((img_h, col_w), 255, dtype=np.uint8)
        p_left = Image.fromarray(np.dstack([pr, pg, pb, pa]), mode="RGBA")
        z_im = self.img_zagonel.copy()
        z_im.thumbnail((int(col_w * 0.96), int(img_h * 0.96)), Image.Resampling.LANCZOS)
        p_left.alpha_composite(z_im, ((col_w - z_im.width) // 2, (img_h - z_im.height) // 2))
        m_col = Image.new("L", (col_w, img_h), 0)
        ImageDraw.Draw(m_col).rounded_rectangle([0, 0, col_w - 1, img_h - 1], radius=self.s(14), fill=255)
        card.paste(p_left, (pad, pad), m_col)

        # Right column: zagonel_nd_uso_real.png
        u_im = self.img_uso_real.copy()
        sw, sh = u_im.size
        t_ratio = col_w / max(1, img_h)
        new_w = int(sh * t_ratio)
        x_off = max(0, (sw - new_w) // 2)
        u_crop = u_im.crop((x_off, 0, min(sw, x_off + new_w), sh)).resize((col_w, img_h), Image.Resampling.LANCZOS)
        card.paste(u_crop, (pad * 2 + col_w, pad), m_col)

        d.text(
            (self.s(16), h - self.s(34)),
            "PRODUTO REAL · 127V (5500W) E 220V (7700W)",
            font=self.f_card_lbl,
            fill=(34, 197, 94, 255),
        )
        return card

    def _make_circular_loupe(
        self,
        src: Image.Image,
        crop_box: tuple[int, int, int, int],
        diameter: int,
        border_col: tuple[int, int, int, int],
    ) -> Image.Image:
        cropped = src.crop(crop_box).resize((diameter, diameter), Image.Resampling.LANCZOS)
        bg = Image.new("RGBA", (diameter, diameter), (245, 248, 252, 255))
        bg.alpha_composite(cropped)
        mask = Image.new("L", (diameter, diameter), 0)
        ImageDraw.Draw(mask).ellipse([1, 1, diameter - 2, diameter - 2], fill=255)
        out = Image.new("RGBA", (diameter, diameter), (0, 0, 0, 0))
        out.paste(bg, (0, 0), mask)
        d = ImageDraw.Draw(out)
        d.ellipse([1, 1, diameter - 2, diameter - 2], outline=border_col, width=max(2, self.s(4)))
        return out

    def _load_flow_clip_frames(self, mp4_path: Path) -> list[Image.Image]:
        vw, vh = self.flow_window_size
        cmd = [
            "ffmpeg",
            "-v",
            "error",
            "-i",
            str(mp4_path),
            "-vf",
            f"scale={vw}:{vh}:flags=lanczos",
            "-f",
            "rawvideo",
            "-pix_fmt",
            "rgb24",
            "-r",
            str(FPS),
            "-",
        ]
        raw = subprocess.check_output(cmd)
        frame_bytes = vw * vh * 3
        n = len(raw) // frame_bytes

        mask = Image.new("L", (vw, vh), 0)
        ImageDraw.Draw(mask).rounded_rectangle([0, 0, vw - 1, vh - 1], radius=self.s(22), fill=255)
        border_overlay = Image.new("RGBA", (vw, vh), (0, 0, 0, 0))
        bd = ImageDraw.Draw(border_overlay)
        bd.rounded_rectangle(
            [0, 0, vw - 1, vh - 1],
            radius=self.s(22),
            outline=(0, 229, 255, 240),
            width=max(2, self.s(3)),
        )
        # Top badge inside the Flow viewport: "VÍDEO · USO NO BANHO"
        bd.rounded_rectangle(
            [self.s(14), self.s(14), self.s(265), self.s(46)],
            radius=self.s(10),
            fill=(9, 12, 20, 215),
            outline=(34, 197, 94, 220),
            width=1,
        )
        bd.text((self.s(24), self.s(21)), "USO REAL · JATO 100%", font=self.f_card_lbl, fill=(34, 197, 94, 255))

        frames: list[Image.Image] = []
        for i in range(n):
            buf = raw[i * frame_bytes : (i + 1) * frame_bytes]
            im = Image.frombytes("RGB", (vw, vh), buf)
            framed = Image.new("RGBA", (vw, vh), (0, 0, 0, 0))
            framed.paste(im, (0, 0), mask)
            framed.alpha_composite(border_overlay)
            frames.append(framed)
        return frames

    def _compute_director_3d_state(self, sc_id: str, sc_prog: float) -> dict[str, Any]:
        """Compute per-frame 3D camera, opacity, exploded view, physical state, and layperson leader-line definitions."""
        if sc_id == "01":
            # Part 1 (0..45%): Real Product Photo hero + scanline laser transition into 3D X-Ray
            # Part 2 (45..100%): Full 3D X-Ray showing watertight bulkhead separating upper water chamber from lower rod
            k = _smoothstep(0.0, 1.0, sc_prog)
            op_k = _smoothstep(0.28, 0.65, sc_prog)
            if sc_prog < 0.45:
                leaders_01 = [
                    ("real_photo_neck", "câmara vedada", (95, -46)),
                    ("real_photo_rod", "haste de calor", (95, 28)),
                ]
            else:
                leaders_01 = [
                    ("camara_vedada", "câmara vedada", (-130, -64)),
                    ("haste_493mm", "haste de calor", (110, 38)),
                ]
            return {
                "cam_pos": _lerp_vec((2.90, 0.35, 2.95), (2.55, 0.50, 2.30), k),
                "cam_tgt": _lerp_vec((0.0, -0.30, 0.05), (0.0, -0.15, 0.02), k),
                "fov": _lerp(36.0, 33.5, k),
                "stage_cx_ratio": 0.54,
                "stage_cy_ratio": 0.35,
                "shell_opacity": _lerp(0.55, 0.16, op_k),
                "explode": _lerp(0.05, 0.25, op_k),
                "water_flow": 0.85,
                "power_level": 0.45,
                "diaphragm_lift": 1.0,
                "leaders": leaders_01,
            }

        if sc_id == "02":
            # Part 1 (0..45%): Macro 3D close-up on the Lower Dry Compartment (Dimmer TRIAC + watertight bulkhead)
            # Part 2 (45..100%): Real shower functioning in the bathroom (Flow video + real installed photo)
            if sc_prog < 0.45:
                k = _smoothstep(0.0, 0.45, sc_prog)
                return {
                    "cam_pos": _lerp_vec((1.75, -0.05, 1.45), (1.50, -0.18, 1.22), k),
                    "cam_tgt": (0.0, -0.22, -0.64),
                    "fov": 28.5,
                    "stage_cx_ratio": 0.62,
                    "stage_cy_ratio": 0.36,
                    "shell_opacity": 0.14,
                    "explode": 0.38,
                    "water_flow": 1.0,
                    "power_level": _lerp(0.45, 0.90, k),
                    "diaphragm_lift": 1.0,
                    "show_real_bath": False,
                    "leaders": [
                        ("regulador_dimmer", "regulador (dimmer)", (-130, -56)),
                        ("compartimento_seco", "compartimento seco", (-130, 52)),
                    ],
                }
            k = _smoothstep(0.45, 1.0, sc_prog)
            return {
                "cam_pos": _lerp_vec((2.20, 0.15, 2.00), (2.05, 0.10, 1.85), k),
                "cam_tgt": (0.0, -0.20, -0.45),
                "fov": 34.0,
                "stage_cx_ratio": 0.25,
                "stage_cy_ratio": 0.36,
                "shell_opacity": 0.15,
                "explode": 0.30,
                "water_flow": 1.0,
                "power_level": 0.88,
                "diaphragm_lift": 1.0,
                "show_real_bath": True,
                "leaders": [
                    ("flow_video_jets", "jato 100% aberto", (85, -52)),
                    ("flow_video_rod", "haste gradual", (-145, -135)),
                ],
            }

        if sc_id == "03":
            # Full-screen clean 3D X-Ray close-up on the Closed Upper Water Tube + Rubber Diaphragm rising against spring
            k = _smoothstep(0.0, 1.0, sc_prog)
            fill_k = _smoothstep(0.0, 0.35, sc_prog)
            lift_k = _smoothstep(0.12, 0.52, sc_prog)
            return {
                "cam_pos": _lerp_vec((2.05, 0.68, 0.55), (1.78, 0.58, -0.08), k),
                "cam_tgt": _lerp_vec((0.0, 0.28, -0.60), (0.0, 0.34, -0.65), k),
                "fov": 29.5,
                "stage_cx_ratio": 0.50,
                "stage_cy_ratio": 0.36,
                "shell_opacity": 0.14,
                "explode": _lerp(0.32, 0.52, fill_k),
                "water_flow": _lerp(0.55, 1.0, fill_k),
                "power_level": 0.0,
                "diaphragm_lift": lift_k,
                "leaders": [
                    ("diafragma", "trava de pressão", (110, -64)),
                    ("tubo_vedado", "tubo de água vedado", (-135, 38)),
                ],
            }

        if sc_id == "04":
            # Part 1 (0..58%): Curved Hot Chamber (700 ml) + Real Resistance Card (resistencia_tse0277_cut.png)
            # Part 2 (58..100%): Close-up on 100% white rod collar + optical loupes comparing white collar vs old Hydra ring
            if sc_prog < 0.58:
                k = _smoothstep(0.0, 0.58, sc_prog)
                return {
                    "cam_pos": _lerp_vec((2.20, 0.45, 2.10), (1.92, 0.28, 2.18), k),
                    "cam_tgt": _lerp_vec((0.0, 0.16, 0.22), (0.0, 0.10, 0.38), k),
                    "fov": 32.0,
                    "stage_cx_ratio": 0.38,
                    "stage_cy_ratio": 0.35,
                    "shell_opacity": 0.14,
                    "explode": 0.36,
                    "water_flow": 1.0,
                    "power_level": _lerp(0.75, 1.0, k),
                    "diaphragm_lift": 1.0,
                    "show_collar_loupe": False,
                    "leaders": [
                        ("espiral_nicr", "mesmo encaixe ND/Turbo", (-105, -66)),
                        ("haste_493mm", "haste 100% branca", (-105, 44)),
                    ],
                }
            k = _smoothstep(0.58, 1.0, sc_prog)
            return {
                "cam_pos": _lerp_vec((1.75, -0.45, 1.65), (1.50, -0.70, 1.40), k),
                "cam_tgt": _lerp_vec((0.0, -0.65, -0.50), (0.0, -0.88, -0.64), k),
                "fov": 29.0,
                "stage_cx_ratio": 0.40,
                "stage_cy_ratio": 0.34,
                "shell_opacity": _lerp(0.18, 0.46, k),
                "explode": _lerp(0.32, 0.10, k),
                "water_flow": 1.0,
                "power_level": 0.90,
                "diaphragm_lift": 1.0,
                "show_collar_loupe": True,
                "leaders": [
                    ("loupe_zagonel_white", "haste 100% branca", (-120, -32)),
                    ("loupe_hydra_ring", "antigo anel colorido", (-120, 32)),
                ],
            }

        # Scene 05: Reassembly of the 3D shell + Real Product Showcase (zagonel_oficial_nd.png + zagonel_nd_uso_real.png) + InspectorRig
        k = _smoothstep(0.0, 0.70, sc_prog)
        return {
            "cam_pos": _lerp_vec((2.65, 0.42, 2.55), (2.85, 0.35, 2.85), k),
            "cam_tgt": _lerp_vec((0.0, -0.18, 0.05), (0.0, -0.25, 0.05), k),
            "fov": 35.0,
            "stage_cx_ratio": 0.34,
            "stage_cy_ratio": 0.34,
            "shell_opacity": _lerp(0.22, 0.65, k),
            "explode": _lerp(0.45, 0.0, k),
            "water_flow": 1.0,
            "power_level": 0.92,
            "diaphragm_lift": 1.0,
            "leaders": [
                ("espiral_nicr", "127V · 5500W", (-110, -72)),
                ("espalhador_78", "220V · 7700W", (-95, -55)),
            ],
        }

    def _draw_top_bar(
        self,
        draw: ImageDraw.ImageDraw,
        scene: dict[str, Any],
        record_audit: bool,
    ) -> None:
        title_txt, badge_txt = scene["top_bar"]
        y0 = self.s(300)
        y1 = self.s(346)

        tb = draw.textbbox((0, 0), title_txt, font=self.f_top)
        tw = tb[2] - tb[0]
        lx0 = self.s(68)
        lx1 = min(self.s(675), lx0 + tw + self.s(44))
        draw.rounded_rectangle(
            [lx0, y0, lx1, y1],
            radius=self.s(22),
            fill=(9, 12, 20, 224),
            outline=(56, 189, 248, 140),
            width=max(1, self.s(2)),
        )
        dot_r = self.s(5)
        dot_cx = lx0 + self.s(18)
        dot_cy = (y0 + y1) // 2
        draw.ellipse([dot_cx - dot_r, dot_cy - dot_r, dot_cx + dot_r, dot_cy + dot_r], fill=(0, 229, 255, 255))
        draw.text((lx0 + self.s(30), y0 + self.s(12)), title_txt, font=self.f_top, fill=(241, 245, 249, 255))

        bb = draw.textbbox((0, 0), badge_txt, font=self.f_badge)
        bw = bb[2] - bb[0]
        rx1 = self.s(875)
        rx0 = max(lx1 + self.s(10), rx1 - bw - self.s(24))
        draw.rounded_rectangle(
            [rx0, y0 + self.s(4), rx1, y1 - self.s(4)],
            radius=self.s(10),
            fill=(15, 23, 42, 215),
            outline=(148, 163, 184, 110),
            width=max(1, self.s(1)),
        )
        draw.text((rx0 + self.s(12), y0 + self.s(12)), badge_txt, font=self.f_badge, fill=(148, 163, 184, 245))

        if record_audit:
            self.record_box_1080(scene["scene"], f"TopBar({title_txt})", lx0, y0, rx1, y1)

    def _draw_leader_lines(
        self,
        draw: ImageDraw.ImageDraw,
        scene_id: str,
        leaders: list[tuple[str, str, tuple[int, int]]],
        anchors_2d: dict[str, tuple[int, int]],
        record_audit: bool,
    ) -> None:
        safe_x0 = self.s(70)
        safe_x1 = self.s(872)
        safe_y0 = self.s(364)
        safe_y1 = self.s(948)

        for idx, (anchor_key, label_txt, (dx_1080, dy_1080)) in enumerate(leaders[:2]):
            ax, ay = anchors_2d.get(anchor_key, (self.W // 2, int(self.H * 0.36)))
            ax = max(safe_x0 + self.s(20), min(safe_x1 - self.s(20), ax))
            ay = max(safe_y0 + self.s(20), min(safe_y1 - self.s(20), ay))

            tb = draw.textbbox((0, 0), label_txt, font=self.f_leader)
            tw = tb[2] - tb[0]
            th = tb[3] - tb[1]

            dx = self.s(dx_1080)
            dy = self.s(dy_1080)
            dir_x = 1 if dx >= 0 else -1

            ex = ax + dx
            ey = max(safe_y0 + th, min(safe_y1 - th, ay + dy))
            shelf_len = self.s(24)

            if dir_x > 0:
                max_hx = safe_x1 - tw - self.s(18)
                hx = min(max_hx, ex + shelf_len)
                ex = min(ex, hx - self.s(10))
                tx0 = hx + self.s(8)
                tx1 = tx0 + tw
            else:
                min_hx = safe_x0 + tw + self.s(18)
                hx = max(min_hx, ex - shelf_len)
                ex = max(ex, hx + self.s(10))
                tx1 = hx - self.s(8)
                tx0 = tx1 - tw

            ty0 = ey - th // 2 - self.s(4)
            ty1 = ty0 + th + self.s(8)

            r_in = max(2, self.s(5))
            r_out = max(4, self.s(10))
            draw.ellipse([ax - r_out, ay - r_out, ax + r_out, ay + r_out], outline=(0, 229, 255, 145), width=max(1, self.s(2)))
            draw.ellipse([ax - r_in, ay - r_in, ax + r_in, ay + r_in], fill=(0, 229, 255, 255))

            draw.line([(ax, ay), (ex, ey), (hx, ey)], fill=(56, 189, 248, 235), width=max(1, self.s(2)))

            pad_x = self.s(8)
            bx0 = max(safe_x0, tx0 - pad_x)
            bx1 = min(safe_x1, tx1 + pad_x)
            by0 = max(safe_y0, ty0 - self.s(2))
            by1 = min(safe_y1, ty1 + self.s(2))
            draw.rounded_rectangle(
                [bx0, by0, bx1, by1],
                radius=self.s(8),
                fill=(9, 11, 18, 212),
                outline=(56, 189, 248, 130),
                width=1,
            )
            draw.text(
                (tx0, ty0),
                label_txt,
                font=self.f_leader,
                fill=(248, 250, 252, 255),
            )

            if record_audit:
                u_x0 = min(ax - r_out, bx0)
                u_y0 = min(ay - r_out, by0)
                u_x1 = max(ax + r_out, bx1)
                u_y1 = max(ay + r_out, by1)
                self.record_box_1080(scene_id, f"LeaderLine_{idx+1}({label_txt})", u_x0, u_y0, u_x1, u_y1)

    def _draw_status_pill(
        self,
        draw: ImageDraw.ImageDraw,
        scene: dict[str, Any],
        record_audit: bool,
    ) -> None:
        dot_hex, pill_txt = scene["status_pill"]
        dot_rgb = tuple(int(dot_hex.lstrip("#")[i : i + 2], 16) for i in (0, 2, 4))

        tb = draw.textbbox((0, 0), pill_txt, font=self.f_pill)
        tw = tb[2] - tb[0]

        safe_left = self.s(68)
        safe_right = self.s(875)
        safe_cx = (safe_left + safe_right) // 2

        pill_w = min(safe_right - safe_left, tw + self.s(54))
        pill_h = self.s(44)
        px0 = max(safe_left, min(safe_right - pill_w, safe_cx - pill_w // 2))
        px1 = min(safe_right, px0 + pill_w)
        py0 = self.s(982)
        py1 = py0 + pill_h

        draw.rounded_rectangle(
            [px0, py0, px1, py1],
            radius=self.s(22),
            fill=(9, 10, 15, 232),
            outline=(*dot_rgb, 165),
            width=max(1, self.s(2)),
        )
        dr = self.s(6)
        dcx = px0 + self.s(20)
        dcy = (py0 + py1) // 2
        draw.ellipse([dcx - dr, dcy - dr, dcx + dr, dcy + dr], fill=(*dot_rgb, 255))
        draw.text((px0 + self.s(34), py0 + self.s(11)), pill_txt, font=self.f_pill, fill=(248, 250, 252, 255))

        if record_audit:
            self.record_box_1080(scene["scene"], f"StatusPill({pill_txt[:22]})", px0, py0, px1, py1)

    def _resolve_action(self, actions_list: list[list[Any] | tuple[float, str]], sc_prog: float) -> str:
        act = str(actions_list[0][1])
        for thresh, name in actions_list:
            if sc_prog >= float(thresh):
                act = str(name)
        return act

    def render_composite_frame(
        self,
        t: float,
        scene: dict[str, Any],
        viseme: str,
        record_audit: bool = False,
    ) -> Image.Image:
        sc_id = scene["scene"]
        sc_elapsed = max(0.0, t - float(scene["start"]))
        sc_prog = min(1.0, sc_elapsed / max(0.01, float(scene["duration"])))

        state_3d = self._compute_director_3d_state(sc_id, sc_prog)
        if sc_id == "04" and state_3d.get("show_collar_loupe", False):
            # Prefer crisp real product photography over 3D when comparing the white rod vs old colored ring
            canvas = Image.new("RGBA", (self.W, self.H), (8, 15, 28, 255))
            anchors_2d = {}
        else:
            canvas, anchors_2d = self.engine_3d.render_3d_stage(t=t, state=state_3d)
        # Register 2D screen anchors for real photographic cards/loupes/video viewports
        anchors_2d["real_photo_neck"] = (self.s(565), self.s(455))
        anchors_2d["real_photo_rod"] = (self.s(516), self.s(735))
        anchors_2d["flow_video_jets"] = (self.s(620), self.s(510))
        anchors_2d["flow_video_rod"] = (self.s(482), self.s(685))
        anchors_2d["loupe_zagonel_white"] = (self.s(275), self.s(680))
        anchors_2d["loupe_hydra_ring"] = (self.s(680), self.s(690))
        draw = ImageDraw.Draw(canvas)

        # SCENE 01: Real Product Hero Photo (zagonel_oficial_nd.png) + Historical Era Badges -> Laser X-Ray Scanner Transition
        if sc_id == "01":
            # In the first 56% of Scene 01, display the real product hero card and wipe it vertically with a cyan X-Ray scanner beam
            hx0, hy0 = self.s(374), self.s(370)
            hw, hh = self.card_zagonel_hero.size
            if sc_prog < 0.56:
                scan_k = _smoothstep(0.32, 0.54, sc_prog)
                split_y = int(round(hh * scan_k))
                if split_y < hh:
                    # Bottom un-scanned portion remains the crisp real photograph of Zagonel ND showering water
                    real_slice = self.card_zagonel_hero.crop((0, split_y, hw, hh))
                    canvas.alpha_composite(real_slice, (hx0, hy0 + split_y))
                if 0.02 < scan_k < 0.98:
                    beam_y = hy0 + split_y
                    draw.line([(hx0 - self.s(12), beam_y), (hx0 + hw + self.s(12), beam_y)], fill=(0, 229, 255, 255), width=max(2, self.s(5)))
                    draw.line([(hx0, beam_y - self.s(6)), (hx0 + hw, beam_y - self.s(6))], fill=(255, 255, 255, 220), width=max(1, self.s(2)))
                if record_audit:
                    self.record_box_1080("01", "Foto_Real_Zagonel_ND_Hero", hx0, hy0, hx0 + hw, hy0 + hh)

            # Historical lineage thumbnails (Thermosystem 2012 & Hydra 2015) stacked in left safe zone above InspectorRig (Y=368..664)
            e1_x, e1_y = self.s(72), self.s(368)
            canvas.alpha_composite(self.card_era1_thumb, (e1_x, e1_y))
            e2_x, e2_y = self.s(72), self.s(520)
            if sc_prog < 0.52:
                canvas.alpha_composite(self.card_era2_thumb, (e2_x, e2_y))
            if record_audit:
                self.record_box_1080(
                    "01",
                    "Miniaturas_Historicas_Thermosystem_Hydra",
                    e1_x,
                    e1_y,
                    e1_x + self.card_era1_thumb.width,
                    e2_y + self.card_era2_thumb.height,
                )

        # SCENE 02: Part 1 (0..45%) Dimmer Explainer Card + 3D Macro of Dry Compartment; Part 2 (45..100%) Real Flow Bath Video + Real Installed Photo
        if sc_id == "02":
            if not state_3d.get("show_real_bath", False):
                dx0, dy0 = self.s(74), self.s(410)
                canvas.alpha_composite(self.card_dimmer_wave, (dx0, dy0))
                if record_audit:
                    self.record_box_1080(
                        "02",
                        "Card_Dimmer_Gradual",
                        dx0,
                        dy0,
                        dx0 + self.card_dimmer_wave.width,
                        dy0 + self.card_dimmer_wave.height,
                    )
            else:
                # 2nd half of Scene 02: Real bathroom shower video (flow_cena02) on right + real installed photo on left!
                f_idx = min(len(self.flow_frames) - 1, int(sc_elapsed * FPS))
                vx0, vy0 = self.flow_window_pos
                vw, vh = self.flow_window_size
                canvas.alpha_composite(self.flow_frames[f_idx], (vx0, vy0))
                ux0, uy0 = self.s(72), self.s(624)
                canvas.alpha_composite(self.card_uso_real_side, (ux0, uy0))
                if record_audit:
                    self.record_box_1080("02", "Flow_Cena02_Uso_Real_Viewport", vx0, vy0, vx0 + vw, vy0 + vh)
                    self.record_box_1080(
                        "02",
                        "Foto_Real_Instalada_Banheiro",
                        ux0,
                        uy0,
                        ux0 + self.card_uso_real_side.width,
                        uy0 + self.card_uso_real_side.height,
                    )

        # SCENE 04: Part 1 (0..58%) Real Longitudinal Resistance Photo Card (ND/Turbo); Part 2 (58..100%) White Collar vs Old Colored Ring Loupes
        if sc_id == "04":
            if not state_3d.get("show_collar_loupe", False):
                rx0, ry0 = self.s(622), self.s(395)
                canvas.alpha_composite(self.card_resistencia_real, (rx0, ry0))
                if record_audit:
                    self.record_box_1080(
                        "04",
                        "Card_Resistencia_Real_ND_Turbo",
                        rx0,
                        ry0,
                        rx0 + self.card_resistencia_real.width,
                        ry0 + self.card_resistencia_real.height,
                    )
            else:
                zx0, zy0 = self.s(72), self.s(395)
                canvas.alpha_composite(self.card_haste_zagonel_real, (zx0, zy0))
                ax0, ay0 = self.s(498), self.s(420)
                canvas.alpha_composite(self.card_haste_hydra_real, (ax0, ay0))
                lx0, ly0 = self.s(310), self.s(720)
                canvas.alpha_composite(self.loupe_white_collar, (lx0, ly0))
                hx0, hy0 = self.s(716), self.s(718)
                canvas.alpha_composite(self.loupe_old_hydra, (hx0, hy0))
                d_rad = self.loupe_old_hydra.width
                draw.line(
                    [(hx0 + self.s(18), hy0 + d_rad - self.s(18)), (hx0 + d_rad - self.s(18), hy0 + self.s(18))],
                    fill=(239, 68, 68, 235),
                    width=max(2, self.s(4)),
                )
                if record_audit:
                    self.record_box_1080(
                        "04",
                        "Comparativo_Real_Haste_Branca_vs_Antiga",
                        zx0,
                        zy0,
                        ax0 + self.card_haste_hydra_real.width,
                        zy0 + self.card_haste_zagonel_real.height,
                    )

        # SCENE 05: Reassembly -> Dual Real Product Showcase Card (zagonel_oficial_nd.png + zagonel_nd_uso_real.png) on center-right
        if sc_id == "05" and sc_prog >= 0.25:
            cx0, cy0 = self.s(338), self.s(384)
            canvas.alpha_composite(self.card_closing_real, (cx0, cy0))
            if record_audit:
                self.record_box_1080(
                    "05",
                    "Card_Fechamento_Produto_Real_Oficial",
                    cx0,
                    cy0,
                    cx0 + self.card_closing_real.width,
                    cy0 + self.card_closing_real.height,
                )

        # Minimalist X-Ray HUD: Top Bar + 1-2 3D->2D Leader Lines + Single Physical Status Pill
        self._draw_top_bar(draw, scene, record_audit)
        self._draw_leader_lines(draw, sc_id, state_3d.get("leaders", []), anchors_2d, record_audit)
        self._draw_status_pill(draw, scene, record_audit)

        # Composite InspectorRig only in opening (Cena 01) and closing (Cena 05), keeping internal 3D scenes 100% clean
        if scene.get("show_rig", False):
            action = self._resolve_action(scene["actions"], sc_prog)
            is_blink = "fechado" if (t % 3.4) < 0.14 else "aberto"
            use_vis = viseme if (action, viseme, is_blink) in self.rig_cache else "X"
            rig_im = self.rig_cache[(action, use_vis, is_blink)]
            bob_y = int(round(math.sin(t * 2.3) * self.s(3)))
            rx = self.s(68)
            ry = self.s(682) + bob_y
            canvas.alpha_composite(rig_im, (rx, ry))
            if record_audit:
                self.record_box_1080(
                    sc_id,
                    f"InspectorRig({action})",
                    rx,
                    self.s(678),
                    rx + rig_im.width,
                    self.s(686) + rig_im.height,
                    kind="rig",
                )

        self._draw_active_caption_beat(canvas, draw, t, scene, record_audit)
        return canvas

    def _draw_active_caption_beat(
        self,
        canvas: Image.Image,
        draw: ImageDraw.ImageDraw,
        t: float,
        scene: dict[str, Any],
        record_audit: bool,
    ) -> None:
        beats = scene.get("caption_beats", [])
        active_beat: dict[str, Any] | None = None
        for b in beats:
            if float(b["start"]) <= t <= float(b["end"]):
                active_beat = b
                break
        if active_beat is None and beats and abs(t - float(scene["start"])) < 0.35:
            active_beat = beats[0]
        if not active_beat:
            return

        words = active_beat["words"]
        active_w_idx = 0
        for idx, w in enumerate(words):
            if t >= float(w["start"]):
                active_w_idx = idx

        tokens = [str(w["text"]) for w in words]
        space_w = draw.textbbox((0, 0), " ", font=self.f_cap)[2]
        tok_widths = [draw.textbbox((0, 0), tok, font=self.f_cap)[2] for tok in tokens]
        total_txt_w = sum(tok_widths) + space_w * max(0, len(tokens) - 1)

        safe_left = self.s(68)
        safe_right = self.s(880)
        safe_cx = (safe_left + safe_right) // 2

        pad_x = self.s(24)
        pad_y = self.s(14)
        pill_w = total_txt_w + pad_x * 2
        pill_h = self.s(78)

        px0 = max(safe_left, min(safe_right - pill_w, safe_cx - pill_w // 2))
        px1 = min(safe_right, px0 + pill_w)
        py0 = self.s(1084)
        py1 = py0 + pill_h

        draw.rounded_rectangle(
            [px0, py0, px1, py1],
            radius=self.s(16),
            fill=(9, 11, 18, 224),
            outline=(56, 189, 248, 120),
            width=max(1, self.s(2)),
        )

        cur_x = px0 + (px1 - px0 - total_txt_w) // 2
        txt_y = py0 + pad_y
        for idx, (tok, tw) in enumerate(zip(tokens, tok_widths)):
            is_act = idx == active_w_idx
            fill_col = (250, 204, 21, 255) if is_act else (255, 255, 255, 255)
            draw.text(
                (cur_x, txt_y),
                tok,
                font=self.f_cap,
                fill=fill_col,
                stroke_width=max(1, self.s(4)),
                stroke_fill=(5, 8, 15, 255),
            )
            if is_act:
                ul_y = py1 - self.s(11)
                draw.line(
                    [(cur_x, ul_y), (cur_x + tw, ul_y)],
                    fill=(250, 204, 21, 255),
                    width=max(2, self.s(4)),
                )
            cur_x += tw + space_w

        if record_audit:
            self.record_box_1080(
                scene["scene"],
                f"CaptionBeat({' '.join(tokens)})",
                px0,
                py0,
                px1,
                py1,
                kind="caption",
            )


def generate_styleframes(
    composer: ZagonelStageComposer,
    timeline: dict[str, Any],
    styleframes_dir: Path,
) -> list[Path]:
    """Generate 1 local styleframe per scene (01..05) at zero AI credits and record layout bounding boxes."""
    styleframes_dir.mkdir(parents=True, exist_ok=True)
    out_paths: list[Path] = []

    sample_progs = {
        "01": 0.25,
        "02": 0.28,
        "03": 0.55,
        "04": 0.35,
        "05": 0.58,
    }

    for sc in timeline["scenes"]:
        sc_id = sc["scene"]
        p = sample_progs.get(sc_id, 0.5)
        t_sample = float(sc["start"]) + float(sc["duration"]) * p
        frame = composer.render_composite_frame(t=t_sample, scene=sc, viseme="A", record_audit=True)
        out_p = styleframes_dir / f"styleframe_cena{sc_id}.png"
        frame.convert("RGB").save(out_p, quality=95)
        out_paths.append(out_p)

        # Also audit second sub-beat of Scene 01 (full 3D), Scene 02 (Flow bath PIP), and Scene 04 (Collar loupe)
        if sc_id == "01":
            t_xray = float(sc["start"]) + float(sc["duration"]) * 0.72
            _ = composer.render_composite_frame(t=t_xray, scene=sc, viseme="A", record_audit=True)
        elif sc_id == "02":
            t_pip = float(sc["start"]) + float(sc["duration"]) * 0.70
            _ = composer.render_composite_frame(t=t_pip, scene=sc, viseme="OU", record_audit=True)
        elif sc_id == "04":
            t_loupe = float(sc["start"]) + float(sc["duration"]) * 0.80
            _ = composer.render_composite_frame(t=t_loupe, scene=sc, viseme="A", record_audit=True)

        # Audit all caption beats of the scene in layout_boxes_1080
        for b in sc.get("caption_beats", []):
            tb = float(b["start"]) + 0.05
            _ = composer.render_composite_frame(t=tb, scene=sc, viseme="EI", record_audit=True)

    return out_paths


def render_video_mp4(
    composer: ZagonelStageComposer,
    timeline: dict[str, Any],
    lipsync: dict[str, Any],
    master_wav: Path,
    out_mp4: Path,
    keyframes_dir: Path,
) -> list[Path]:
    """Stream composed RGB frames to ffmpeg (H.264 + AAC) and save extracted keyframes per scene."""
    viseme_frames: list[str] = lipsync["viseme_frames"]
    n_frames = len(viseme_frames)

    cmd = [
        "ffmpeg",
        "-y",
        "-f",
        "rawvideo",
        "-pix_fmt",
        "rgb24",
        "-s",
        f"{composer.W}x{composer.H}",
        "-r",
        str(FPS),
        "-i",
        "-",
        "-i",
        str(master_wav),
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        "-preset",
        "veryfast",
        "-crf",
        "20" if composer.W >= 1080 else "22",
        "-c:a",
        "aac",
        "-b:a",
        "192k" if composer.W >= 1080 else "160k",
        "-movflags",
        "+faststart",
        "-shortest",
        str(out_mp4),
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    assert proc.stdin is not None

    scenes = timeline["scenes"]
    for f_idx in range(n_frames):
        t = f_idx / FPS
        vis = viseme_frames[f_idx] if f_idx < len(viseme_frames) else "X"
        active_sc = scenes[-1]
        for sc in scenes:
            if float(sc["start"]) <= t <= float(sc["end"]):
                active_sc = sc
                break
        frame = composer.render_composite_frame(t=t, scene=active_sc, viseme=vis, record_audit=False)
        proc.stdin.write(frame.convert("RGB").tobytes())

    proc.stdin.close()
    rc = proc.wait()
    if rc != 0:
        raise RuntimeError(f"ffmpeg falhou ao renderizar {out_mp4} (exit code {rc})")

    keyframes_dir.mkdir(parents=True, exist_ok=True)
    kf_paths: list[Path] = []
    for sc in scenes:
        sc_id = sc["scene"]
        if sc_id == "01":
            p_mid = 0.25
        elif sc_id == "02":
            p_mid = 0.28
        elif sc_id == "04":
            p_mid = 0.35
        else:
            p_mid = 0.55
        t_mid = float(sc["start"]) + float(sc["duration"]) * p_mid
        kf_p = keyframes_dir / f"keyframe_cena{sc_id}.png"
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-ss",
                f"{t_mid:.3f}",
                "-i",
                str(out_mp4),
                "-frames:v",
                "1",
                "-update",
                "1",
                str(kf_p),
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        kf_paths.append(kf_p)
        if sc_id == "02":
            t_uso = float(sc["start"]) + float(sc["duration"]) * 0.72
            kf_uso = keyframes_dir / "keyframe_cena02_uso_real.png"
            subprocess.run(
                [
                    "ffmpeg",
                    "-y",
                    "-ss",
                    f"{t_uso:.3f}",
                    "-i",
                    str(out_mp4),
                    "-frames:v",
                    "1",
                    "-update",
                    "1",
                    str(kf_uso),
                ],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            kf_paths.append(kf_uso)
        elif sc_id == "04":
            t_s2 = float(sc["start"]) + float(sc["duration"]) * 0.80
            kf_p2 = keyframes_dir / "keyframe_cena04_passo2.png"
            subprocess.run(
                [
                    "ffmpeg",
                    "-y",
                    "-ss",
                    f"{t_s2:.3f}",
                    "-i",
                    str(out_mp4),
                    "-frames:v",
                    "1",
                    "-update",
                    "1",
                    str(kf_p2),
                ],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            kf_paths.append(kf_p2)

    return kf_paths


def run_pipeline(
    prod_dir: Path,
    mode: str,
    skip_tts: bool = False,
    tts_engine: str = "auto",
    ml_clips: bool = False,
) -> None:
    build_dir = prod_dir / "_preview_build"
    if not skip_tts or not (build_dir / "timeline.json").exists():
        timeline = asyncio.run(synth_all_scenes(build_dir, prod_dir, tts_engine=tts_engine, ml_clips=ml_clips))
    else:
        timeline = json.loads((build_dir / "timeline.json").read_text(encoding="utf-8"))
        spec_by_id = {s["id"]: s for s in SCENES_SPEC}
        for sc in timeline.get("scenes", []):
            sp = spec_by_id.get(sc.get("scene"))
            if sp:
                sc["top_bar"] = sp["top_bar"]
                sc["status_pill"] = sp["status_pill"]
                sc["title"] = sp["title"]
                sc["motor"] = sp["motor"]
        (build_dir / "timeline.json").write_text(json.dumps(timeline, ensure_ascii=False, indent=2), encoding="utf-8")

    lipsync = json.loads((build_dir / "lipsync.json").read_text(encoding="utf-8"))
    master_wav = build_dir / "master_audio.wav"

    w, h = (540, 960) if mode == "preview" else (1080, 1920)
    if mode == "preview":
        out_mp4 = prod_dir / "preview.mp4"
    elif ml_clips:
        out_mp4 = prod_dir / "video_final_ml_clips_1080p.mp4"
    else:
        out_mp4 = prod_dir / "video_final_1080p.mp4"
    kf_dir = build_dir / ("keyframes" if mode == "preview" else "keyframes_final")

    composer = ZagonelStageComposer(prod_dir=prod_dir, width=w, height=h, ml_clips=ml_clips)
    styleframes = generate_styleframes(composer, timeline, build_dir / "styleframes")
    keyframes = render_video_mp4(composer, timeline, lipsync, master_wav, out_mp4, kf_dir)

    if mode == "preview":
        animatic_p = prod_dir / "animatic_portao2.mp4"
        shutil.copy2(out_mp4, animatic_p)

    max_beat_words = max(
        (b["word_count"] for sc in timeline["scenes"] for b in sc.get("caption_beats", [])),
        default=0,
    )
    audit_report = {
        "mode": mode,
        "ml_clips": ml_clips,
        "resolution": [w, h],
        "fps": FPS,
        "video_path": out_mp4.name,
        "flow_source_clip": composer.flow_source_name,
        "total_duration_s": timeline["total_duration"],
        "req_007_ai_disclosure": not ml_clips,
        "max_caption_words_per_beat": max_beat_words,
        "styleframes": [str(p.relative_to(prod_dir)) for p in styleframes],
        "keyframes": [str(p.relative_to(prod_dir)) for p in keyframes],
        "layout_boxes_1080": composer.layout_boxes_1080,
    }
    (build_dir / "render_audit.json").write_text(json.dumps(audit_report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(
        f"OK [{mode}]: {out_mp4.name} ({w}x{h}, {timeline['total_duration']:.2f}s) | "
        f"styleframes={len(styleframes)} | keyframes={len(keyframes)} | max_beat_words={max_beat_words}"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Render Portao 2 animatic/preview.mp4 or Portao 3 video_final_1080p.mp4.")
    parser.add_argument("--product-dir", type=Path, default=DEFAULT_PROD_DIR)
    parser.add_argument("--mode", choices=["preview", "final"], default="preview")
    parser.add_argument("--skip-tts", action="store_true", help="Reuse existing TTS audio in _preview_build/")
    parser.add_argument("--tts-engine", choices=["auto", "azure", "edge"], default="auto")
    parser.add_argument("--ml-clips", action="store_true", help="Render ML Clips variant without flow_ia clip")
    args = parser.parse_args()
    run_pipeline(
        args.product_dir,
        args.mode,
        skip_tts=args.skip_tts,
        tts_engine=args.tts_engine,
        ml_clips=args.ml_clips,
    )


if __name__ == "__main__":
    main()
