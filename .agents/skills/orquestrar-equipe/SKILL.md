---
name: orquestrar-equipe
description: >-
  Como o Coordenador roteia menções nominais (@Curador, @Carlos, @Steve, @Revisor-Skills),
  escolhe entre subagentes isolados sob demanda ou Swarm enxuto, coordena revisão cruzada
  nos Portões 1 a 4 e executa o protocolo pós-crítica (causa-raiz, revisão de skill, commit Git
  e recriação em contexto limpo). Use sempre que conduzir o pipeline de produtos ou responder
  a pedidos dirigidos a um especialista pelo nome.
---

# Orquestrar Equipe Especializada (Coordenador)

Runbook operacional do agente principal (**Coordenador** — única interface direta com o usuário) para dirigir a equipe definida em `.agents/plugins/equipe-bicho-grilo/` conforme [0007-equipe-agentes-especializados-e-governanca-skills.md](../../../docs/decisoes/0007-equipe-agentes-especializados-e-governanca-skills.md) e [0003-fluxo-aprovacao-e-publicacao.md](../../../docs/decisoes/0003-fluxo-aprovacao-e-publicacao.md).

## 1. Roteamento Nominal (`@Curador`, `@Carlos`, `@Steve`, `@Revisor-Skills`)

Sempre que a mensagem do usuário mencionar um especialista pelo nome, encaminhe o pedido diretamente ao agente correspondente mantendo o contexto principal enxuto e livre de detalhes operacionais internos do especialista:

| Menção | Agente (`TypeName`) | Arquivos mínimos a informar |
|---|---|---|
| `@Curador` | `curador` | Pasta `produtos/<slug>/` e objetivo da pesquisa/ajuste |
| `@Carlos` | `carlos` | `produtos/<slug>/ficha.md`, `produtos/<slug>/roteiro.md` e caminhos de mídia/quadros/`pacote.md` quando aplicável |
| `@Steve` | `steve` | `produtos/<slug>/ficha.md`, `produtos/<slug>/roteiro.md` e `produtos/<slug>/assets/` |
| `@Revisor-Skills` | `revisor-skills` | `RODADA N/3`, pareceres anteriores (se `N > 1`), crítica/origem, causa-raiz, arquivo(s) alvo, diff e fontes |

- Ao delegar via `invoke_subagent` ou `send_message`, solicite apenas os caminhos produzidos, o resumo objetivo da entrega e eventuais pedidos de consulta ou feedbacks marcados com `@Nome` — preservando a convenção de `AGENTS.md`.
- Quando um especialista devolver na resposta uma consulta factual, sugestão visual ou feedback marcado com `@Nome` de um colega (ex.: `@Carlos` consultando `@Curador` ou submetendo `roteiro.md` ao `@Steve`), o Coordenador encaminha apenas os caminhos e a pergunta específica ao colega e devolve a resposta ao solicitante.

## 2. Modo Híbrido (Subagentes sob Demanda vs. Swarm Enxuto)

1. **Padrão dos Portões 1 a 4 — Subagentes isolados sob demanda (`invoke_subagent` / `send_message`):**
   - Portão 1 aciona `curador`;
   - Portão 2 aciona `carlos` (+ consultas pontuais a `curador` e validação visual de entrada do `steve`);
   - Portões 3 e 4 acionam `steve` (+ textos editoriais de `pacote.md` via `carlos` e revisão visual multimodal do `carlos`).
   - Guarde o `conversationId` de cada especialista ativo na sessão para encaminhar críticas ou pedidos subsequentes mantendo a memória exata de como a peça foi criada.
2. **Gatilho e bootstrap de Swarm enxuto (`/swarm` / ferramenta `swarm`):**
   - Ative apenas quando o usuário solicitar colaboração direta ao vivo em Swarm (ex.: *"junta Carlos e Steve em swarm"* ou `/swarm`) ou quando houver paralelismo real entre múltiplos produtos **após encerrar a fase de calibração (`REQ-001`)**.
   - Ao criar cada worker com `swarm{action:"add"}`, adicione exclusivamente os especialistas necessários à etapa corrente e garanta que o `brief` inicial instrua explicitamente: (a) ler `.agents/plugins/equipe-bicho-grilo/agents/<nome>.md` e sua respectiva `SKILL.md`, (b) publicar no mural compartilhado via `post_message` em **modo Swarm enxuto** listando os `@nomes` ativos e evitando `@all`, e (c) **não** adicionar helpers extras via `swarm{action:"add"}`. Ao concluir o portão, encerre os workers ociosos via `swarm{action:"kill"}` e poste `[done] <resumo>` no mural.

## 3. Revisão em Camadas nos Portões 1 a 4 (`REQ-014`) e Portão 4 / Vitrine

