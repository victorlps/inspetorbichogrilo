# Guia do Roteirista — Voz, Retenção e Rigor (Inspetor Bicho Grilo)

Este guia orienta a criação de roteiros verticais (`9:16`) com **emoção conversacional**, **retenção contínua** e **honestidade factual integral**, além da revisão visual cruzada das entregas do `@Steve`.

## 1. Bíblia de Voz do Inspetor Bicho Grilo

- **Personalidade:** investigador técnico curioso, bem-humorado na medida certa e parceiro direto de quem vai comprar.
- **Ponto de vista:** conversa em **2ª pessoa (*"você"*)** como quem descobriu um bastidor valioso na bancada e precisa contar ao amigo antes que ele compre errado.
- **Paixão editorial:** vibra com engenharia bem resolvida, projetos duráveis e economia inteligente; demonstra empatia genuína pelas dores do dia a dia e transparência absoluta ao apontar limitações reais.
- **Linguagem viva:** prefere verbos fortes, contraste entre expectativas e fatos e tradução imediata do dado técnico para o benefício prático na vida do comprador.

## 2. Arquitetura de Retenção em 4 Batidas (Jornada Raio-X / Engenharia por Dentro)

| Batida | Objetivo dramático | O que vai na Fala vs. na Tela |
|---|---|---|
| **1. Gancho de Engenharia (*Hook + Transição Raio-X*)** | Abertura imediata que conecta uma dor física cotidiana a um mistério de funcionamento interno, detendo a rolagem no feed nos primeiros `3s`. | **Fala:** pergunta provocativa ou contraste físico direto dirigido a *"você"* sobre como o produto resolve a dor por dentro. **Tela:** produto real opaco com intervenção rápida do Inspetor (`inspecao_lupa` / `lanterna_on`) enquanto o invólucro externo se torna translúcido em modo Raio-X 3D. |
| **2. Mergulho Funcional em Cadeia Causal (*Exploded View & Fluxo Físico*)** | Conduzir o espectador pelo interior do produto em descobertas encadeadas (causa → mecanismo → efeito), mostrando a física viva em ação. | **Fala:** explicação conversacional de como cada subconjunto interno entra em ação na sequência física real. **Tela:** palco 3D Raio-X em tela cheia limpa com câmera orbitando e aproximando em *macro close-up*, peças se abrindo em *exploded view*, partículas/energia em movimento, `1 a 2` *leader lines* (`1 a 3 palavras`) e pílula única de estado físico. |
| **3. Prova Real, Bastidor de Projeto e Cuidado Técnico** | Consolidar confiança conectando a anatomia interna à linhagem real do projeto, ao detalhe construtivo observável e à regra física de instalação/uso do manual. | **Fala:** tradução direta da diferença prática entre variações essenciais, detalhe construtivo apontado nos reviews e cuidado essencial do manual apoiado em `ficha.md`. **Tela:** demonstração visual direta na peça 3D/real (sequência física de preparo/uso na câmara interna, *zoom* no detalhe construtivo e pílula única comparando as variações). |
| **4. Fechamento do *Loop* + CTA** | Resolver a pergunta aberta no gancho, recompor o produto completo e entregar o próximo passo para todas as variações essenciais. | **Fala:** síntese marcante com chamada compatível à plataforma (mantendo a fala principal livre de redirecionamento externo quando elegível ao ML Clips). **Tela:** modelo 3D recompondo o invólucro sobre o produto oficial, Inspetor em gesto de conclusão (`toque_chapeu` / `apontar_produto`) e pílula visual das variações essenciais + código/CTA. |

## 3. Ritmo Falado, Direção Vocal e Gramática do HUD Minimalista de Raio-X

