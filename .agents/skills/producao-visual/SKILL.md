---
name: producao-visual
description: >-
  Como cocriar a camada visual animada de roteiro.md (simulações físicas Estado A -> Ação -> Estado B,
  motores visuais, rótulos espaciais e orçamento Flow), gerar quadros de transformação e animatic no
  Portão 2, e renderizar o episódio 9:16 1080p com animações procedurais Canvas/SVG/WebGL, Flow Omni,
  Rig 2.5D e TTS comercial natural no Portão 3.
---

# Direção de Arte e Animação Visual Explicativa (Portões 2 e 3)

Fluxo visual e técnico derivado de [0005-pipeline-hibrido-25d-e-flow.md](../../../docs/decisoes/0005-pipeline-hibrido-25d-e-flow.md), [0006-governanca-qualidade-finops-e-composicao-visual.md](../../../docs/decisoes/0006-governanca-qualidade-finops-e-composicao-visual.md), [0008-sala-de-producao-coautoria-e-tres-portoes.md](../../../docs/decisoes/0008-sala-de-producao-coautoria-e-tres-portoes.md), [0010-motor-video-programatico-web-deterministico.md](../../../docs/decisoes/0010-motor-video-programatico-web-deterministico.md), [fase-1.md](../../../docs/requisitos/fase-1.md) (`REQ-003` a `REQ-007`, `REQ-012`, `REQ-014`, `REQ-015`) e da fonte única [.agents/formato/biblia.md](../../formato/biblia.md).

**Pré-requisito único (fora do ciclo por produto):** confirme a presença do pacote de camadas PNG do **Rig 2.5D** em `assets/personagem/rig/` extraído de [referencia-oficial.jpg](../../../assets/personagem/referencia-oficial.jpg).

## 1. Coautoria de Animações Explicativas e Portão 2 (`roteiro.md`, quadros de transformação e animatic)

- Leia `produtos/<slug>/ficha.md`, `produtos/<slug>/assets/` e [.agents/formato/biblia.md](../../formato/biblia.md).
- Na **sala de produção (Swarm enxuto)**, alinhe a lente criativa com `@Carlos` e `@Curador` e assuma a camada visual de `produtos/<slug>/roteiro.md`:
  1. **Coreografia de transformação física por cena (`Estado A → Ação Física → Estado B`):** projete para cada batida narrativa uma demonstração visual contínua em movimento — simulações procedurais `HTML5 Canvas 2D / SVG / WebGL` (células, cristais, vapor, calor, pressão, dutos, balança física, comparativo estrutural lado a lado) ou planos cinematográficos/reais em tela aberta, acompanhados apenas dos rótulos espaciais ancorados ao objeto e da presença pontual do `Rig 2.5D` definidos em `biblia.md`.
  2. **Orçamento Flow (`## 3.`):** calcule os créditos por cena seguindo a regra tarifária e de promoção de resolução definida em [0006](../../../docs/decisoes/0006-governanca-qualidade-finops-e-composicao-visual.md), com linha `Total` exata, e registre `**Aviso determinístico (REQ-007):** **SIM**` quando houver cena `flow_ia`.
  3. **Quadros de transformação e animatic (`0` crédito Flow):** capture no motor determinístico os *styleframes* representativos de cada cena em `_preview_build/styleframes/` (acompanhados de amostras de transformação), sintetize a voz rascunho via **`edge-tts`** em cadência conversacional natural e monte `animatic_portao2.mp4` para o Portão 2.
- Submeta na sala para parecer científico e físico do `@Curador` antes de Mike acionar o **Espectador frio** e apresentar o Portão 2 ao usuário. **Consuma créditos do Google Flow após aprovação explícita do usuário.**

## 2. Produção técnica de Animação e Vídeo (`Portão 3`)

