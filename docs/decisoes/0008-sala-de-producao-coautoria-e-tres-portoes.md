---
status: "accepted"
date: 2026-11-22
decision-makers: victor
---

# Sala de produção com coautoria por ofício, bíblia de formato e fluxo em 3 portões

## Contexto e problema

A equipe definida em [0007-equipe-agentes-especializados-e-governanca-skills.md](0007-equipe-agentes-especializados-e-governanca-skills.md), o funil de [0003-fluxo-aprovacao-e-publicacao.md](0003-fluxo-aprovacao-e-publicacao.md) e a revisão em camadas de [0006-governanca-qualidade-finops-e-composicao-visual.md](0006-governanca-qualidade-finops-e-composicao-visual.md) passaram por dois ciclos completos de produção ("testes de fogo", informado pelo usuário) com o mesmo produto, a ducha Zagonel ND (`produtos/ducha-eletronica-zagonel-nd-7700w/`). As críticas e as causas registradas estão nas mensagens dos commits abaixo:

| Commit | Crítica registrada | Arquivos que a causa-raiz apontou |
|---|---|---|
| `eaabcca` | Limpeza comercial dos assets, URLs profundas, confronto de 4 marketplaces e amostra de reviews (revisão do teste de fogo sobre o *baseline* `62ebf47`) | `curadoria/SKILL.md`, `curador.md` |
| `c95d08a` | "Roteiro e vídeo pareciam apresentação de PowerPoint" em vez de engenharia do produto por dentro | `curadoria`, `roteirista`, `producao-visual` |
| `514bf2c` | Jargão sem tradução no HUD e na fala (`TRIAC`); água parecendo passar pela placa eletrônica; benefício principal pouco destacado; ausência de foto ou vídeo real do produto funcionando; gancho sem costura | `roteirista`, `producao-visual` |

As críticas de `c95d08a` e `514bf2c` foram feitas sobre o vídeo, mas suas causas estavam no roteiro e na direção de arte, etapas que o usuário aprovou antes, em texto.

A análise do fluxo feita com o usuário nesta sessão encontrou seis causas estruturais:

1. **Autoria invertida:** o roteirista (`@Carlos`) não tem ferramentas de imagem nem de shell ([carlos.md](../../.agents/plugins/equipe-bicho-grilo/agents/carlos.md)), mas escreve em `roteiro.md` a direção de arte (câmera, vista explodida, HUD), conforme a [skill roteirista](../../.agents/skills/roteirista/SKILL.md). O diretor de arte (`@Steve`) valida a exequibilidade e executa ([steve.md](../../.agents/plugins/equipe-bicho-grilo/agents/steve.md)); depois `@Carlos` revisa o vídeo comparando-o ao próprio roteiro.
2. **Revisão em cascata e tardia:** cada especialista recebe a entrega do outro já pronta, sem momento de cocriação antes do investimento de trabalho ([orquestrar-equipe](../../.agents/skills/orquestrar-equipe/SKILL.md), seção 3).
3. **Coordenador como intermediário de toda comunicação:** as trocas entre especialistas passam por Mike, que repassa os caminhos de arquivo e a pergunta específica ([orquestrar-equipe](../../.agents/skills/orquestrar-equipe/SKILL.md), seção 1; [AGENTS.md](../../AGENTS.md)).
4. **Fidelidade factual fora do circuito visual:** o `@Curador` atua no Portão 1 e, depois, só quando consultado ([curador.md](../../.agents/plugins/equipe-bicho-grilo/agents/curador.md)); nenhuma etapa prevê a revisão dele sobre os quadros do vídeo, onde apareceu o erro físico da água.
5. **Ausência do ponto de vista do espectador:** as revisões verificam aderência ao artefato anterior (a régua do `@Carlos` sobre o vídeo é o próprio roteiro), não a compreensão do público leigo.
6. **Aprendizado por crítica isolada:** o próprio autor diagnostica a causa; os três commits classificaram a falha como lacuna da própria skill (Causa A), e a instância é encerrada e recriada a cada crítica. Os mesmos parâmetros (área segura, legendas, `15` palavras por frase, créditos Flow) aparecem repetidos em `0006`, em [fase-1.md](../requisitos/fase-1.md), nas skills `roteirista` e `producao-visual` e em `roteiro.md`, e as definições de agente descrevem o papel principalmente por restrições ("exclusivamente", "nunca", "pare sem").

O usuário informou que, na sessão de produção do segundo ciclo, os agentes trabalharam até esgotar a cota da assinatura.

## Opções consideradas

### Opção 1: Sala de produção por produto, coautoria por ofício, bíblia de formato e 3 portões

