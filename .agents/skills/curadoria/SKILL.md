---
name: curadoria
description: Como pesquisar, filtrar anúncios nos marketplaces e auditar reviews e fontes técnicas para gerar a ficha de curadoria (Portão 1) de um produto. Use ao iniciar ou revisar a curadoria de qualquer produto candidato em produtos/.
---

# Curadoria (Portão 1)

Fluxo de pesquisa e triagem derivado de [0001-canais-e-afiliados-fase-1.md](../../../docs/decisoes/0001-canais-e-afiliados-fase-1.md), [busca-eficiente-e-mcps-marketplaces.md](../../../docs/pesquisa/busca-eficiente-e-mcps-marketplaces.md) e [fase-1.md](../../../docs/requisitos/fase-1.md) (`REQ-001`, `REQ-002`).

## 1. Preparação e verificação de fontes

- Processe **um produto por vez** durante a fase de calibração (`REQ-001`).
- Trate registros históricos (como `~/Dev/vendas_online`) apenas como pista inicial; verifique cronologia de marcas, especificações, preços, anúncios e consenso de fóruns diretamente nas fontes atuais.
- Pesquise a história real de engenharia/marca e o consenso técnico de especialistas (fóruns, fabricantes, imprensa setorial) antes de redigir o ângulo editorial.

## 2. Busca nos marketplaces e critérios de parada

- Utilize busca cirúrgica por **modelo exato + especificação crítica** (tensão, potência ou SKU) via subagente `browser` na sessão autenticada do usuário, priorizando APIs oficiais autenticadas quando configuradas.
- Deduplique resultados por catálogo/SKU e por vendedor distinto.
- Aplique **parada por suficiência qualitativa** (sem número fixo de anúncios): encerre a varredura na loja ao identificar **1 anúncio líder sólido** (Loja Oficial ou alta reputação, entrega rápida/Full/Prime, volume relevante de avaliações e preço coerente) acompanhado das referências comparáveis disponíveis, ou pare ao atingir o **teto de ruído** e refine o termo de busca.
- Confronte o melhor representante qualificado de cada marketplace aberto da Fase 1 (Mercado Livre, Amazon, Shopee e Parceiro Magalu) para eleger **1 link principal de afiliado** para o vídeo.

## 3. Auditoria quantitativa de *reviews* (1★ a 3★)

- Extraia a **distribuição exata de estrelas** do anúncio líder (percentual ou contagem de 5★, 4★, 3★, 2★ e 1★).
- Leia os comentários escritos de 1★ a 3★ e conte a **recorrência real** de cada padrão, distinguindo erros de instalação ou expectativa de defeitos crônicos ou mudanças reais de projeto.

## 4. Entrega do Portão 1 (`produtos/<slug>/ficha.md`)

- Crie `produtos/<slug>/ficha.md` contendo: problema real resolvido, especificações e história com fontes verificadas, loja e link principal de afiliado, ângulo editorial e imagens/vídeos de referência incorporados para visualização direta no *preview* de Markdown (`REQ-001`).
- Aguarde a aprovação explícita do usuário no chat antes de criar `roteiro.md`, áudio ou qualquer renderização (`REQ-002`).
