# AGENTS.md

## Projeto

Projeto de venda online, Inspetor Bicho Grilo. Ver `docs/visao.md` quando existir.

O usuário escreve a documentação com a IA como coautora. Ele a usa para decidir, e as sessões de IA a usam como memória.

## Convenções

- Escreva em português do Brasil.
- Para criar, editar ou revisar documentos em `docs/`, use a skill [documentar](.agents/skills/documentar/SKILL.md). Ela traz o método, os modelos, a regra de evidência e a regra de aceite.
- Nunca leia, imprima em logs nem versione `.env*` e outros arquivos de credenciais. Para checar a configuração, verifique só se o arquivo existe (`test -f`).
- Ao delegar a um subagente, peça só a conclusão e os caminhos dos arquivos, não dados brutos.
- Salve saídas extensas de comandos em arquivo e mostre no console só contagens e status.
- Este arquivo traz só a visão geral do projeto, comandos e convenções, como recomenda o [formato AGENTS.md](https://agents.md/). Fase, status, tarefas e mapa de documentos não entram nele, porque mudam a cada sessão e os próprios documentos já os registram.
