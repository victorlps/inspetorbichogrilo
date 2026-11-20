"""Generate edge-tts narration audio, subtitles, and Rhubarb lip-sync JSON."""

from __future__ import annotations

import asyncio
import json
import subprocess
from pathlib import Path

import edge_tts

REPO_ROOT = Path(__file__).resolve().parents[2]
RHUBARB_BIN = REPO_ROOT / ".venv" / "tools" / "Rhubarb-Lip-Sync-1.14.0-macOS" / "rhubarb"
VOICE = "pt-BR-AntonioNeural"
RATE = "+6%"

SCENES = [
    (
        "01",
        "Em 2012 eu comprei um chuveiro muito bom da Thermosystem. Fiquei chateado quando achei que a marca tinha acabado, "
        "até descobrir que ela passou pela Hydra, foi vendida em 2024 para a Zagonel e o mesmo projeto reapareceu intacto aqui, na Zagonel ND.",
        "Em 2012 eu comprei um chuveiro muito bom da Thermosystem. Fiquei chateado quando achei que a marca tinha acabado, "
        "até descobrir que ela passou pela Hydra, foi vendida em 2024 para a Zagonel e o mesmo projeto reapareceu intacto aqui, na Zagonel êne dê.",
    ),
    (
        "02",
        "São 7700 Watts em 220 Volts com controle eletrônico contínuo: "
        "você gira a haste e o vapor sobe na hora, sem precisar fechar o registro até a água virar um fiapo.",
        "São 7700 Watts em 220 Volts com controle eletrônico contínuo: "
        "você gira a haste e o vapor sobe na hora, sem precisar fechar o registro até a água virar um fiapo.",
    ),
    (
        "03",
        "Nos quase três mil reviews, 95% aprovam. E por que os poucos casos negativos queimam no primeiro mês? "
        "Não é defeito de fábrica: é ligar sem encher de água fria ou em fio fino que não aguenta 7700 Watts.",
        "Nos quase três mil reviews, 95% aprovam. E por que os poucos casos negativos queimam no primeiro mês? "
        "Não é defeito de fábrica: é ligar sem encher de água fria ou em fio fino que não aguenta 7700 Watts.",
    ),
    (
        "04",
        "Projeto testado há mais de dez anos e resistência fácil de achar. "
        "Quer conferir a Zagonel ND? O link tá na bio, ou comenta ZAGONEL que eu te mando.",
        "Projeto testado há mais de dez anos e resistência fácil de achar. "
        "Quer conferir a Zagonel êne dê? O link tá na bio, ou comenta ZAGONEL que eu te mando.",
    ),
]


async def synth_scene(idx: str, text: str, out_dir: Path) -> tuple[Path, list[dict]]:
    """Synthesize MP3 and collect word-level boundary timestamps."""
    mp3_path = out_dir / f"audio_{idx}.mp3"
    comm = edge_tts.Communicate(text, VOICE, rate=RATE, boundary="WordBoundary")
    words: list[dict] = []
    with open(mp3_path, "wb") as f:
        async for chunk in comm.stream():
            if chunk["type"] == "audio":
                f.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                words.append(
                    {
                        "text": chunk["text"],
                        "start": chunk["offset"] / 10_000_000.0,
                        "duration": chunk["duration"] / 10_000_000.0,
                    }
                )
    return mp3_path, words


def ffprobe_duration(path: Path) -> float:
    """Return media duration in seconds using ffprobe."""
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


async def build_audio_and_lipsync(out_dir: Path) -> None:
    """Generate all scene audios, combined WAV, and Rhubarb lip-sync JSON."""
    out_dir.mkdir(parents=True, exist_ok=True)
    concat_list = out_dir / "concat.txt"
    timeline: list[dict] = []
    t_cursor = 0.0

    with open(concat_list, "w") as cl:
        for idx, caption_text, tts_text in SCENES:
            mp3_path, words = await synth_scene(idx, tts_text, out_dir)
            dur = ffprobe_duration(mp3_path)
            cl.write(f"file '{mp3_path.resolve()}'\n")
            for w in words:
                w["start"] += t_cursor
            timeline.append(
                {
                    "scene": idx,
                    "start": round(t_cursor, 3),
                    "end": round(t_cursor + dur, 3),
                    "duration": round(dur, 3),
                    "text": caption_text,
                    "words": words,
                }
            )
            t_cursor += dur

    full_wav = out_dir / "narration.wav"
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat_list),
            "-ar",
            "16000",
            "-ac",
            "1",
            str(full_wav),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    lipsync_json = out_dir / "lipsync.json"
    subprocess.run(
        [
            str(RHUBARB_BIN),
            "--recognizer",
            "phonetic",
            "-f",
            "json",
            "-o",
            str(lipsync_json),
            str(full_wav),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    meta_path = out_dir / "timeline.json"
    meta_path.write_text(json.dumps({"total_duration": round(t_cursor, 3), "scenes": timeline}, ensure_ascii=False, indent=2))
    print(f"Audio + Rhubarb done: {t_cursor:.2f}s | cues={len(json.loads(lipsync_json.read_text())['mouthCues'])}")


if __name__ == "__main__":
    target = REPO_ROOT / "produtos" / "ducha-eletronica-zagonel-nd-7700w" / "_preview_build"
    asyncio.run(build_audio_and_lipsync(target))
