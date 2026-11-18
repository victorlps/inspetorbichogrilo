# Como buscar e filtrar produtos nos marketplaces de forma eficiente (APIs oficiais, filtros e MCPs) sem ruído excessivo?

Fontes lidas em 2026-11-18. Reverificar endpoints, requisitos de acesso e disponibilidade de MCPs até 2027-02-18.

## Fatos observados por frente

### 1. APIs oficiais de busca e catálogo para afiliados
- **Mercado Livre (`/sites/MLB/search`):** a API do Mercado Livre expõe `GET https://api.mercadolibre.com/sites/MLB/search` com parâmetros de filtro por termo (`q`), categoria (`category`), `limit` e `offset`. Em teste direto realizado em `2026-11-18` sem token OAuth (`curl "https://api.mercadolibre.com/sites/MLB/search?q=Zagonel+ND+7700W&limit=3"`), o endpoint retornou **`HTTP 403` (`{"message":"forbidden","error":"forbidden","status":403}`)**, confirmando que consultas anônimas sem autenticação OAuth 2.0 estão bloqueadas.
- **Shopee Brasil (Affiliate Open API):** o programa de afiliados da Shopee disponibiliza endpoint GraphQL oficial (`POST https://open-api.affiliate.shopee.com.br/graphql`) com a query `productOfferV2` (`keyword`, `listType`, `sortType`, `page`, `limit`), retornando `itemId`, `productName`, `offerLink`, `priceMin`/`priceMax`, `sales`, `ratingStar`, `commissionRate` e `shopType`, mediante `AppId` e `Secret` (assinatura SHA256) solicitados após conta ativa de afiliado. Fonte: [Shopee Affiliate Open API](https://affiliateshopee.com.br/).
- **Amazon Brasil (Product Advertising API / PA-API):** o acesso às chaves da PA-API é gerenciado no Portal de Associados, mas as cotas de requisições (TPS e chamadas diárias) são vinculadas ao volume de vendas qualificadas nos últimos 30 dias e a conta está sujeita à meta inicial de 3 vendas qualificadas em 180 dias. Fonte: [Associados Amazon Brasil — Central de Ajuda](https://associados.amazon.com.br/help/node/topic/G8TW5AE9XL2VX9VM).
- **Parceiro Magalu:** disponibilidade de API aberta de busca de catálogo para divulgadores em CPF — **não verificado** nesta rodada.

### 2. Servidores MCP (*Model Context Protocol*) para marketplaces (auditoria de código em `2026-11-18`)
- **`givaldos/cloobe-mcp`:** repositório sem licença definida (`license: None`), consulta o agregador de terceiros `cloo.be` em vez das APIs oficiais dos marketplaces.
- **`newerton/mcp-mercado-livre`:** licença MIT, usa `fetch` sobre páginas HTML de `https://lista.mercadolivre.com.br` (*scraping* HTML, não API oficial do Mercado Livre).
- **`andrehocsis/rally-mcp-server`:** sem licença definida (`license: None`), chama `https://api.mercadolibre.com/sites/MLB/search` sem autenticação OAuth (bloqueado com `HTTP 403` no teste ao vivo) e não implementa consulta real à API GraphQL da Shopee (retorna instrução textual em vez de executar `productOfferV2`).
- **MCP oficial dos marketplaces (Mercado Livre, Amazon Associados, Shopee, Magalu):** não foi localizado servidor MCP oficial mantido diretamente por esses quatro marketplaces para afiliados nesta rodada — **não verificado**.

### 3. Limitação de busca livre nos sites
- Conforme informado pelo usuário a partir do uso prático e registrado em [automacao-coleta-publicacao-e-dm.md](automacao-coleta-publicacao-e-dm.md), buscas textuais genéricas nos sites retornam muitos anúncios repetidos e itens fora da especificação, enquanto *scraping* HTTP direto sofre bloqueio (`403`/anti-bot).

## Inferências

- **Inferência:** Na Fase 1 inicial (antes de atingir volume de vendas para liberar cotas da PA-API da Amazon e aprovação de credenciais da Shopee Affiliate Open API), a busca combinada de **filtros específicos (modelo exato, tensão/potência, catálogo/SKU)** + **navegação assistida em sessão autenticada** é o caminho imediato para evitar ruído e bloqueios anti-bot, enquanto **Shopee Affiliate Open API** e **ML `/sites/MLB/search`** são candidatos naturais a automação/MCP próprio após validar as credenciais oficiais.
- **Inferência:** Adotar um servidor MCP público de terceiros sem auditoria de código cria risco de dependência externa, alteração de links de afiliado ou quebra de termos de uso; caso se adote MCP no futuro, o caminho seguro é encapsular apenas APIs oficiais com credenciais do próprio usuário.
