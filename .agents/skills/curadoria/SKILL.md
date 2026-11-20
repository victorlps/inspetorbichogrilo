---
name: curadoria
description: Como pesquisar, filtrar anúncios nos marketplaces e auditar reviews e fontes técnicas para gerar a ficha de curadoria (Portão 1) de um produto. Use ao iniciar ou revisar a curadoria de qualquer produto candidato em produtos/.
---

# Curadoria (Portão 1)

Fluxo de pesquisa e triagem derivado de [0001-canais-e-afiliados-fase-1.md](../../../docs/decisoes/0001-canais-e-afiliados-fase-1.md), [0006-governanca-qualidade-finops-e-composicao-visual.md](../../../docs/decisoes/0006-governanca-qualidade-finops-e-composicao-visual.md), [busca-eficiente-e-mcps-marketplaces.md](../../../docs/pesquisa/busca-eficiente-e-mcps-marketplaces.md) e [fase-1.md](../../../docs/requisitos/fase-1.md) (`REQ-001`, `REQ-002`, `REQ-003`, `REQ-014`).

## 1. Preparação e verificação de fontes

- Processe **um produto por vez** durante a fase de calibração (`REQ-001`), mantendo o nome de pasta `produtos/<slug>/` em *kebab-case* curto baseado em modelo e marca.
- Trate registros históricos externos (como `~/Dev/vendas_online`, quando presentes na máquina) apenas como pista inicial; verifique cronologia de marcas, especificações, preços, anúncios e consenso de fóruns diretamente nas fontes atuais.
- Pesquise a história real de engenharia/marca e o consenso técnico de especialistas (fóruns, fabricantes, imprensa setorial) antes de redigir o ângulo editorial.
- Sempre que o ângulo editorial abordar funcionamento interno, colete e salve em `produtos/<slug>/assets/` (via `browser` ou `run_command` com `curl`/Python/`Pillow`) a **foto da peça aberta, vista explodida ou diagrama do manual oficial do fabricante** (`REQ-001`), nomeando o arquivo com termo descritivo reconhecido pelo validador (`camara`, `intern`, `explod`, `encaixe`, `manual` ou `diagrama`, ex.: `ref_camara_interna.png`).

## 2. Busca nos marketplaces e critérios de parada

- Utilize busca cirúrgica por **modelo exato + especificação crítica** (tensão, potência ou SKU) acionando o subagente `browser` via `invoke_subagent` na sessão autenticada do usuário; priorize APIs oficiais autenticadas somente quando já houver script ou CLI configurado no repositório (conferindo a existência de arquivos de credenciais exclusivamente via `test -f` sem ler `.env*`). Caso `browser` ou APIs autenticadas estejam indisponíveis ou deslogados, execute a busca pública via `search_web` e marque dados dependentes de sessão logada (como comissão ativa `GANHOS %`) como **não verificado**.
- Deduplique resultados por catálogo/SKU e por vendedor distinto.
- Verifique **todas as variações essenciais de compra** (ex.: `127V` e `220V`, capacidades ou tamanhos principais), checando se a página principal atende ambas no mesmo URL ou se o seletor alterna ID/URL e exigindo **links diretos separados** com confirmação de **comissão ativa na barra de afiliados (`GANHOS %`)** para cada variação entregue ao comprador.
- Aplique **parada por suficiência qualitativa** (encerrando a varredura por critérios de qualidade, livre de cota numérica fixa de anúncios): conclua a busca na loja ao identificar **1 anúncio líder sólido por variação essencial** (loja oficial ou reputação consolidada, entrega ágil Full/Prime, volume relevante de avaliações frente aos concorrentes diretos e preço coerente com o histórico do modelo) acompanhado das referências comparáveis disponíveis, ou refine o termo de busca quando os resultados deixarem de corresponder ao modelo/SKU exato.
- Confronte o melhor representante qualificado de cada marketplace aberto da Fase 1 (Mercado Livre, Amazon, Shopee e Parceiro Magalu) para eleger o **programa principal** (priorizando cobertura completa das variações essenciais, comissão ativa confirmada, entrega rápida e reputação do vendedor, com `1` link por variação essencial quando houver mais de uma voltagem/versão).