1. **Papéis por ofício:**
   - **Mike (Coordenador):** abre cada produto com o briefing, aciona o Espectador frio, conduz os portões com o usuário, conduz a retro ao fechar o produto, aplica as alterações de skill aprovadas, registra commits e atualiza a vitrine (`REQ-008`).
   - **`@Curador`:** dono de `ficha.md` (Portão 1) e guardião da fidelidade física e factual até o fim do produto, revisando a decupagem visual, os *styleframes* e os quadros do vídeo.
   - **`@Carlos`:** dono da camada narrativa (gancho, fala, intenção vocal, benefício principal, dicionário fonético e textos de `pacote.md`).
   - **`@Steve`:** dono da camada visual (decupagem, motor visual por cena, coreografia, HUD, *styleframes*, orçamento Flow) e da produção audiovisual.
   - **Espectador frio:** instância nova a cada revisão, que recebe apenas o animatic ou o vídeo, sem ficha, roteiro, skills ou bíblia, e relata o que entendeu, onde se perdeu e se interromperia a rolagem. Não é especialista permanente.
   - **`@Revisor-Skills`:** audita o diff consolidado de skills, agentes e bíblia gerado na retro de cada produto.
2. **Sala de produção (Swarm enxuto):** Curador, Carlos e Steve conversam diretamente no mural durante a cocriação. Mike abre a sala com o briefing, entra nos portões e encerra a sala ao fim do produto. O artefato de cena continua sendo `roteiro.md`, organizado em camadas com dono: a narrativa e o dicionário fonético de `@Carlos`; a decupagem visual, o mapa por motor e o orçamento Flow de `@Steve`; as notas de fidelidade do `@Curador`.
3. **Bíblia de formato:** documento único com a estrutura do episódio, a linguagem acessível, o HUD, a coreografia `Produto Real ↔ Raio-X ↔ Uso Real` e os quadros de referência aprovados. Fica em `.agents/formato/biblia.md`, com os quadros em `.agents/formato/referencias/`, e parte do vídeo da Zagonel e das críticas dos dois ciclos. Os parâmetros de enquadramento continuam decididos em `0006` e `REQ-015`; a bíblia é o único lugar operacional onde os agentes os leem.
4. **Três portões do usuário:**
   - **Portão 1 — Ficha e ângulo editorial:** `ficha.md` do `@Curador` com o ângulo editorial.
   - **Portão 2 — Storyboard cocriado:** `roteiro.md` em camadas com `1` *styleframe* local por cena e um animatic com voz rascunho (`edge-tts`), acompanhados do parecer do `@Curador` sobre fidelidade e do relato do Espectador frio. A aprovação deste portão libera o gasto de créditos Flow e a produção final.
   - **Portão 3 — Vídeo final e pacote:** `video_final_1080p.mp4` e `pacote.md`, acompanhados do parecer do `@Curador` e do relato do Espectador frio. O *preview* intermediário passa a ser etapa interna da sala. Este portão é obrigatório.
5. **Crítica e aprendizado:**
   - A sala corrige a entrega criticada na mesma instância. Uma lacuna de skill percebida durante o produto é corrigida na entrega e registrada para a retro.
   - As correções internas antes de cada portão seguem a parada adaptativa com teto calibrável de `3` rodadas de `0007`, escalando ao usuário ao atingir a 3ª.
   - Ao fechar o produto, Mike conduz uma retro curta, que cumpre a auditoria de processo de `REQ-013` e classifica cada aprendizado em padrão de formato (bíblia), método de ofício (skill ou agente) ou insumo de outra etapa. O `@Revisor-Skills` audita um único diff consolidado por produto, e Mike registra um commit.
6. **Fonte única:** a bíblia guarda o formato; os ADRs guardam ferramentas, stack e custos; skills e definições de agente descrevem o ofício em linguagem de papéis ("você é dono de X e colabora com Y") e apontam para essas fontes em vez de repetir seus valores.

#### Viabilidade de custo (FinOps)

1. **Inventário de recursos:**
   - Mídia: mesmo consumo-base de `0006` (`8` créditos Flow por clipe `8s` em `360p`, `0` crédito no *upscale* a `1080p` até `10s`, `~800` caracteres de TTS por vídeo).
   - Animatic do Portão 2: *styleframes* montados em CPU local com ativos já existentes e voz rascunho `edge-tts` (serviço online gratuito da Microsoft, já usado no Degrau 0 de `0006`): `0` crédito Flow e `US$ 0`. O áudio rascunho é de uso interno e não entra no pacote publicado.
   - Espectador frio: `2` instâncias por produto (Portões 2 e 3), mais as rodadas de correção.
   - Sala em Swarm: a descrição da ferramenta `swarm` do Antigravity (lida em 2026-11-22) informa que workers em espera não consomem cota até alguém publicar no mural, enquanto `0007` classifica o uso frequente de Swarm como *Quota Heavy*. O consumo de tokens por produto em Swarm frente aos subagentes isolados é **não verificado**.
   - Retro: `1` auditoria do `@Revisor-Skills` por produto, no lugar de `1` a `3` rodadas a cada crítica.