- **Planos de fenômeno físico e ambiente real (`flow_ia`):** acione `browser` na Web UI do Google Flow conforme [0006](../../../docs/decisoes/0006-governanca-qualidade-finops-e-composicao-visual.md), [0010](../../../docs/decisoes/0010-motor-video-programatico-web-deterministico.md) e [.agents/formato/biblia.md](../../formato/biblia.md) (`§4`), priorizando planos macro de fenômenos naturais/físicos e cenas humanas em ambiente aberto, sobrepondo o recorte oficial do produto exemplar apenas no momento orgânico da narrativa. Ao operar no navegador integrado do Antigravity, promova o clipe aprovado na Web UI, obtenha a URL assinada `https://flow-content.google/video/...` via `list_network_requests`, baixe via `curl -fsSL` em `produtos/<slug>/assets/` e masterize na resolução vertical canônica de `biblia.md` via `ffmpeg` (`lanczos` + `h264_videotoolbox`, conforme detalhado em `0010`).
- **Integridade autoral e recortes alfa:** componha cenas com ativos oficiais íntegros do fabricante, gravação própria, acervos `CC0`/domínio público ou animações/clipes autorais (`Determinístico` / `flow_ia`), conforme a Lei nº 9.610/98 (arts. 29 e 46, verificada em `2026-11-20`). Gere recortes alfa limpos por *floodfill* a partir das bordas externas para preservar rótulos e detalhes internos opacos.
- **Simulações procedurais no Motor Web Determinístico (`Determinístico`):** estruture `produtos/<slug>/episode_spec.json` e execute `src/video/build_episode_manifest.py` sobre `src/video/web_engine/` (conforme [0010](../../../docs/decisoes/0010-motor-video-programatico-web-deterministico.md); scripts `Pillow/numpy` e `Three.js` permanecem suportados), garantindo:
  - animações contínuas quadro a quadro desenhadas em `Canvas 2D / SVG` que mostram visualmente mudanças de temperatura, pressão, fase, porosidade, massa ou fluxo mecânico;
  - pré-carregamento síncrono no DOM de todas as poses, piscadas e visemas do `Rig 2.5D` alternados via `display`, e alternância para palco de altura expandida quando o Inspetor cede a tela inteira à simulação;
  - cumprimento integral da área segura, da faixa de legendas e do orçamento enxuto de palavras visíveis em tela definidos em [.agents/formato/biblia.md](../../formato/biblia.md);
  - suporte sob demanda ao corte opcional `--ml-clips` quando solicitado para publicação no Mercado Livre Clips.
- **Voz comercial em cadência natural e *lip-sync* PT-BR:** sintetize a locução final conforme [0006](../../../docs/decisoes/0006-governanca-qualidade-finops-e-composicao-visual.md) (conferindo a presença de `.env*` exclusivamente via `test -f`) em velocidade conversacional respirada, sincronizando `WordBoundary` em batidas que quebram nas fronteiras de pontuação e aplicando visemas nativos ao `Rig 2.5D`.
- **Geração de imagem por IA (`REQ-012`):** quando necessária para texturas ou elementos ilustrativos auxiliares, acione `image-generator` via `invoke_subagent` (ou `gemini-api` via `run_command`) respeitando os degraus de resolução de rascunho e arte final estabelecidos em [fase-1.md](../../../docs/requisitos/fase-1.md) (`REQ-012`).

## 3. Validação determinística e entrega do Portão 3

- Execute `python3 src/video/validate_gates.py produtos/<slug> --portao 3` verificando integridade do áudio, área segura, orçamento enxuto de texto em tela, presença dos quadros finais, aviso `REQ-007` e licença comercial válida de todos os ativos.
- Entregue **`produtos/<slug>/video_final_1080p.mp4`** e monte **`produtos/<slug>/pacote.md`** unindo os textos editoriais e o resumo de variações do `@Carlos` ao código curto da vitrine, links verificados e aviso `REQ-007`.
- Submeta os quadros de transformação finais e `pacote.md` ao parecer de fidelidade do `@Curador` antes de sinalizar a Mike para o **Espectador frio** e apresentação ao usuário.