## 3. Auditoria quantitativa de *reviews* (`1★` a `3★`)

- Extraia a **distribuição exata de estrelas** do anúncio líder de cada variação essencial (ou do anúncio único compartilhado) registrando os `5` níveis no formato compatível com o validador (`XX% (5★)` ou `5★ (XX%)`, de `5★` a `1★`). O validador determinístico aceita soma dentro da margem **`99,5%`–`100,5%`** (`±0,5%`); caso a loja exiba inteiros cujo arredondamento fique fora dessa margem, registre os percentuais exatos da loja com uma nota explícita e sinalize ao Coordenador.
- Leia comentários escritos de `1★` a `3★` em amostra qualitativa suficiente até saturar os padrões recorrentes e conte a **recorrência real** de cada padrão, distinguindo objetivamente relatos sem causa declarada nos comentários das características reais de projeto e das orientações preventivas documentadas no manual oficial.

## 4. Validação determinística e entrega do Portão 1 (`produtos/<slug>/ficha.md`)

- Crie `produtos/<slug>/ficha.md` estruturada nas **6 seções numeradas obrigatórias (`## 1.` a `## 6.`)** exigidas pelo validador local cobrindo os 5 blocos do Portão 1 (`REQ-001` e `REQ-003`):
  1. `## 1. Problema real resolvido`
  2. `## 2. História real de engenharia & marca`
  3. `## 3. Especificações técnicas, auditoria de reviews (1★–3★) e consenso`
  4. `## 4. Confronto entre marketplaces e links principais`
  5. `## 5. Ângulo editorial proposto`
  6. `## 6. Referências audiovisuais do produto` (imagens salvas em `produtos/<slug>/assets/` incorporadas para visualização direta no *preview* de Markdown e links/recortes de manuais ou vídeos locais de referência)
- Antes de devolver a entrega ao **Coordenador**, execute via `run_command` o validador determinístico **`python3 src/video/validate_gates.py produtos/<slug> --portao 1`** (salvando eventuais saídas extensas em `/tmp/` para manter `produtos/<slug>/` restrita à curadoria), confirmando: (a) presença das `6` seções `## 1.`..`## 6.`, (b) existência e tamanho não nulo em disco de todas as imagens/arquivos citados (incluindo evidência visual interna quando abordar mecanismo interno) e (c) soma de estrelas dentro de `99,5%`–`100,5%`.
- Devolva ao **Coordenador** (ou no mural em Swarm enxuto) apenas os caminhos gerados (`ficha.md` e `assets/`) e o resumo objetivo dessa checagem para submissão ao usuário no Portão 1 (`REQ-002`), encerrando seu escopo sem avançar para roteiro, áudio ou vídeo.

## 5. Checagem factual sob demanda e resposta a feedback de outras etapas

- Ao receber consulta factual do `@Carlos` ou do `@Steve` durante os Portões 2 a 4, confira os dados diretamente nas fontes salvas ou em nova consulta verificável, devolva confirmação objetiva com link e data de leitura (ou declare o item como **não verificado**) e registre novas fontes confirmadas também em `produtos/<slug>/ficha.md`.
- Ao receber feedback de outra etapa ou crítica do usuário, siga os 3 caminhos definidos em `curador.md`:
  - **Causa A (lacuna estrutural nesta skill ou em `curador.md`):** pare sem editar arquivos de configuração nem refazer `ficha.md` e devolva a proposta de diff em linguagem afirmativa (com fontes) ao Coordenador para auditoria pelo `@Revisor-Skills` antes da recriação em contexto limpo;
  - **Causa B (falha de briefing ou insumo externo):** devolva feedback em linguagem afirmativa ao responsável (via Coordenador ou mural em Swarm enxuto), mantendo esta skill intacta;
  - **Causa C (complemento factual ou ajuste pontual já previsto nesta skill):** atualize `produtos/<slug>/ficha.md` / `assets/` com dados verificados, reexecute `python3 src/video/validate_gates.py produtos/<slug> --portao 1` e devolva os caminhos atualizados ao Coordenador (ou no mural em Swarm enxuto).
