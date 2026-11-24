---
name: revisao-skills-e-agentes
description: >-
  Como auditar o diff consolidado da retro de cada produto (ou propostas estruturais) em
  .agents/formato/biblia.md, .agents/skills/, .agents/plugins/ e AGENTS.md sob os padrões do
  Antigravity e do projeto Inspetor Bicho Grilo.
---

# Revisão de Skills, Agentes e Bíblia (`@Revisor-Skills`)

Régua objetiva usada pelo `@Revisor-Skills` para auditar o diff consolidado da retro de cada produto (ou ajustes estruturais enviados por `@Mike`) antes do commit no Git.

## 1. Critérios Obrigatórios da Régua

1. **Conformidade Antigravity (`agy-customizations`, `plugin`):**
   - Consulte quando necessário `~/.gemini/antigravity/builtin/skills/agy-customizations/docs/{rules.md,skills.md,plugins.md}` e `~/.gemini/antigravity/builtin/skills/plugin/SKILL.md` (lidos em `2026-11-19`);
   - `SKILL.md` traz `name` em *kebab-case* igual ao diretório e `description` em 3ª pessoa; materiais extensos ficam em `references/`;
   - Agentes em `.agents/plugins/<nome>/agents/*.md` declaram `name`, `description`, `tools` mínimas ao papel e `subagent: true` / `mainAgent: false`;
   - `AGENTS.md` respeita o teto de **`24 KB` (`24.000` bytes)** e orçamento agregado de **`20.000` tokens** (verificado via `wc -c`).
2. **Linguagem de papéis e afirmativa:** agentes e skills descrevem de forma positiva o que cada papel possui, com quem colabora e os critérios esperados de execução.
3. **Fonte única (*single source of truth*):** parâmetros de formato (identidade editorial, área segura, legendas, rótulos espaciais e orçamento de palavras em tela) moram em `.agents/formato/biblia.md`; ferramentas e custos moram em `docs/decisoes/`; skills e agentes apontam para essas fontes evitando duplicar valores numéricos.
4. **Evidência e honestidade numérica:** fatos externos trazem fonte e data de leitura (ou link para `docs/`); convenções calibráveis estão vinculadas a um ADR.
5. **Correção na fonte (*fix at the source*) e Replicabilidade (`docs/visao.md`):** cada ajuste vai para o lugar certo (padrão de formato → `biblia.md`; método de ofício → skill/agente do dono) e funciona para qualquer produto ou nicho, mantendo particularidades de um produto apenas em `produtos/<slug>/`.

## 2. Contrato de Entrada, Parada Adaptativa e Parecer

- **Teto calibrável (`0007` / `0008`):** parada adaptativa em até **`3` rodadas** entre `@Mike` e `@Revisor-Skills`.
- **Entrada esperada:** `RODADA: N/3`, pareceres anteriores (se `N > 1`), resumo da retro do produto (ou origem da mudança), caminho(s) alvo, diff consolidado e fontes. Leia os arquivos atuais em disco via `read_file` e opere em modo estritamente somente-leitura.
- **Formato do parecer:**

```markdown
STATUS: APROVADO | AJUSTAR | ESCALAR_USUARIO
RODADA: <N>/3
PONTOS_VERIFICADOS:
- Conformidade Antigravity: <OK | AJUSTE — evidência curta>
- Linguagem de papéis e afirmativa: <OK | AJUSTE — evidência curta>
- Fonte única: <OK | AJUSTE — evidência curta>
- Evidência e honestidade numérica: <OK | AJUSTE — evidência curta>
- Correção na fonte e Replicabilidade: <OK | AJUSTE — evidência curta>
RESSALVAS_AFIRMATIVAS:
- <Com STATUS APROVADO: "Nenhuma.">
- <Com STATUS AJUSTAR: lista cirúrgica em linguagem afirmativa do que ajustar.>
- <Com STATUS ESCALAR_USUARIO: resumo objetivo do impasse e opções para decisão do usuário.>
```
