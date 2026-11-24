# Roteiro e Storyboard Investigativo (Portão 2) — Como Funciona a Fruta Liofilizada?

- **Tema principal:** A física e a fabricação da fruta liofilizada (*freeze-drying*) e sua dinâmica energética/estrutural em caminhadas longas nas montanhas
- **Exemplar real auditado (entrada orgânica na Cena 06):** daVIDA — Linha Snack Só Fruta `15 g` (`Morango` EAN `7898968451323`; demais variações catalogadas em [pacote.md](pacote.md))
- **Lente criativa adotada (`biblia.md` §2):** Combinação **Lente 2 (Ciência do Processo / "Como é Feito")** + **Lente 3 (Dinâmica Física em Campo / Comparativo)**
- **Duração orgânica medida (`Azure AI Speech F0`, cadência natural `+8%` a `+9%`):** **`80,8s`** (`00s–81s`, `6` cenas animadas contínuas em `Canvas 2D` + `Flow 1080p`)
- **Corte derivado opcional ML Clips (`≤ 60s`):** sob demanda na etapa de publicação (`--ml-clips`)
- **Palavra-chave de DM (`REQ-010`):** `TRILHA` · **Código curto da vitrine (`REQ-008`):** `IBG-002`
- **Aviso determinístico (REQ-007):** **SIM** *(Cena 05 utiliza plano externo cinematográfico de montanha `flow_ia` composto com simulação física determinística)*

---

## Opções de Gancho Investigativo (`0–3s`) — `@Carlos`

1. **Opção A — Paradoxo Sensorial e Físico (ADOTADA):**
   > *"Já mordeu um morango seco que estala na boca e derrete na língua?"*
   - **Por que venceu:** parte de uma experiência física contraintuitiva imediata (seco/crocante por fora, fruta fresca derretendo na língua um segundo depois) que abre organicamente as 4 perguntas investigativas do episódio: o que é, como é fabricada, o que a diferencia das outras técnicas e por que brilha nas montanhas.
2. **Opção B — Bastidor Termodinâmico:**
   > *"Como tirar toda a água de uma fruta usando gelo a quarenta graus negativos em vez de calor?"*
3. **Opção C — Desafio Físico na Montanha:**
   > *"Por que carregar fruta fresca na montanha significa subir ladeira levando noventa por cento de água nas costas?"*

---

## 1. Mapa de Cenas (Coautoria `@Carlos` + `@Steve` + `@Curador`)

| Cena | Tempo | Motor Visual (`@Steve`) | Transformação Visual Animada `Estado A → Ação Física → Estado B` (`@Steve`) | Intenção Vocal (`@Carlos`) | Fala Exata — Narração PT-BR (`@Carlos`) |
|---|---|---|---|---|---|
| **01** | `00s–13s` | `Determinístico` (`Canvas 2D` + [davida_morango_macro_textura.png](assets/davida_morango_macro_textura.png)) + `Rig 2.5D` | Corte transversal de morango fresco repleto de gotículas azuis de água líquida (`Estado A`) → `34` gotas de água se desprendem e evaporam sem encolher o contorno celular nem remover as esferas verdes de Vitamina C, abrindo lupa óptica com zoom contínuo sobre a foto macro real porosa [davida_morango_macro_textura.png](assets/davida_morango_macro_textura.png) (`Estado B`). Rótulos espaciais: `-90% Água` e `Esponja Crocante`. | `[curioso → revelação clara]` | Já mordeu um morango seco que estala na boca e derrete na língua? Isso é fruta liofilizada: a fruta inteira com noventa por cento menos água. Ela mantém o formato original, a cor viva e os nutrientes naturais. |
| **02** | `13s–28s` | `Determinístico` (`Canvas 2D` Microscópio Celular em tela cheia, `show_rig: false`) | Termômetro criogênico lateral despenca de `+20 °C` até `-40 °C` enquanto onda de congelamento varre `19` células vegetais hexagonais: a água líquida em movimento (`Estado A`) cristaliza-se instantaneamente em microcristais hexagonais simétricos (`Ação Física`) que sustentam cada parede celular intacta e protegem a Vitamina C (`Estado B`). Rótulos espaciais: `-40 °C`, `Microcristais` e `Parede Intacta`. | `[investigativo → fascínio técnico]` | Como ela é fabricada? Em vez de forno, começa num frio extremo. A quarenta graus negativos, a água congela rápido em microcristais bem finos. Esses cristais viram um esqueleto interno que protege cada parede celular. |
| **03** | `28s–42s` | `Determinístico` (`Canvas 2D` Câmara de Alto Vácuo & Sublimação em tela cheia, `show_rig: false`) | Dentro da câmara selada, o ponteiro do manômetro varre até a faixa ciano de `Alto Vácuo` (abaixo do ponto triplo); os microcristais azuis dentro do favo celular (`Estado A`) sublimam diretamente em correntes ascendentes de partículas de vapor capturadas pela serpentina fria no topo (`Ação Física`), deixando microporos abertos secos sem nenhuma gota líquida (`Estado B`). Rótulos: `Alto Vácuo`, `Gelo → Vapor` e `Poros Abertos`. | `[didático → descoberta física]` | Depois, bombas criam alto vácuo, abaixo do ponto triplo da água. Nessa pressão, água líquida não existe: o gelo vira vapor direto. Sem líquido puxando as fibras, sobra uma esponja seca cheia de poros. |
| **04** | `42s–56s` | `Determinístico` (`Canvas 2D` Comparativo Físico Triplo) + `Rig 2.5D` | Três câmaras lado a lado em transformação simultânea: na `Estufa Quente`, ondas térmicas laranjas murcham/encolhem o morango escuro enquanto a Vitamina C escapa; na `Fritura Óleo`, óleo amarelo borbulhante sobe e preenche os poros; na `Liofilização`, o morango preserva `100%` do volume, poros limpos e Vitamina C brilhante (`100% Intacta`). | `[contraste analítico → clareza]` | Veja a diferença para as outras técnicas de secagem. Na estufa quente, o calor encolhe a fruta e reduz a vitamina C. Nos chips fritos a vácuo, o óleo entra nos poros. Já na liofilização, fica só fruta. |
| **05** | `56s–69s` | `Flow Omni 360p -> 1080p` (`flow_ia` [flow_trilha_1080p.mp4](assets/flow_trilha_1080p.mp4)) + `Determinístico` (`Canvas 2D` Balança Física) | Plano cinematográfico de caminhada na crista da montanha acima do mar de nuvens ao nascer do sol; surge no céu superior direito (100% livre da silhueta do montanhista) uma balança física de travessão: o prato esquerdo cede pesado sob morangos cheios d'água pingando (`198 g Fresca`), elevando no prato direito a fatia porosa ultraleve irradiando pulsos dourados de energia (`15 g Seca`). | `[energia de campo → síntese prática]` | Por isso ela brilha em caminhadas longas nas montanhas. Fruta fresca carrega peso morto de água, amassa na mochila e fermenta. Sem água, cento e noventa e oito gramas viram quinze gramas de energia rápida. |
| **06** | `69s–82s` | `Determinístico` (`Canvas 2D` + [davida_morango_pouch.png](assets/davida_morango_pouch.png)) + `Rig 2.5D` | Entrada orgânica do exemplar auditado: o sachê real [davida_morango_pouch.png](assets/davida_morango_pouch.png) (`100% Fruta`) aparece ao lado da demonstração física da esponja seca na serra — tesoura e linha tracejada indicam o rasgo superior sem zip enquanto gotículas azuis de neblina são atraídas pelos poros abertos (`Puxa Umidade`), encerrando com o selo discreto `Bio · IBG-002`. | `[dica prática de amigo → fechamento sereno]` | Um exemplo real pra trilha é esse sachê daVIDA, feito só de fruta. Como a esponja seca puxa umidade do ar, abriu na serra, coma na hora. Os detalhes estão no código IBG-002 na bio. |

