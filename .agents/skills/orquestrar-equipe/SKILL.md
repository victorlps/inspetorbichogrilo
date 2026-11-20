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

Runbook operacional do agente principal (Coordenador) para dirigir a equipe definida em `.agents/plugins/equipe-bicho-grilo/` conforme [0007-equipe-agentes-especializados-e-governanca-skills.md](../../../docs/decisoes/0007-equipe-agentes-especializados-e-governanca-skills.md) e [0003-fluxo-aprovacao-e-publicacao.md](../../../docs/decisoes/0003-fluxo-aprovacao-e-publicacao.md).

## 1. Roteamento Nominal (`@Curador`, `@Carlos`, `@Steve`, `@Revisor-Skills`)

Sempre que a mensagem do usuário mencionar um especialista pelo nome, encaminhe o pedido diretamente ao agente correspondente mantendo o contexto principal enxuto e livre de detalhes operacionais internos do especialista:

| Menção | Agente (`TypeName`) | Arquivos mínimos a informar |
|---|---|---|
| `@Curador` | `curador` | Pasta `produtos/<slug>/` e objetivo da pesquisa/ajuste |
| `@Carlos` | `carlos` | `produtos/<slug>/ficha.md`, `produtos/<slug>/roteiro.md` e mídia/quadros quando aplicável |
| `@Steve` | `steve` | `produtos/<slug>/ficha.md`, `produtos/<slug>/roteiro.md` e `produtos/<slug>/assets/` |
| `@Revisor-Skills` | `revisor-skills` | Caminhos dos arquivos alterados/propostos, crítica original, causa-raiz e fontes |

- Ao delegar via `invoke_subagent` ou `send_message`, solicite apenas os caminhos produzidos, o resumo objetivo da entrega e eventuais pedidos de consulta para outros especialistas — preservando a convenção de `AGENTS.md`.
- Se o especialista solicitar consulta a um colega (ex.: `@Carlos` pedindo validação visual ao `@Steve` ou checagem factual ao `@Curador`), repasse apenas os caminhos e a pergunta específica ao colega e devolva a resposta ao solicitante.

## 2. Modo Híbrido (Subagentes sob Demanda vs. Swarm Enxuto)

1. **Padrão dos Portões 1 a 4 — Subagentes isolados sob demanda (`invoke_subagent` / `send_message`):**
   - Portão 1 aciona apenas `curador`;
   - Portão 2 aciona `carlos` (+ consultas pontuais a `steve` e `curador`);
   - Portões 3 e 4 acionam `steve` (+ revisão multimodal de `carlos`).
   - Guarde o `conversationId` de cada especialista ativo na sessão para encaminhar críticas ou pedidos subsequentes mantendo a memória exata de como a peça foi criada.
2. **Gatilho de Swarm enxuto (`swarm`):**
   - Ative apenas quando o usuário solicitar colaboração direta ao vivo (ex.: *"junta Carlos e Steve em swarm"* ou `/teamwork`) ou quando houver paralelismo real entre múltiplos produtos após a fase de calibração.
   - Adicione ao mural exclusivamente os workers necessários à etapa corrente, evitando `@all` e encerrando o Swarm ao concluir o portão.

## 3. Revisão em Camadas nos Portões 1 a 4 (`REQ-014`)

Execute a revisão combinando validação determinística local (`0` tokens) e revisão cruzada entre especialistas antes de apresentar cada portão ao usuário:

- **Portão 1 (`ficha.md`):** entrega do `@Curador` → script determinístico local (`5` blocos, arquivos em disco, soma de estrelas = `100%`) → aprovação do usuário (`REQ-001`, `REQ-002`).
- **Portão 2 (`roteiro.md`):** criação pelo `@Carlos` → script determinístico local (teto calibrável de `15` palavras por frase, duração estimada, dicionário fonético, mapa de cenas, orçamento Flow e links válidos) + validação visual de entrada pelo `@Steve` (e checagem factual pelo `@Curador` quando houver dúvida de evidência) → aprovação do usuário (`REQ-003`, `REQ-004`).
- **Portões 3 e 4 (`preview.mp4` / MP4 final `1080×1920` + `pacote.md`):** produção pelo `@Steve` (com textos editoriais de `pacote.md` alinhados ao `@Carlos`) → script determinístico local (áudio `> 0 bytes` e marcas temporais/visemas, área segura `9:16`, ativos presentes em disco, disparo de `REQ-007` para cena `flow_ia`, licença comercial válida no Portão 4) + revisão visual multimodal pelo `@Carlos` sobre *styleframes*, quadros-chave e vídeos → aprovação do usuário (`REQ-005` a `REQ-008`).

## 4. Protocolo Pós-Crítica (Causa-Raiz → Revisão → Commit → Contexto Limpo)

Sempre que o usuário criticar uma entrega de especialista (diretamente ou via `@Nome`):

1. **Diagnóstico no contexto original:** encaminhe a crítica à **mesma instância viva** do especialista responsável (ou informe a peça produzida e a crítica caso venha de sessão anterior) pedindo o diagnóstico da **causa-raiz** em um de três destinos:
   - **Causa A — Lacuna na própria skill ou definição de agente:** o especialista pesquisa referências verificáveis se necessário e formula uma proposta objetiva de diff em linguagem afirmativa.
   - **Causa B — Falha em insumo ou contexto vindo de outro responsável (a montante):** o especialista redige um feedback estruturado em linguagem afirmativa para o responsável (`@Curador`, `@Carlos`, `@Steve` ou Coordenador), mantendo a própria skill livre de regras defensivas ou restritivas.
   - **Causa C — Deslize pontual de execução (a skill já cobria bem o princípio):** o especialista aponta onde desviou e recria a peça diretamente sem inflar a skill.
2. **Fluxo da Causa B (a montante):** encaminhe o feedback afirmativo ao responsável para corrigir o artefato de entrada (`ficha.md`, `roteiro.md` ou orientação do Coordenador) e, após corrigido, acione o especialista original para refazer sua entrega com o insumo atualizado.
3. **Fluxo da Causa A (revisão de skill com `@Revisor-Skills`):**
   - Submeta ao `revisor-skills` (em contexto isolado): a crítica do usuário, a causa-raiz apontada, o diff proposto em linguagem afirmativa e as fontes consultadas.
   - Conduza em **parada adaptativa com teto de `3` rodadas**: se aprovar na 1ª rodada, encerre imediatamente; se pedir ajustes, repasse ao especialista para adequar (máximo até a 3ª rodada). Caso estagne sem avanço ou chegue à 3ª rodada sem `APROVADO`, interrompa o ciclo e apresente ao usuário um resumo objetivo das duas posições para decisão.
4. **Aplicação, Commit Isolado e Recriação em Contexto Limpo:**
   - Após `STATUS: APROVADO` do `@Revisor-Skills`, aplique as edições nos arquivos de skill/agente (atualizando links simbólicos em `.claude/skills/` se criar ou renomear skill).
   - Registre um **commit isolado no Git** apenas com os arquivos de customização alterados (`learn(<agente>): <resumo curto>`, documentando a crítica, a causa-raiz e a evidência no corpo da mensagem).
   - Encerre a instância antiga do especialista (`manage_subagents` `kill`, ou `swarm` `kill`) e lance uma **nova instância limpa** já lendo a skill atualizada para recriar a entrega.
   - Entregue ao usuário a nova peça pronta acompanhada de um resumo curto do ajuste aprovado e do hash do commit gerado.