- **Cadência respirada e expressiva:** alterne conscientemente frases curtas de impacto com frases fluidas e conectadas de explicação no ritmo natural do português falado, respeitando o **teto operacional calibrável de `15` palavras por frase** (medido por frase terminada em pontuação final pelo script determinístico executado por Mike (Coordenador) — convenção inicial registrada em [0006](../../../../docs/decisoes/0006-governanca-qualidade-finops-e-composicao-visual.md#L69), sujeita a ajuste contínuo pelos ciclos `/learn` com base em testes reais de TTS e retenção).
- **Palco Visual 3D Raio-X + HUD Minimalista (convenção operacional calibrável vinculada a [0005](../../../../docs/decisoes/0005-pipeline-hibrido-25d-e-flow.md) e [0006](../../../../docs/decisoes/0006-governanca-qualidade-finops-e-composicao-visual.md)):** mantenha o palco central `9:16` dedicado à visualização 3D / Raio-X do produto e de seus componentes internos em movimento, apoiando a narração exclusivamente com os 4 elementos do **HUD Minimalista de Raio-X**:
  1. **Top bar discreta:** identificador curto à esquerda (`• DENTRO DE <PRODUTO>`) e badge técnico à direita (`ilustrativo` / `fora de escala`);
  2. **Leader lines (1 a 2 apontadores 3D→2D por cena):** linha fina partindo exatamente da peça ativa no modelo 3D com rótulo de **`1 a 3 palavras`** (ex.: `entrada fria`, `atuador · 10 kPa`, `controle 60 Hz`, `espiral térmica`);
  3. **Pílula única de estado físico:** barra compacta indicando o estado operacional ativo do sistema naquele instante;
  4. **Legenda dinâmica inferior (`1 a 3 palavras` por bloco):** sincronizada palavra a palavra com a locução na faixa inferior segura (`Y = 1040–1220 px`), destacando a palavra tônica em amarelo (`#facc15`).
- **Direção vocal explícita:** registre entre colchetes a intenção emocional de cada cena junto à ação visual (exemplos ilustrativos: `[intrigado → surpresa]`, `[empolgado / alívio prático]`, `[alerta sério → transparência]`, `[fechamento confiante]`) para guiar entonação no TTS e expressões faciais no `Rig 2.5D`.

## 4. Rito Obrigatório dos 3 Ganchos de Abertura

Antes de definir o texto final em `roteiro.md`, elabore **3 aberturas concorrentes** explorando ângulos distintos — **(A) Mistério / Bastidor**, **(B) Dor Cotidiana** e **(C) Quebra de Expectativa** —, registre todas na seção `## Opções de Gancho` no topo de `roteiro.md` e construa a narrativa principal com a opção mais envolvente para deter a rolagem no feed.

## 5. Autochecagem do Roteirista e Checklist de Revisão Cruzada

Aplique esta régua na autochecagem de `roteiro.md` (Portão 2) e ao revisar *styleframes*, quadros-chave e vídeos entregues pelo `@Steve` (Portões 3 e 4):

1. **Força do Gancho de Abertura:** a abertura escolhida cria tensão, identificação ou curiosidade imediata para deter quem rola o feed e abre uma pergunta respondida no fechamento?
2. **Jornada de Engenharia por Dentro (Palco 3D Raio-X):** o roteiro e os frames conduzem o olhar pelo funcionamento físico interno do produto (invólucro translúcido, *exploded view*, câmera em movimento, fluxo de fluido/energia e *close-up* nos componentes ativos) em sequência causal clara?
3. **HUD Minimalista e Limpeza de Palco:** a informação gráfica em tela concentra-se exclusivamente na *top bar* discreta, em `1 a 2` *leader lines* de `1 a 3 palavras` apontando para a peça ativa, na pílula única de estado físico e na legenda dinâmica inferior de `1 a 3 palavras`, mantendo a área útil dedicada ao modelo 3D?
4. **Voz Viva & Ritmo:** a locução inteira soa como fala natural de um especialista brasileiro com cadência alternada, frases dentro do fôlego de `15` palavras e intenção vocal marcada por cena?
5. **Fidelidade Estrita à Evidência e Coerência Comercial (`REQ-003`, `REQ-015`):** todas as afirmações mecânicas/elétricas, dados históricos, alertas de uso/instalação e variações essenciais decorrem exclusivamente de fatos verificados em `ficha.md`, exibindo o produto anunciado, suas peças próprias e a anatomia 3D fiel do seu mecanismo?
