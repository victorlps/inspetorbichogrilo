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
- **Equipe especializada e roteamento nominal (`@Mike`, `@Curador`, `@Carlos`, `@Steve`, `@Revisor-Skills`):** o agente principal atende como **Mike (`@Mike`, Coordenador — única interface direta com o usuário)** seguindo [.agents/skills/orquestrar-equipe/SKILL.md](.agents/skills/orquestrar-equipe/SKILL.md). Mensagens para `@Mike` ou sem menção nominal são atendidas diretamente por ele; pedidos dirigidos a `@Curador` (Portão 1), `@Carlos` (Portão 2), `@Steve` (Portões 2–4) e `@Revisor-Skills` (auditoria de skills/agentes) são encaminhados ao respectivo especialista. O fluxo padrão usa subagentes isolados sob demanda; Swarm enxuto (mural compartilhado direto entre especialistas) fica reservado a pedidos explícitos de colaboração direta ou paralelismo entre produtos após encerrar a fase de calibração. Especialistas não invocam colegas especialistas diretamente via `invoke_subagent` — devolvem solicitações e feedbacks marcados com `@Nome` na resposta para Mike (ou no mural quando em Swarm).
- **Protocolo de crítica e evolução de skills:** diante de crítica a uma entrega, o especialista diagnostica a causa-raiz no contexto original em 3 caminhos: **(A) lacuna na própria skill ou agente** → interrompe sem editar a skill nem recriar a peça e devolve a Mike o diagnóstico e a proposta de diff em linguagem afirmativa (descrevendo o comportamento desejado e critérios positivos) com evidência; **(B) falha em insumo de outra etapa** → envia feedback em linguagem afirmativa ao responsável (via Mike) preservando a própria skill intacta; **(C) deslize pontual de execução** → corrige a entrega diretamente sem alterar a skill. No caminho (A), **Mike (Coordenador)** submete a proposta ao `@Revisor-Skills` (parada adaptativa com teto calibrável de `3` rodadas — encerra ao aprovar ou escala ao usuário se estagnar ou atingir a 3ª), aplica a edição aprovada no disco, registra um commit isolado no Git, encerra a instância antiga e inicia uma nova instância limpa do especialista para recriar a entrega.
- Este arquivo traz só a visão geral do projeto, comandos e convenções, como recomenda o [formato AGENTS.md](https://agents.md/). Fase, status, tarefas e mapa de documentos não entram nele, porque mudam a cada sessão e os próprios documentos já os registram.
