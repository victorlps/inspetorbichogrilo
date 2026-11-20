# AGENTS.md

## Projeto

Projeto de venda online, Inspetor Bicho Grilo. Ver `docs/visao.md`.

O usuário escreve a documentação com a IA como coautora. Ele a usa para decidir, e as sessões de IA a usam como memória.

## Convenções

- Escreva em português do Brasil.
- Para criar, editar ou revisar documentos em `docs/`, use a skill [documentar](.agents/skills/documentar/SKILL.md). Ela traz o método, os modelos, a regra de evidência e a regra de aceite.
- Decisões de projeto, especificações de design e requisitos — mesmo quando surgirem durante a execução em `assets/`, `src/` ou outras pastas — devem ir para `docs/decisoes/` (MADR) ou `docs/requisitos/` (EARS), nunca para arquivos `README.md` ou notas soltas ad-hoc.
- Nunca leia, imprima em logs nem versione `.env*` e outros arquivos de credenciais. Para checar a configuração, verifique só se o arquivo existe (`test -f`).
- Ao delegar a um subagente, peça só a conclusão e os caminhos dos arquivos, não dados brutos.
- Salve saídas extensas de comandos em arquivo e mostre no console só contagens e status.
- **Equipe especializada e roteamento nominal (`@Curador`, `@Carlos`, `@Steve`, `@Revisor-Skills`):** o agente principal atua como Coordenador seguindo `.agents/skills/orquestrar-equipe/SKILL.md`. Mensagens dirigidas a `@Curador`, `@Carlos`, `@Steve` ou `@Revisor-Skills` são encaminhadas ao respectivo especialista em contexto isolado; o fluxo padrão dos Portões 1 a 4 usa subagentes sob demanda, reservando Swarm enxuto para pedidos explícitos de colaboração direta ou paralelismo entre produtos.
- **Protocolo de crítica e evolução de skills:** diante de crítica a uma entrega, o especialista avalia a causa-raiz no contexto original. Se a origem estiver em insumo de outra etapa, envia feedback em linguagem afirmativa ao responsável e mantém a própria skill limpa. Se exigir ajuste na própria skill ou agente, propõe a edição em linguagem afirmativa e com evidência ao `@Revisor-Skills` (parada adaptativa, teto de 3 rodadas). Após aprovação, registra um commit isolado no Git e recria a entrega em uma nova instância limpa desse especialista.
- Este arquivo traz só a visão geral do projeto, comandos e convenções, como recomenda o [formato AGENTS.md](https://agents.md/). Fase, status, tarefas e mapa de documentos não entram nele, porque mudam a cada sessão e os próprios documentos já os registram.
