# Bíblia de Formato — Inspetor Bicho Grilo (`9:16`)

Fonte única operacional de identidade editorial, voz, gramática de animação visual e parâmetros técnicos verticais (`9:16`), derivada de [0004-identidade-visual-personagem.md](../../docs/decisoes/0004-identidade-visual-personagem.md), [0005-pipeline-hibrido-25d-e-flow.md](../../docs/decisoes/0005-pipeline-hibrido-25d-e-flow.md), [0006-governanca-qualidade-finops-e-composicao-visual.md](../../docs/decisoes/0006-governanca-qualidade-finops-e-composicao-visual.md), [0008-sala-de-producao-coautoria-e-tres-portoes.md](../../docs/decisoes/0008-sala-de-producao-coautoria-e-tres-portoes.md), [0010-motor-video-programatico-web-deterministico.md](../../docs/decisoes/0010-motor-video-programatico-web-deterministico.md) e [fase-1.md](../../docs/requisitos/fase-1.md) (`REQ-015`).

---

## 1. Identidade Editorial e Invariantes da Marca (valem para qualquer tema e produto)

- **Identidade editorial (*"Como as coisas funcionam?"*):** cada episódio é uma investigação visual e informativa sobre o fenômeno principal, a engenharia interna ou o processo físico de fabricação do tema — respondendo com clareza *o que é aquilo, como funciona ou é fabricado, o que diferencia essa técnica das alternativas existentes e por que ela entrega vantagem real na prática* — em **2ª pessoa (*"você"*)**, com curiosidade técnica e bom humor na medida certa.
- **Entrada orgânica e pontual do produto exemplar:** o produto curado entra na narrativa exatamente no momento em que a explicação do fenômeno encontra sua aplicação concreta no mundo real, ocupando apenas uma fração pontual do episódio como exemplar auditado; o catálogo completo de variações, fichas comerciais e links fica concentrado em `pacote.md` e na vitrine da bio.
- **Clareza para o público leigo (Analogia + Causa Física):** todo princípio científico, etapa industrial ou mecanismo de engenharia é traduzido imediatamente por uma **analogia cotidiana tangível** ligada ao efeito físico percebido na prática.
- **Duração, ritmo e cadência vocal orgânicos:** a duração total do episódio, a quantidade de cenas e a velocidade da locução nascem organicamente da profundidade do tema e da respiração natural da fala humana (alternando perguntas/frases curtas com explicações fluidas em torno de **`~15` palavras por frase** como referência calibrável de fôlego falado, e registrando a intenção vocal entre colchetes por cena, ex.: `[curioso → descoberta clara]`). Quando uma plataforma exigir teto curto específico (como Mercado Livre Clips em até `60s`), gera-se um corte derivado independente sob demanda, preservando o episódio principal em seu tempo natural.
- **Rigor científico e factual:** toda explicação de fenômeno, comparação entre técnicas, dado numérico e característica do exemplar decorre exclusivamente do dossiê verificado em `produtos/<slug>/ficha.md`.
- **Área segura `9:16` (`1080×1920`):** todos os elementos de foco, rótulos espaciais, rosto do personagem e legendas operam dentro de **`X = 48..887 px`** e **`Y = 288..1247 px`** (folga lateral esquerda recomendada **`X ≥ 65 px`** para compatibilidade com Reels).
- **Legendas dinâmicas:** blocos curtos de **`1 a 3 palavras`** por batida na faixa **`Y = 1040–1220 px`**, sincronizados palavra a palavra com destaque na tônica ativa e ocultação limpa nas pausas respiratórias.

---

## 2. Lentes Criativas de Episódio (escolhidas em coautoria)

`@Carlos` e `@Steve` escolhem no Portão 2 a lente (ou combinação de lentes) que torna o funcionamento do tema imediatamente visível desde os primeiros `3s`:

| Lente | Quando escolher | Jornada investigativa | Gramática visual (`@Steve`) |
|---|---|---|---|
| **1. Engenharia / Raio-X por Dentro** | Eletroeletrônicos, ferramentas, válvulas ou sistemas cujo segredo está no mecanismo interno. | Abre no contraste funcional ou mistério mecânico e mergulha dentro da peça em operação. | Palco escuro técnico (`#090a0f`, *Fresnel* `#00e5ff`), vistas explodidas animadas e compartimentos fisicamente estanques com fluxos contínuos confinados aos seus dutos reais. |
| **2. Ciência do Processo / "Como é Feito"** | Alimentos técnicos, materiais avançados ou insumos cujo diferencial nasce da transformação física/industrial. | Abre no contraste sensorial entre matéria-prima e resultado, revela a transformação celular/física passo a passo e confronta com métodos rivais. | Simulações procedurais animadas em corte (`Canvas 2D / SVG / WebGL`) mostrando mudança de fase, temperatura, pressão e estrutura microscópica em movimento contínuo, combinadas a macros reais. |
| **3. Dinâmica Física em Campo / Comparativo** | Equipamentos outdoor, EDC, casa ou esporte onde a física aparece no peso, resistência, isolamento ou ergonomia em uso. | Abre direto na situação física real em campo, demonstra visualmente a diferença mecânica/energética entre abordagens e apresenta o exemplar em ação. | Planos de ação em ambiente real (`flow_ia` ou ativo verificado) articulados a simulações físicas comparativas (balança, transferência térmica, tensão, volume) em tela aberta. |

