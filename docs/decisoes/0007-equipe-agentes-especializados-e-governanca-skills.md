---
status: "accepted"
date: 2026-11-20
decision-makers: victor
---

# Equipe de agentes especializados, revisão cruzada e governança de skills com contexto limpo

## Contexto e problema

Conforme [visao.md](../visao.md) e [0003-fluxo-aprovacao-e-publicacao.md](0003-fluxo-aprovacao-e-publicacao.md), o projeto opera com custo inicial mínimo, rigor técnico e evolução contínua em portões de aprovação. Na prática de produção, a concentração de curadoria, FinOps, requisitos e roteirização em um único contexto monolítico misturou assuntos não relacionados, degradou a qualidade narrativa do roteiro e manteve acoplados dois ofícios distintos na mesma skill (`roteiro` e `direção de arte / vídeo`).

Além disso, [0006-governanca-qualidade-finops-e-composicao-visual.md](0006-governanca-qualidade-finops-e-composicao-visual.md) havia previsto dois subagentes revisores dedicados em modelo `flash` (Crítico de Roteiro e Inspetor Visual Multimodal) para compensar o risco de um agente único revisar a si próprio, mas não estabelecia um fluxo formal para nomear especialistas no chat (`@Curador`, `@Carlos`, `@Steve`), endereçar críticas à causa-raiz sem inflar skills com regras restritivas nem auditar alterações de skills antes de recriar a entrega em contexto limpo.

As evidências sobre feedback externo, retorno decrescente entre `2` e `3` rodadas, parada adaptativa, modos de falha multiagente e recursos nativos do Antigravity estão registradas em [equipe-agentes-especializados-e-revisao-iterativa.md](../pesquisa/equipe-agentes-especializados-e-revisao-iterativa.md).

## Opções consideradas

### Opção 1: Equipe de 4 especialistas permanentes (`curador`, `carlos`, `steve`, `revisor-skills`) em modo híbrido, revisão cruzada e protocolo pós-crítica em até `3` rodadas

1. **Plugin local e separação de skills:** empacotar os 4 especialistas em `.agents/plugins/equipe-bicho-grilo/` (`curador.md`, `carlos.md`, `steve.md`, `revisor-skills.md`), preservando as regras gerais em [AGENTS.md](../../AGENTS.md) e as skills em `.agents/skills/` (com links simbólicos em `.claude/skills/`) para manter portabilidade entre motores ([visao.md](../visao.md)). A antiga skill `roteiro-e-video` é desmembrada em **`roteirista`** (storytelling, retenção, gancho de abertura imediato que desperta curiosidade, tensão ou identificação instantânea para deter a rolagem no feed conforme [.agents/skills/roteirista/references/guia-roteirista.md](../../.agents/skills/roteirista/references/guia-roteirista.md), textos de `pacote.md` e revisão visual das entregas do `@Steve`) e **`producao-visual`** (direção de arte, área segura `9:16`, Rig 2.5D, Flow `Omni 360p→1080p`, TTS e composição `Pillow/ffmpeg`), operando em conjunto com **`curadoria`** e as novas skills **`revisao-skills-e-agentes`** e **`orquestrar-equipe`**.
2. **Coordenador e modo híbrido:** o agente principal atua como Coordenador roteando menções nominais (`@Curador`, `@Carlos`, `@Steve`, `@Revisor-Skills`). O fluxo padrão dos Portões 1 a 4 (com o Portão 3 opcional após calibração, conforme [0003](0003-fluxo-aprovacao-e-publicacao.md) e [0006](0006-governanca-qualidade-finops-e-composicao-visual.md)) executa em **subagentes isolados sob demanda** (menor custo e menor contexto), reservando o modo **Swarm enxuto** (`swarm`) exclusivamente para pedidos explícitos de colaboração direta ao vivo (como `Carlos ↔ Steve`) ou paralelismo entre múltiplos produtos **somente após encerrar a fase de calibração** (`REQ-001`).
3. **Revisão cruzada substituindo o Revisor QA dedicado:** combinam-se validações determinísticas locais (`0` tokens) com revisão cruzada entre os próprios especialistas sobre as entregas dos autores (`@Curador` no Portão 1, `@Carlos` no Portão 2 e `@Steve` nos Portões 3 e 4, respeitando a opcionalidade do Portão 3) — `@Steve` valida exequibilidade visual, mapa de cenas e orçamento Flow de `roteiro.md` no Portão 2 (com `@Curador` acionado para checagem factual sob demanda), e `@Carlos` valida multimodalmente *styleframes*, quadros-chave e aderência narrativa nas entregas do `@Steve` nos Portões 3 e 4 — eliminando as `2` a `3` instanciações separadas do Revisor QA em `flash`.
4. **Protocolo pós-crítica e governança de skills (`@Revisor-Skills`):** diante de crítica a uma entrega, o especialista diagnostica a causa-raiz no contexto original:
   - *Causa a montante (insumo/contexto de outro responsável):* emite feedback em linguagem afirmativa para o responsável sem adicionar regras defensivas na própria skill;
   - *Deslize pontual de execução:* recria diretamente sem alterar a skill;
   - *Causa interna (lacuna na própria skill/agente):* propõe diff em linguagem afirmativa e com evidência ao `@Revisor-Skills`, que audita em **parada adaptativa com teto calibrável de `3` rodadas** (aprovando na 1ª quando conforme ou escalando resumo ao usuário em caso de estagnação ou ao atingir a 3ª). Aprovado, registra-se **commit isolado no Git** e o Coordenador encerra a instância antiga e sobe uma **nova instância limpa** do especialista para recriar a peça. Nesta fase não se cria trava programática em código (`hooks.json` ou `run_workflow`), mantendo a operação simples e adicionando trava mecânica apenas se surgir evidência prática de descumprimento.

