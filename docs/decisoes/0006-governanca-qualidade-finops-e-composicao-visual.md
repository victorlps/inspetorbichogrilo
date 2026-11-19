---
status: "accepted"
date: 2026-11-19
decision-makers: victor
---

# Governança de qualidade em camadas, FinOps sob demanda em ADRs e alinhamento real dos Portões às ferramentas

## Contexto e problema

Conforme [visao.md](../visao.md), o projeto exige rigor técnico, qualidade visual profissional condicionada ao custo inicial mínimo (com reinvestimento progressivo condicionado ao retorno validado) e processo replicável independente de produto ou nicho. O fluxo em 4 portões ([0003-fluxo-aprovacao-e-publicacao.md](0003-fluxo-aprovacao-e-publicacao.md)) e o pipeline híbrido Rig 2.5D + Google Flow ([0005-pipeline-hibrido-25d-e-flow.md](0005-pipeline-hibrido-25d-e-flow.md)) já eliminaram o gargalo de 55s/quadro em CPU, porém a auditoria das ferramentas reais e do mercado amplo de IAs mostrou quatro pontos para decisão formal:

1. **Avaliação contínua de custo (FinOps) e escada de investimento:** decidir entre manter um agente LLM rodando continuamente para auditar custos ou aplicar análise determinística sob gatilho em ADRs, organizando o stack em degraus de gasto condicionado a receita sem excluir ferramentas que tenham planos *Free* úteis para provas de conceito (PoCs).
2. **Alinhamento dos Portões 1 a 4 às ferramentas reais:** o Portão 3 havia sido desenhado para evitar 12h+ de render 3D no Blender gerando *viewport* descartável, enquanto no Google Flow `Omni Flash 1.2` o gasto de créditos ocorre no clipe `360p` e o *upscale* para `1080p` custa `0` crédito até `10s`; além disso, o dicionário fonético, o mapa de cenas e o orçamento de créditos pertencem ao Portão 2, e o Portão 1 precisa assegurar referências técnicas internas quando aplicável.
3. **Stack técnico coerente com o ambiente real (`Intel Core i7-5557U`) e licenciamento comercial:** `rhubarb` está ausente na máquina e restrito a inglês/fonético aproximado; `ffmpeg 9.0.2` local traz `overlay` e `videotoolbox` sem `drawtext`/`ass`; `Pillow` e `numpy` já rodam em Python 3.14; e o áudio `pt-BR` gratuito pede caminho oficial (`Azure AI Speech F0`) com fallback offline (`Piper pt_BR`) e trilha/SFX comercialmente limpa na entrega pública.
4. **Revisão em camadas e critério visual `9:16`:** estruturar checagens determinísticas e revisores LLM nos Portões 1 a 4 respeitando o bloqueio de áudio/vídeo antes do Portão 2 (`REQ-002` e `REQ-004`) e o critério visual por natureza da cena em `1080×1920`.

As evidências colhidas estão registradas em [custo-agentes-revisores-e-finops.md](../pesquisa/custo-agentes-revisores-e-finops.md), [video-ia-vs-renderizacao-deterministica-mecanismos.md](../pesquisa/video-ia-vs-renderizacao-deterministica-mecanismos.md), [alinhamento-ferramentas-producao-video-e-audio.md](../pesquisa/alinhamento-ferramentas-producao-video-e-audio.md) e [panorama-mercado-ia-imagem-audio-video.md](../pesquisa/panorama-mercado-ia-imagem-audio-video.md).

## Opções consideradas

### Opção 1: Governança enxuta em 4 frentes (FinOps sob demanda em ADRs + Portões 1–4 realinhados + escada de investimento 0/1/2 + revisão em camadas)

