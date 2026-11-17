---
name: documentar
description: Como escrever os documentos deste projeto (visão, requisitos, decisões e notas de pesquisa) junto com o usuário, com os modelos e a regra de evidência. Use ao criar, editar ou revisar qualquer arquivo em docs/.
---

# Documentar

Fontes lidas em 2026-11-17.

## Como trabalhar

O método vem da skill [doc-coauthoring](https://github.com/anthropics/skills/tree/main/skills/doc-coauthoring), da Anthropic, reduzido ao que serve a um projeto do usuário com a IA como coautora. Os documentos são do usuário: suposições da IA, como metas e números sem fonte, viram regra sem base.

- Antes de escrever, pergunte ao usuário o contexto que falta. Não suponha leitores, metas nem números.
- Antes de redigir, apresente as opções e deixe o usuário escolher o que entra.
- Pergunte uma decisão por vez, com as opções e o efeito de cada uma, e só o que a fase atual precisa decidir. Não embuta na pergunta uma troca que o usuário não aceitou. Perguntas abertas, agrupadas ou que antecipam fases futuras deixam o usuário sem como escolher.
- Prefira edições pequenas e revisáveis a reescritas.
- Ao terminar, teste o documento com um leitor sem contexto, que responde perguntas só com o texto e confere se cada afirmação continua fiel à fonte.

## Onde esta skill fica

A skill fica em `.agents/skills/documentar/`, caminho lido pelo [Antigravity](https://antigravity.google/docs/skills) e pelo [Gemini CLI](https://geminicli.com/docs/cli/skills/). O Claude Code lê skills só em `.claude/skills/` e aceita ali um link simbólico para outra pasta ([skills](https://code.claude.com/docs/en/skills)); por isso `.claude/skills/documentar` é um link para ela. As regras de toda sessão ficam no `AGENTS.md`, na raiz, e não há `CLAUDE.md` nem `GEMINI.md`: o Antigravity lê o `AGENTS.md` sempre, e o Claude Code o lê quando não há `CLAUDE.md`, a partir da versão 2.1.277 ([memória](https://code.claude.com/docs/en/memory)). O motivo é que o projeto precisa poder ser trabalhado por qualquer motor.

## Onde cada coisa fica

| Documento | Arquivo | Conteúdo |
|---|---|---|
| Visão | `docs/visao.md` | Objetivo, escopo, qualidades, como o usuário trabalha e restrições. |
| Requisitos | `docs/requisitos/` | Comportamentos testáveis. |
| Decisões | `docs/decisoes/NNNN-titulo.md` | Uma decisão por arquivo. As regras que uma decisão gera ficam nesta skill, cada uma com o motivo e o link para a decisão. |
| Pesquisa | `docs/pesquisa/tema.md` | Uma pergunta por arquivo. |

- Outros tipos de documento entram nesta tabela só quando o usuário pedir.
- Uma pasta só é criada junto com o primeiro documento dela, para que a estrutura só cresça quando houver conteúdo.
- Escreva de forma afirmativa, no presente: o documento descreve o estado atual, e o porquê de cada escolha fica na decisão que a registra.
- Tarefas, próximos passos e status não entram nos documentos.

## Evidência

A regra existe para que cada fato tenha fonte, data de leitura e, se mudar com o tempo, prazo para reverificar.

- Fato externo leva link da fonte oficial e data de leitura. Se todas as fontes do documento foram lidas no mesmo dia, basta uma linha no topo: "Fontes lidas em AAAA-MM-DD."
- Dado que muda com o tempo (preço, limite, termos de uso) leva "Reverificar até AAAA-MM-DD."
- Sem fonte oficial, o fato é marcado como **não verificado** e não sustenta decisão.
- Inferência é marcada como **inferência**.
- Dado informado pelo usuário é identificado como tal e não precisa de link.

## Aceite

Só o usuário aceita um documento, porque as decisões do projeto são dele. Visão e requisitos começam, logo abaixo do título, com "Proposto em AAAA-MM-DD." Quando o usuário aceitar no chat, troque por "Aceito por victor em AAAA-MM-DD." Decisões registram o aceite no campo `status` do MADR, abaixo. Notas de pesquisa não têm aceite: são evidência, e o aceite acontece na decisão que as usa.

## Requisitos

Requisitos usam EARS para que cada um tenha um critério de aceite que o usuário observa sem ler código.

Cada requisito tem:
- ID estável (`REQ-001`), nunca reutilizado;
- frase numa das formas do [EARS](https://alistairmavin.com/ears/), abaixo;
- critério de aceite que o usuário observa sem ler código.

"Deve" traduz "shall". Não use "pode" nem "deveria" em requisito.

| Padrão EARS | Forma em português |
|---|---|
| Ubíquo | O `<sistema>` deve `<resposta>`. |
| Por estado (While) | Enquanto `<pré-condição>`, o `<sistema>` deve `<resposta>`. |
| Por evento (When) | Quando `<gatilho>`, o `<sistema>` deve `<resposta>`. |
| Recurso opcional (Where) | Onde houver `<recurso>`, o `<sistema>` deve `<resposta>`. |
| Comportamento indesejado (If/Then) | Se `<gatilho indesejado>`, então o `<sistema>` deve `<resposta>`. |
| Complexo | Enquanto `<pré-condição>`, quando `<gatilho>`, o `<sistema>` deve `<resposta>`. |

## Decisões

Use as seções do [modelo mínimo do MADR 4.0.0](https://raw.githubusercontent.com/adr/madr/4.0.0/template/adr-template-minimal.md), em português, com o cabeçalho de estado do [modelo completo](https://raw.githubusercontent.com/adr/madr/4.0.0/template/adr-template.md), porque ele registra o contexto, as opções e o motivo de qualquer escolha. A seção de consequências é opcional.

```markdown
---
status: "proposed"
date: AAAA-MM-DD
decision-makers: victor
---

# <título curto: problema e solução>

## Contexto e problema

## Opções consideradas

## Decisão

Opção escolhida: <opção>, porque <justificativa>.

### Consequências

- Bom: ...
- Ruim: ...
```

O `status` usa os valores do MADR: `proposed`, `accepted`, `rejected`, `deprecated` ou `superseded by NNNN`. Quando o usuário aceitar no chat, passe a `accepted` e atualize a data.

## Pesquisa

- Não há lista separada de perguntas de pesquisa: cada nota é uma pergunta, porque uma lista de perguntas é plano de trabalho, não documento.
- O título é a pergunta que a nota responde, descrita pelo problema, não pela categoria de ferramenta, porque partir da categoria já escolhe a solução antes de entender o problema.
- Separe fatos (com fonte) de inferências.
- Nenhuma recomendação antes da evidência, porque uma opção recomendada cedo ancora a escolha do usuário.
