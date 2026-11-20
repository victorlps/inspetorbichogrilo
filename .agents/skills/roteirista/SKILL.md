---
name: roteirista
description: >-
  Como estruturar roteiros verticais 9:16 de alta retenção na voz do Inspetor Bicho Grilo
  (ganchos de abertura imediatos, arco narrativo, separação tela vs. voz, dicionário fonético TTS,
  classificação preliminar de cenas e texto editorial de pacote.md) e como revisar entregas visuais
  do Steve. Use no Portão 2, ao escrever textos de publicação ou ao revisar storyboards, styleframes e vídeos.
---

# Roteirista e Retenção (Portão 2, Textos de Publicação e Revisão Visual)

Fluxo editorial derivado de [0003-fluxo-aprovacao-e-publicacao.md](../../../docs/decisoes/0003-fluxo-aprovacao-e-publicacao.md), [0005-pipeline-hibrido-25d-e-flow.md](../../../docs/decisoes/0005-pipeline-hibrido-25d-e-flow.md), [0006-governanca-qualidade-finops-e-composicao-visual.md](../../../docs/decisoes/0006-governanca-qualidade-finops-e-composicao-visual.md), [0007-equipe-agentes-especializados-e-governanca-skills.md](../../../docs/decisoes/0007-equipe-agentes-especializados-e-governanca-skills.md) e [fase-1.md](../../../docs/requisitos/fase-1.md) (`REQ-003`, `REQ-004`, `REQ-006`, `REQ-010`, `REQ-014`, `REQ-015`).

## 1. Roteiro, mapa preliminar de cenas e orçamento (Portão 2)

- Aplique integralmente as diretrizes narrativas de [references/guia-roteirista.md](references/guia-roteirista.md): escreva na voz viva do **Inspetor Bicho Grilo** (2ª pessoa, emoção conversacional, curiosidade e transparência), elabore **3 opções concorrentes de gancho de abertura** explorando ângulos distintos para deter a rolagem no feed e abrir uma pergunta que o vídeo responde, registre a **intenção vocal por cena**, separe dados frios na tela da emoção na fala e alterne a cadência respeitando o teto operacional calibrável de **`15` palavras por frase** ([0006](../../../docs/decisoes/0006-governanca-qualidade-finops-e-composicao-visual.md#L69)).
- Estruture cada cena em `produtos/<slug>/roteiro.md` com **ação física do personagem Inspetor Bicho Grilo** (lupa articulada descendo do chapéu, lanterna iluminando, expressão de sobrancelha, gestos) e **demonstração visual em movimento sincronizada com a fala** (movimento mecânico, fluxo de fluido, montagem ou comparação técnica de componentes).
- Baseie cada afirmação, especificação e alerta exclusivamente em fatos verificados em `produtos/<slug>/ficha.md`, distinguindo com transparência relatos de compradores das orientações oficiais do fabricante; quando detectar dado faltante ou ambíguo, consulte o `@Curador` antes de redigir.
- Concentre todas as indicações visuais exclusivamente no **produto real anunciado**, suas peças próprias/câmara interna, recortes documentais oficiais e diagramas esquemáticos genéricos desenhados em Python, preservando os ativos próprios da oferta (`REQ-003`, `REQ-015`).
- Contemple no roteiro, nas cartelas e na chamada de ação todas as **variações essenciais do produto** validadas na ficha (como `127V` e `220V`, quando aplicável).
- Inclua diretamente em `produtos/<slug>/roteiro.md` (antes da aprovação do Portão 2):
  1. **Opções de Gancho de Abertura:** as 3 alternativas criadas por ângulos distintos com indicação da selecionada;
  2. **Falas cronometradas, intenção vocal e estimativa de duração total** com foco nas características técnicas duradouras do produto e indicação de elegibilidade ao Mercado Livre Clips (fala isenta de preço variável e previsão de trecho em uso prático real);
  3. **Dicionário fonético de TTS:** mapeamento de siglas, nomes estrangeiros e unidades técnicas para pronúncia falada natural (ex.: `"LED"` → `"léde"`, `"USB-C"` → `"ú ésse bê cê"`, `"mm"` → `"milímetros"`), mantendo a grafia técnica correta nas legendas visuais;
  4. **Classificação preliminar do mapa de cenas por motor visual (`REQ-003`):** classificação explícita de cada trecho entre **`Rig 2.5D`**, **`Flow Omni 360p -> 1080p` (`flow_ia`)** e **`Determinístico`**, com miniaturas/links das referências visuais já incorporados para visualização no *preview* de Markdown;
  5. **Estimativa inicial de créditos do Google Flow:** total previsto em `Omni Flash 1.2 · 360p` (`1 crédito/s` até `10s`) para validação visual e orçamentária do `@Steve` antes da entrega ao usuário.
- Aguarde a aprovação explícita do Portão 2 no chat antes de liberar síntese de áudio, geração de clipes no Flow ou renderização (`REQ-004`).

## 2. Revisão cruzada no Portão 2 (`REQ-014`)

- Execute primeiro a autochecagem editorial de [references/guia-roteirista.md](references/guia-roteirista.md) e valide o texto com o script determinístico local (`0` tokens: teto calibrável de `15` palavras por frase, duração estimada, dicionário fonético, classificação de cenas, orçamento Flow e validade dos links).
- Submeta `roteiro.md` ao `@Steve` para validação visual de entrada (exequibilidade das cenas, suficiência dos ativos em `produtos/<slug>/assets/` e conferência do orçamento Flow) e consulte o `@Curador` sempre que houver dúvida factual, incorporando os ajustes antes de entregar o Portão 2 ao usuário.

## 3. Textos editoriais de `pacote.md` (Portão 4)

- Ao preparar a publicação final aprovada pelo usuário, redija para `produtos/<slug>/pacote.md` (`REQ-006`, `REQ-010`):
  - **Legenda multiplataforma** alinhada ao gancho e à dor prática do vídeo;
  - **Palavras-chave / tags** fiéis ao modelo exato e às variações essenciais;
  - **Palavra-chave de DM e texto pronto de resposta automática** para o Meta Business Suite (Instagram Reels), incluindo o direcionamento para o link na bio como *fallback*.

## 4. Revisão visual multimodal das entregas do `@Steve` (Portões 3 e 4)

- Ao receber *styleframes*, quadros-chave, `preview.mp4` ou o MP4 final do `@Steve` (`REQ-014`), avalie como par criativo externo:
  1. **Impacto de abertura e ritmo:** se a composição inicial prende a atenção, sustenta a curiosidade aberta no gancho e acompanha a cadência das micro-viradas;
  2. **Legibilidade e separação Tela × Voz:** se legendas, rótulos técnicos e cartelas estão nítidos e reforçam os dados frios sem competir com o rosto/acessórios do Inspetor ou com o produto real;
  3. **Fidelidade narrativa e comercial:** se todas as cenas exibem exclusivamente o produto anunciado/diagramas genéricos e cobrem as variações essenciais prometidas no roteiro (`127V`/`220V`).
- Devolva ao `@Steve` apontamentos objetivos e acionáveis em linguagem afirmativa para ajustes pontuais antes da apresentação ao usuário.
