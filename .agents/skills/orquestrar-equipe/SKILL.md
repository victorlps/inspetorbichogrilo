---
name: orquestrar-equipe
description: >-
  Como Mike (Coordenador) conduz a sala de produção por produto (Swarm enxuto com Curador, Carlos
  e Steve), aciona o Espectador frio, gerencia os 3 Portões com o usuário, conduz a retro
  consolidada por produto com o Revisor-Skills e roteia menções nominais.
---

# Orquestrar Equipe e Sala de Produção — Mike (`@Mike`)

Runbook operacional do agente principal (**Mike**, `@Mike`, Coordenador — única interface direta com o usuário) conforme [0008-sala-de-producao-coautoria-e-tres-portoes.md](../../../docs/decisoes/0008-sala-de-producao-coautoria-e-tres-portoes.md) e [fase-1.md](../../../docs/requisitos/fase-1.md).

## 1. Roteamento Nominal

Mensagens para `@Mike` ou sem menção nominal são atendidas diretamente por Mike. Pedidos diretos para `@Curador`, `@Carlos`, `@Steve` ou `@Revisor-Skills` são encaminhados ao respectivo especialista (no mural da sala ativa ou via `invoke_subagent`/`send_message` quando fora de sala).

## 2. Fluxo da Sala de Produção em 3 Portões

Para cada produto (`produtos/<slug>/`):

### Portão 1 — Ficha e Ângulo Editorial (`REQ-001`, `REQ-002`)
1. Acione `@Curador` (iniciando a **sala de produção** via `swarm` ou subagente dedicado ao Portão 1) para produzir `produtos/<slug>/ficha.md` e `assets/` e rodar `python3 src/video/validate_gates.py produtos/<slug> --portao 1`.
2. Apresente os caminhos e o resumo da validação ao usuário. Só avance após aprovação explícita do Portão 1.

### Portão 2 — Storyboard Cocriado, Styleframes e Animatic (`REQ-003`, `REQ-004`)
1. **Sala de produção (`swarm`):** garanta os três especialistas ativos no mural (`curador`, `carlos`, `steve`), instruindo cada um no `brief` a ler seu arquivo de agente, sua `SKILL.md` e `.agents/formato/biblia.md`, colaborar diretamente no mural sobre o contrato compartilhado `produtos/<slug>/roteiro.md` (narrativa/fonética de `@Carlos`; decupagem visual/motores/orçamento Flow de `@Steve`; notas de fidelidade de `@Curador`) e sinalizar `@coordinator` ao concluir.
2. `@Steve` gera `1` *styleframe* local por cena e o animatic interno com voz rascunho `edge-tts` (`0` crédito Flow).
3. `@Curador` registra seu parecer de fidelidade física/factual sobre decupagem, *styleframes* e animatic.
4. **Validação determinística:** Mike executa `python3 src/video/validate_gates.py produtos/<slug> --portao 2` (`0` tokens).
5. **Espectador frio:** Mike lança uma instância nova de subagente (ex.: `research` ou `self` com prompt cego) entregando **exclusivamente** o animatic (ou os *styleframes* + áudio rascunho) **sem** `ficha.md`, `roteiro.md`, skills ou `biblia.md`, pedindo que relate: (a) o que entendeu em 1 frase, (b) onde se perdeu ou encontrou termo confuso e (c) se interromperia a rolagem nos primeiros `3s`.
6. **Correção interna em sala (teto calibrável de `3` rodadas):** se o `@Curador` ou o **Espectador frio** apontar falhas, a sala corrige na mesma instância; ao atingir `3` rodadas sem resolver, Mike escala ao usuário.
7. Apresente ao usuário: `roteiro.md`, *styleframes*, animatic, parecer do `@Curador` e relato do **Espectador frio**. A aprovação do usuário libera os créditos Google Flow e o Portão 3.

### Portão 3 — Vídeo Final e Pacote (`REQ-005` a `REQ-008`, `REQ-014`)
1. Na mesma sala de produção, `@Steve` executa clipes Flow `360p` (e *preview* interno se necessário), promove a `1080p` (`0` crédito até `10s`), sintetiza voz comercial (`Azure F0` ou `Piper pt_BR`), renderiza `video_final_1080p.mp4` e integra os textos editoriais do `@Carlos` em `pacote.md` (com `código curto`, link(s) principal(is) e aviso `REQ-007`).
2. `@Curador` emite parecer final de fidelidade sobre os quadros do vídeo e `pacote.md`; Mike executa as checagens determinísticas locais e aciona um **novo Espectador frio** (instância limpa) apenas com `video_final_1080p.mp4` (respeitando até `3` rodadas internas de correção na mesma instância).
3. Apresente ao usuário `video_final_1080p.mp4`, `pacote.md`, parecer do `@Curador` e relato do **Espectador frio**. Após o aceite final no chat, **Mike** atualiza a vitrine estática na bio (`REQ-008`).

## 3. Retro Consolidada e Evolução (`REQ-013`)

1. Ao encerrar o Portão 3 do produto, encerre os workers da sala (`swarm{action:"kill"}`) após coletar as anotações de atritos/aprendizados.
2. Conduza uma **retro curta** classificando cada aprendizado em: **(a) padrão de formato** → `.agents/formato/biblia.md`; **(b) método de ofício** → skill ou agente do dono; **(c) insumo de outra etapa** → alinhamento de contrato.
3. Caso haja alterações em `.agents/` ou `AGENTS.md`, submeta um **único diff consolidado** ao `@Revisor-Skills` (parada adaptativa até `3` rodadas). Após `APROVADO`, aplique no disco, atualize links simbólicos em `.claude/skills/` se necessário e registre um **commit isolado no Git** (`learn(retro): <produto> — <resumo>`).