---

## 2. Dicionário Fonético de TTS (`pt-BR-AntonioNeural`)

| Termo / Sigla na Fala | Pronúncia Fonética Enviada ao TTS | Exibição na Legenda Dinâmica |
|---|---|---|
| `vitamina C` | `vitamina cê` | `vitamina C` |
| `daVIDA` | `da vida` | `daVIDA` |
| `IBG-002` | `í bê gê zero zero dois` | `IBG-002` |
| `90%` | `noventa por cento` | `90%` |
| `-40 °C` | `quarenta graus negativos` | `-40 °C` |
| `198 g` | `cento e noventa e oito gramas` | `198 g` |
| `15 g` | `quinze gramas` | `15 g` |

---

## 3. Orçamento de Créditos do Google Flow (`REQ-003` / ADR `0006`)

| Cena | Clipe / Ativo | Resolução Base & Promoção | Créditos Google Flow |
|---|---|---|---|
| **Cena 05** | Caminhada em crista de montanha ao amanhecer ([flow_trilha_360p.mp4](assets/flow_trilha_360p.mp4) → [flow_trilha_1080p.mp4](assets/flow_trilha_1080p.mp4), `8s` em câmera suave `1,85×` cobrindo `12,8s`) | `360p` base + promoção gratuita na Web UI | **`8 créditos`** |
| **Cenas 01, 02, 03, 04 e 06** | Simulações físicas procedurais em `HTML5 Canvas 2D` + ativos reais verificados | Renderização local `1080×1920` | **`0 créditos`** |
| **Total** | **Episódio completo (`80,8s`)** | **`1080×1920 @ 24 fps`** | **`8 créditos`** *(ativos no master; `16` acumulados no teste dentro do teto de `30`)* |

---

## 4. Notas de Fidelidade Física e Factual (`@Curador`)

- **Parecer preliminar sobre decupagem e simulações (`Portão 2`):** **APROVADO** — todas as etapas físicas representadas nas simulações `Canvas 2D` refletem fielmente os dados verificados em [ficha.md](ficha.md):
  1. Redução de água livre de `~90%` (`92,4%` de redução de massa no morango `198 g → 15 g`) mantendo geometria macroscópica por ausência de tensão superficial líquida (`Cena 01`);
  2. Congelamento rápido a `-40 °C` (dentro da faixa industrial `-30 °C` a `-50 °C` verificada na literatura UNESP/UNICAMP/Embrapa) formando microcristais uniformes que preservam as paredes celulares e o ácido ascórbico (`Cena 02`);
  3. Câmara de alto vácuo abaixo do ponto triplo da água (`< 611,657 Pa` / `< 0,006 atm`), promovendo sublimação direta `Gelo → Vapor` capturado no condensador criogênico superior (`Cena 03`);
  4. Diferenciação física exata contra secagem convectiva em estufa quente (colapso celular e perda térmica de Vitamina C) e contra falsos chips fritos a vácuo (absorção de óleo nos poros) (`Cena 04`);
  5. Balanço real de massa `198 g` morango fresco vs. `15 g` liofilizado na montanha (`Cena 05`) e fidelidade morfológica integral ao sachê laminado opaco `daVIDA 15 g` termosselado sem fecho *zip-lock* e altamente higroscópico após aberto (`Cena 06`).
