---
status: "accepted"
date: 2026-11-24
decision-makers: victor
---

# Motor Web Determinístico orientado a manifesto (`HTML5/CSS3/SVG + Playwright + VideoToolbox`) para cenas técnicas e de composição em `9:16`

## Contexto e problema

O pipeline híbrido estabelecido em [0005-pipeline-hibrido-25d-e-flow.md](0005-pipeline-hibrido-25d-e-flow.md) e [0006-governanca-qualidade-finops-e-composicao-visual.md](0006-governanca-qualidade-finops-e-composicao-visual.md) adotou `Python (Pillow/numpy) + ffmpeg` para renderizar localmente cenas determinísticas e o personagem `Rig 2.5D`, combinados a clipes externos do Google Flow (`Omni Flash 1.2 · 360p -> 1080p`) e locução comercial `Azure AI Speech F0`.

Na produção completa do piloto `IBG-001` (`ducha-eletronica-zagonel-nd-7700w`) e no benchmark controlado registrado em [motores-video-programatico-e-benchmark-local.md](../pesquisa/motores-video-programatico-e-benchmark-local.md) no hardware local (`Intel Core i7-5557U @ 3.10 GHz`, `4` threads, `16 GB RAM`, `Intel Iris Graphics 6100`), surgiram três limitações claras no motor `Pillow`:

1. **Acabamento gráfico e acoplamento de código:** `PIL.ImageDraw` carece de layout flexível, sombras suaves, gradientes complexos, física de mola (*spring*) e tipografia rica, exigindo `2.835` linhas imperativas em [render_zagonel.py](../../src/video/render_zagonel.py) acopladas a um único produto.
2. **Lentidão de CPU por quadro:** rotacionar e redimensionar camadas PNG de alta resolução do `InspectorRig` em Python CPU levou **`155,23 s`** para `5 s` de vídeo (`31,05×` o tempo real, projetando **`~25,9 min`** para um vídeo de `50 s`).
3. **Necessidade de replicabilidade multi-nicho ([visao.md](../visao.md)):** produtos de alimentos, processos industriais e comparativos de campo (Lentes 2 e 3 de [biblia.md](../../.agents/formato/biblia.md)) pedem diagramas vetoriais fluidos, cartões comparativos com fotos reais e transições suaves reutilizáveis entre produtos sem reescrever o renderizador do zero.

## Opções consideradas

### Opção 1: Motor Web Determinístico orientado a manifesto (`HTML5/CSS3/SVG + Playwright Headless Chrome + ffmpeg VideoToolbox`) integrado ao pipeline híbrido

