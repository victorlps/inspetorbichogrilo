---
status: "accepted"
date: 2026-11-17
decision-makers: victor
---

# Canais, programas de afiliados e conversão na Fase 1

## Contexto e problema

Na Fase 1 descrita em [visao.md](../visao.md), o projeto **Inspetor Bicho Grilo** opera como afiliado sem estoque próprio, com custo inicial mínimo e sem presença humana em câmera (*dark*). A pesquisa em [mercado-social-commerce-e-afiliados.md](../pesquisa/mercado-social-commerce-e-afiliados.md) mostrou que:

- **Mercado Livre, Amazon, Shopee e Parceiro Magalu** permitem entrada inicial sem barreira de audiência equivalente à do YPP (com registro explícito de adesão por CPF em Shopee e Parceiro Magalu; a Amazon exige ao menos 3 vendas qualificadas nos primeiros 180 dias para análise definitiva da conta).
- **YouTube Shopping** exige integração prévia ao YPP (e residência no Brasil); **TikTok Shop Afiliado** tem corte citado como **não verificado** entre 1.000 e 2.000 seguidores para criadores independentes.
- Na **Shopee**, atuar como Pessoa Jurídica na *Comissão Extra* exige emissão de uma NFS-e separada para cada vendedor tomador do serviço.
- Nos canais nativos de marketplace, o **Mercado Livre Clips** exige vídeo vertical (`9:16`) dedicado a um único produto mostrando uso real ([regras-originalidade-e-monetizacao-dark.md](../pesquisa/regras-originalidade-e-monetizacao-dark.md)). As regras de formato do **Shopee Vídeo** e a observação do projeto anterior sobre não citar preço variável no ML Clips permanecem marcadas como **não verificado**.
- Na conversão por mensagem direta ([automacao-coleta-publicacao-e-dm.md](../pesquisa/automacao-coleta-publicacao-e-dm.md)), a automação via ManyChat exige conta Profissional vinculada a Página do Facebook e respeita janela de 24 horas após interação do usuário, enquanto a alternativa gratuita nativa no Meta Business Suite está marcada como **não verificado** em documentação oficial nesta rodada.

É necessário definir em qual regime fiscal iniciar, quais programas e canais de publicação usar na Fase 1 e como converter visualizações em cliques sem diluir o tráfego inicial.

## Opções consideradas

1. **Cadastro amplo em Pessoa Física (CPF) com 1 link principal por vídeo e conversão por bio + teste de DM nativa:** operar em CPF (sem abrir PJ na Fase 1) nos 4 programas abertos (Mercado Livre, Amazon, Shopee e Parceiro Magalu), escolhendo **1 programa principal por vídeo** conforme melhor preço, comissão e disponibilidade; publicar o vídeo `9:16` no YouTube Shorts, Instagram Reels e TikTok; reaproveitar condicionalmente no ML Clips (apenas quando houver demonstração de uso real do produto e verificando as diretrizes vigentes de preço) e no Shopee Vídeo (após verificar suas regras); converter via página única de links na bio (ferramenta a definir na implementação) e testar a automação gratuita de comentário-para-DM no Meta Business Suite no Instagram, mantendo o link na bio como *fallback*.
2. **Apenas Mercado Livre e Amazon em CPF:** restringir o cadastro inicial a dois programas e postergar Shopee e Magalu para uma segunda etapa.
3. **Vitrine multi-loja em todos os vídeos:** exibir links de todas as lojas simultaneamente em cada vídeo, deixando o comprador escolher o marketplace.

## Decisão

Opção escolhida: **Opção 1 (Cadastro amplo em Pessoa Física com 1 link principal por vídeo e conversão por bio + teste de DM nativa)**, porque o usuário informou que o maior custo da operação está na curadoria e na produção de conteúdo, não no cadastro dos programas. Operar em CPF evita abertura de CNPJ e emissão de múltiplas NFS-e na Fase 1; concentrar 1 link principal por vídeo evita diluir cliques na meta de 3 vendas em 180 dias da Amazon; e publicar em Shorts, Reels e TikTok constrói audiência para liberar YouTube Shopping e TikTok Shop sem custo mensal de ferramentas de DM.

### Consequências

- **Bom:** aproveita o melhor marketplace disponível para cada produto curado sem custo fixo mensal e mantém os vídeos `9:16` prontos para distribuição nas três redes sociais.
- **Bom:** evita burocracia fiscal de PJ na Fase 1 e concentra a conversão de cada vídeo em um único destino principal.
- **Ruim:** obriga a verificar na prática as retenções/recibos de PF na *Comissão Extra* da Shopee e no Parceiro Magalu (marcados como **não verificado** na pesquisa), bem como a disponibilidade real da automação gratuita de DM no Meta Business Suite.
- **Ruim:** a migração para PJ/CNPJ precisará ser decidida em nova ADR antes da Fase 2 (operação própria/seller) ou se o volume de rendimentos em CPF justificar planejamento tributário.
