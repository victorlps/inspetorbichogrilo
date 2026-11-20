"""Deterministic Portao 1 and Portao 2 validators for product curation and script artifacts."""

from __future__ import annotations

import argparse
import re
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
        errors.append(f"[Portão 2] Frases acima do teto de 15 palavras (0006): {'; '.join(long_sentences)}")

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
        errors.append(f"[Portão 2] Frases expandidas (TTS) acima de 15 palavras: {'; '.join(long_spoken_sentences)}")

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


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate product Portao 1 and/or Portao 2 artifacts deterministically.")
    parser.add_argument("product_dir", type=Path, help="Path to produtos/<slug>")
    parser.add_argument("--portao", type=int, action="append", choices=[1, 2], help="Gate(s) to validate (default: 1 and 2)")
    args = parser.parse_args()

    gates = args.portao or [1, 2]
    all_ok = True
    for g in gates:
        ok, errs, stats = validate_portao_1(args.product_dir) if g == 1 else validate_portao_2(args.product_dir)
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
