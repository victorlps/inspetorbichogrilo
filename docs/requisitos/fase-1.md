# Requisitos — Fase 1 (Inspetor Bicho Grilo)

Aceito por victor em 2026-11-17.

Requisitos derivados de [visao.md](../visao.md) e das decisões aceitas em [0001-canais-e-afiliados-fase-1.md](../decisoes/0001-canais-e-afiliados-fase-1.md), [0002-pipeline-personagem-e-video.md](../decisoes/0002-pipeline-personagem-e-video.md) e [0003-fluxo-aprovacao-e-publicacao.md](../decisoes/0003-fluxo-aprovacao-e-publicacao.md).

## Curadoria e Portão 1

- **REQ-001:** Enquanto o fluxo estiver em calibração, o sistema deve processar um produto candidato por vez, gerando uma ficha de curadoria (`ficha.md`) na pasta do produto contendo o problema real resolvido, as especificações com fontes verificadas, a loja e o link principal de afiliado, o ângulo editorial e as referências audiovisuais do produto (imagens incorporadas e links diretos para eventuais vídeos locais de referência) antes de iniciar qualquer roteiro.
  - **Critério de aceite:** O usuário abre `ficha.md` no *preview* de Markdown, visualiza diretamente as imagens do produto (e links clicáveis para vídeos de referência, quando houver) junto aos cinco itens preenchidos, e verifica que nenhum arquivo de roteiro, áudio ou vídeo foi criado ainda e nenhum outro produto foi iniciado em paralelo.

- **REQ-002:** Quando o usuário aprovar a ficha de curadoria no chat, o sistema deve liberar a criação do roteiro; se o usuário reprovar ou pedir ajustes, o sistema deve atualizar ou marcar apenas `ficha.md` como descartada sem executar roteiro, geração de áudio ou renderização.
  - **Critério de aceite:** Após aprovação no chat, o arquivo de roteiro é criado na pasta do produto; após reprovação ou pedido de ajuste, apenas `ficha.md` é alterada, sem criação de arquivos de roteiro, áudio ou vídeo.

## Roteiro e Portão 2

- **REQ-003:** Enquanto o produto estiver na etapa de roteiro, o sistema deve produzir `roteiro.md` com a fala exata cronometrada, a lista de cenas por trecho com referências visuais incorporadas/clicáveis (imagens e clipes de apoio) e a indicação de elegibilidade ao Mercado Livre Clips (uso real do produto e ausência de menção a preço variável enquanto a regra do ML não for verificada em fonte oficial).
  - **Critério de aceite:** O usuário abre `roteiro.md` no *preview* de Markdown e confere as falas com duração estimada, a descrição e miniatura/link de cada cena audiovisual e, quando marcado como elegível ao ML Clips, a ausência de preço variável falado e a previsão de trecho em uso real.

- **REQ-004:** Quando o usuário aprovar o roteiro no chat, o sistema deve liberar o Portão 3 (ou o Portão 4 caso o usuário tenha dispensado explicitamente o Portão 3); se o usuário reprovar ou pedir alterações, o sistema deve revisar apenas o roteiro sem gerar áudio ou renderização.
  - **Critério de aceite:** Após aprovação no chat, o fluxo avança para a geração do *preview* leve (ou render final, se o Portão 3 estiver dispensado); após pedido de ajuste ou reprovação, apenas o arquivo de roteiro é alterado, sem criação de arquivos de áudio ou vídeo.

## Personagem, *Preview* (Portão 3) e Pacote Final (Portão 4)

- **REQ-005:** Enquanto o usuário não dispensar explicitamente o Portão 3 após calibrar dicção e enquadramento, o sistema deve gerar a narração em áudio e um único vídeo de *preview* leve (`preview.mp4`) em baixa resolução já com áudio e imagem combinados do personagem sincronizado (Rig 2.5D + eventual rascunho *Omni 360p*) antes da renderização final em alta definição.
  - **Critério de aceite:** O usuário encontra `preview.mp4` na pasta do produto, reproduz diretamente no player padrão do sistema para conferir dicção, sincronia labial e enquadramento com som e imagem juntos, e verifica que nenhum vídeo MP4 final em alta definição foi gerado ainda.

