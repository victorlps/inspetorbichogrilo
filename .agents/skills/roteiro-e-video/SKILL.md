---
name: roteiro-e-video
description: Como estruturar roteiro com mapa de cenas e orçamento (Portão 2), aplicar direção de arte e stack real (Pillow/ffmpeg, Flow Omni 360p->1080p, Azure F0/edge-tts/Piper pt_BR), validar em camadas e entregar Portão 3 e Portão 4. Use ao criar ou revisar roteiros, imagens de conceito e vídeos de produtos.
---

# Roteiro e Vídeo (Portões 2 a 4)

Fluxo de produção derivado de [0005-pipeline-hibrido-25d-e-flow.md](../../../docs/decisoes/0005-pipeline-hibrido-25d-e-flow.md), [0006-governanca-qualidade-finops-e-composicao-visual.md](../../../docs/decisoes/0006-governanca-qualidade-finops-e-composicao-visual.md), [0003-fluxo-aprovacao-e-publicacao.md](../../../docs/decisoes/0003-fluxo-aprovacao-e-publicacao.md), [0004-identidade-visual-personagem.md](../../../docs/decisoes/0004-identidade-visual-personagem.md) e [fase-1.md](../../../docs/requisitos/fase-1.md) (`REQ-003` a `REQ-007`, `REQ-012`, `REQ-014` e `REQ-015`).

**Pré-requisito único (fora do ciclo por produto):** mantenha preparado em `assets/personagem/` o pacote fatiado de camadas PNG do **Rig 2.5D** extraído de [referencia-oficial.jpg](../../../assets/personagem/referencia-oficial.jpg) antes de executar renderizações do personagem.

## 1. Roteiro, mapa de cenas e orçamento (Portão 2)

- Estruture cada cena em `produtos/<slug>/roteiro.md` com **ação física do personagem Inspetor Bicho Grilo** (lupa articulada descendo do chapéu, lanterna iluminando, expressão de sobrancelha, gestos) e **demonstração visual em movimento sincronizada com a fala** (como movimento mecânico, fluxo de fluido, montagem ou comparação técnica de componentes).
- Exiba em tela apenas o **produto real anunciado** (`REQ-003`), utilizando recortes de imprensa ou documentos oficiais quando precisar dar prova visual a fatos históricos ou certificações.
- Inclua diretamente em `roteiro.md` (antes da aprovação do Portão 2):
  1. **Falas cronometradas e estimativa de duração total** com foco nas características técnicas duradouras do produto e indicação de elegibilidade ao Mercado Livre Clips (fala isenta de preço variável e presença de trecho real de uso prático);
  2. **Dicionário fonético de TTS:** mapeamento de siglas, nomes estrangeiros e unidades técnicas para pronúncia falada natural (ex.: `"LED"` → `"léde"`, `"USB-C"` → `"ú ésse bê cê"`, `"mm"` → `"milímetros"`), mantendo a grafia técnica correta nas legendas visuais;
  3. **Mapa de cenas por motor visual (`REQ-003`):** classificação explícita de cada trecho entre **`Rig 2.5D`**, **`Flow Omni 360p -> 1080p` (`flow_ia`)** e **`Determinístico`**, com miniaturas/links das referências visuais já incorporados para visualização no *preview* de Markdown;
  4. **Orçamento explícito de créditos do Google Flow:** total de créditos previstos em `Omni Flash 1.2 · 360p` (`1 crédito/s` até `10s`) para aprovação antes de qualquer geração de vídeo.
- Aguarde a aprovação explícita do Portão 2 no chat antes de sintetizar áudio, gerar clipes no Flow ou renderizar (`REQ-004`).

## 2. Direção de Arte e Stack Técnico Real (entre Portão 2 e Portão 3)

- **Grid de palco `9:16` e Área Segura (`1080×1920`):** mantenha todos os elementos críticos (produto, rosto do apresentador, chamadas visuais e legendas) dentro da área livre verificada em [0006](../../../docs/decisoes/0006-governanca-qualidade-finops-e-composicao-visual.md) (**`X = 48..887 px`** — com margem esquerda interna conservadora `≥ 65 px` — e **`Y = 288..1247 px`**, ou coordenadas proporcionais em baixa resolução), deixando livres as margens ocupadas pelas interfaces das plataformas.
- **Legendas dinâmicas em blocos curtos:** exiba legendas de **1 a 3 palavras por batida** com destaque visual na palavra ativa (fonte *bold* branca com contorno escuro nítido), posicionadas em **`Y = 1040–1220 px`** (`1080×1920`) acima da barra inferior das redes.
- **Critério visual por natureza da cena (`REQ-015`):**
  - **Cenas externas, ambiente e uso real (`flow_ia`):** utilize a **Web UI do Google Flow** na assinatura **Google AI Pro** com **`Omni Flash 1.2 · 360p`** (*Text*, *Frames*, *Ingredients* ou *Video-to-Video Editing* em `9:16`, `1 crédito/s` até `10s`) guiado pela foto real do produto no Portão 3, promovendo o clipe aprovado para **`1080p` a `0` crédito** no Portão 4 (até `10s`).
  - **Mecanismos internos, esquemas técnicos e medidas (`Determinístico`):** utilize composição programática em **Python (`Pillow`/`numpy`) + `ffmpeg` (`overlay`/`videotoolbox`/`libx264`)** ancorada em foto real da peça aberta ou diagrama oficial do fabricante, gerando setas direcionais, camadas, rótulos exatos e legendas em quadros nítidos compatíveis com o hardware local.