- **Portão 1 (`ficha.md`):** `@Curador` executa `python3 src/video/validate_gates.py produtos/<slug> --portao 1` (`6` seções `## 1.`..`## 6.`, arquivos em disco, soma de estrelas `99,5%`–`100,5%`) e devolve os caminhos e resumo ao Coordenador → aprovação do usuário (`REQ-001`, `REQ-002`).
- **Portão 2 (`roteiro.md`):** `@Carlos` devolve `produtos/<slug>/roteiro.md` ao Coordenador → **o Coordenador executa `python3 src/video/validate_gates.py produtos/<slug> --portao 2`** (`0` tokens: teto calibrável de `15` palavras por frase e sua expansão fonética, dicionário fonético, rótulos de motor, continuidade `00s–...`, orçamento Flow com linha `Total` e disparo `REQ-007`) e encaminha ao `@Steve` para validação visual de entrada (e ao `@Curador` se houver dúvida factual). A revisão cruzada `@Carlos ↔ @Steve` segue **parada adaptativa com teto calibrável de `3` rodadas**; após `@Carlos` incorporar os ajustes do `@Steve`, o Coordenador **reexecuta `python3 src/video/validate_gates.py produtos/<slug> --portao 2`** antes de submeter à aprovação do usuário (`REQ-003`, `REQ-004`).
- **Portões 3 e 4 (`preview.mp4` / `video_final_1080p.mp4` + `pacote.md`):**
  - No Portão 4, o Coordenador coleta os textos editoriais de `pacote.md` com `@Carlos` e fornece o `código curto` da vitrine e o(s) **link(s) principal(is) de afiliado (por variação essencial)** ao `@Steve` para montagem integrada de `produtos/<slug>/video_final_1080p.mp4` e `produtos/<slug>/pacote.md`;
  - `@Steve` executa a checagem determinística local de mídia em script Python (`0` tokens, ou `--portao 3`/`--portao 4` quando estendidos em `src/video/validate_gates.py`: áudio `> 0 bytes` e marcas temporais/visemas, área segura rígida `X = 48..887 px` / `Y = 288..1247 px` e alerta se `X < 65 px`, ativos em disco, disparo `REQ-007` e licença comercial válida no Portão 4) e devolve os caminhos de *styleframes*, quadros-chave, vídeo (`preview.mp4` ou `video_final_1080p.mp4`) e `pacote.md` (no Portão 4) ao Coordenador → revisão multimodal do `@Carlos` (com **parada adaptativa e teto calibrável de `3` rodadas**, escalando ao usuário se estagnar ou atingir a 3ª) → apresentação do Coordenador ao usuário → atualização da vitrine estática na bio pelo **Coordenador** somente após o aceite final no chat (`REQ-005` a `REQ-008`) e recomendação explícita para executar `/learn` ao concluir o ciclo do produto (`REQ-013`).

## 4. Protocolo Pós-Crítica (Causa-Raiz → Revisão → Commit → Contexto Limpo)

Sempre que o usuário criticar uma entrega de especialista (diretamente ou via `@Nome`):

1. **Diagnóstico no contexto original:** encaminhe a crítica à **mesma instância viva** do especialista responsável (ou lance-a informando o artefato produzido e a crítica caso venha de sessão anterior) pedindo o diagnóstico da **causa-raiz** em um de três caminhos:
   - **Causa A — Lacuna na própria skill ou definição de agente:** o especialista **interrompe sem editar arquivos de configuração nem recriar a entrega**, e devolve ao Coordenador o diagnóstico + proposta objetiva de diff em linguagem afirmativa com fontes pesquisadas quando aplicável.
   - **Causa B — Falha em insumo ou contexto vindo de outra etapa:** o especialista devolve feedback estruturado em linguagem afirmativa ao responsável (via Coordenador, ou no mural em Swarm enxuto), mantendo a própria skill intacta.
   - **Causa C — Deslize pontual de execução (a skill já cobria bem o princípio):** o especialista aponta onde desviou e corrige a entrega diretamente sem alterar a skill.
2. **Fluxo da Causa B:** encaminhe o feedback afirmativo ao responsável para corrigir o artefato de entrada (`ficha.md`, `roteiro.md` ou orientação do Coordenador) respeitando **parada adaptativa com teto calibrável de `3` rodadas** entre as etapas (escalando resumo ao usuário se persistir impasse após 3 ciclos) e, após corrigido, acione o especialista original para refazer sua entrega com o insumo atualizado.
3. **Fluxo da Causa A (auditoria com `@Revisor-Skills`):**
   - Submeta ao `revisor-skills` em contexto isolado o pacote completo de entrada: `RODADA: 1/3`, crítica/origem, causa-raiz diagnosticada, caminho(s) do(s) arquivo(s) alvo, diff proposto em linguagem afirmativa e fontes consultadas.
   - Conduza em **parada adaptativa com teto calibrável de `3` rodadas**: se retornar `APROVADO` na Rodada `1/3`, avance imediatamente ao Passo 4; se retornar `AJUSTAR`, encaminhe as ressalvas ao especialista proponente para ajustar a proposta e reenvie incrementando `RODADA: N/3` junto com os pareceres anteriores; se retornar `ESCALAR_USUARIO`, encerre o loop e apresente ao usuário o resumo objetivo do impasse e das opções — assim que o usuário decidir no chat, retome o Passo 4 aplicando a decisão escolhida.
4. **Aplicação pelo Coordenador, Commit Isolado e Recriação em Contexto Limpo:**
   - Após `STATUS: APROVADO` do `@Revisor-Skills` (ou decisão do usuário após escalação), **o Coordenador** aplica as edições nos arquivos de skill/agente em disco (atualizando links simbólicos em `.claude/skills/` se criar ou renomear skill).
   - **O Coordenador** registra um **commit isolado no Git** apenas com os arquivos de customização alterados (`learn(<agente>): <resumo curto>`, documentando a crítica, a causa-raiz e a evidência no corpo da mensagem).
   - **O Coordenador** encerra a instância antiga do especialista (`manage_subagents` `kill`) e lança uma **nova instância limpa** já lendo a skill atualizada para recriar a entrega; se estiver em **Swarm enxuto** ativo, lembre que nomes encerrados com `swarm` `kill` não podem ser reutilizados no mesmo Swarm — adicione `<nome>-2` com a skill atualizada ou encerre o Swarm e relance via `invoke_subagent`.
   - Entregue ao usuário a nova peça pronta acompanhada de um resumo curto do ajuste aprovado e do hash do commit gerado.
