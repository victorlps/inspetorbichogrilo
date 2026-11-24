# Bíblia de Formato — Inspetor Bicho Grilo (`9:16`)

Fonte única operacional de marca, voz, arquitetura criativa e parâmetros técnicos verticais (`9:16`), derivada de [0004-identidade-visual-personagem.md](../../docs/decisoes/0004-identidade-visual-personagem.md), [0005-pipeline-hibrido-25d-e-flow.md](../../docs/decisoes/0005-pipeline-hibrido-25d-e-flow.md), [0006-governanca-qualidade-finops-e-composicao-visual.md](../../docs/decisoes/0006-governanca-qualidade-finops-e-composicao-visual.md), [0008-sala-de-producao-coautoria-e-tres-portoes.md](../../docs/decisoes/0008-sala-de-producao-coautoria-e-tres-portoes.md) e [fase-1.md](../../docs/requisitos/fase-1.md) (`REQ-015`).

---

## 1. Invariantes da Marca (valem para qualquer produto)

- **Personalidade e ponto de vista:** investigador técnico curioso, bem-humorado na medida certa e parceiro direto de quem vai comprar, falando em **2ª pessoa (*"você"*)**.
- **Clareza para o público leigo (Analogia + Benefício Principal):** todo termo técnico, processo industrial ou propriedade de material é traduzido imediatamente por uma **analogia cotidiana clara** conectada ao **benefício prático principal** na vida do comprador.
- **Rigor factual:** toda afirmação, especificação, alerta e cobertura de variações essenciais decorre exclusivamente do que foi verificado em `produtos/<slug>/ficha.md`.
- **Guia de ritmo e direção vocal:** alterne frases curtas de impacto com explicações fluidas (usando **`~15` palavras por frase** como referência de fôlego falado, calibrável por produto) e registre a intenção emocional entre colchetes por cena (ex.: `[intrigado → alívio prático]`).
- **Área segura `9:16` (`1080×1920`):** mantenha todos os elementos críticos (produto, rosto do personagem, legendas e chamadas visuais) dentro de **`X = 48..887 px`**, **`Y = 288..1247 px`** (folga lateral esquerda recomendada **`X ≥ 65 px`** para compatibilidade com Reels).
- **Legendas legíveis:** blocos curtos de **`1 a 3 palavras`** por batida na faixa **`Y = 1040–1220 px`**, com alto contraste e destaque na palavra tônica ativa (paleta definida pela direção de arte para o produto).

---

## 2. Lentes Criativas de Episódio (escolhidas em coautoria)

Em vez de um molde único, `@Carlos` e `@Steve` escolhem no Portão 2 a lente (ou combinação de lentes) que melhor valoriza o produto e prende a atenção nos primeiros `3s`:

| Lente | Quando escolher | Abertura e jornada | Direção de arte (`@Steve`) |
|---|---|---|---|
| **1. Engenharia / Raio-X 3D** | Eletroeletrônicos, ferramentas, mecânica ou produtos onde o valor está no mecanismo interno. | Pode abrir com dor cotidiana + transição para dentro, ou direto no corte interno. | Palco Raio-X (`#090a0f`, *Fresnel* `#00e5ff`), vistas explodidas e **compartimentos fisicamente estanques** (fluidos/fluxos confinados aos seus dutos, separados de partes secas). |
| **2. Processo / "Como é Feito"** | Alimentos, insumos, materiais ou produtos cujo diferencial está na fabricação ou matéria-prima. | Abre na curiosidade sensorial/material ou no resultado final e explica as etapas-chave de transformação. | Paleta e diagramação orgânicas ao tema (antes/depois, macro de textura, fluxograma animado em etapas limpas, sem forçar estética de Raio-X ciano). |
| **3. Teste Prático / Comparativo** | Itens de uso direto (casa, EDC, camping, jardinagem) onde o ganho é ergonômico, de resistência ou comparativo. | Pode abrir direto em **ação real extrema** nos `0–3s` ou em comparação A vs. B antes de explicar o porquê. | Foco em uso prático real (`flow_ia` ou ativo real), comparativos lado a lado e sobreposições limpas apenas onde ajudarem a leitura. |

---

## 3. Direção de Arte, HUD e Presença do Inspetor (`@Steve`)

- **HUD sob demanda e leitura instantânea:** use apenas os elementos que ajudam o espectador leigo a entender a cena em leitura rápida sem pausar (ex.: identificador discreto, `1 a 2` apontadores curtos de `1 a 3 palavras` ancorados diretamente sobre o elemento visível na camada ativa — foto real, vídeo ou 3D — sem sobrepor outras molduras, e pílula de benefício em português cotidiano, reservando tabelas ou pares densos de medidas para `pacote.md`). Cenas de uso real podem rodar limpas apenas com a legenda dinâmica.
- **Presença do Inspetor (`Rig 2.5D`):** livre para entrar na abertura, em PiP comentando um teste/processo, em reações pontuais ou no fechamento — sempre respeitando a área segura e sem cobrir o foco principal da cena.

---

## 4. Motores Visuais por Natureza da Cena

- **`Rig 2.5D`:** apresentador Inspetor Bicho Grilo com *lip-sync* determinístico PT-BR.
- **`Flow Omni 360p -> 1080p` (`flow_ia`):** cenas externas, atmosfera natural e uso prático real guiado por foto real do produto (`1 crédito/s` em `360p` até `10s`; *upscale* a `1080p` a `0` crédito até `10s`). Dispara aviso determinístico de IA (`REQ-007`).
- **`Determinístico`:** visualizações 3D, vistas explodidas, processos animados, comparativos e composições via `Python (numpy/Pillow) + ffmpeg` (e estúdio interativo `Three.js` quando aplicável), ancorados nos ativos reais de `ficha.md`.

---

## 5. Referências Externas de Qualidade

As referências visuais de qualidade desta bíblia devem vir exclusivamente de referências externas aprovadas pelo usuário (não de entregas internas ainda em calibração). Esta seção permanece aberta para catalogar os quadros e links externos de referência conforme forem selecionados.

- **Estilo Raio-X / Engenharia por Dentro (`voceaprendeu.shop` — `@voceaprendeu` e `@teensinei`, informado pelo usuário e lido em `2026-11-20`):** palco escuro limpo com modelo 3D translúcido em movimento contínuo, *leader lines* finas de `1 a 3 palavras`, pílula única de estado físico e legenda dinâmica com palavra tônica destacada e sublinhada em amarelo (`#facc15`).