---

## 3. Gramática de Animação Visual, Rótulos Espaciais e Presença do Inspetor (`@Steve`)

- **Demonstração visual animada (`Estado A → Ação Física → Estado B`):** cada cena responde à pergunta da narrativa por **transformação visual contínua em movimento** (ex.: tecido celular congelando e sublimando vapor sob vácuo; comparação física lado a lado onde uma estrutura colapsa sob calor enquanto outra mantém poros abertos; balança física reagindo à perda de água; caminhada real na montanha), enquanto toda a argumentação verbal flui pela voz e pela legenda dinâmica.
- **Palco aberto e orçamento enxuto de palavras na tela:** para que o olho acompanhe o fenômeno animado, a cena opera em tela aberta com no máximo **`1` pílula curta de contexto** e **`1 a 2` rótulos espaciais de `1 a 3 palavras`** (ou grandeza física pontual como `-40 °C`, `Alto Vácuo`, `Gelo → Vapor`) ancorados diretamente às partes do objeto em transformação, mantendo o total simultâneo fora da legenda em **até `14` palavras visíveis** *(convenção calibrável vinculada a [0006](../../docs/decisoes/0006-governanca-qualidade-finops-e-composicao-visual.md) e [0010](../../docs/decisoes/0010-motor-video-programatico-web-deterministico.md))*.
- **Presença do Inspetor (`Rig 2.5D`):** atua como anfitrião curioso em entradas pontuais (gancho, reação curta em PiP ou fechamento), cedendo a tela inteira (`show_rig: false`) nos momentos de simulação microscópica/física detalhada ou paisagem cinematográfica; quando presente, a área de simulação ocupa a faixa superior acima da silhueta do chapéu e das antenas.

---

## 4. Motores Visuais por Natureza da Cena

- **`Rig 2.5D`:** apresentador Inspetor Bicho Grilo com *lip-sync* determinístico PT-BR e camadas pré-carregadas sincronizadas quadro a quadro.
- **`Flow Omni 360p -> 1080p` (`flow_ia`):** planos cinematográficos ou macro de fenômenos físicos e cenas humanas em ambiente natural (gerados em `360p`, promovidos gratuitamente na Web UI do Google Flow e masterizados em `1080×1920`, conforme [0006](../../docs/decisoes/0006-governanca-qualidade-finops-e-composicao-visual.md) e [0010](../../docs/decisoes/0010-motor-video-programatico-web-deterministico.md)), priorizando fenômenos visuais puros e ação humana natural, sobrepondo o recorte oficial real quando o produto exemplar é apresentado. Dispara aviso determinístico de IA (`REQ-007`).
- **`Determinístico`:** simulações físicas, termodinâmicas e celulares procedurais em `HTML5 Canvas 2D / SVG / WebGL`, comparativos mecânicos lado a lado e composições executadas pelo **Motor Web Determinístico** orientado a manifesto (`src/video/web_engine/`, conforme [0010](../../docs/decisoes/0010-motor-video-programatico-web-deterministico.md), mantendo compatibilidade com scripts `Pillow/numpy` e estúdios `Three.js`), ancoradas nos dados científicos e ativos verificados de `ficha.md`.

---

## 5. Referências Externas de Qualidade

As referências visuais de qualidade desta bíblia vêm exclusivamente de referências externas aprovadas pelo usuário. Esta seção permanece aberta para catalogar novos quadros e links externos conforme forem selecionados.

- **Animação Explicativa "Como Funciona" / Raio-X por Dentro (`voceaprendeu.shop` — `@voceaprendeu` e `@teensinei`, informado pelo usuário e lido em `2026-11-20`):** palco limpo com objeto/sistema em transformação física contínua, *leader lines* finas de `1 a 3 palavras` ancoradas diretamente na estrutura animada, indicador único de estado físico e legenda dinâmica sincronizada com palavra tônica destacada e sublinhada em amarelo (`#facc15`).