- **REQ-006:** Quando o usuário aprovar o *preview* leve (ou aprovar o roteiro com o Portão 3 dispensado), o sistema deve gerar o vídeo vertical (`9:16`) final do personagem com *lip-sync* local (Rig 2.5D + eventual clipe final do Google Flow), compô-lo com trechos visuais do produto obtidos de fontes autorizadas ou da sessão do usuário e gerar o pacote de publicação (`pacote.md` com legenda, palavras-chave/tags, código curto da vitrine, link principal de afiliado e instruções de postagem) junto ao arquivo MP4 final sem marca d'água.
  - **Critério de aceite:** Somente após essa aprovação o usuário encontra na pasta do produto o vídeo MP4 vertical em alta definição sem marca d'água (com personagem sincronizado e visuais do produto) e o arquivo `pacote.md` completo para upload manual nas plataformas.

- **REQ-007:** Se o vídeo incluir cenário ou *B-roll* fotorrealista gerado por IA, ou for destinado ao TikTok enquanto a isenção para mascote 3D estilizado não estiver verificada, então o sistema deve registrar em `pacote.md` o aviso para ativar ou conferir a marcação de conteúdo sintético na plataforma aplicável.
  - **Critério de aceite:** Ao abrir `pacote.md` de um vídeo com trecho fotorrealista gerado por IA (ou destinado ao TikTok), o usuário vê o aviso explícito de marcação de IA junto às instruções de postagem; quando não aplicável, o aviso não aparece.

## Vitrine de links e conversão

- **REQ-008:** Quando o usuário aprovar o pacote final no Portão 4 no chat, o sistema deve adicionar o produto à página estática da vitrine de links na bio com busca e código curto único do vídeo apontando para o link principal de afiliado aprovado; se o Portão 4 for reprovado, o sistema deve manter a vitrine inalterada.
  - **Critério de aceite:** Antes da aprovação no Portão 4, o produto não aparece na vitrine; após a aprovação no chat, o usuário abre a página da vitrine, busca pelo código curto informado em `pacote.md` ou pelo nome do produto e confirma que o card abre o link principal aprovado.

- **REQ-009:** Quando um link de afiliado na vitrine precisar ser substituído por esgotamento de estoque ou troca de loja, o sistema deve atualizar o destino no catálogo da vitrine mantendo o código curto do vídeo e o endereço público da página na bio.
  - **Critério de aceite:** O usuário busca o mesmo código curto na página da vitrine e verifica que ele passou a abrir o novo link principal sem alterar a URL pública da bio.

- **REQ-010:** Quando o pacote de publicação incluir palavra-chave para comentário no Instagram Reels, o sistema deve registrar em `pacote.md` a palavra-chave e a mensagem de resposta com o link ou instrução da vitrine para configuração na automação gratuita do Meta Business Suite, mantendo o direcionamento para a bio como *fallback*.
  - **Critério de aceite:** O usuário encontra em `pacote.md` a palavra-chave, o texto pronto para configurar a resposta automática no Meta Business Suite e a referência ao link na bio caso a automação não esteja disponível na conta.

## Privacidade e segurança

- **REQ-011:** O sistema deve manter credenciais em arquivos `.env*` não lidos e não versionados e operar em formato *dark*, sem expor chaves de API nem dados pessoais do usuário em fichas, roteiros, pacotes de publicação, vitrine ou logs.
  - **Critério de aceite:** O usuário verifica que `.env*` consta como ignorado no `.gitignore` e que nenhum arquivo de produto (`ficha.md`, roteiro, `pacote.md`) ou página da vitrine contém credenciais ou identidade pessoal do usuário.

- **REQ-012:** Onde houver geração de imagens por IA para provas de conceito, rascunhos ou exploração visual, o sistema deve solicitar a menor resolução útil (`512px` / `0.5K`), reservando `1K` ou superior apenas para arte final aprovada.
  - **Critério de aceite:** O usuário verifica nas propriedades/dimensões das imagens de rascunho ou conceito geradas que a resolução não ultrapassa a faixa `0.5K` (`512px` no lado base).

## Melhoria contínua do processo

- **REQ-013:** Quando um ciclo completo dos 4 portões de um produto for concluído, o sistema deve propor ao usuário uma auditoria do processo com o comando `/learn` para otimizar o fluxo com base nos atritos e aprendizados observados.
  - **Critério de aceite:** Ao encerrar o Portão 4 de um produto, o usuário recebe o registro dos pontos de atrito do ciclo e a recomendação explícita para executar `/learn`.
