---
name: producao-visual
description: >-
  Como cocriar a camada visual de roteiro.md (decupagem, motor visual, direção de arte e orçamento Flow),
  gerar styleframes e animatic no Portão 2, e executar a produção final 9:16 (Rig 2.5D, Flow Omni
  360p->1080p, composições determinísticas, TTS comercial e pacote.md) no Portão 3.
---

# Direção de Arte e Produção Visual (Portões 2 e 3)

Fluxo visual e técnico derivado de [0005-pipeline-hibrido-25d-e-flow.md](../../../docs/decisoes/0005-pipeline-hibrido-25d-e-flow.md), [0006-governanca-qualidade-finops-e-composicao-visual.md](../../../docs/decisoes/0006-governanca-qualidade-finops-e-composicao-visual.md), [0008-sala-de-producao-coautoria-e-tres-portoes.md](../../../docs/decisoes/0008-sala-de-producao-coautoria-e-tres-portoes.md), [fase-1.md](../../../docs/requisitos/fase-1.md) (`REQ-003` a `REQ-007`, `REQ-012`, `REQ-014`, `REQ-015`) e da fonte única [.agents/formato/biblia.md](../../formato/biblia.md).

**Pré-requisito único (fora do ciclo por produto):** confirme se `assets/personagem/rig/` possui o pacote de camadas PNG do **Rig 2.5D** extraído de [referencia-oficial.jpg](../../../assets/personagem/referencia-oficial.jpg).

## 1. Coautoria visual e Portão 2 (`roteiro.md`, *styleframes* e animatic)

- Leia `produtos/<slug>/ficha.md`, `produtos/<slug>/assets/` e [.agents/formato/biblia.md](../../formato/biblia.md).
- Na **sala de produção (Swarm enxuto)**, alinhe a lente criativa com `@Carlos` e `@Curador` e assuma a camada visual de `produtos/<slug>/roteiro.md`:
  1. **Direção de arte e decupagem visual por cena:** escolha a paleta, o ritmo de cortes, a presença do Inspetor (`Rig 2.5D` na abertura, em PiP ou fechamento), os elementos de HUD estritamente úteis (ou tela limpa) e o **Motor Visual** (`Rig 2.5D`, `Flow Omni 360p -> 1080p` [`flow_ia`] ou `Determinístico`) de cada cena na tabela `## 1. Mapa de Cenas`.
  2. **Orçamento Flow (`## 3.`):** calcule `1 crédito/s` em `360p` (até `10s`; `0` crédito no *upscale* para `1080p`) com linha `Total` exata, e garanta a linha `**Aviso determinístico (REQ-007):** **SIM**` quando houver cena `flow_ia`.
  3. **Styleframes e animatic (`0` crédito Flow):** gere `1` *styleframe* local por cena em `_preview_build/styleframes/` usando os ativos reais e o motor determinístico, sintetize uma voz rascunho via **`edge-tts`** e monte o animatic para o Portão 2.
- Submeta na sala para parecer de fidelidade do `@Curador` antes de Mike acionar o **Espectador frio** e apresentar o Portão 2 ao usuário. **Aguarde a aprovação explícita do Portão 2 pelo usuário antes de consumir créditos do Google Flow.**

## 2. Produção técnica e stack (`Portão 3`)

- **Cenas externas e uso prático (`flow_ia`):** após aprovação do Portão 2, acione `browser` via `invoke_subagent` na Web UI do Google Flow (`Google AI Pro · Omni Flash 1.2 · 360p` guiado por foto real, `1 crédito/s` até `10s`). Valide o movimento internamente e promova os clipes aprovados para **`1080p` a `0` crédito**.
- **Integridade autoral e comercial de mídia externa:** componha cenas externas exclusivamente com ativos oficiais do fabricante, gravação própria, acervos com licença comercial explícita (`CC0`/domínio público) ou recriação original (`flow_ia` / `Determinístico`), preservando a operação afiliada livre de trechos virais de terceiros sem autorização (Lei nº 9.610/98, arts. 29 e 46, verificada em `2026-11-20`).
- **Visualizações e composições locais (`Determinístico`):** produza animações em **Python (`numpy` + `Pillow`) + `ffmpeg` (`overlay`/`videotoolbox` com fallback `libx264`)** (e estúdio interativo `Three.js` quando aplicável), adaptando a técnica à lente do produto:
  - na lente *Engenharia / Raio-X 3D*: morfologia fiel, compartimentos fisicamente estanques e fluxos confinados aos seus dutos;
  - na lente *Processo / "Como é Feito"*: etapas de transformação animadas, diagramas claros e texturas/ativos reais;
  - na lente *Teste Prático / Comparativo*: composições dinâmicas com fotos/clipes reais e comparativos nítidos.
  Sempre respeite a área segura, o ajuste tipográfico sem truncamento dentro de molduras, a ancoragem de apontadores na camada visível ativa e a legibilidade definidas em [.agents/formato/biblia.md](../../formato/biblia.md).
- **Voz comercial e *lip-sync* PT-BR:** sintetize a locução final via **`Azure AI Speech F0`** (checando credenciais apenas com `test -f` sem ler `.env*`) ou fallback offline **`Piper pt_BR`** em CPU, aplicando *lip-sync* determinístico grafema→visema em Python no `Rig 2.5D` e trilha/SFX sob licença comercial válida (`YouTube Audio Library`/`CC0` ou áudio nativo Flow).
- **Geração de imagem por IA (`REQ-012`):** quando estritamente necessária, use `image-generator` via `invoke_subagent` (ou fallback `gemini-api` via `run_command`) em `512px` (`0.5K`) para rascunhos e `1K+` apenas para arte final aprovada.

## 3. Validação determinística e entrega do Portão 3

- Execute as checagens determinísticas locais (`src/video/validate_gates.py` / `ffprobe` / `Pillow`): integridade do áudio (`> 0 bytes` e marcas temporais/RMS), área segura de `biblia.md`, presença e uso real dos ativos em disco, aviso `REQ-007` e licença comercial válida de todos os ativos publicados.
- Entregue **`produtos/<slug>/video_final_1080p.mp4`** e monte **`produtos/<slug>/pacote.md`** integrando os textos editoriais do `@Carlos` ao `código curto`, link(s) principal(is) de afiliado e aviso `REQ-007`.
- Submeta os quadros finais e `pacote.md` ao parecer de fidelidade do `@Curador` na sala antes de sinalizar a Mike para o **Espectador frio** e entrega ao usuário. Ajuste na mesma instância qualquer crítica e anote aprendizados para a retro consolidada.
