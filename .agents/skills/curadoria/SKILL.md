---
name: curadoria
description: Como pesquisar, filtrar anúncios nos marketplaces e auditar reviews e fontes técnicas para gerar a ficha de curadoria (Portão 1) de um produto. Use ao iniciar ou revisar a curadoria de qualquer produto candidato em produtos/.
---

# Curadoria (Portão 1)

Fluxo de pesquisa e triagem derivado de [0001-canais-e-afiliados-fase-1.md](../../../docs/decisoes/0001-canais-e-afiliados-fase-1.md), [0006-governanca-qualidade-finops-e-composicao-visual.md](../../../docs/decisoes/0006-governanca-qualidade-finops-e-composicao-visual.md), [busca-eficiente-e-mcps-marketplaces.md](../../../docs/pesquisa/busca-eficiente-e-mcps-marketplaces.md) e [fase-1.md](../../../docs/requisitos/fase-1.md) (`REQ-001`, `REQ-002`, `REQ-014`).

## 1. Preparação e verificação de fontes

- Processe **um produto por vez** durante a fase de calibração (`REQ-001`).
- Trate registros históricos (como `~/Dev/vendas_online`) apenas como pista inicial; verifique cronologia de marcas, especificações, preços, anúncios e consenso de fóruns diretamente nas fontes atuais.
- Pesquise a história real de engenharia/marca e o consenso técnico de especialistas (fóruns, fabricantes, imprensa setorial) antes de redigir o ângulo editorial.
- Sempre que o ângulo editorial abordar funcionamento interno, colete e salve **foto da peça aberta, vista explodida ou diagrama do manual oficial do fabricante** (`REQ-001`).

## 2. Busca nos marketplaces e critérios de parada

- Utilize busca cirúrgica por **modelo exato + especificação crítica** (tensão, potência ou SKU) via subagente `browser` na sessão autenticada do usuário, priorizando APIs oficiais autenticadas quando configuradas.
- Deduplique resultados por catálogo/SKU e por vendedor distinto.
- Verifique **todas as variações essenciais de compra** (ex.: `127V` e `220V`, capacidades ou tamanhos principais), checando se a página principal atende ambas no mesmo URL ou se o seletor alterna ID/URL e exigindo **links diretos separados** com confirmação de **comissão ativa na barra de afiliados (`GANHOS %`)** para cada variação entregue ao comprador.
- Aplique **parada por suficiência qualitativa** (encerrando a varredura por critérios de qualidade, livre de cota numérica fixa de anúncios): conclua a busca na loja ao identificar **1 anúncio líder sólido por variação essencial** (Loja Oficial ou alta reputação, entrega rápida/Full/Prime, volume relevante de avaliações e preço coerente) acompanhado das referências comparáveis disponíveis, ou refine o termo de busca ao atingir o **teto de ruído**.
- Confronte o melhor representante qualificado de cada marketplace aberto da Fase 1 (Mercado Livre, Amazon, Shopee e Parceiro Magalu) para eleger o **programa principal** (com `1` link por variação essencial, quando houver mais de uma voltagem/versão) para o vídeo.

## 3. Auditoria quantitativa de *reviews* (1★ a 3★)

- Extraia a **distribuição exata de estrelas** do anúncio líder (percentual ou contagem de 5★, 4★, 3★, 2★ e 1★).
- Leia os comentários escritos de 1★ a 3★ e conte a **recorrência real** de cada padrão, distinguindo objetivamente relatos sem causa declarada nos comentários das características reais de projeto e das orientações preventivas documentadas no manual oficial.

## 4. Validação determinística e entrega do Portão 1 (`produtos/<slug>/ficha.md`)

- Crie `produtos/<slug>/ficha.md` contendo: problema real resolvido, especificações e história com fontes verificadas, loja e link(s) principal(is) de afiliado cobrindo as variações essenciais confirmadas, ângulo editorial e referências audiovisuais **exclusivas do produto anunciado**, suas peças/câmara internas e documentos oficiais incorporados para visualização direta no *preview* de Markdown (`REQ-001` e `REQ-003`).
- Antes de apresentar `ficha.md` no chat, execute **validação determinística local (`REQ-014`)** confirmando: (a) presença dos 5 blocos obrigatórios, (b) existência em disco de todas as imagens e referências citadas e (c) distribuição de estrelas totalizando 100%, registrando o resumo objetivo dessa checagem junto à entrega.
- Aguarde a aprovação explícita do usuário no chat mantendo a pasta restrita à curadoria (`REQ-002`) antes de criar roteiro, áudio ou renderização.

## 5. Checagem factual sob demanda e resposta a feedback a montante

- Ao receber consulta factual do `@Carlos` ou do `@Steve` durante os Portões 2 a 4, confira os dados diretamente nas fontes salvas ou em nova consulta verificável, entregando confirmação objetiva com link/data ou declarando o item como **não verificado**.
- Ao receber feedback de outro especialista apontando lacuna em `ficha.md` ou nos ativos coletados, trate a falha na origem: complemente `ficha.md` e os arquivos de referência com linguagem afirmativa e dados verificados, e proponha ajuste nesta skill ao `@Revisor-Skills` apenas quando identificar uma falha estrutural recorrente do método de curadoria.