- **1. FinOps sob demanda na skill `documentar`:** incluir subseção `Viabilidade de custo (FinOps)` apenas ao elaborar ou revisar ADRs em `docs/decisoes/` que envolvam ferramentas, infraestrutura, APIs externas, tokens de IA ou créditos de plataforma. A análise inventaria recursos locais e de IA, calcula projeção determinística de **1, 30, 100 e 300 execuções/mês** em créditos/% da cota e em US$ (explicitando o ponto de saturação) e registra alternativas econômicas **somente quando necessário** (gargalo técnico comprovado, saturação de cota ou desvio da restrição de custo inicial mínimo de [visao.md](../visao.md)).
- **2. Portões 1 a 4 realinhados e revisão em camadas antes do usuário:**
  - **Portão 1 (`ficha.md`):** coleta de foto de peça aberta, vista explodida ou manual oficial do fabricante sempre que o ângulo editorial abordar mecanismo interno (`REQ-001`), precedida por validação determinística local de completude (5 blocos preenchidos, arquivos locais existentes e distribuição de estrelas somando 100%).
  - **Portão 2 (`roteiro.md`, preservando `REQ-002` e `REQ-004` sem áudio nem render):** consolida fala cronometrada, **dicionário fonético de TTS**, **mapa de cenas por motor visual** (`Rig 2.5D`, `Flow Omni 360p → 1080p` [`flow_ia`] ou `Determinístico`) e **orçamento explícito de créditos do Flow** antes de consumir qualquer crédito; validado por (a) checagem determinística de texto (parâmetro editorial calibrável de até **15 palavras por frase**, estimativa de duração falada, dicionário fonético preenchido, mapa/orçamento completos e links válidos) e (b) **Agente Crítico de Roteiro** (`flash`, contexto isolado apenas com `ficha.md` e `roteiro.md`, teto fixo de **2 rodadas**).
  - **Portão 3 (`preview.mp4` — opcional/dispensável após calibração de voz e formato):** valida narração real (com checagem `> 0 bytes` e marcas temporais/visemas no `Azure AI Speech F0`/`edge-tts` ou segmentação por frase/RMS no fallback `Piper pt_BR`), ritmo, legendas e os clipes **`Omni 360p`** gerados na Web UI do Google Flow já prontos para promoção gratuita a `1080p` ou edição pontual *video-to-video*, precedido por validação determinística visual/áudio e **Agente Inspetor Visual Multimodal** (`flash`, contexto isolado sobre *styleframes* e quadros-chave).
  - **Portão 4 (`video_final_1080p.mp4` + `pacote.md` + vitrine):** executa **upscale `0` crédito `360p → 1080p`** sobre os clipes `Omni 360p` aprovados (até `10s` no Google AI Pro), compõe em `1080×1920`, aciona deterministicamente o aviso de IA (`REQ-007`) sempre que o mapa de cenas contiver cena `flow_ia`, confirma licença comercial válida para os ativos do pacote publicado, passa por validação determinística + **Agente Inspetor Visual Multimodal** (`flash`) e libera atualização da vitrine apenas após aceite final (`REQ-008`).
