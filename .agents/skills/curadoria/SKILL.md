---
name: curadoria
description: >-
  Como pesquisar a ciência/engenharia do tema ("como funciona" e comparação entre técnicas),
  filtrar um produto exemplar nos marketplaces e auditar reviews (1★ a 3★) para entregar ficha.md
  (Portão 1) e atuar como guardião da fidelidade física, científica e factual nos Portões 2 e 3.
---

# Curadoria Científica e Comercial (Portão 1 e Guardião de Fidelidade)

Fluxo derivado de [0001-canais-e-afiliados-fase-1.md](../../../docs/decisoes/0001-canais-e-afiliados-fase-1.md), [0006-governanca-qualidade-finops-e-composicao-visual.md](../../../docs/decisoes/0006-governanca-qualidade-finops-e-composicao-visual.md), [0008-sala-de-producao-coautoria-e-tres-portoes.md](../../../docs/decisoes/0008-sala-de-producao-coautoria-e-tres-portoes.md), [fase-1.md](../../../docs/requisitos/fase-1.md) (`REQ-001`, `REQ-002`, `REQ-014`) e [.agents/formato/biblia.md](../../formato/biblia.md).

## 1. Dossiê Duplo: Ciência do Fenômeno ("Como Funciona") + Exemplar Auditado

- Processe **um tema/produto por vez** durante a fase de calibração (`REQ-001`), em `produtos/<slug>/` (*kebab-case* curto).
- Construa `ficha.md` unindo duas frentes complementares verificadas em fontes primárias e técnicas atuais (citando **URL profunda** e **data de leitura**):
  1. **Investigação científica e comparativa do assunto principal:** documente o que é o fenômeno/tecnologia, como ocorre passo a passo sua fabricação ou funcionamento interno (grandezas físicas, mudanças de fase, mecanismos celulares ou mecânicos), o que diferencia fisicamente essa técnica das alternativas convencionais ou imitações de mercado e por que ela entrega vantagem real na atividade humana estudada.
  2. **Auditoria técnica e comercial do produto exemplar:** verifique cronologia da marca, especificações oficiais por variação essencial (dimensões, massa, composição, potência, normas e instruções de conservação), morfologia externa/embalagem e preços vigentes.
- Salve em `produtos/<slug>/assets/` a **foto da peça aberta, vista explodida, macro estrutural ou diagrama técnico do processo**, nomeada com termo reconhecido pelo validador (`camara`, `intern`, `explod`, `encaixe`, `manual` ou `diagrama`), além de fotos oficiais íntegras do exemplar em fundo limpo ou uso real autêntico (inspecionadas via `read_file` com extensão real `PNG`, `JPG` ou `WEBP`).

## 2. Busca nos marketplaces e critérios de parada

- Execute busca cirúrgica por **modelo/produto exato + especificação crítica** via subagente `browser` ou ferramentas locais (conferindo a presença de `.env*` exclusivamente com `test -f`), e valide imediatamente a elegibilidade de comissão dos anúncios candidatos executando `PYTHONPATH=. .venv/bin/python src/publish/affiliate_links.py --verify-urls <url1> <url2> ...` no perfil persistente autenticado. Priorize na `§ 4.` anúncios ativos que retornem link curto comissionado válido (`https://meli.la/...`, `https://amzn.to/...` ou equivalente parametrizado) já no Portão 1.
- Deduplique por SKU/vendedor e mapeie as variações essenciais disponíveis para compor o catálogo completo de `pacote.md` e da vitrine.
- Aplique **parada por suficiência qualitativa**: ao confirmar **1 anúncio líder sólido por variação essencial** nos quatro marketplaces da Fase 1 (**Mercado Livre, Amazon, Shopee e Parceiro Magalu**), confronte-os na `§ 4.` para eleger o programa principal (ou registre ausência qualificada com termo e data).

## 3. Auditoria quantitativa de *reviews* (`1★` a `3★`)

- Registre a distribuição exata das `5` estrelas (`XX% (5★)` ou `5★ (XX%)`) somando `99,5%`–`100,5%`.
- Leia comentários `1★` a `3★` até saturar os padrões recorrentes, registrando o **tamanho exato da amostra (`N`)** e a **contagem numérica de ocorrências**, distinguindo causas físicas/naturais do processo, cuidados reais de uso e relatos genéricos.

## 4. Entrega do Portão 1 (`produtos/<slug>/ficha.md`)

Estruture `ficha.md` nas **6 seções obrigatórias (`## 1.` a `## 6.`)**:
1. `## 1. Problema real resolvido` (contexto físico da atividade e dilema das soluções comuns)
2. `## 2. História real de engenharia & marca` (origem tecnológica e trajetória verificada do fabricante)
3. `## 3. Especificações técnicas, auditoria de reviews (1★–3★) e consenso` (incluindo subseção **"Por Dentro" + Morfologia do Processo/Mecanismo** e confronto físico com técnicas alternativas)
4. `## 4. Confronto entre marketplaces e links principais`
5. `## 5. Ângulo editorial proposto` (estruturado na linha *"Como as coisas funcionam?"* de `biblia.md`, indicando as perguntas científicas/visuais centrais e o ponto natural de entrada do exemplar)
6. `## 6. Referências audiovisuais do produto`

Higienize `produtos/<slug>/assets/` mantendo exclusivamente ativos referenciados na `§ 6.` e execute **`python3 src/video/validate_gates.py produtos/<slug> --portao 1`** (salvando saídas extensas em arquivo temporário). Entregue os caminhos e o resumo da validação para `@Mike` apresentar no Portão 1.

## 5. Guardião da fidelidade científica e física (Portões 2 e 3)

- Permaneça ativo na **sala de produção (Swarm enxuto)** com `@Carlos` e `@Steve` até o Portão 3:
  - **No Portão 2:** revise as simulações visuais propostas por `@Steve`, a explicação narrativa de `@Carlos` e os quadros de transformação/animatic, registrando na seção `## 4. Notas de Fidelidade Física e Factual (@Curador)` de `roteiro.md` seu parecer (`APROVADO` ou ajustes objetivos) quanto às leis físicas/termodinâmicas, diferenciação correta entre técnicas, proporções e fidelidade morfológica ao exemplar real.
  - **No Portão 3:** audite os quadros finais de `video_final_1080p.mp4` e os dados/variações de `pacote.md`, assegurando precisão científica na animação e fidelidade integral ao produto real.
- Diante de apontamento em sala, refine na mesma instância e anote aprendizados de método para a retro consolidada de encerramento.
