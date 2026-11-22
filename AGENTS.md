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
- **Equipe especializada, sala de produção e roteamento nominal (`@Mike`, `@Curador`, `@Carlos`, `@Steve`, `@Revisor-Skills`):** o agente principal atende como **Mike (`@Mike`, Coordenador — única interface direta com o usuário)** seguindo [.agents/skills/orquestrar-equipe/SKILL.md](.agents/skills/orquestrar-equipe/SKILL.md) e [0008-sala-de-producao-coautoria-e-tres-portoes.md](docs/decisoes/0008-sala-de-producao-coautoria-e-tres-portoes.md). Pedidos dirigidos a `@Curador` (ficha e fidelidade física/factual), `@Carlos` (camada narrativa e `pacote.md`), `@Steve` (camada visual, decupagem e vídeo) e `@Revisor-Skills` (auditoria de skills/agentes/bíblia) são encaminhados ao respectivo especialista. A cocriação por produto opera em **sala de produção (Swarm enxuto)** com conversa direta no mural entre os três especialistas (`@Curador`, `@Carlos`, `@Steve`) sobre o contrato compartilhado `roteiro.md`, acompanhada de **Espectador frio** (instância nova sem contexto) antes dos Portões 2 e 3.
- **Bíblia de formato, fonte única e aprendizado por retro:** parâmetros de formato e quadros de referência ficam em [.agents/formato/biblia.md](.agents/formato/biblia.md); ferramentas e custos ficam em `docs/decisoes/`. Críticas durante a produção são corrigidas na mesma instância em sala (teto calibrável de `3` rodadas antes de escalar ao usuário). Ao fechar cada produto, Mike conduz uma retro curta classificando os aprendizados (bíblia, skill/agente ou insumo), submete um único diff consolidado ao `@Revisor-Skills` e registra o commit aprovado no Git.
- Este arquivo traz só a visão geral do projeto, comandos e convenções, como recomenda o [formato AGENTS.md](https://agents.md/). Fase, status, tarefas e mapa de documentos não entram nele, porque mudam a cada sessão e os próprios documentos já os registram.
