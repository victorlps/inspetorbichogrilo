# O que pode ser automatizado na coleta de produtos, publicação de vídeos e conversão por DM sem violar termos ou sofrer bloqueios?

Fontes lidas em 2026-11-17. Reverificar limites de API e políticas até 2027-02-17.

## Fatos observados por frente de automação

### 1. Coleta de produtos e fontes técnicas
- **Observação do projeto anterior (`~/Dev/vendas_online`):** consultas HTTP diretas a marketplaces como Mercado Livre e Shopee sofreram bloqueio (`403` / desafio anti-bot), sendo contornadas via controle de navegador (`browser`) sobre sessão previamente autenticada pelo usuário para capturar links reais (`/p/MLB...`), fotos e reputação do vendedor (`~/Dev/vendas_online/GEMINI.md`).
- **Termos de uso para coleta em navegador e APIs oficiais de afiliados:** a permissão contratual para automação via navegador nos termos de cada marketplace e a disponibilidade de APIs abertas de catálogo para afiliados não foram verificadas — **não verificado**.

### 2. Publicação programática de vídeos nas redes sociais
- **YouTube Data API v3 (`videos.insert`):** cota padrão de **10.000 unidades/dia** para endpoints gerais, com `videos.insert` e `search.list` separados em limites próprios após reestruturação de cotas, e aumentos acima do padrão sujeitos a auditoria formal de conformidade pela Google. Fontes: [Auditoria e Cotas da YouTube Data API](https://developers.google.com/youtube/data/guides/quota_and_compliance_audits) e [Histórico de Revisões — YouTube Data API](https://developers.google.com/youtube/data/revision_history). O limite exato de uploads/dia por projeto — **não verificado** no painel específico do projeto nesta rodada.
- **Instagram Graph API (Meta):** limite de publicação em janela móvel de 24 horas (até **100 publicações a cada 24 horas** via `POST /<IG_ID>/media_publish`, consultável em `GET /<IG_ID>/content_publishing_limit`), com carrosséis contando como 1 post. Fonte: [Content Publishing — Instagram Platform](https://developers.facebook.com/documentation/instagram-platform/content-publishing). Exigência de conta Profissional vinculada a Página do Facebook, teto de **200 chamadas/hora** por token e **50 contêineres** — **não verificado** diretamente na página específica de *rate limits* nesta rodada.
- **TikTok Content Posting API:** limite de **6 requisições de inicialização por minuto** por `access_token` (janela deslizante, erro `429 rate_limit_exceeded`), e aplicativos não auditados ficam restritos ao modo privado (`SELF_ONLY`) para até 5 usuários/dia até aprovação na auditoria do portal. Fontes: [Direct Post — TikTok Content Posting API](https://developers.tiktok.com/doc/content-posting-api-reference-direct-post) e [Content Sharing Guidelines — TikTok](https://developers.tiktok.com/doc/content-sharing-guidelines). Teto diário exato de **15 a 25 vídeos/dia** por conta — **não verificado** diretamente na documentação oficial nesta rodada.

### 3. Automação de comentários e mensagens diretas (Instagram DM)
- **Regras da plataforma via parceiro oficial (ManyChat):**
  - Exige conta Profissional vinculada a Página do Facebook e interação prévia do usuário (comentário, DM com palavra-chave ou resposta/menção em Story), abrindo uma **janela de 24 horas** para envio de mensagens automatizadas. Fonte: [Regras de automação de DM no Instagram (ManyChat)](https://manychat.com/blog/instagram-dm-automation-rules/).
  - Relatos de suporte indicam teto aproximado de **750 chamadas/hora** para respostas privadas e necessidade de variar o texto das respostas públicas nos comentários para evitar bloqueio por spam — **não verificado** na documentação oficial da Meta; relato em [Comunidade ManyChat](https://community.manychat.com/general-q-a-43/instagram-business-account-disabled-due-to-automation-10161).
- **Alternativa nativa gratuita (Meta Business Suite):** automação básica de palavras-chave para comentários e DMs diretamente pelo Meta Business Suite — **não verificado** em documentação oficial da Meta nesta rodada.

## Inferências

- **Inferência:** Diante dos bloqueios anti-bot observados contra *scraping* HTTP direto no projeto anterior, a viabilidade de coleta automatizada depende de verificar os termos de uso ou APIs oficiais de cada marketplace antes de definir o mecanismo definitivo.
- **Inferência:** No Instagram, a automação de DM por palavra-chave depende de conta Profissional vinculada a Página do Facebook e respeita a janela de 24 horas após interação do usuário; no YouTube e TikTok, os limites exatos e fluxos de auditoria de API precisam de validação direta nos portais oficiais antes de implementar publicação automática.
