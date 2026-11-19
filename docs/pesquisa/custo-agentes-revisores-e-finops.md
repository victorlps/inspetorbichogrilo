# Como avaliar e controlar custos de infra, tokens e créditos em fluxos multi-agentes sem criar desperdício no próprio revisor?

Fontes lidas em 2026-11-18. Reverificar custos de modelos, créditos e práticas de FinOps para IA até 2027-02-18.

## Fatos observados

### 1. Dinâmica de custo em fluxos multi-agentes (FinOps para IA)
- **Amplificação exponencial por ciclos iterativos:** sínteses retornadas em busca web que referenciam a [FinOps Foundation (`finops.org`)](https://www.finops.org/) apontam que fluxos agênticos deslocam o gasto de linear para composto quando operam em laços iterativos de planejamento → execução de ferramentas → verificação → reenvio acumulado de histórico (*Context Window Creep*). A leitura automatizada direta das páginas de `https://www.finops.org/` retornou erro HTTP `403`, razão pela qual tanto essa dinâmica quanto os múltiplos quantitativos citados em fontes secundárias (`5×–30×` em laços agênticos e `3×–10×` em ciclos de revisão/rejeição) permanecem **não verificado** na fonte primária e sem benchmark próprio no repositório.
- **Cinco frentes de controle operacional listadas em resultados de busca web (`finops.org` e literatura secundária — **não verificado** na leitura direta da documentação primária):**
  1. Adoção da métrica de custo por resultado concluído (*cost per successful outcome*) em vez de custo isolado por token — **não verificado** na fonte primária;
  2. Atribuição granular de tokens por etapa/agente — **não verificado** na fonte primária;
  3. Otimização e isolamento de contexto (enxugamento de *prompt* e execução sem histórico acumulado quando dispensável) — **não verificado** na fonte primária;
  4. Travas programáticas em tempo de execução (*runtime guardrails*, circuit breakers e tetos fixos de rodadas) — **não verificado** na fonte primária;
  5. Hierarquia de execução (*Code-First* / *Shift-Left*): validações objetivas executam em script determinístico (custo zero de tokens) antes de acionar modelos de linguagem, reservando julgamento semântico isolado a modelos leves — padrão arquitetural **não verificado** em estudo de caso primário único nesta rodada.

### 2. Parâmetros de custo medidos e documentados no projeto
- **Infraestrutura local de renderização ([0005-pipeline-hibrido-25d-e-flow.md](../decisoes/0005-pipeline-hibrido-25d-e-flow.md)):** máquina local (`Intel Core i7-5557U`, 16 GB RAM, `Intel Iris Graphics 6100`, sem GPU NVIDIA nem Apple Silicon) levou **55 segundos por quadro** no Blender `CYCLES` em CPU (`540×720`, 24 amostras) e falhou no `BLENDER_EEVEE_NEXT` em modo `--background` por ausência de contexto GPU no macOS *headless*.
- **Geração de imagens por IA ([personagem-consistente-e-animacao-3d.md](personagem-consistente-e-animacao-3d.md)):** registro anterior do projeto anota que a saída de `gemini-3.1-flash-image` consome **747 tokens em `512px`**, **1.120 em `1K`**, **1.680 em `2K`** e **2.520 em `4K`**.
- **Geração de vídeo no Google Flow ([Ajuda do Google Flow — Gerenciar seus créditos](https://support.google.com/flow/answer/16526234?hl=pt-br&co=GENIE.Platform%3DDesktop) e [Google Blog — Gemini Omni 1.2 Flash](https://blog.google/innovation-and-ai/technology/developers-tools/introducing-gemini-omni-1-2-flash/)):**
  - **`Omni Flash 1.2` (até `10s`, todos os usuários):** **`360p` = 1 crédito por segundo**; **`720p` = 3 créditos por segundo** (o modo `360p` custa 1/3 do custo de `720p`).
  - **`Omni Flash 1.2` (`11` a `15s`, assinantes Plus, Pro e Ultra):** `360p` cobra `1 crédito/s` até `10s` e `2 créditos/s` extras entre `11` e `15s`; `720p` cobra `3 créditos/s` até `10s` e `6 créditos/s` extras entre `11` e `15s`.
  - **Aumento de resolução (`upscale`) para `720p` ou `1080p` no Plus, Pro e Ultra:** **`0` crédito para vídeos de `1` a `10` segundos** (e `1 crédito/s` extra acima de `10` segundos).
  - **`Veo 3.1 Lite` (`4`, `6` ou `8s` em `720p`):** **10 créditos fixos por geração** para assinantes não-Ultra (incluindo Pro) e **5 créditos** para Ultra.
  - **Cotas mensais sem acúmulo entre ciclos:** Google AI Plus (`200` créditos/mês), Google AI Pro (`1.000` créditos/mês), Google AI Ultra US$ 100 (`10.000` créditos/mês) e Google AI Ultra US$ 200 (`25.000` créditos/mês).
  - **Dados informados/observados pelo usuário nesta sessão na interface do Google Flow:** saldo inicial exibido de `1.050` créditos e consumo exato de **8 créditos** no teste prático de um clipe **`Omni 1.2 Flash · 360p · 8s`**.
  - **Valores não cobertos nesta consulta:** preço avulso da compra extra de créditos de IA e tarifas unitárias de API de texto/imagem em US$ fora das assinaturas — **não verificado**.

## Inferências

- **Inferência:** Instanciar um agente LLM rodando continuamente para auditar custos em toda tarefa tende a reproduzir o overhead iterativo descrito em FinOps para IA, consumindo contexto e gerando trocas ou críticas dispensáveis quando o fluxo já opera dentro de ferramentas locais gratuitas ou da cota mensal paga.
- **Inferência:** Substituir um agente contínuo por checagens determinísticas locais a custo zero (contagem objetiva de itens, ativos e cotas em scripts) combinadas com uma subseção obrigatória de viabilidade de custo (`FinOps`) apenas no momento de tomar ou revisar decisões arquiteturais em `docs/decisoes/` evita desperdício rotineiro mantendo disciplina financeira.
- **Inferência:** Ao delegar revisões semânticas indispensáveis (como oralidade de roteiro e inspeção de quadros visuais), executá-las em modelo leve (`flash`), em contexto isolado apenas com os artefatos da etapa e com teto fixo de rodadas limita o crescimento composto de tokens.
- **Inferência:** No cenário atual com Google AI Pro (`1.000` créditos/mês já pagos), gerar clipes externos curtos de até `10s` em `Omni Flash 1.2 · 360p` (`1 crédito/s`) e aplicar o aumento de resolução para `720p`/`1080p` a `0` crédito comporta até **125 clipes de 8s por mês** dentro da assinatura já mantida, sem custo adicional em dólar.
