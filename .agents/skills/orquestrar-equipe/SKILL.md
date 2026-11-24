---
name: orquestrar-equipe
description: >-
  Como Mike (Coordenador) conduz a sala de produção por produto (Swarm enxuto com Curador, Carlos
  e Steve), aciona o Espectador frio sobre caráter educativo e animação visual, gerencia os 3
  Portões com o usuário, conduz a retro consolidada com o Revisor-Skills e roteia menções nominais.
---

# Orquestrar Equipe e Sala de Produção — Mike (`@Mike`)

Runbook operacional do agente principal (**Mike**, `@Mike`, Coordenador — única interface direta com o usuário) conforme [0008-sala-de-producao-coautoria-e-tres-portoes.md](../../../docs/decisoes/0008-sala-de-producao-coautoria-e-tres-portoes.md), [fase-1.md](../../../docs/requisitos/fase-1.md) e [.agents/formato/biblia.md](../../formato/biblia.md).

## 1. Roteamento Nominal e Proteção Proativa de Cota

Mensagens para `@Mike` ou gerais são atendidas diretamente por Mike. Pedidos diretos para `@Curador`, `@Carlos`, `@Steve` ou `@Revisor-Skills` são encaminhados ao respectivo especialista (no mural da sala ativa ou via `invoke_subagent`/`send_message`).

Em execuções multi-etapas sujeitas à janela de renovação de cota ([antigravity.google/docs/plans](https://antigravity.google/docs/plans) e [antigravity.google/docs/commands/schedule](https://antigravity.google/docs/commands/schedule), verificados em `2026-11-24`), Mike mantém um checkpoint atualizado no diretório de artefatos da conversa (`execution_state.md`) e registra logo no início da execução um *watchdog* proativo via ferramenta `schedule` (`CronExpression`, `IsDaemon: false`), garantindo retomada automática após a renovação da janela caso um turno seja interrompido no servidor; ao concluir a entrega final, Mike encerra o agendamento via `manage_task` (`Action="kill"`).

## 2. Fluxo da Sala de Produção em 3 Portões

Para cada tema/produto (`produtos/<slug>/`):

### Portão 1 — Dossiê Científico e Comercial (`REQ-001`, `REQ-002`)
1. Acione `@Curador` para produzir `produtos/<slug>/ficha.md` (cobrindo tanto a ciência/engenharia de *"como funciona"* e o confronto com técnicas alternativas quanto a auditoria do produto exemplar e seus ativos em `assets/`) e rodar `python3 src/video/validate_gates.py produtos/<slug> --portao 1`.
2. Apresente os caminhos e o resumo da validação ao usuário, avançando após aprovação do Portão 1 (ou em fluxo contínuo quando expressamente autorizado pelo usuário para calibração).

### Portão 2 — Storyboard Investigativo, Animações de Rascunho e Animatic (`REQ-003`, `REQ-004`)
1. **Sala de produção (`swarm` ou coautoria estruturada):** garanta os três especialistas alinhados sobre `.agents/formato/biblia.md` e `produtos/<slug>/roteiro.md` (narrativa investigativa *"Como as coisas funcionam?"* e fonética de `@Carlos`; coreografia de simulações animadas, motores e orçamento Flow de `@Steve`; notas de fidelidade científica e física de `@Curador`).
2. `@Steve` captura os quadros de transformação por cena e gera `animatic_portao2.mp4` com voz rascunho `edge-tts` em cadência natural (`0` crédito Flow).
3. `@Curador` registra seu parecer de fidelidade científica e morfológica sobre decupagem, quadros e animatic.
4. **Validação determinística:** Mike executa `python3 src/video/validate_gates.py produtos/<slug> --portao 2` (`0` tokens).
5. **Espectador frio:** Mike lança uma instância limpa de subagente (`research` ou `self` com contexto zero) entregando **exclusivamente** o animatic/quadros + áudio, pedindo avaliação objetiva sobre 4 pontos:
   - **(a) Aprendizado real:** o que aprendeu sobre *como o assunto funciona* em 1–2 frases;
   - **(b) Caráter informativo vs. propaganda:** se o episódio transmite caráter genuinamente educativo (*"como as coisas funcionam?"*) com entrada natural e pontual do produto exemplar;
   - **(c) Animação visual vs. slides:** se a explicação acontece por demonstrações visuais animadas em movimento contínuo (ou se alguma cena ainda lembra quadro estático de texto);
   - **(d) Retenção e clareza:** se pararia a rolagem nos primeiros `3s` e se algum termo/ritmo gerou dúvida.
6. **Correção interna em sala (teto calibrável de `3` rodadas):** caso o `@Curador` ou o **Espectador frio** aponte sensação de propaganda, excesso de texto em tela ou falha física, a equipe refina na mesma instância antes da entrega; persistindo impasse na `3ª` rodada, Mike escala ao usuário.
7. Apresente ao usuário `roteiro.md`, quadros, animatic, parecer do `@Curador` e relato do **Espectador frio**.

### Portão 3 — Episódio Final Animado `1080p` e Pacote (`REQ-005` a `REQ-008`, `REQ-014`)
1. `@Steve` produz os planos `flow_ia` aprovados, sintetiza a voz comercial em cadência natural (`Azure F0` ou `Piper pt_BR`), renderiza as simulações animadas e composições em `video_final_1080p.mp4` (em duração orgânica livre) e integra os textos e variações do `@Carlos` em `pacote.md` (com código curto, links e aviso `REQ-007`). Cortes derivados opcionais para plataformas de teto curto (`--ml-clips`) são gerados sob demanda na etapa de publicação.
2. `@Curador` emite parecer final de fidelidade científica e física; Mike roda `python3 src/video/validate_gates.py produtos/<slug> --portao 3` e aciona uma **nova instância limpa de Espectador frio** avaliando os mesmos 4 critérios sobre `video_final_1080p.mp4` (e quadros em início/meio/fim de cada cena), iterando até `3` rodadas internas se necessário.
3. Apresente ao usuário `video_final_1080p.mp4`, `pacote.md`, parecer do `@Curador` e relato do **Espectador frio**. Após o aceite final no chat, **Mike** ativa o item em `vitrine/catalogo.json` (`REQ-008`) e executa autonomamente a sincronização de links curtos de afiliado, o deploy da vitrine no GitHub Pages e a publicação nas plataformas via `src/publish/publish_all.py`, seguindo [checklist-publicacao.md](references/checklist-publicacao.md).

## 3. Retro Consolidada e Evolução (`REQ-013`)

1. Ao encerrar o produto, colete os aprendizados da equipe e encerre eventuais workers ativos (`swarm{action:"kill"}`).
2. Classifique cada aprendizado na fonte correta: **(a) padrão de formato** → `.agents/formato/biblia.md`; **(b) método de ofício** → skill ou agente do dono; **(c) insumo entre etapas** → ajuste de contrato.
3. Quando houver evolução em `.agents/` ou `AGENTS.md`, submeta um **único diff consolidado** ao `@Revisor-Skills` (parada adaptativa até `3` rodadas). Após `APROVADO`, mantenha os links simbólicos em `.claude/skills/` alinhados e registre commit isolado no Git (`learn(retro): <produto> — <resumo>`).
