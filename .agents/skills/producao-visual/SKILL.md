---
name: producao-visual
description: >-
  Como validar a exequibilidade visual de roteiro.md e executar direção de arte e produção técnica
  9:16 (grid e área segura 1080x1920, legendas 1-3 palavras, styleframes locais, TTS pt-BR
  Azure F0/edge-tts/Piper com lip-sync Rig 2.5D, composições Pillow/ffmpeg e Flow Omni 360p->1080p)
  para entregar preview.mp4 (Portão 3) e o pacote final MP4 1080p (Portão 4).
---

# Direção de Arte e Produção Visual (Portões 2 a 4)

Fluxo visual e técnico derivado de [0004-identidade-visual-personagem.md](../../../docs/decisoes/0004-identidade-visual-personagem.md), [0005-pipeline-hibrido-25d-e-flow.md](../../../docs/decisoes/0005-pipeline-hibrido-25d-e-flow.md), [0006-governanca-qualidade-finops-e-composicao-visual.md](../../../docs/decisoes/0006-governanca-qualidade-finops-e-composicao-visual.md), [0007-equipe-agentes-especializados-e-governanca-skills.md](../../../docs/decisoes/0007-equipe-agentes-especializados-e-governanca-skills.md) e [fase-1.md](../../../docs/requisitos/fase-1.md) (`REQ-003` a `REQ-008`, `REQ-012`, `REQ-014`, `REQ-015`).

**Pré-requisito único (fora do ciclo por produto):** mantenha preparado em `assets/personagem/rig/` o pacote fatiado de camadas PNG do **Rig 2.5D** extraído de [referencia-oficial.jpg](../../../assets/personagem/referencia-oficial.jpg) antes de executar renderizações do personagem.

## 1. Validação Visual de Entrada (Portão 2 junto ao `@Carlos`)

- Ao revisar `produtos/<slug>/roteiro.md` antes da entrega do Portão 2, verifique:
  1. **Exequibilidade e clareza cênica:** cada fala possui ação física coerente do **Inspetor Bicho Grilo** e demonstração visual executável com o acervo do produto;
  2. **Classificação por motor visual (`REQ-003`, `REQ-015`):** cenas externas, ambiente e uso prático usam `Flow Omni 360p -> 1080p` (`flow_ia`) guiado por foto real do produto; mecanismos internos, esquemas técnicos, rótulos e medidas usam `Determinístico` (`Pillow`/`numpy` + `ffmpeg`); apresentações diretas e reações usam `Rig 2.5D`;
  3. **Disponibilidade de ativos e orçamento Flow:** todos os arquivos referenciados existem em `produtos/<slug>/assets/` (ou têm captura/preparo definido) e a soma de créditos em `Omni Flash 1.2 · 360p` (`1 crédito/s` até `10s`) está exata;
  4. **Bloqueio de Portão (`REQ-004`):** aguarde a aprovação explícita do Portão 2 pelo usuário no chat antes de sintetizar áudio, gerar clipes no Flow ou renderizar quadros.

## 2. Direção de Arte, Área Segura `9:16` e Stack Técnico Real

- **Grid de palco `9:16` e Área Segura (`1080×1920`):** mantenha todos os elementos críticos (produto real, rosto e acessórios do apresentador, chamadas visuais e legendas) dentro da área livre verificada em [0006](../../../docs/decisoes/0006-governanca-qualidade-finops-e-composicao-visual.md) (**`X = 48..887 px`** — com folga lateral esquerda conservadora **`≥ 65 px`** — e **`Y = 288..1247 px`**, ou coordenadas proporcionais em baixa resolução), deixando livres as margens ocupadas pelas interfaces das plataformas.
- **Legendas dinâmicas em blocos curtos:** exiba legendas de **1 a 3 palavras por batida** com destaque visual na palavra ativa (fonte *bold* branca com contorno escuro nítido), posicionadas na faixa **`Y = 1040–1220 px`** (`1080×1920`) acima da barra inferior das redes.
- **Critério visual por natureza da cena (`REQ-015`):**
  - **Cenas externas, ambiente e uso real (`flow_ia`):** utilize a **Web UI do Google Flow** na assinatura **Google AI Pro** com **`Omni Flash 1.2 · 360p`** (*Text*, *Frames*, *Ingredients* ou *Video-to-Video Editing* em `9:16`, `1 crédito/s` até `10s`) guiado pela foto real do produto no Portão 3, promovendo o clipe aprovado para **`1080p` a `0` crédito** no Portão 4 (até `10s`).
  - **Mecanismos internos, esquemas técnicos e medidas (`Determinístico`):** utilize composição programática em **Python (`Pillow`/`numpy`) + `ffmpeg` (`overlay`/`videotoolbox`/`libx264`)** ancorada em foto real da peça aberta ou diagrama oficial do fabricante, gerando setas direcionais, camadas, rótulos exatos e legendas em quadros nítidos compatíveis com o hardware local (`Intel Core i7-5557U`).
