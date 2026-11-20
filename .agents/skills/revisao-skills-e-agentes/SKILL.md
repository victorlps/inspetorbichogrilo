---
name: revisao-skills-e-agentes
description: >-
  Como auditar propostas de criação ou alteração em skills (.agents/skills/), agentes
  (.agents/plugins/) e regras de equipe sob os padrões do Antigravity e do projeto Inspetor
  Bicho Grilo (linguagem afirmativa, evidência, correção na fonte, replicabilidade e orçamento de
  contexto). Use exclusivamente como régua do Revisor-Skills antes de commitar alterações de configuração.
---

# Revisão de Skills e Agentes (`@Revisor-Skills`)

Esta skill define a régua objetiva usada pelo `@Revisor-Skills` para auditar propostas de criação ou alteração em `.agents/skills/`, `.agents/plugins/` ou regras de equipe em `AGENTS.md` (enviadas por `@Curador`, `@Carlos`, `@Steve` ou por `Mike`, Coordenador) antes do commit no Git.

## 1. Critérios Obrigatórios da Régua

1. **Conformidade Antigravity (`agy-customizations`, `plugin` e `migrate-agent-settings`):**
   - Consulte diretamente, quando aplicável a schemas ou limites (resolvendo `$HOME` via `echo "$HOME"` caso `read_file` exija caminho iniciado em `/`): `~/.gemini/antigravity/builtin/skills/agy-customizations/docs/{rules.md,skills.md,plugins.md}`, `~/.gemini/antigravity/builtin/skills/plugin/SKILL.md` e `~/.gemini/antigravity/builtin/skills/migrate-agent-settings/SKILL.md` (lidos em `2026-11-19`);
   - `SKILL.md` possui frontmatter YAML com `name` em *kebab-case* idêntico ao nome do diretório e `description` objetiva em 3ª pessoa descrevendo o que faz e quando usar;
   - Materiais de apoio extensos (guias detalhados, tabelas longas, exemplos) ficam em `references/` com links relativos (*progressive disclosure*), mantendo o `SKILL.md` principal conciso e direto ao fluxo;
   - Definições de agentes em `.agents/plugins/<nome>/agents/*.md` declaram `name`, `description`, lista explícita `tools` contendo apenas os nomes nativos necessários ao papel e `subagent: true` / `mainAgent: false` como padrão dos especialistas (aceitando `mainAgent: true` apenas quando o papel for desenhado explicitamente para atuar também como agente principal);
   - Regras sempre ativas (`AGENTS.md`) respeitam o teto de **`24 KB` (`24.000` bytes)** por arquivo e o orçamento agregado de **`20.000` tokens** definidos em `~/.gemini/antigravity/builtin/skills/agy-customizations/docs/rules.md` (lido em `2026-11-19`), conferido via `wc -c` e mantendo as descrições em frontmatter enxutas.
2. **Linguagem afirmativa:** as instruções descrevem o comportamento desejado, os critérios positivos de verificação e exemplos do resultado esperado, mantendo o estilo livre de listas proibitivas reativas; fronteiras estruturais de segurança ou de papel (como manter `.env*` fora de leitura, preservar modo auditoria sem escritas ou não invocar colegas especialistas via `invoke_subagent`) devem explicitar claramente o escopo positivo permitido e o limite operacional.
3. **Regra de evidência e honestidade numérica:** números, limites técnicos ou padrões empíricos citados trazem fonte verificada e data de leitura (ou referência a documento em `docs/`); parâmetros operacionais escolhidos pelo projeto são explicitamente identificados como **convenção calibrável** (ou equivalente explícito como *parâmetro operacional calibrável*) vinculado a um ADR em `docs/decisoes/`.
4. **Correção na fonte (*fix at the source*):** utilizando o mapa da equipe em `revisor-skills.md`, rejeite acréscimo de regras defensivas na skill de um agente para compensar falha de insumo vindo de outro responsável (ex.: `@Curador`, `@Carlos`, `@Steve` ou `Mike`, Coordenador); exija o redirecionamento em linguagem afirmativa como feedback para o responsável na origem.
5. **Replicabilidade entre nichos e produtos (`docs/visao.md`):** o método descrito nas skills gerais e agentes funciona para qualquer produto ou categoria, mantendo exemplos ou restrições específicas de um único produto apenas em `produtos/<slug>/`.

## 2. Contrato de Entrada, Auditoria e Parada Adaptativa

- **Convenção calibrável de rodadas ([0007](../../../docs/decisoes/0007-equipe-agentes-especializados-e-governanca-skills.md)):** este protocolo aplica **parada adaptativa com teto calibrável de `3` rodadas** entre o proponente (via Mike, Coordenador) e `@Revisor-Skills`.
- **Contrato de entrada esperado de Mike:** `RODADA: N/3`, pareceres das rodadas anteriores (quando `N > 1`), crítica/origem da mudança, diagnóstico de causa-raiz, caminho(s) do(s) arquivo(s) alvo, diff ou proposta completa de texto e eventuais fontes consultadas. Leia o(s) arquivo(s) alvo atuais no disco via `read_file` (e confira bytes via `wc -c` em `run_command` somente-leitura quando tocar `AGENTS.md`). Se faltar item essencial para auditar, devolva `STATUS: AJUSTAR` nas Rodadas `1/3` e `2/3` (ou `STATUS: ESCALAR_USUARIO` na Rodada `3/3`) solicitando exatamente os insumos faltantes.
- **Execução estritamente somente-leitura:** emita apenas o parecer sem editar arquivos no disco nem gravar logs temporários.
- **Critério objetivo dos 3 status:**
  - `APROVADO`: todos os 5 critérios da Seção 1 estão atendidos (caminho normal esperado já na Rodada `1/3`);
  - `AJUSTAR`: válido apenas nas Rodadas `1/3` e `2/3` quando há correções cirúrgicas pendentes ou avanço objetivo frente à rodada anterior;
  - `ESCALAR_USUARIO`: obrigatório sempre que **(a)** na Rodada `2/3` persistir o mesmo item pendente em `AJUSTE` sem avanço objetivo frente às `RESSALVAS_AFIRMATIVAS` da Rodada 1 (estagnação), **ou (b)** a Rodada `3/3` encerrar sem atender todos os 5 critérios.

## 3. Formato Obrigatório do Parecer

```markdown
STATUS: APROVADO | AJUSTAR | ESCALAR_USUARIO
RODADA: <N>/3
PONTOS_VERIFICADOS:
- Conformidade Antigravity: <OK | AJUSTE — evidência curta>
- Linguagem afirmativa: <OK | AJUSTE — evidência curta>
- Evidência e honestidade numérica: <OK | AJUSTE — evidência curta>
- Correção na fonte (fix at the source): <OK | AJUSTE — evidência curta>
- Replicabilidade: <OK | AJUSTE — evidência curta>
RESSALVAS_AFIRMATIVAS:
- <Com STATUS APROVADO: "Nenhuma.">
- <Com STATUS AJUSTAR: lista cirúrgica em linguagem afirmativa do que ajustar.>
- <Com STATUS ESCALAR_USUARIO: resumo objetivo do impasse e das opções para decisão do usuário.>
```
