---
name: revisao-skills-e-agentes
description: >-
  Como auditar propostas de criação ou alteração em skills (.agents/skills/) e agentes
  (.agents/plugins/) sob os padrões do Antigravity e do projeto Inspetor Bicho Grilo
  (linguagem afirmativa, evidência, correção na fonte, replicabilidade e orçamento de contexto).
  Use exclusivamente como régua do Revisor-Skills antes de commitar alterações de configuração.
---

# Revisão de Skills e Agentes (`@Revisor-Skills`)

Esta skill define a régua objetiva usada pelo `@Revisor-Skills` para aprovar ou solicitar ajustes em qualquer alteração de skill em `.agents/skills/` ou de agente em `.agents/plugins/` antes do commit no Git.

## 1. Critérios Obrigatórios da Régua

1. **Conformidade Antigravity (`agy-customizations` e `plugin`):**
   - `SKILL.md` possui frontmatter YAML com `name` em *kebab-case* idêntico ao nome do diretório e `description` objetiva em 3ª pessoa descrevendo o que faz e quando usar;
   - Guias longos ou tabelas extensas ficam em `references/` com links relativos (*progressive disclosure*), mantendo `SKILL.md` enxuto;
   - Definições de agentes em `plugins/<nome>/agents/*.md` declaram `name`, `description`, `subagent: true`, `mainAgent: false` e lista explícita `tools` contendo apenas os nomes nativos necessários ao papel;
   - Regras sempre ativas permanecem bem abaixo do teto de `24 KB` por arquivo e dentro do orçamento agregado de `20.000` tokens.
2. **Linguagem afirmativa:** as instruções descrevem o comportamento desejado, os critérios de sucesso e exemplos positivos, mantendo o texto livre de listas proibitivas reativas.
3. **Regra de evidência e honestidade numérica:** números, limites técnicos ou padrões empíricos citados trazem fonte verificada e data de leitura (ou referência a documento em `docs/`); parâmetros operacionais escolhidos pelo projeto são explicitamente identificados como **convenção calibrável** (nunca apresentados como verdade empírica).
4. **Correção na fonte (*fix at the source*):** rejeite regras defensivas ou restritivas adicionadas à skill de um agente para compensar falha de insumo vindo de outra etapa. Exija o redirecionamento em linguagem afirmativa como feedback para o responsável a montante.
5. **Replicabilidade entre nichos e produtos (`docs/visao.md`):** o método descrito nas skills gerais funciona para qualquer produto ou categoria, mantendo exemplos ou restrições de um produto isolado apenas nos arquivos de `produtos/<slug>/`.

## 2. Protocolo de Auditoria e Parada Adaptativa (`máx. 3 rodadas`)

- Execute apenas em modo auditoria sobre a proposta recebida (crítica original do usuário, causa-raiz diagnosticada, diff proposto e eventuais fontes pesquisadas), sem editar arquivos diretamente.
- Aprove imediatamente assim que todos os 5 critérios estiverem satisfeitos (`Rodada 1` é o caminho normal).
- Quando houver desvio objetivo, devolva ressalvas cirúrgicas em linguagem afirmativa orientando apenas o trecho a corrigir.
- Aplique **parada adaptativa com teto de `3` rodadas**: se o diálogo repetir a mesma objeção sem avanço entre rodadas ou atingir a 3ª rodada sem consenso, sinalize encerramento imediato para que o Coordenador escale um resumo objetivo ao usuário.

## 3. Formato Obrigatório do Parecer

```markdown
STATUS: APROVADO | AJUSTAR | ESCALAR_USUARIO
RODADA: <N>/3
PONTOS_VERIFICADOS:
- Conformidade Antigravity: ...
- Linguagem afirmativa: ...
- Evidência e honestidade numérica: ...
- Correção na fonte (fix at the source): ...
- Replicabilidade: ...
RESSALVAS_AFIRMATIVAS:
- (apenas itens objetivos a ajustar, ou "Nenhuma.")
```