2. **Projeção determinística de escala:**

   | Produtos/mês | Créditos Flow (% da cota Pro de `1.000`) | Caracteres TTS (% do Azure F0 de `500.000`) | Instâncias do Espectador frio | Custo adicional de mídia |
   |---|---|---|---|---|
   | `1` | `8` (`0,8%`) | `~800` (`0,16%`) | `2` | `US$ 0` |
   | `30` | `240` (`24%`) | `~24.000` (`4,8%`) | `60` | `US$ 0` |
   | `100` | `800` (`80%`) | `~80.000` (`16%`) | `200` | `US$ 0` |
   | `300` | `2.400` (`240%`) | `~240.000` (`48%`) | `600` | Degrau 2 de `0006`, ex.: Google AI Ultra a `US$ 100/mês` (`24%` de `10.000` créditos, conforme `0007`) |

   O ponto de saturação de mídia continua em `125` produtos/mês no Google AI Pro. O ponto de saturação da cota de tokens da assinatura com a sala em Swarm é **não verificado**; o esgotamento informado pelo usuário ocorreu no protocolo de `0007`, com recriação de instâncias a cada crítica.
3. **Alternativa mais econômica (quando necessário):** se a sala em Swarm pressionar a cota, a cocriação passa a rodar em subagentes isolados com troca direta de mensagens entre especialistas, mantendo papéis, portões e retro.

### Opção 2: Manter `0003`, `0006` e `0007` e seguir evoluindo as skills por crítica

Manter os 4 portões, o Coordenador como intermediário e o protocolo de diagnóstico, auditoria e recriação a cada crítica, acrescentando regras às skills conforme surgirem novas críticas.

### Opção 3: Ajuste pontual no Portão 2

Incluir *styleframes* no Portão 2, mantendo a autoria de `@Carlos` sobre a direção de arte, o Coordenador como intermediário e o protocolo de crítica atual.

## Decisão

Opção escolhida: **Opção 1 (Sala de produção por produto, coautoria por ofício, bíblia de formato e 3 portões)**, porque coloca cada camada da cena sob o especialista do ofício correspondente, mostra o visual ao usuário no portão em que nasceram as causas das críticas de `c95d08a` e `514bf2c`, inclui fidelidade factual e compreensão do espectador antes da avaliação do usuário e concentra o aprendizado em um diff consolidado por produto. A Opção 2 mantém as causas 1 a 6, e a Opção 3 antecipa a visualização, mas mantém as causas 1, 3, 4, 5 e 6.

Esta decisão substitui:

- em `0003`, a estrutura de 4 portões e a opcionalidade do Portão 3;
- em `0006`, o Portão 2 sem áudio, o Portão 3 de *preview* e a revisão em camadas por portão, mantendo o stack, a escada de investimento, o critério visual por natureza da cena e os parâmetros de enquadramento;
- em `0007`, o Coordenador como intermediário padrão, a restrição do Swarm ao pós-calibração, a revisão cruzada `@Carlos ↔ @Steve` e o protocolo de recriação a cada crítica, mantendo a equipe, o `@Revisor-Skills` e o teto de `3` rodadas.

Os requisitos de [fase-1.md](../requisitos/fase-1.md) que citam os Portões 3 e 4, o *preview*, a revisão cruzada ou o `/learn` (`REQ-003` a `REQ-008`, `REQ-013` e `REQ-014`) e o protocolo descrito em [AGENTS.md](../../AGENTS.md) são revisados para refletir esta decisão.

### Consequências

- **Bom:** o usuário avalia o visual no Portão 2, antes da produção do vídeo final, e recebe as entregas com parecer factual e relato de compreensão leiga.
- **Bom:** o padrão de formato é decidido uma vez e reutilizado em produtos de nichos diferentes, testando a replicabilidade exigida por [visao.md](../visao.md).
- **Ruim:** exige revisar `AGENTS.md` e os requisitos citados, reescrever as definições de agente e as skills `curadoria`, `roteirista`, `producao-visual`, `revisao-skills-e-agentes` e `orquestrar-equipe`, criar a bíblia de formato e ajustar `src/video/validate_gates.py` ao `roteiro.md` em camadas.
- **Ruim:** o consumo de cota da sala em Swarm ainda não foi medido e precisa ser observado no primeiro produto produzido nesta estrutura.