- **Áudio TTS, trilha/SFX e *lip-sync* nativo PT-BR:** sintetize a locução via **`edge-tts`** (partida imediata no Degrau 0) ou via evolução gratuita oficial **`Azure AI Speech F0`** (`500.000` chars/mês grátis com marcas `WordBoundary` e visemas quando suportados pela voz `pt-BR`), validando imediatamente **`arquivo > 0 bytes`** e marcas temporais e acionando **`Piper pt_BR`** offline em CPU com alinhamento por frase e RMS caso ocorra indisponibilidade do endpoint. Aplique **mapeamento determinístico grafema→visema para português em Python** no Rig 2.5D e utilize trilha/SFX sob licença comercial válida no Degrau 0 (`YouTube Audio Library`/`CC0` ou áudio nativo Flow).
- **Escada de investimento e caixa de ferramentas (`0006`):** mantenha disponíveis os planos *Free* de fornecedores comerciais (`ElevenLabs Free`, `Recraft Web Free`, `Suno Free`) para provas de conceito (PoCs) e avaliação interna de ganho real antes de assinar; componha o pacote publicado no **Portão 4** exclusivamente com ativos gerados sob licença comercial válida (em cota gratuita comercial ou já no plano pago/API comercial ativado nos Degraus 1 e 2 conforme [0006](../../../docs/decisoes/0006-governanca-qualidade-finops-e-composicao-visual.md), respeitando fornecedores que exigem geração final em conta paga).
- **Validação rápida por *styleframes* locais:** monte 1 quadro estático de composição por cena aproveitando exclusivamente os ativos locais já existentes (economizando integralmente créditos de nova geração de imagem) para confirmar enquadramento, escala e contraste antes de gerar `preview.mp4`.

## 3. Revisão em Camadas Antes da Entrega ao Usuário (`REQ-014`)

Execute a verificação respeitando a separação entre os portões (`REQ-002` e `REQ-004`) e inclua o resumo objetivo de aprovação junto ao entregável apresentado no chat:

### Antes do Portão 2 (`roteiro.md`)
1. **Validação determinística de texto e plano (script local):** confira objetivamente o teto calibrável de até **15 palavras por frase** na locução ([0006](../../../docs/decisoes/0006-governanca-qualidade-finops-e-composicao-visual.md)), a estimativa de duração falada, o preenchimento do dicionário fonético para siglas/unidades detectadas, a classificação de todas as cenas por motor, a soma exata do orçamento de créditos Flow e a validade dos links/referências em `roteiro.md`.
2. **Agente Crítico de Roteiro (subagente `flash` em contexto isolado, máximo de 2 rodadas):** forneça exclusivamente `ficha.md` e `roteiro.md` para aprovar: (a) oralidade conversacional direta em frases curtas, (b) abertura com gancho claro nos primeiros 3 segundos, (c) fidelidade integral aos fatos verificados em `ficha.md` e (d) coerência direta entre cada fala e a ação visual correspondente.

### Antes dos Portões 3 (`preview.mp4`) e 4 (pacote final `1080×1920`)
1. **Validação determinística de mídia e enquadramento (script local):** confira integridade da faixa de áudio (`> 0 bytes` com marcas temporais/visemas no `Azure F0`/`edge-tts` ou segmentação por frase/RMS no fallback `Piper pt_BR`), enquadramento de todos os elementos e legendas na área segura (**`X = 48..887 px`**, **`Y = 288..1247 px`** ou faixa proporcional), presença em disco de todos os ativos/vídeos referenciados, acionamento automático do aviso de IA (`REQ-007`) sempre que houver cena `flow_ia` e confirmação de licença comercial válida nos ativos que entram no pacote final do Portão 4.
2. **Agente Inspetor Visual Multimodal (subagente `flash` em contexto isolado):** inspecione os *styleframes* e quadros-chave gerados confirmando nitidez das legendas e rótulos, destaque claro do produto real, separação limpa entre legendas, rosto e acessórios do apresentador, e aderência ao critério visual por natureza da cena.

## 4. Geração de imagens por IA (`REQ-012`)

- Solicite a menor resolução útil (`512px` / `0.5K`, ~747 tokens) em provas de conceito, rascunhos e exploração visual.
- Reserve resoluções maiores (`1K+`) exclusivamente para a arte final aprovada.

## 5. *Preview* de calibração (Portão 3) e Pacote Final (Portão 4)

- **Portão 3 (ativo durante calibração; dispensável após decisão explícita do usuário):** gere a narração verificada e `preview.mp4` combinando o Rig 2.5D em *lip-sync* determinístico PT-BR, composições determinísticas (`Pillow`/`numpy` + `ffmpeg`) e os clipes **`Omni 360p`** já prontos para promoção a `1080p` (ou edição pontual *video-to-video*), permitindo validar voz, ritmo, legendas e movimento real no player padrão do sistema (`REQ-005`).
- **Portão 4 (`REQ-006`, `REQ-007`, `REQ-008`):** após aprovação do Portão 3 (ou diretamente após o Portão 2 quando o Portão 3 estiver dispensado), promova os clipes `Omni 360p` aprovados para **`1080p` (`0` crédito até `10s` no Google AI Pro)**, execute a montagem final `9:16` (`1080×1920`) via `Python (Pillow/numpy) + ffmpeg (overlay/videotoolbox)`, entregue o MP4 final limpo composto exclusivamente por ativos com licença comercial válida junto com `pacote.md` (legenda, palavras-chave/tags, código curto da vitrine, link principal de afiliado, palavra-chave de DM `REQ-010` e aviso determinístico de IA `REQ-007`) e atualize a vitrine estática na bio logo após a aprovação final no chat (`REQ-008`).
