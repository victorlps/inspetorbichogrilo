# Bíblia de Formato — Inspetor Bicho Grilo (`9:16`)

Fonte única operacional para estrutura de episódio, voz, linguagem acessível, HUD, coreografia visual e enquadramento vertical (`9:16`), derivada de [0004-identidade-visual-personagem.md](../../docs/decisoes/0004-identidade-visual-personagem.md), [0005-pipeline-hibrido-25d-e-flow.md](../../docs/decisoes/0005-pipeline-hibrido-25d-e-flow.md), [0006-governanca-qualidade-finops-e-composicao-visual.md](../../docs/decisoes/0006-governanca-qualidade-finops-e-composicao-visual.md), [0008-sala-de-producao-coautoria-e-tres-portoes.md](../../docs/decisoes/0008-sala-de-producao-coautoria-e-tres-portoes.md) e [fase-1.md](../../docs/requisitos/fase-1.md) (`REQ-015`).

---

## 1. Identidade, Voz e Linguagem Acessível

- **Personalidade:** investigador técnico curioso, bem-humorado na medida certa e parceiro direto de quem vai comprar.
- **Ponto de vista:** conversa em **2ª pessoa (*"você"*)** como quem descobriu um bastidor valioso e precisa explicar ao amigo antes que ele compre errado.
- **Engenharia e processos traduzidos ao leigo (Analogia + Benefício Principal):** todo termo técnico (componente, princípio físico ou etapa industrial) é introduzido como curiosidade e traduzido imediatamente por uma **analogia cotidiana clara** conectada ao **benefício prático principal** que o comprador sente no uso real.
- **Ritmo falado e fôlego:** alterne frases curtas de impacto com explicações fluidas, respeitando o parâmetro operacional calibrável de até **`15` palavras por frase** (tanto literal quanto na expansão do Dicionário Fonético, conforme `0006`).
- **Direção vocal:** registre entre colchetes a intenção emocional de cada cena (ex.: `[intrigado → alívio prático]`) para guiar o TTS e as expressões do `Rig 2.5D`.

## 2. Arquitetura Narrativa e Coreografia (`Produto Real ↔ Por Dentro ↔ Uso Real ↔ Produto Real`)

O episódio vertical (`~45–60s`) segue quatro batidas conectadas:

| Batida | Função dramática | Camada Narrativa (`@Carlos`) | Camada Visual (`@Steve`) |
|---|---|---|---|
| **1. Gancho & Dor Real (`0–3s`+)** | Deter a rolagem nos primeiros `3s` ligando uma dor cotidiana ao benefício principal do produto. | Pergunta ou contraste direto ao espectador. | Foto oficial nítida do produto real com intervenção do Inspetor (`Rig 2.5D`) acionando a transição (*scanner* / *cross-fade* alinhado) para o modo "Por Dentro". |
| **2. Costura Causal ("Por Dentro": Raio-X 3D ou Processo)** | Responder diretamente ao gancho explicando *como* o mecanismo interno ou o processo de fabricação entrega o benefício. | Analogia cotidiana imediata + explicação causal conectada ao gancho. | Palco em tela cheia limpa (`Rig 2.5D` fora de quadro): modelo Raio-X 3D (`#00e5ff`) com **compartimentos fisicamente estanques** (fluidos/fluxos confinados ao seu duto/câmara, separados de eletrônica seca) ou diagramação animada em etapas de processo (ex.: sublimação/liofilização), guiada por `SCRIPT_BEATS`. |
| **3. Uso Prático Real + Prova/Cuidado** | Provar o benefício funcionando na vida real e dar transparência sobre instalação, manutenção, composição ou variações. | Demonstração do benefício + alerta prático ou comparativo fiel a `ficha.md`. | Clipe/foto real do produto funcionando em uso prático (`flow_ia` ou ativo real verificado) pareado ao detalhe fotográfico da peça/ingrediente ou comparativo de variações essenciais. |
| **4. Fechamento do *Loop* + CTA** | Fechar a pergunta do gancho reafirmando o benefício e orientar o próximo passo para todas as variações. | Síntese confiante + chamada compatível com a plataforma (sem preço variável/redirecionamento proibido no ML Clips). | Recomposição para a foto oficial real do produto, retorno do Inspetor (`Rig 2.5D`) em gesto de conclusão e pílula final com variações essenciais e código/CTA. |

## 3. Palco `9:16`, Área Segura e HUD Minimalista

Parâmetros decididos em `0006` e `REQ-015` (fonte operacional única):

- **Resolução e proporção:** `1080×1920` (`9:16`), fundo de palco Raio-X em `#090a0f` com contorno *Fresnel* ciano `#00e5ff`.
- **Área segura rígida:** **`X = 48..887 px`**, **`Y = 288..1247 px`** (adotando folga lateral esquerda recomendada **`X ≥ 65 px`** para compatibilidade com Reels).
- **HUD Minimalista (máximo de 4 elementos simultâneos, todos em linguagem leiga):**
  1. **Top bar discreta:** identificador curto (`• <PRODUTO>`) + badge contextual (`ilustrativo`, `corte 3D`, `uso real`).
  2. **Leader lines (1 a 2 apontadores por cena):** linha fina ancorada na peça/etapa ativa com rótulo de **`1 a 3 palavras`** descrevendo a função prática.
  3. **Pílula única de estado e benefício:** barra compacta na parte superior/média (`Y = 288..1020 px`) traduzindo o estado físico no benefício real.
  4. **Legendas dinâmicas inferiores:** blocos curtos de **`1 a 3 palavras`** por batida na faixa **`Y = 1040–1220 px`**, fonte *bold* branca com contorno escuro nítido e palavra ativa destacada em amarelo (`#facc15`).

## 4. Motores Visuais por Natureza da Cena

- **`Rig 2.5D`:** apresentador Inspetor Bicho Grilo com *lip-sync* determinístico PT-BR na abertura, reações pontuais e fechamento; cede a tela cheia nas cenas técnicas.
- **`Flow Omni 360p -> 1080p` (`flow_ia`):** cenas externas, atmosfera natural e uso prático real guiado por foto real do produto (`1 crédito/s` em `360p` até `10s`; *upscale* a `1080p` a `0` crédito até `10s`). Dispara aviso determinístico de IA (`REQ-007`).
- **`Determinístico`:** mecanismos internos em Raio-X 3D, vistas explodidas, fluxogramas/processos de fabricação animados e comparativos técnicos via `Python (numpy/Pillow) + ffmpeg` (e estúdio interativo `Three.js` quando aplicável), ancorados nos ativos reais e diagramas de `ficha.md`.

## 5. Referências Externas de Qualidade

As referências visuais de qualidade desta bíblia devem vir exclusivamente de referências externas aprovadas pelo usuário (não de entregas internas ainda em calibração). Esta seção permanece aberta para catalogar os quadros e links externos de referência conforme forem selecionados.