- **3. Stack técnico alinhado ao ambiente local (`Intel Core i7-5557U`) + escada de investimento em 3 degraus:**
  - **Degrau 0 — Validação inicial (`US$ 0` adicional/mês):**
    - *Voz `pt-BR`:* partida imediata com **`edge-tts`** já instalado, evoluindo para **`Azure AI Speech F0`** (`500.000` chars/mês grátis ≈ `625` vídeos/mês com suporte oficial de API, `WordBoundary` e visemas quando disponíveis na voz escolhida), mantendo **`Piper pt_BR`** offline em CPU como plano B resiliente;
    - *Sincronia labial e composição local:* **lip-sync determinístico PT-BR em Python** (grafema→visema sobre texto + marcas temporais/visemas + amplitude RMS, substituindo `Rhubarb Lip Sync` previsto em `0005`), **Rig 2.5D local** sobre pacote único de camadas PNG extraído de [referencia-oficial.jpg](../../assets/personagem/referencia-oficial.jpg), e motor determinístico em **Python (`Pillow`/`numpy`) + `ffmpeg` (`overlay`/`videotoolbox`/`libx264`)** dispensando `drawtext`/`libass` e Chromium *headless*;
    - *Vídeo externo e áudio ambiente:* Google Flow Web UI Pro (`Omni Flash 1.2 · 360p → 1080p` a `0` crédito até `10s`, máximo `125` clipes de `8s`/mês na cota já paga) e trilha/SFX de bibliotecas comerciais livres (`YouTube Audio Library` / `CC0`) ou áudio nativo do clipe Flow.
  - **Degrau 1 — Primeiras comissões confirmadas (`~US$ 6–10/mês`, acionado somente após receita recorrente cobrindo o gasto com folga):** salto de áudio via **`ElevenLabs Starter`** (`US$ 6/mês`, voz `pt-BR` + SFX + música com licença comercial) ou *pay-per-use* (**`Gemini 3.8 Flash-Lite TTS`** `~US$ 0,008`/vídeo em 2026 + **`Google Lyria 3`** `US$ 0,04`/trilha `30s`), e vetores `SVG` editáveis sob demanda via **`Recraft API`** (`US$ 0,05–0,08`/SVG, créditos sem expiração).
  - **Degrau 2 — Escala e automação (`> 100 vídeos/mês` ou receita consolidada):** gateway *pay-per-use* **`fal.ai`** (`Kling v2.5 Turbo Pro` `US$ 0,56`/8s, `Seedance 2.0`, testes pontuais de `Kling Avatar`/`OmniHuman` apenas em ganchos de `3–5s`) e upgrade de cota (`Azure S0`, `ElevenLabs Creator` ou `Google AI Ultra`) quando o faturamento justificar.
  - **Regra de caixa de ferramentas (PoC versus Publicação comercial):** manter disponíveis na caixa de ferramentas planos *Free* de fornecedores comerciais (`ElevenLabs Free`, `Recraft Web Free`, `Suno Free`) para provas de conceito internas e validação de ganho real; compor o pacote publicado do **Portão 4** exclusivamente com ativos produzidos sob licença comercial válida (gerados em cota gratuita comercial ou já na conta paga/API comercial escolhida, respeitando fornecedores que exigem gerar o ativo final já na conta paga).
- **4. Critério visual por natureza da cena + Área Segura `9:16`:**
  - **Cenas externas, uso prático e atmosfera natural:** vídeo por IA na **Web UI do Google Flow** (`Omni Flash 1.2 · 360p → 1080p`, suporte verificado para *Ingredients/Frames/Editing* em `9:16`).
  - **Mecanismos internos, esquemas e medidas:** composição determinística via `Python (Pillow/numpy) + ffmpeg` ancorada em foto real da peça ou diagrama oficial do fabricante.
  - **Área Segura `9:16` (`1080×1920`) e legendas:** manter todos os elementos críticos dentro da área livre oficial verificada no template vertical Google/YouTube (**`X = 48..887 px`**, **`Y = 288..1247 px`**; margem lateral esquerda `≥ 65 px` como folga conservadora para Reels) e exibir legendas dinâmicas de **1 a 3 palavras** com destaque visual na palavra ativa na faixa **`Y = 1040–1220 px`**.

#### Viabilidade de custo (FinOps)

1. **Inventário de recursos (Degrau 0 atual):**
   - Scripts determinísticos, `edge-tts` / `Piper pt_BR`, **`Azure AI Speech F0`** (`0–500.000` chars/mês grátis), lip-sync PT-BR em Python e composição `Pillow`/`numpy` + `ffmpeg`: CPU local / API gratuita comercial, `0` tokens pagos de mídia, `US$ 0`.
   - Subagentes revisores em modelo `flash` (Crítico de Roteiro com teto de 2 rodadas + Inspetor Visual sobre quadros-chave): executados na sessão/assinatura de agente já utilizada pelo usuário *(tarifa avulsa por token de API — **não verificado**)*.
   - Google Flow Web UI `Omni Flash 1.2` para clipe externo de `8s`: **`8` créditos** em `360p` (`1` crédito/s) + aumento de resolução até `1080p` para clipes de `1` a `10s` a **`0` crédito** na assinatura **Google AI Pro** já mantida pelo usuário (`1.000` créditos/mês sem acúmulo).
