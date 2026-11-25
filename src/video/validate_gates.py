"""Deterministic Portao 1, 2, and 3 validators for product curation, storyboard/animatic, and final video artifacts (ADR 0008)."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

LOCAL_LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
FORBIDDEN_LEAK_RE = re.compile(r"/Users/|BEGIN PRIVATE KEY|AZURE_SPEECH_KEY|OPENAI_API_KEY|GEMINI_API_KEY|\.env\b")
TECH_TOKEN_RE = re.compile(
    r"\b\d+(?:[.,]\d+)?\s*(?:mm²|kWh|kW|MHz|GHz|W|V|A|Hz|mAh|L|kg|g|cm|mm|m|%)"
    r"|\b[A-Z]{2,}[A-Z0-9_-]*\b"
    r"|\b[A-Z][a-z]+(?:[A-Z][a-z]+|system|tech)\b"
)
PRICE_SPEECH_RE = re.compile(r"R\$\s*\d+|\b\d+\s*reais\b", re.IGNORECASE)


def _extract_local_paths(md_text: str) -> list[str]:
    paths: list[str] = []
    for raw_target in LOCAL_LINK_RE.findall(md_text):
        target = raw_target.strip().split()[0]
        if target.startswith(("http://", "https://", "#", "mailto:", "conversation://", "file://")):
            continue
        paths.append(target)
    return paths


def _check_privacy(md_text: str, label: str, errors: list[str]) -> None:
    for m in FORBIDDEN_LEAK_RE.finditer(md_text):
        errors.append(f"[{label}] Termo ou caminho sensível exposto ({m.group(0)}) — viola REQ-011.")


def validate_portao_1(prod_dir: Path) -> tuple[bool, list[str], dict[str, object]]:
    """Run deterministic checks for Portao 1 (ficha.md)."""
    ficha_path = prod_dir / "ficha.md"
    errors: list[str] = []
    stats: dict[str, object] = {}

    if not ficha_path.exists():
        return False, [f"[Portão 1] Arquivo ausente: {ficha_path}"], stats

    text = ficha_path.read_text(encoding="utf-8")
    _check_privacy(text, "Portão 1", errors)

    # 1. Check 5+1 mandatory sections
    required_headings = ["## 1.", "## 2.", "## 3.", "## 4.", "## 5.", "## 6."]
    missing_h = [h for h in required_headings if h not in text]
    if missing_h:
        errors.append(f"[Portão 1] Seções obrigatórias ausentes em ficha.md: {', '.join(missing_h)}")

    # 2. Check all linked local assets exist on disk
    local_links = _extract_local_paths(text)
    missing_files = [rel for rel in local_links if not (prod_dir / rel).exists() or (prod_dir / rel).stat().st_size == 0]
    if missing_files:
        errors.append(f"[Portão 1] Ativos referenciados ausentes ou vazios: {', '.join(missing_files)}")
    stats["local_assets"] = len(local_links)

    # Check internal mechanism visual evidence when internal functionality is discussed (REQ-001)
    if re.search(r"câmara interna|peça aberta|vista explodida|mecanismo interno|resistência de encaixe", text, re.IGNORECASE):
        if not any(re.search(r"(camara|intern|explod|encaixe|manual|diagrama)", p, re.IGNORECASE) for p in local_links):
            errors.append("[Portão 1] Ângulo aborda funcionamento interno, mas não há foto/diagrama interno vinculado.")

    # 3. Extract 5★..1★ percentages and validate total ≈ 100%
    star_pcts: dict[int, float] = {}
    for star in (5, 4, 3, 2, 1):
        m1 = re.search(rf"(\d+(?:[.,]\d+)?)\s*%\s*\(\s*{star}★\s*\)", text)
        m2 = re.search(rf"{star}★\s*\(\s*(\d+(?:[.,]\d+)?)\s*%\s*\)", text)
        m = m1 or m2
        if m:
            star_pcts[star] = float(m.group(1).replace(",", "."))
        else:
            errors.append(f"[Portão 1] Percentual para {star}★ não encontrado no formato padrão em ficha.md.")

    if len(star_pcts) == 5:
        total_pct = round(sum(star_pcts.values()), 2)
        stats["star_total_pct"] = total_pct
        if not (99.5 <= total_pct <= 100.5):
            errors.append(f"[Portão 1] Soma das estrelas ({total_pct:.2f}%) foge de 100% (±0.5%).")

    return len(errors) == 0, errors, stats


def _split_sentences(speech: str) -> list[str]:
    clean = re.sub(r"[*_\"“”]", "", speech).strip()
    # Split on punctuation followed by whitespace or end (preserving decimal numbers like 1.2)
    parts = re.split(r"[.!?]+(?!\d)(?=\s|$)", clean)
    return [p.strip() for p in parts if p.strip()]


def _extract_table_rows(section_text: str) -> list[list[str]]:
    rows: list[list[str]] = []
    for raw in section_text.splitlines():
        line = raw.strip()
        if not line.startswith("|") or not line.endswith("|"):
            continue
        cells = [c.strip() for c in line[1:-1].split("|")]
        if all(re.fullmatch(r":?-+:?", c or "-") for c in cells):
            continue
        rows.append(cells)
    return rows


def _parse_time_range(cell: str) -> tuple[int, int] | None:
    m = re.search(r"(\d+)\s*s\s*[–-]\s*(\d+)\s*s", cell)
    if not m:
        return None
    return int(m.group(1)), int(m.group(2))


def validate_portao_2(prod_dir: Path) -> tuple[bool, list[str], dict[str, object]]:
    """Run deterministic checks for Portao 2 (roteiro.md)."""
    roteiro_path = prod_dir / "roteiro.md"
    errors: list[str] = []
    warnings: list[str] = []
    stats: dict[str, object] = {}

    if not roteiro_path.exists():
        return False, [f"[Portão 2] Arquivo ausente: {roteiro_path}"], stats

    text = roteiro_path.read_text(encoding="utf-8")
    _check_privacy(text, "Portão 2", errors)

    # Check local media references exist
    local_links = _extract_local_paths(text)
    missing_files = [rel for rel in local_links if not (prod_dir / rel).exists() or (prod_dir / rel).stat().st_size == 0]
    if missing_files:
        errors.append(f"[Portão 2] Referências de mídia ausentes ou vazias: {', '.join(missing_files)}")
    stats["local_assets"] = len(local_links)

    # Split major sections
    sec1_m = re.search(r"##\s*1\..*?(?=##\s*2\.|\Z)", text, re.DOTALL)
    sec2_m = re.search(r"##\s*2\..*?(?=##\s*3\.|\Z)", text, re.DOTALL)
    sec3_m = re.search(r"##\s*3\..*", text, re.DOTALL)

    if not (sec1_m and sec2_m and sec3_m):
        errors.append("[Portão 2] Seções obrigatórias (1. Mapa de Cenas, 2. Dicionário Fonético, 3. Orçamento Flow) ausentes.")
        return False, errors, stats

    # Check Section 4 (Notas de Fidelidade do @Curador — ADR 0008)
    sec4_m = re.search(r"##\s*4\..*fidelidade.*", text, re.IGNORECASE | re.DOTALL)
    stats["has_curador_fidelity_notes"] = bool(sec4_m)
    if not sec4_m:
        errors.append("[Portão 2] Seção '## 4. Notas de Fidelidade Física e Factual (@Curador)' ausente em roteiro.md (ADR 0008).")

    # 1. Validate scene table: continuity, visual engines, speech length <= 15 words, no variable price
    scene_rows = _extract_table_rows(sec1_m.group(0))[1:]  # skip header
    if not scene_rows:
        errors.append("[Portão 2] Tabela de cenas vazia na seção 1.")

    prev_end: int | None = None
    total_words = 0
    max_sentence_words = 0
    long_sentences: list[str] = []
    all_speeches: list[str] = []
    has_flow_ia = False

    valid_engines = ("rig 2.5d", "flow_ia", "determinístico", "flow omni")
    for idx, row in enumerate(scene_rows, start=1):
        if len(row) < 6:
            errors.append(f"[Portão 2] Linha de cena {idx} com colunas insuficientes ({len(row)} < 6).")
            continue
        time_cell, engine_cell, speech_cell = row[1], row[2], row[5]
        tr = _parse_time_range(time_cell)
        if not tr:
            errors.append(f"[Portão 2] Tempo inválido na cena {idx}: {time_cell}")
        else:
            start_s, end_s = tr
            if end_s <= start_s:
                errors.append(f"[Portão 2] Intervalo de tempo inválido na cena {idx}: {start_s}s–{end_s}s")
            if prev_end is None and start_s != 0:
                errors.append(f"[Portão 2] Primeira cena deveria iniciar em 00s (iniciou em {start_s}s).")
            if prev_end is not None and start_s != prev_end:
                errors.append(f"[Portão 2] Lacuna ou sobreposição temporal antes da cena {idx}: {prev_end}s -> {start_s}s.")
            prev_end = end_s

        eng_low = engine_cell.lower()
        if not any(v in eng_low for v in valid_engines):
            errors.append(f"[Portão 2] Motor visual ausente ou inválido na cena {idx}: {engine_cell}")
        if "flow_ia" in eng_low or "flow omni" in eng_low:
            has_flow_ia = True

        all_speeches.append(speech_cell)
        if PRICE_SPEECH_RE.search(speech_cell):
            errors.append(f"[Portão 2] Preço variável detectado na fala da cena {idx} (incompatível com ML Clips / calibração).")

        for sent in _split_sentences(speech_cell):
            wc = len(re.findall(r"[0-9A-Za-zÀ-ÿ²%]+(?:-[0-9A-Za-zÀ-ÿ]+)?", sent))
            total_words += wc
            if wc > max_sentence_words:
                max_sentence_words = wc
            if wc > 15:
                long_sentences.append(f"Cena {idx} ({wc} pal): '{sent}'")

    if long_sentences:
        warnings.append(f"[Portão 2] Alerta de ritmo (>15 palavras escritas): {'; '.join(long_sentences)}")

    stats["scenes"] = len(scene_rows)
    stats["timeline_s"] = prev_end or 0
    stats["total_words"] = total_words
    stats["est_speech_s"] = round(total_words / 2.6, 1)
    stats["max_sentence_words"] = max_sentence_words

    # 2. Check Phonetic Dictionary covers every technical term/acronym/unit detected in speech
    dict_rows = _extract_table_rows(sec2_m.group(0))[1:]
    dict_terms: dict[str, str] = {}
    for row in dict_rows:
        if len(row) >= 2:
            term = re.sub(r"[`*_]", "", row[0]).strip()
            phon = re.sub(r"[`*_]", "", row[1]).strip()
            if term and phon:
                dict_terms[term] = phon

    speech_blob = " ".join(all_speeches)
    detected_tech = set(m.group(0).strip() for m in TECH_TOKEN_RE.finditer(speech_blob))
    missing_phon: list[str] = []
    for tok in sorted(detected_tech):
        if tok in dict_terms:
            continue
        # Match unit/code part cleanly when spaced differently (e.g., "6 mm²" / "40 A")
        if any(tok == dt or tok in dt.split() for dt in dict_terms):
            continue
        missing_phon.append(tok)

    if missing_phon:
        errors.append(f"[Portão 2] Termos técnicos/siglas na fala ausentes no Dicionário Fonético: {', '.join(missing_phon)}")

    # Compute expanded spoken-word count and max spoken sentence length using phonetic dictionary
    spoken_total_words = 0
    max_spoken_sentence_words = 0
    long_spoken_sentences: list[str] = []
    sorted_terms = sorted(dict_terms.items(), key=lambda kv: len(kv[0]), reverse=True)
    for sp_cell in all_speeches:
        for sent in _split_sentences(sp_cell):
            expanded = sent
            for term, phon in sorted_terms:
                expanded = re.sub(rf"\b{re.escape(term)}(?![0-9A-Za-zÀ-ÿ])", phon, expanded)
            swc = len(re.findall(r"[0-9A-Za-zÀ-ÿ²%]+(?:-[0-9A-Za-zÀ-ÿ]+)?", expanded))
            spoken_total_words += swc
            if swc > max_spoken_sentence_words:
                max_spoken_sentence_words = swc
            if swc > 15:
                long_spoken_sentences.append(f"({swc} faladas): '{expanded}'")
    if long_spoken_sentences:
        warnings.append(f"[Portão 2] Alerta de ritmo (>15 palavras faladas): {'; '.join(long_spoken_sentences)}")
    if warnings:
        stats["warnings"] = warnings

    stats["spoken_words"] = spoken_total_words
    stats["est_spoken_s"] = round(spoken_total_words / 2.6, 1)
    stats["max_spoken_sentence_words"] = max_spoken_sentence_words
    stats["phonetic_entries"] = len(dict_terms)
    stats["tech_tokens_checked"] = sorted(detected_tech)

    # 3. Validate Google Flow Credit Budget & REQ-007 AI disclosure trigger
    budget_rows = _extract_table_rows(sec3_m.group(0))[1:]
    if not budget_rows:
        errors.append("[Portão 2] Tabela de orçamento de créditos do Google Flow vazia na seção 3.")
    else:
        summed_credits = 0
        stated_total: int | None = None
        for row in budget_rows:
            if len(row) < 4:
                continue
            label = re.sub(r"[`*_]", "", row[0]).strip().lower()
            m_cr = re.search(r"(\d+)[\s`*_]*créditos?", row[3], re.IGNORECASE)
            if "total" in label:
                if m_cr:
                    stated_total = int(m_cr.group(1))
            elif m_cr:
                summed_credits += int(m_cr.group(1))
        if stated_total is None:
            errors.append("[Portão 2] Linha 'Total' de créditos Flow não encontrada na tabela de orçamento.")
        elif stated_total != summed_credits:
            errors.append(f"[Portão 2] Soma do orçamento Flow divergente: cenas={summed_credits}, total={stated_total}.")
        if has_flow_ia and stated_total == 0:
            errors.append("[Portão 2] Há cena flow_ia no roteiro, mas o orçamento previsto em 360p está zerado.")
        stats["flow_credits_budget"] = stated_total

    if has_flow_ia and not re.search(r"Aviso determinístico.*REQ-007.*:\*\*[\s*]*SIM", text, re.IGNORECASE):
        errors.append("[Portão 2] Há cena flow_ia, mas o disparo automático REQ-007 não está marcado como SIM no cabeçalho.")

    return len(errors) == 0, errors, stats


def _ffprobe_streams(mp4_path: Path) -> dict[str, object]:
    out = subprocess.check_output(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration,size:stream=codec_type,codec_name,width,height",
            "-of",
            "json",
            str(mp4_path),
        ],
        text=True,
    )
    return json.loads(out)


def _validate_render_common(
    prod_dir: Path,
    gate_num: int,
    expected_video_name: str,
    expected_res: tuple[int, int],
) -> tuple[bool, list[str], dict[str, object]]:
    """Run deterministic checks for Portao 3 (preview.mp4) or Portao 4 (video_final_1080p.mp4)."""
    label = f"Portão {gate_num}"
    errors: list[str] = []
    warnings: list[str] = []
    stats: dict[str, object] = {}

    build_dir = prod_dir / "_preview_build"
    timeline_path = build_dir / "timeline.json"
    audit_path = build_dir / "render_audit.json"
    video_path = prod_dir / expected_video_name

    for req_p in (timeline_path, audit_path, video_path):
        if not req_p.exists() or req_p.stat().st_size == 0:
            errors.append(f"[{label}] Arquivo obrigatório ausente ou vazio: {req_p.name}")

    if errors:
        return False, errors, stats

    timeline = json.loads(timeline_path.read_text(encoding="utf-8"))
    audit = json.loads(audit_path.read_text(encoding="utf-8"))

    # (a) Validate TTS audio files (> 1024 bytes) & WordBoundary events for all scenes
    scenes = timeline.get("scenes", [])
    if not scenes:
        errors.append(f"[{label}] Nenhuma cena encontrada em timeline.json.")

    total_words = 0
    max_beat_words = 0
    for sc in scenes:
        sc_id = sc.get("scene", "?")
        a_file = build_dir / str(sc.get("audio_file", f"audio_{sc_id}.mp3"))
        if not a_file.exists() or a_file.stat().st_size < 1024:
            errors.append(f"[{label}] Áudio TTS ausente ou truncado (<1024 bytes) na Cena {sc_id}: {a_file.name}")
        raw_w = sc.get("raw_words", [])
        if not raw_w:
            errors.append(f"[{label}] Eventos WordBoundary ausentes na Cena {sc_id}.")
        total_words += len(raw_w)
        for beat in sc.get("caption_beats", []):
            wc = int(beat.get("word_count", len(beat.get("words", []))))
            if wc > max_beat_words:
                max_beat_words = wc
            if wc < 1 or wc > 3:
                errors.append(f"[{label}] Batida de legenda fora da regra de 1–3 palavras (Cena {sc_id}: {wc} palavras).")

    stats["scenes_checked"] = len(scenes)
    stats["tts_word_events"] = total_words
    stats["max_caption_words_per_beat"] = max_beat_words

    # (b) Validate 9:16 Safe Zone coordinates in canonical 1080x1920 space:
    # Hard limit: X = 48..887 px, Y = 288..1247 px; Warning if X < 65 px; Captions in Y = 1040..1220 px
    boxes = audit.get("layout_boxes_1080", [])
    if not boxes:
        errors.append(f"[{label}] Lista layout_boxes_1080 vazia em render_audit.json.")

    for b in boxes:
        sc_id = b.get("scene", "?")
        b_label = b.get("label", "elem")
        kind = b.get("kind", "element")
        x0, y0, x1, y1 = [int(v) for v in b.get("bbox_1080", [0, 0, 0, 0])]
        if x0 < 48 or x1 > 887 or y0 < 288 or y1 > 1247:
            errors.append(
                f"[{label}] Elemento '{b_label}' (Cena {sc_id}) invade área proibida das redes: "
                f"bbox_1080=({x0},{y0},{x1},{y1}) fora de X=48..887, Y=288..1247."
            )
        elif x0 < 65:
            warnings.append(
                f"[{label}] Alerta: '{b_label}' (Cena {sc_id}) com X={x0}px (< 65px folga conservadora Reels)."
            )
        if kind == "caption" and (y0 < 1040 or y1 > 1220):
            errors.append(
                f"[{label}] Legenda '{b_label}' (Cena {sc_id}) fora da faixa Y=1040..1220 px: Y={y0}..{y1}."
            )

    stats["boxes_audited"] = len(boxes)

    # Optional visual word-budget check for web_motion_engine episodes (biblia.md §3: <= 14 visible non-caption words)
    screen_words_map = audit.get("scene_screen_words", {})
    if isinstance(screen_words_map, dict) and screen_words_map:
        max_screen_words = max(int(v) for v in screen_words_map.values())
        stats["max_screen_words_non_caption"] = max_screen_words
        for sc_k, w_cnt in screen_words_map.items():
            if int(w_cnt) > 14:
                errors.append(
                    f"[{label}] Excesso de texto fixo na tela (Cena {sc_k}: {w_cnt} palavras > 14 de biblia.md §3 — priorize animação visual com rótulos espaciais curtos)."
                )

    if warnings:
        stats["warnings"] = warnings

    # (c) Validate styleframes & keyframes exist on disk
    sf_list = audit.get("styleframes", [])
    kf_list = audit.get("keyframes", [])
    if len(sf_list) < len(scenes):
        errors.append(f"[{label}] Styleframes insuficientes ({len(sf_list)} < {len(scenes)} cenas).")
    for rel in sf_list + kf_list:
        p = prod_dir / rel
        if not p.exists() or p.stat().st_size == 0:
            errors.append(f"[{label}] Quadro visual ausente ou vazio: {rel}")
    stats["styleframes"] = len(sf_list)
    stats["keyframes"] = len(kf_list)

    # (d) Validate rendered MP4 via ffprobe (resolution, H.264 + AAC streams, duration consistency)
    probe = _ffprobe_streams(video_path)
    streams = probe.get("streams", [])
    fmt = probe.get("format", {})
    v_stream = next((s for s in streams if s.get("codec_type") == "video"), None)
    a_stream = next((s for s in streams if s.get("codec_type") == "audio"), None)

    if not v_stream:
        errors.append(f"[{label}] Stream de vídeo ausente em {video_path.name}.")
    else:
        vw, vh = int(v_stream.get("width", 0)), int(v_stream.get("height", 0))
        stats["video_resolution"] = f"{vw}x{vh}"
        stats["video_codec"] = v_stream.get("codec_name")
        if (vw, vh) != expected_res:
            errors.append(f"[{label}] Resolução de {video_path.name} incorreta: {vw}x{vh} (esperado {expected_res[0]}x{expected_res[1]}).")

    if not a_stream:
        errors.append(f"[{label}] Stream de áudio ausente em {video_path.name}.")
    else:
        stats["audio_codec"] = a_stream.get("codec_name")

    vid_dur = round(float(fmt.get("duration", 0.0)), 2)
    tl_dur = round(float(timeline.get("total_duration", 0.0)), 2)
    stats["video_duration_s"] = vid_dur
    if abs(vid_dur - tl_dur) > 0.6:
        errors.append(f"[{label}] Duração do vídeo ({vid_dur}s) diverge da timeline ({tl_dur}s).")

    # (e) Validate REQ-007 AI disclosure trigger when roteiro.md contains flow_ia
    roteiro_path = prod_dir / "roteiro.md"
    if roteiro_path.exists():
        r_text = roteiro_path.read_text(encoding="utf-8")
        if "flow_ia" in r_text.lower() and not timeline.get("req_007_ai_disclosure", False):
            errors.append(f"[{label}] Roteiro usa flow_ia, mas flag req_007_ai_disclosure não está ativa em timeline.json.")

    return len(errors) == 0, errors, stats


AFFILIATE_URL_PREFIXES = (
    "https://meli.la/",
    "https://mercadolivre.com/sec/",
    "https://www.mercadolivre.com.br/sec/",
    "https://amzn.to/",
)


def _is_monetized_affiliate_url(url: str) -> bool:
    u = url.strip()
    return u.startswith(AFFILIATE_URL_PREFIXES) or "tag=" in u or "matt_tool=" in u


def _extract_blockquote_clean(section_text: str) -> str:
    lines: list[str] = []
    for line in section_text.splitlines():
        if line.strip().startswith(">"):
            clean = re.sub(r"^>\s?", "", line.strip())
            clean = clean.replace("**", "").replace("`", "")
            lines.append(clean)
    return "\n".join(lines).strip()


def validate_portao_3(
    prod_dir: Path,
    require_vitrine_entry: bool = False,
) -> tuple[bool, list[str], dict[str, object]]:
    """Run deterministic checks for Portao 3 (video_final_1080p.mp4 + pacote.md platform syntax + catalogo.json affiliate readiness)."""
    ok, errors, stats = _validate_render_common(
        prod_dir,
        gate_num=3,
        expected_video_name="video_final_1080p.mp4",
        expected_res=(1080, 1920),
    )
    pacote_path = prod_dir / "pacote.md"
    if not pacote_path.exists() or pacote_path.stat().st_size == 0:
        errors.append("[Portão 3] Arquivo pacote.md ausente ou vazio.")
        return False, errors, stats

    p_text = pacote_path.read_text(encoding="utf-8")
    _check_privacy(p_text, "Portão 3", errors)
    if not re.search(r"REQ-007|inteligência artificial|gerad[oa] por IA", p_text, re.IGNORECASE):
        errors.append("[Portão 3] Aviso determinístico de conteúdo de IA (REQ-007) ausente em pacote.md.")

    unresolved_ph = re.findall(r"<LINK_[^>]+>", p_text)
    if unresolved_ph:
        errors.append(f"[Portão 3] Placeholders de link pendentes em pacote.md: {', '.join(sorted(set(unresolved_ph)))}")

    if re.search(r"substituir os placeholders|gerar link curto `/sec/", p_text, re.IGNORECASE):
        errors.append("[Portão 3] Instrução residual de rascunho ('substituir os placeholders' / 'gerar link curto') presente em pacote.md.")

    code_m = re.search(r"\b(IBG-\d{3,})\b", p_text)
    if not code_m:
        errors.append("[Portão 3] Código curto da vitrine (IBG-XXX) ausente em pacote.md.")
        vitrine_code = ""
    else:
        vitrine_code = code_m.group(1)
        stats["vitrine_code"] = vitrine_code

    # Validate platform-specific caption/title constraints so zero post-approval rework happens during upload
    ig_m = re.search(r"### 2\.1 Instagram Reels\s+(.*?)(?=\n### |\n---)", p_text, re.S)
    tt_m = re.search(r"### 2\.2 TikTok\s+(.*?)(?=\n### |\n---)", p_text, re.S)
    yt_m = re.search(r"### 2\.3 YouTube Shorts\s+(.*?)(?=\n### |\n---)", p_text, re.S)

    ig_cap = _extract_blockquote_clean(ig_m.group(1)) if ig_m else ""
    tt_cap = _extract_blockquote_clean(tt_m.group(1)) if tt_m else ""
    if not ig_cap or len(ig_cap) > 2200:
        errors.append(f"[Portão 3] Legenda do Instagram Reels ausente ou acima de 2200 caracteres ({len(ig_cap)} chars).")
    elif vitrine_code and vitrine_code not in ig_cap:
        errors.append(f"[Portão 3] Legenda do Instagram Reels precisa citar o código {vitrine_code}.")

    if not tt_cap or len(tt_cap) > 2200:
        errors.append(f"[Portão 3] Legenda do TikTok ausente ou acima de 2200 caracteres ({len(tt_cap)} chars).")
    elif vitrine_code and vitrine_code not in tt_cap:
        errors.append(f"[Portão 3] Legenda do TikTok precisa citar o código {vitrine_code}.")

    if not yt_m:
        errors.append("[Portão 3] Seção '### 2.3 YouTube Shorts' ausente em pacote.md.")
    else:
        yt_block = yt_m.group(1)
        yt_title_m = re.search(r"- \*\*Título sugerido[^\n]*\n\s*`([^`]+)`", yt_block)
        yt_title = yt_title_m.group(1).strip() if yt_title_m else ""
        yt_desc = _extract_blockquote_clean(yt_block)
        if not yt_title or len(yt_title) > 100:
            errors.append(f"[Portão 3] Título do YouTube Shorts ausente ou acima de 100 caracteres ({len(yt_title)} chars).")
        elif "#shorts" not in yt_title.lower():
            errors.append("[Portão 3] Título do YouTube Shorts precisa incluir #shorts.")
        if not yt_desc or len(yt_desc) > 5000:
            errors.append(f"[Portão 3] Descrição do YouTube Shorts ausente ou acima de 5000 caracteres ({len(yt_desc)} chars).")
        if "<" in yt_title or ">" in yt_title or "<" in yt_desc or ">" in yt_desc:
            errors.append(
                "[Portão 3] Título ou descrição do YouTube Shorts contém '<' ou '>' literais (rejeitados pela API e pelo YouTube Studio)."
            )

    # Validate vitrine/catalogo.json affiliate links when entry exists (or when require_vitrine_entry=True)
    catalogo_path = prod_dir.resolve().parents[1] / "vitrine" / "catalogo.json"
    if catalogo_path.exists() and vitrine_code:
        cat_data = json.loads(catalogo_path.read_text(encoding="utf-8"))
        card = next((p for p in cat_data.get("produtos", []) if p.get("codigo") == vitrine_code), None)
        if card is None:
            if require_vitrine_entry:
                errors.append(f"[Portão 3] Card {vitrine_code} ausente em vitrine/catalogo.json.")
        else:
            variacoes = card.get("variacoes", [])
            stats["vitrine_variations"] = len(variacoes)
            if not variacoes:
                errors.append(f"[Portão 3] Card {vitrine_code} em vitrine/catalogo.json está sem variações.")
            unmonetized = [
                f"{v.get('rotulo', '?')} -> {v.get('url', '')}"
                for v in variacoes
                if not _is_monetized_affiliate_url(str(v.get("url", "")))
            ]
            stats["vitrine_monetized_pct"] = round(100.0 * (len(variacoes) - len(unmonetized)) / max(len(variacoes), 1), 1)
            if unmonetized:
                errors.append(
                    f"[Portão 3] Card {vitrine_code} em vitrine/catalogo.json possui URLs sem link curto/tag de afiliado: "
                    + "; ".join(unmonetized)
                )

    stats["pacote_md_bytes"] = pacote_path.stat().st_size
    return len(errors) == 0, errors, stats


def validate_portao_4(prod_dir: Path) -> tuple[bool, list[str], dict[str, object]]:
    """Backward-compatible alias for Portao 3 final package validator."""
    return validate_portao_3(prod_dir)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate product Portao 1, 2, 3, and/or 4 artifacts deterministically.")
    parser.add_argument("product_dir", type=Path, help="Path to produtos/<slug>")
    parser.add_argument("--portao", type=int, action="append", choices=[1, 2, 3, 4], help="Gate(s) to validate (default: 1 and 2)")
    args = parser.parse_args()

    gates = args.portao or [1, 2]
    validators = {
        1: validate_portao_1,
        2: validate_portao_2,
        3: validate_portao_3,
        4: validate_portao_4,
    }
    all_ok = True
    for g in gates:
        ok, errs, stats = validators[g](args.product_dir)
        status = "APROVADO" if ok else "FALHOU"
        print(f"=== PORTÃO {g}: {status} ===")
        print("Resumo:", stats)
        for err in errs:
            print("  ERRO:", err)
        if not ok:
            all_ok = False
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
