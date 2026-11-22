---
name: curadoria
description: Como pesquisar, filtrar anúncios nos marketplaces, auditar reviews e fontes técnicas para entregar ficha.md (Portão 1) e atuar como guardião da fidelidade física e factual nos Portões 2 e 3.
---

# Curadoria (Portão 1 e Guardião de Fidelidade)

Fluxo derivado de [0001-canais-e-afiliados-fase-1.md](../../../docs/decisoes/0001-canais-e-afiliados-fase-1.md), [0006-governanca-qualidade-finops-e-composicao-visual.md](../../../docs/decisoes/0006-governanca-qualidade-finops-e-composicao-visual.md), [0008-sala-de-producao-coautoria-e-tres-portoes.md](../../../docs/decisoes/0008-sala-de-producao-coautoria-e-tres-portoes.md) e [fase-1.md](../../../docs/requisitos/fase-1.md) (`REQ-001`, `REQ-002`, `REQ-014`).

## 1. Preparação e verificação de fontes

- Processe **um produto por vez** durante a fase de calibração (`REQ-001`), em `produtos/<slug>/` (*kebab-case* curto).
- Verifique cronologia de marcas, especificações oficiais do fabricante por variação essencial (dimensões, capacidade/potência, faixa operacional, compatibilidade de peças/insumos e normas), preços e consenso técnico diretamente em fontes atuais, citando em `ficha.md` a **URL específica (link profundo)** e a **data de leitura**.
- **Dissecação "Por Dentro" e Morfologia:** para produtos físicos/técnicos ou alimentos/processos industriais, documente:
  1. **Cadeia funcional interna ou processo de fabricação:** sequência passo a passo que gera o benefício real, distinguindo dados nominais do fabricante de princípios físicos/industriais verificados na literatura técnica.
  2. **Morfologia e topologia:** silhueta, proporções, posição de comandos/conexões e isolamento físico entre compartimentos (ou etapas de transformação, quando for processo).
- Quando o ângulo abordar funcionamento interno ou processo, salve em `produtos/<slug>/assets/` a **foto da peça aberta, vista explodida, diagrama oficial ou referência visual do processo**, nomeada com termo reconhecido pelo validador (`camara`, `intern`, `explod`, `encaixe`, `manual` ou `diagrama`).
- **Limpeza comercial de `assets/`:** utilize imagens oficiais do fabricante (isoladas e de uso real), recortes de manual ou fotos limpas em fundo neutro, sem marcas d'água, logotipos terceiros ou apresentadores alheios. Inspecione cada imagem via `read_file` e mantenha a extensão real (`PNG`, `JPG`, `WEBP`).

## 2. Busca nos marketplaces e critérios de parada

- Use busca cirúrgica por **modelo/produto exato + especificação crítica** via subagente `browser` na sessão autenticada (ou API oficial configurada, checando credenciais apenas com `test -f` sem ler `.env*`). Em caso de bloqueio de login/*captcha*, faça busca pública complementar via `search_web` e marque comissão/link curto dependente de login como **não verificado**.
- Deduplique por SKU/vendedor e verifique **todas as variações essenciais** (ex.: `127V`/`220V`, pesos/sabores), garantindo links diretos separados e comissão ativa (`GANHOS %`).
- Aplique **parada por suficiência qualitativa**: ao identificar **1 anúncio líder sólido por variação essencial** nos quatro marketplaces da Fase 1 (**Mercado Livre, Amazon, Shopee e Parceiro Magalu**), confronte-os na `§ 4.` para eleger o programa principal e gere os links curtos já no Portão 1 (ou registre ausência qualificada com termo e data).

## 3. Auditoria quantitativa de *reviews* (`1★` a `3★`)

- Registre a distribuição exata das `5` estrelas (`XX% (5★)` ou `5★ (XX%)`) somando `99,5%`–`100,5%`.
- Leia comentários `1★` a `3★` até saturar os padrões recorrentes, registrando o **tamanho exato da amostra (`N`)** e a **contagem numérica de ocorrências**, separando relatos sem causa declarada das características de projeto e cuidados do manual.

## 4. Entrega do Portão 1 (`produtos/<slug>/ficha.md`)

Estruture `ficha.md` nas **6 seções obrigatórias (`## 1.` a `## 6.`)**:
1. `## 1. Problema real resolvido`
2. `## 2. História real de engenharia & marca` (ou origem e processo produtivo)
3. `## 3. Especificações técnicas, auditoria de reviews (1★–3★) e consenso` (incluindo subseção **"Por Dentro" + Morfologia**)
4. `## 4. Confronto entre marketplaces e links principais`
5. `## 5. Ângulo editorial proposto`
6. `## 6. Referências audiovisuais do produto`

Higienize `produtos/<slug>/assets/` mantendo apenas ativos referenciados na `§ 6.` e execute **`python3 src/video/validate_gates.py produtos/<slug> --portao 1`** (salvando saídas extensas em `/tmp/`). Devolva os caminhos e o resumo da validação para `@Mike` apresentar no Portão 1.

## 5. Guardião da fidelidade na sala de produção (Portões 2 e 3)

- Após aprovação do Portão 1, permaneça na **sala de produção (Swarm enxuto)** com `@Carlos` e `@Steve` até o Portão 3:
  - **No Portão 2:** revise a decupagem visual de `@Steve`, a fala de `@Carlos` e os *styleframes*/animatic, registrando na seção de **Notas de fidelidade** de `roteiro.md` e no mural o seu parecer (`APROVADO` ou ajustes objetivos) sobre leis físicas, isolamento de câmaras/etapas, especificações, variações essenciais e aderência às fotos reais.
  - **No Portão 3:** confira os quadros finais de `video_final_1080p.mp4` e `pacote.md` antes da entrega ao usuário, garantindo fidelidade integral ao produto real.
- Diante de crítica ou ajuste, corrija na mesma instância e anote eventuais aprendizados de método para a retro consolidada de encerramento.