Substituir o desenho imperativo em `Pillow` para novos produtos por um motor declarativo em `src/video/web_engine/` que:
- recebe um manifesto JSON por episódio (`episode_spec.json`) com cenas, lente criativa, paleta, ativos reais verificados, batidas de legenda higienizadas para pontuação isolada do `WordBoundary` do `Azure AI Speech F0` (conforme [checklist-publicacao.md](../../.agents/skills/orquestrar-equipe/references/checklist-publicacao.md)) e trilha de visemas por quadro (`lipsync.json`);
- renderiza templates e simulações procedurais `HTML5 Canvas 2D / CSS3 / SVG` (com transformações físicas quadro a quadro, física de mola determinística em JavaScript, rótulos espaciais curtos ancorados no objeto mantendo convenção calibrável de até `14` palavras simultâneas fora da legenda, área segura `X = 48..887 px`, `Y = 288..1247 px` de `0006` e [biblia.md](../../.agents/formato/biblia.md), e camadas PNG do `Rig 2.5D` pré-carregadas no DOM) usando **`2` abas paralelas** do `Playwright` sobre o `Google Chrome` já instalado;
- avança o tempo quadro a quadro (`window.__setFrame(frame)`) em sincronia determinística e envia os quadros em memória via `image2pipe` diretamente para o encoder de hardware **`ffmpeg (h264_videotoolbox)`** (com fallback `libx264`);
- compõe clipes `flow_ia` gerados na Web UI do Google Flow ([labs.google/fx/pt/tools/flow](https://labs.google/fx/pt/tools/flow) · `Omni Flash 1.2`, onde o clipe base `360p` é promovido gratuitamente a `720p Aprimorada` na interface web e masterizado localmente para `1080×1920` via `ffmpeg lanczos + h264_videotoolbox`, verificado ao vivo em `2026-11-24`), gerando sob demanda o corte derivado opcional `video_final_ml_clips_1080p.mp4` (`≤ 60 s`) a partir do mesmo motor determinístico.

#### Viabilidade de custo (FinOps)

1. **Inventário de recursos (Degrau 0 mantido a `US$ 0` adicional):**
   - **Renderização local (`Playwright` + `Google Chrome` + `ffmpeg h264_videotoolbox`):** `US$ 0`, licença comercial irrestrita (`Apache 2.0` + padrões W3C), consumo medido de **`~4,1 min` (`243,9 s`) de CPU local** e `236,2 MB` de RAM por vídeo de `50 s` (`4,88×` tempo real). Quando houver `1` cena `flow_ia` de `~8–10 s`, a variante determinística adicional `ML Clips` re-renderiza essa cena (`~10 s × 4,88 ≈ 48,8 s` / `~0,8 min` estimados pelo fator medido, totalizando `~4,9 min` por produto).
   - **Locução comercial (`Azure AI Speech F0`):** `~800` caracteres por vídeo dentro da cota gratuita oficial de `500.000` caracteres/mês (`US$ 0` até `625` vídeos/mês, conforme `0006`).
   - **Cenas externas opcionais (`Google Flow Web UI Pro`):** `0` a `16` créditos por produto (`0` quando 100% determinístico; `8` créditos para `1` clipe de `8 s` ou `16` créditos para `2` clipes de `8 s` em `360p` com *upscale* a `1080p` a `0` crédito na cota já paga de `1.000` créditos/mês).
2. **Projeção determinística de escala (cenário padrão de `1` clipe Flow `8 s` = `8` créditos + `50 s` de render Web Determinístico + variante `ML Clips` = `~4,9 min`/produto):**

   | Produtos/mês | Tempo total de render local (`i7-5557U`) | Créditos Flow (% da cota Pro de `1.000`) | Caracteres TTS (% do Azure `F0` de `500.000`) | Custo financeiro adicional |
   |---:|---:|---:|---:|---:|
   | `1` | `~4,9 min` *(incl. variante ML Clips)* | `8` (`0,8%`) | `~800` (`0,16%`) | **`US$ 0`** |
   | `30` | `~2 h 27 min` / mês (`~5 min`/dia) | `240` (`24%`) | `~24.000` (`4,8%`) | **`US$ 0`** |
   | `100` | `~8 h 10 min` / mês (`~16 min`/dia) | `800` (`80%`) | `~80.000` (`16%`) | **`US$ 0`** |
   | `300` | `~24 h 30 min` / mês (`~49 min`/dia) | `2.400` (`240%` — excede Pro) | `~240.000` (`48%`) | **Degrau 2 de `0006`** (`Google AI Ultra` `US$ 100/mês` ou `fal.ai` sob demanda; CPU local ainda comporta a carga em lotes noturnos a `US$ 0`) |

   - **Ponto de saturação:** a cota de mídia do Google AI Pro satura em **`125` produtos/mês** (`1.000 / 8`), ou **`62` produtos/mês** se usados `2` clipes de `8 s` (`16` créditos); a CPU local do `i7-5557U` comporta confortavelmente `300+` vídeos/mês (~`49 min`/dia de processamento em background), contra `~130 h`/mês que seriam exigidas pelo antigo motor `Pillow`.
3. **Alternativas mais econômicas / escala (somente quando necessário):** caso o volume supere a capacidade local ou exija renderização paralela horizontal na Fase 2, os mesmos templates HTML5/SVG rodam em *containers* CPU *serverless* (Cloud Run / GitHub Actions / VPS sob demanda) sem reescrever a camada visual.

### Opção 2: Adotar Remotion 4 (`React + TypeScript`) localmente

Utilizar o framework `Remotion 4.0` com `--concurrency=2` e `Google Chrome` local. Entrega a mesma qualidade visual da Opção 1 e ecossistema maduro para *Remotion Lambda*, porém no benchmark local ([motores-video-programatico-e-benchmark-local.md](../pesquisa/motores-video-programatico-e-benchmark-local.md)) consumiu **`3,53×` mais tempo** (`86,08 s` para `5 s`, ~`14,3 min` por vídeo de `50 s`), **`5,7×` mais memória RAM** (`1.346,5 MB`), adicionou `247` pacotes `npm` ao diretório de vídeo e impõe licença paga caso a equipe ultrapasse `3` pessoas.

### Opção 3: Editores tradicionais controlados via MCP ou CLI (`DaVinci Resolve MCP`, `Premiere/AE MCP`, `MLT`)

Operar NLEs de desktop via servidores MCP ou XML `melt`. Inadequado para o hardware atual (`Dual-Core i7` com `Iris 6100` sem GPU dedicada) no caso de Resolve/Adobe, ou exige instalar e manter *stack* multimídia adicional (`MLT`) com menor expressividade tipográfica/vetorial CSS para infográficos animados.

### Opção 4: Manter `Python (Pillow/numpy)` como motor principal

Preservar a arquitetura de `render_zagonel.py`. Mantém zero dependência de navegador *headless*, mas perpetua a lentidão de `31,05×` tempo real e a limitação estética de desenho 2D manual.

## Decisão

Opção escolhida: **Opção 1 (Motor Web Determinístico orientado a manifesto: `HTML5/CSS3/SVG + Playwright Headless Chrome + ffmpeg VideoToolbox`)**, porque no benchmark empírico local igualou a qualidade gráfica de estúdio do `Remotion` sendo `3,53×` mais rápida e `5,7×` mais econômica em RAM que o `Remotion`, e `6,36×` mais rápida que o `Pillow`, além de operar integralmente sobre binários e pacotes já instalados no ambiente local (`.venv`, `Google Chrome` e `ffmpeg`) sob licença comercial aberta irrestrita e custo adicional `US$ 0`.

Esta decisão atualiza a implementação técnica do motor `Determinístico` descrita em [0006-governanca-qualidade-finops-e-composicao-visual.md](0006-governanca-qualidade-finops-e-composicao-visual.md) e [fase-1.md](../requisitos/fase-1.md) (`REQ-006` e `REQ-015`), mantendo `render_zagonel.py` funcional por retrocompatibilidade para o produto-piloto `IBG-001`.

### Consequências

- **Bom:** reduz o tempo de renderização local de um vídeo `1080p` de `~25,9 min` (`Pillow`) para `~4,1 min`, habilitando física de mola, tipografia moderna, sombras, gradientes e diagramas SVG reutilizáveis entre nichos por simples troca de manifesto JSON.
- **Bom:** preserva `US$ 0` de custo adicional e zero restrição de licença comercial em qualquer tamanho de equipe.
- **Ruim:** requer o navegador `Google Chrome` (ou Chromium compatível com `Playwright`) disponível no ambiente de execução e disciplina nos templates CSS para impedir estouro de texto fora da área segura `9:16`.