#### Viabilidade de custo (FinOps)

1. **Inventário de recursos:**
   - Scripts determinísticos de validação (Portões 1 a 4): CPU local, `0` tokens de IA, `US$ 0`.
   - Clipes Google Flow e síntese TTS `pt-BR`: exatamente o mesmo consumo-base de mídia previsto em [0006](0006-governanca-qualidade-finops-e-composicao-visual.md) (`0` créditos extras de Flow e `0` caracteres extras de TTS decorrentes da nova estrutura de equipe; base de `1` clipe `8s` `Omni 360p→1080p` = `8` créditos Flow + `~800` chars TTS/vídeo).
   - Turnos de LLM em subagentes: eliminação das `2` a `3` instanciações de subagentes revisores dedicados em `flash` por produto previstas em `0006` (`2` com Portão 3 dispensado; `3` com Portão 3 ativo), substituídas por revisão cruzada nos turnos já existentes de `@Steve` e `@Carlos`, somada ao acionamento sob demanda do `@Revisor-Skills` apenas quando uma crítica exige atualizar uma skill ou agente *(tarifa unitária avulsa por token de API fora da assinatura de agente já mantida pelo usuário — **não verificado**)*.
2. **Projeção determinística de escala (custo combinado herdado de `0006` + delta da arquitetura de equipe):**
   - **`1` vídeo/mês:** `8` créditos Flow (`0,8%` Pro) + `~800` chars TTS (`0,16%` Azure `F0`) | **`0` créditos/chars incrementais (`US$ 0` adicional)**; redução de `2` a `3` subagentes revisores dedicados em `flash` (eventual acionamento sob demanda do `@Revisor-Skills` somente quando houver crítica com edição de skill).
   - **`30` vídeos/mês:** `240` créditos Flow (`24%` Pro) + `~24.000` chars TTS (`4,8%` Azure `F0`) | **`0` créditos/chars incrementais (`US$ 0` adicional)**; redução de `60` a `90` instanciações de subagentes revisores dedicados por mês (com acionamento sob demanda de `@Revisor-Skills` restrito a críticas com edição de skill).
   - **`100` vídeos/mês:** `800` créditos Flow (`80%` Pro) + `~80.000` chars TTS (`16%` Azure `F0`) | **`0` créditos/chars incrementais (`US$ 0` adicional)**; redução de `200` a `300` instanciações de subagentes revisores dedicados por mês (com acionamento sob demanda de `@Revisor-Skills` restrito a críticas com edição de skill).
   - **`300` vídeos/mês:** `2.400` créditos Flow (ultrapassa a saturação de `125` vídeos/mês do Degrau 0 no Google AI Pro e exige o **Degrau 2** de `0006`, ex.: `Google AI Ultra` `US$ 100/mês` com `10.000` créditos/mês registrados em [custo-agentes-revisores-e-finops.md](../pesquisa/custo-agentes-revisores-e-finops.md) → `24%` da cota Ultra) + `~240.000` chars TTS (`48%` Azure `F0`) | **`0` créditos/chars incrementais** pela arquitetura de equipe (`US$ 0` extra além do Degrau 2 de mídia); redução de `600` a `900` instanciações de subagentes revisores dedicados por mês (com acionamento sob demanda de `@Revisor-Skills` restrito a críticas com edição de skill).
   - **Ponto de saturação:** os limites físicos de mídia permanecem idênticos aos calculados em `0006` (`125` vídeos/mês no Google AI Pro e `625` vídeos/mês no Azure `F0`). No consumo de tokens da assinatura do usuário, o modo padrão em subagentes isolados reduz o volume acumulado por turno frente ao chat monolítico, enquanto o uso frequente de **Swarm** (*Quota Heavy*) acelera o consumo da cota dinâmica da sessão *(ponto numérico exato de saturação da cota dinâmica da assinatura — **não verificado**)*.
