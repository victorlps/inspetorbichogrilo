# Guia do Roteirista — Voz, Retenção e Rigor (Inspetor Bicho Grilo)

Este guia orienta a criação de roteiros verticais (`9:16`) com **emoção conversacional**, **retenção contínua** e **honestidade factual integral**, além da revisão visual cruzada das entregas do `@Steve`.

## 1. Bíblia de Voz do Inspetor Bicho Grilo

- **Personalidade:** investigador técnico curioso, bem-humorado na medida certa e parceiro direto de quem vai comprar.
- **Ponto de vista:** conversa em **2ª pessoa (*"você"*)** como quem descobriu um bastidor valioso na bancada e precisa contar ao amigo antes que ele compre errado.
- **Paixão editorial:** vibra com engenharia bem resolvida, projetos duráveis e economia inteligente; demonstra empatia genuína pelas dores do dia a dia e transparência absoluta ao apontar limitações reais.
- **Linguagem viva:** prefere verbos fortes, contraste entre expectativas e fatos e tradução imediata do dado técnico para o benefício prático na vida do comprador.
- **Engenharia traduzida para o leigo (Regra da Analogia + Benefício Principal):** sempre que apresentar um componente técnico ou princípio físico (semicondutor, atuador, sensor, modulação), introduza-o como um gancho de curiosidade traduzido por uma **analogia cotidiana imediata** (ex.: *"funciona como um dimmer que regula a potência milímetro a milímetro"*) e conecte-o diretamente ao **benefício prático principal do produto** na vida do comprador.

## 2. Arquitetura de Retenção em 4 Batidas (`Produto Real → Raio-X 3D → Uso Real → Produto Real`)

| Batida | Objetivo dramático | O que vai na Fala vs. na Tela |
|---|---|---|
| **1. Gancho Conectado à Dor Real (*Produto Real → Transição Raio-X*)** | Abertura imediata que contrasta a limitação do produto comum citado no gancho com a promessa física do produto analisado, detendo a rolagem nos primeiros `3s`. | **Fala:** pergunta provocativa ou contraste direto dirigido a *"você"* sobre a dor cotidiana que o produto resolve. **Tela:** **foto oficial nítida do produto real** com intervenção rápida do Inspetor (`inspecao_lupa` / `lanterna_on`), iniciando a transição alinhada do invólucro para o modo Raio-X 3D. |
| **2. Costura Causal e Mergulho Funcional (*Exploded View + Analogia Acessível*)** | Responder diretamente ao problema levantado no gancho, explicando o mecanismo interno por analogia simples e mostrando como ele entrega o benefício principal. | **Fala:** costura direta com o gancho (por que o sistema comum falha vs. como o mecanismo interno deste produto regula ou atua gradualmente sem perda de desempenho). **Tela:** palco 3D Raio-X com **delimitação física explícita entre compartimentos** (fluido contido exclusivamente dentro da tubulação/câmara vedada, separado da placa eletrônica seca), *exploded view*, `1 a 2` *leader lines* em português intuitivo (`1 a 3 palavras`) e pílula única traduzindo o benefício ativo. |
| **3. Produto Real Funcionando em Uso Prático + Cuidado Técnico** | Provar o benefício principal na vida real com o produto em operação e consolidar confiança com o bastidor construtivo e a regra física de instalação/uso do manual. | **Fala:** demonstração clara do benefício principal em operação real seguida do detalhe construtivo verificado em `ficha.md` e do cuidado essencial de uso/instalação. **Tela:** **vídeo/imagem real do produto funcionando de verdade em uso prático** (`flow_ia` + foto real em operação demonstrando o controle e o desempenho), seguido do detalhe fotográfico/3D da peça e da pílula comparativa das variações essenciais. |
| **4. Fechamento do *Loop* com Produto Real + CTA** | Fechar a pergunta aberta no gancho reafirmando o benefício principal, exibir o produto real completo e entregar o próximo passo para todas as variações essenciais. | **Fala:** síntese do benefício principal com chamada compatível à plataforma (mantendo a fala principal livre de redirecionamento externo quando elegível ao ML Clips). **Tela:** recomposição do modelo 3D para a **foto oficial nítida do produto real**, Inspetor em gesto de conclusão (`toque_chapeu` / `apontar_produto`) e pílula visual das variações essenciais + código/CTA. |

## 3. Ritmo Falado, Direção Vocal e Gramática do HUD Minimalista de Raio-X