2. **Projeção determinística de escala (Degrau 0 — cenário-base de `1` clipe externo `8s` `360p→1080p` + `~800` chars `Azure F0`/vídeo):**
   - **`1` vídeo/mês:** `8` créditos Flow (`0,8%` cota Pro) + `~800` chars (`0,16%` cota Azure `F0`) | **`US$ 0` adicional**.
   - **`30` vídeos/mês:** `240` créditos Flow (`24%` Pro) + `~24.000` chars (`4,8%` Azure `F0`) | **`US$ 0` adicional**.
   - **`100` vídeos/mês:** `800` créditos Flow (`80%` Pro) + `~80.000` chars (`16%` Azure `F0`) | **`US$ 0` adicional**.
   - **Ponto de saturação no Degrau 0:** **`125` vídeos/mês** no Google AI Pro (`1.000 / 8`); o **`Azure AI Speech F0`** comporta até **`625` vídeos/mês** (`500.000 / 800`) antes de exigir tier `S0` ou `Chirp 3: HD` (`1.250` vídeos/mês grátis).
   - **`300` vídeos/mês:** `2.400` créditos Flow (`240%` Pro; excede a cota mensal Pro e aciona o **Degrau 2**, por exemplo `fal.ai` / `Google AI Ultra` US$ 100/mês) + `~240.000` chars (`48%` Azure `F0`, ainda dentro da cota gratuita de voz; preço excedente avulso do Flow — **não verificado**).
3. **Alternativas mais econômicas (somente quando necessário):** antes de migrar aos **Degraus 1 ou 2**, reduza duração de clipes Flow ou substitua planos externos por composição determinística 2.5D sobre fotos reais locais (`0` crédito); o reinvestimento pago é liberado somente quando comissões reais validarem o retorno conforme os gatilhos dos Degraus 1 e 2.

### Opção 2: Manter agente LLM contínuo de FinOps, `Rhubarb` externo e Portão 3 descartável herdado do Blender

Manter agente auditor em toda execução, depender do binário inglês `Rhubarb` e descartar clipes `360p` gerando novos em `720p` no Portão 4.

### Opção 3: Investir em assinaturas pagas (`ElevenLabs` / `Recraft` / `fal.ai`) já na validação inicial antes de faturar

Assumir despesas mensais ou recargas pagas desde o vídeo 1 antes de validar conversão real no Degrau 0.

## Decisão

Opção escolhida: **Opção 1 (Governança enxuta em 4 frentes com escada de investimento 0/1/2)**, porque viabiliza toda a validação inicial com **`US$ 0` adicional** (`Azure F0` oficial + Flow Web UI Pro com *upscale* `0` crédito + `Pillow/ffmpeg`), mantém ferramentas *freemium* (`ElevenLabs`, `Recraft`, `Suno`) acessíveis para PoCs garantindo licença comercial estrita apenas na publicação do Portão 4, e reserva reinvestimentos pagos (`Degraus 1 e 2`) exclusivamente para quando houver retorno financeiro comprovado.

Registra-se que o teto inicial de **15 palavras por frase**, a escolha do modelo **`flash`** para revisores e as coordenadas **`Y = 1040–1220 px`** (com folga conservadora **`X ≥ 65 px`**) constituem **convenções operacionais iniciais desta decisão**, sujeitas a calibração contínua nos ciclos `/learn` (`REQ-013`).

### Consequências

- **Bom:** garante caminho comercialmente seguro a `US$ 0` adicional até `125` vídeos/mês no Degrau 0 e orienta exatamente onde reinvestir os primeiros retornos financeiros (voz/SFX comercial e SVG nativo no Degrau 1; escala/vídeo *pay-per-use* no Degrau 2).
- **Bom:** preserva a liberdade experimental com planos *Free* em provas de conceito sem contaminar vídeos publicados com ativos restritos de uso não-comercial.
- **Ruim:** exige construir uma única vez o conjunto de camadas PNG do Rig 2.5D, configurar o recurso gratuito `Azure F0` ao migrar do `edge-tts` e checar a licença comercial dos ativos antes de aprovar o Portão 4.