3. **Alternativas mais econômicas (quando necessário):** caso sessões de Swarm pressionem a cota da assinatura do usuário, restringir a operação integralmente ao modo padrão de subagentes isolados sob demanda e executar revisões cruzadas apenas em entregas finais ou críticas.

### Opção 2: Manter agente generalista único + 2 subagentes revisores dedicados em `flash` (`0006`)

Manter toda a produção em uma única conversa generalista com skill única `roteiro-e-video` e revisão dedicada em `flash`, aceitando contaminação de contexto entre curadoria, roteiro e vídeo e ausência de auditoria dedicada antes de alterar skills.

### Opção 3: Operar permanentemente em Swarm com 5 agentes fixos (incluindo Revisor QA separado) e trava em código desde o início

Manter todos os papéis em mural Swarm contínuo com um 5º agente exclusivo para QA e bloqueios programáticos em `hooks.json`/`run_workflow`, elevando o consumo de cota e a complexidade operacional já na fase inicial de calibração.

## Decisão

Opção escolhida: **Opção 1 (Equipe de 4 especialistas permanentes em modo híbrido com revisão cruzada e protocolo pós-crítica em até `3` rodadas)**, porque isola contextos por ofício sem multiplicar camadas burocráticas de QA, preserva feedback externo independente entre pares distintos, protege a qualidade das skills via `@Revisor-Skills` + commit no Git antes da recriação em contexto limpo e mantém custo incremental zero em mídia com menor sobrecarga de contexto por turno.

Registra-se que o teto de **`3` rodadas com parada adaptativa** no ciclo de revisão de skills constitui **parâmetro operacional calibrável** derivado de resultados empíricos de refinamento iterativo e debate multiagente ([equipe-agentes-especializados-e-revisao-iterativa.md](../pesquisa/equipe-agentes-especializados-e-revisao-iterativa.md)), sujeito a ajuste contínuo pelos ciclos `/learn`.

### Consequências

- **Bom:** reduz interferência de contexto entre garimpo comercial, roteiro, produção audiovisual e governança de skills, facilitando ajustes cirúrgicos via menção direta (`@Curador`, `@Carlos`, `@Steve`, `@Revisor-Skills`).
- **Bom:** garante rastreabilidade completa de mudanças em skills no Git e evita regras restritivas ou sem fonte contaminando o comportamento futuro dos agentes.
- **Ruim:** exige que o Coordenador roteie menções e gerencie o ciclo de encerramento e relançamento de instâncias após commits em skills; caso a equipe passe a usar Swarm autônomo com frequência, será necessário monitorar a cota e avaliar trava programática em `hooks.json` ou `run_workflow`.