- **Cadência respirada e expressiva:** alterne conscientemente frases curtas de impacto com frases fluidas e conectadas de explicação no ritmo natural do português falado, respeitando o **teto operacional calibrável de `15` palavras por frase** (medido por frase terminada em pontuação final pelo script determinístico executado por Mike (Coordenador) — convenção inicial registrada em [0006](../../../../docs/decisoes/0006-governanca-qualidade-finops-e-composicao-visual.md#L69), sujeita a ajuste contínuo pelos ciclos `/learn` com base em testes reais de TTS e retenção).
- **Palco Visual 3D Raio-X + HUD Minimalista (convenção operacional calibrável vinculada a [0005](../../../../docs/decisoes/0005-pipeline-hibrido-25d-e-flow.md) e [0006](../../../../docs/decisoes/0006-governanca-qualidade-finops-e-composicao-visual.md)):** mantenha o palco central `9:16` dedicado à visualização 3D / Raio-X do produto e de seus componentes internos em movimento, apoiando a narração exclusivamente com os 4 elementos do **HUD Minimalista de Raio-X**:
  1. **Top bar discreta:** identificador curto à esquerda (`• DENTRO DE <PRODUTO>`) e badge técnico à direita (`ilustrativo` / `fora de escala`);
  2. **Leader lines intuitivas para o leigo (1 a 2 apontadores 3D→2D por cena):** linha fina partindo exatamente da peça ativa no modelo 3D com rótulo de **`1 a 3 palavras` em português claro que descreve a função prática da peça** (ex.: `haste gradual`, `regulador eletrônico`, `câmara vedada`, `resistência interna`);
  3. **Pílula única de estado e benefício prático:** barra compacta traduzindo o estado físico ativo no ganho real que o usuário sente (ex.: `🟢 FLUXO 100% FORTE · AJUSTE EXATO`, `🔵 CÂMARA CHEIA · PARTIDA SEGURA`);
  4. **Legenda dinâmica inferior (`1 a 3 palavras` por bloco):** sincronizada palavra a palavra com a locução na faixa inferior segura (`Y = 1040–1220 px`), destacando a palavra tônica em amarelo (`#facc15`).
- **Direção vocal explícita:** registre entre colchetes a intenção emocional de cada cena junto à ação visual (exemplos ilustrativos: `[intrigado → surpresa]`, `[empolgado / alívio prático]`, `[alerta sério → transparência]`, `[fechamento confiante]`) para guiar entonação no TTS e expressões faciais no `Rig 2.5D`.

## 4. Rito Obrigatório dos 3 Ganchos de Abertura

Antes de definir o texto final em `roteiro.md`, elabore **3 aberturas concorrentes** explorando ângulos distintos — **(A) Mistério / Bastidor**, **(B) Dor Cotidiana** e **(C) Quebra de Expectativa** —, registre todas na seção `## Opções de Gancho` no topo de `roteiro.md` e construa a narrativa principal com a opção mais envolvente para deter a rolagem no feed.

## 5. Autochecagem do Roteirista e Checklist de Revisão Cruzada

Aplique esta régua na autochecagem de `roteiro.md` (Portão 2) e ao revisar *styleframes*, quadros-chave e vídeos entregues pelo `@Steve` (Portões 3 e 4):

1. **Costura Causal Gancho → Dor → Benefício Principal:** a cena seguinte ao gancho responde diretamente à pergunta ou contraste da abertura e deixa cristalino o **benefício prático principal do produto** para o usuário?
2. **Engenharia Acessível ao Leigo (Analogia + HUD Intuitivo):** todo componente técnico na fala e no HUD é explicado por sua função prática ou analogia cotidiana simples, mantendo *leader lines* e pílula de estado em linguagem direta e compreensível para o público geral?
3. **Presença do Produto Real Funcionando + Delimitação Física do Raio-X 3D:** o vídeo exibe claramente a **foto oficial do produto real e o clipe/imagem dele funcionando de verdade em uso prático** (`Real → Raio-X 3D → Uso Real → Real`), e o modelo Raio-X 3D separa com paredes/câmaras bem delimitadas o caminho físico do fluido dos componentes eletrônicos secos?
4. **HUD Minimalista, Voz Viva & Ritmo:** o palco mantém apenas os 4 elementos do HUD minimalista (*top bar*, 1–2 *leader lines* de `1 a 3 palavras`, pílula única de estado/benefício e legenda dinâmica inferior de `1 a 3 palavras`), e a locução inteira respeita a cadência natural brasileira com frases dentro do fôlego de `15` palavras?
5. **Fidelidade Estrita à Evidência e Coerência Comercial (`REQ-003`, `REQ-015`):** todas as afirmações mecânicas/elétricas, histórico de marca/linhagem, compatibilidade de peças, alertas de uso/instalação e variações essenciais decorrem exclusivamente de fatos verificados na versão atualizada de `ficha.md`?