- **Áudio TTS, trilha/SFX e *lip-sync* nativo PT-BR:** sintetize a locução via **`edge-tts`** (partida imediata no Degrau 0) ou via evolução gratuita oficial **`Azure AI Speech F0`** (`500.000` chars/mês grátis com marcas `WordBoundary` e visemas quando suportados pela voz `pt-BR`), validando imediatamente **`arquivo > 0 bytes`** e marcas temporais e acionando **`Piper pt_BR`** offline em CPU com alinhamento por frase e RMS caso ocorra indisponibilidade do endpoint. Aplique **mapeamento determinístico grafema→visema para português em Python** no Rig 2.5D e utilize trilha/SFX sob licença comercial válida no Degrau 0 (`YouTube Audio Library`/`CC0` ou áudio nativo Flow).
- **Escada de investimento e caixa de ferramentas (`0006`):** mantenha disponíveis os planos *Free* de fornecedores comerciais (`ElevenLabs Free`, `Recraft Web Free`, `Suno Free`) para provas de conceito (PoCs) e avaliação interna de ganho real antes de assinar; componha o pacote publicado no **Portão 4** exclusivamente com ativos gerados sob licença comercial válida (em cota gratuita comercial ou já no plano pago/API comercial ativado nos Degraus 1 e 2 conforme [0006](../../../docs/decisoes/0006-governanca-qualidade-finops-e-composicao-visual.md), respeitando fornecedores que exigem geração final em conta paga).
- **Validação rápida por *styleframes* locais:** monte 1 quadro estático de composição por cena aproveitando exclusivamente os ativos locais já existentes (economizando integralmente créditos de nova geração de imagem) para confirmar enquadramento, escala e contraste antes de renderizar `preview.mp4`.

## 3. Geração de Imagens por IA (`REQ-012`)

- Solicite a menor resolução útil (`512px` / `0.5K`, ~747 tokens) em provas de conceito, rascunhos e exploração visual.
- Reserve resoluções maiores (`1K+`) exclusivamente para a arte final aprovada.

## 4. Validação Determinística e Revisão Cruzada com `@Carlos` (`REQ-014`)

- **Camada 1 — Validação determinística local (`0` tokens):** antes de apresentar entregas nos Portões 3 e 4, confira em script local: (a) integridade do áudio TTS (`> 0 bytes` com marcas temporais/visemas no `Azure F0`/`edge-tts` ou segmentação por frase/RMS no fallback `Piper pt_BR`), (b) coordenadas de todos os elementos e legendas dentro da área segura (**`X = 48..887 px`**, **`Y = 288..1247 px`** ou faixa proporcional), (c) presença em disco de todos os ativos e clipes referenciados, (d) disparo automático do aviso de IA (`REQ-007`) quando houver cena `flow_ia` e (e) confirmação de licença comercial válida nos ativos que entram no pacote final do Portão 4.
- **Camada 2 — Revisão visual cruzada com `@Carlos`:** envie os *styleframes* e quadros-chave representativos (junto a `preview.mp4` ou ao vídeo final) ao `@Carlos` para validar nitidez das legendas, destaque do produto real, separação limpa entre legendas/rosto/acessórios e coerência narrativa com o roteiro antes de entregar ao usuário.

## 5. *Preview* de Calibração (Portão 3) e Pacote Final (Portão 4)

- **Portão 3 (ativo durante calibração; dispensável após decisão explícita do usuário):** gere a narração verificada e `preview.mp4` combinando o Rig 2.5D em *lip-sync* determinístico PT-BR, composições determinísticas (`Pillow`/`numpy` + `ffmpeg`) e os clipes **`Omni 360p`** já prontos para promoção a `1080p` (ou edição pontual *video-to-video*), permitindo validar voz, ritmo, legendas e movimento real no player padrão do sistema (`REQ-005`).
- **Portão 4 (`REQ-006`, `REQ-007`, `REQ-008`):** após aprovação do Portão 3 (ou diretamente após o Portão 2 quando o Portão 3 estiver dispensado), promova os clipes `Omni 360p` aprovados para **`1080p` (`0` crédito até `10s` no Google AI Pro)**, execute a montagem final `9:16` (`1080×1920`) via `Python (Pillow/numpy) + ffmpeg (overlay/videotoolbox)`, entregue o MP4 final limpo composto exclusivamente por ativos com licença comercial válida junto com `pacote.md` completo (integrando os textos editoriais do `@Carlos`, código curto da vitrine, link principal de afiliado e aviso determinístico de IA `REQ-007`) e atualize a vitrine estática na bio logo após a aprovação final no chat (`REQ-008`).
