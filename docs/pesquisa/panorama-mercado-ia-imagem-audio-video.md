# Quais opções de IA (gratuitas, freemium, pay-per-use e por assinatura) o mercado oferece hoje para imagem, voz em português, efeitos sonoros, vídeo e animação de mascote, e quanto custam por vídeo?

Fontes lidas em 2026-11-19. Reverificar preços, cotas gratuitas e termos comerciais até 2027-02-19.

## Fatos observados

### 1. Padrão adotado por canais *dark* / *faceless* no mercado (panorama 2026)
- Resultados de busca na web sobre fluxos de canais *dark* em vídeo vertical curto (YouTube Shorts, TikTok, Instagram Reels) apontam duas configurações predominantes:
  - **Stack modular:** roteiro gerado por LLM, narração expressiva em serviços dedicados (com destaque frequente para ElevenLabs), planos visuais (*B-roll*) em modelos generativos (`Kling`, `Wan`, `Runway`, `Luma Dream Machine`) e montagem com legendas dinâmicas no `CapCut` — **não verificado** em estudo quantitativo primário de mercado nesta rodada.
  - **Estúdios *all-in-one*:** ferramentas de publicação automatizada (`AutoShorts.ai`, `Faceless.video`, `Kompozy`), acompanhadas de alertas recorrentes sobre restrições de monetização no Programa de Parcerias do YouTube (*inauthentic content*) contra produção em massa com *templates* de baixa variação — panorama de síntese secundária de busca web (**não verificado** em estudo quantitativo primário de mercado nesta rodada).

### 2. Geração de imagens, vetores editáveis (`SVG`) e edição
- **Recraft ([Preços](https://www.recraft.ai/pricing) e [Tabela de preços da API](https://www.recraft.ai/docs/api-reference/pricing)):**
  - **Plano gratuito na web:** gerações ficam públicas na galeria da comunidade, pertencem à Recraft e **não incluem licença comercial**.
  - **Planos pagos e API *pay-as-you-go*:** conferem direitos comerciais e propriedade privada; na API, compra-se saldo pré-pago que **não expira** (`US$ 1 = 1.000 unidades`).
  - **Preços unitários na API:** `V4.1 Flash V2` (raster) = **`US$ 0,007`/imagem**; `V4.1` e `V4 Styles` (raster) = **`US$ 0,035`/imagem**; **vetores `SVG` nativos editáveis** em `V4 Styles Vector` = **`US$ 0,05`/vetor**, `V4.1 Vector` = **`US$ 0,08`/vetor**, `Pro vector` = `US$ 0,12` (`V4 Styles`) a `US$ 0,30` (`V4`/`V4.1`); também oferece operações de vetorização (*Vectorize*), remoção e troca de fundo via API.
- **Gemini 3.1 Flash Image (`Nano Banana 2`) — documentação oficial da Gemini Developer API (guia `gemini-api-guides/pricing.md` consultado via MCP oficial `gemini-api-docs`):**
  - *Free Tier* indisponível na API; *Paid Tier* cobra `US$ 0,50`/1M tokens de entrada e `US$ 60,00`/1M tokens de saída de imagem: **`0.5K` (`512px`, `747` tokens) = `US$ 0,045`**, **`1K` (`1.120` tokens) = `US$ 0,067`**, **`2K` (`1.680` tokens) = `US$ 0,101`** e **`4K` (`2.520` tokens) = `US$ 0,151`**.
  - No gateway [`fal.ai`](https://fal.ai/pricing) (`fal-ai/nano-banana-2` e `/edit`), o valor tabelado é **`US$ 0,08`/imagem**.
- **Outras plataformas citadas no mercado (resultados de busca web — preços, limites gratuitos e termos exatos **não verificado** diretamente nas documentações oficiais nesta rodada):**
  - `FLUX.1 [schnell]` (~`US$ 0,003`/MP) e `FLUX.2` / `FLUX 3` (~`US$ 0,009–0,048`/MP via `fal.ai` / `Replicate`);
  - `Ideogram 4.5` (API pré-paga entre `US$ 0,03` e `US$ 0,10`/imagem em geração por texto, citada para renderização de texto dentro de imagens, além de cota semanal gratuita na web);
  - `GPT Image` (OpenAI, ~`US$ 0,12–0,21`/imagem em alta qualidade, sem *free tier* na API);
  - `Leonardo AI` (plano web gratuito citado com `150` tokens rápidos/dia em gerações públicas e API separada por tokens).

### 3. Áudio: vozes em português brasileiro (`pt-BR`), efeitos sonoros (`SFX`) e música
- **Google Cloud Text-to-Speech ([Tabela oficial de preços](https://cloud.google.com/text-to-speech/pricing) e [Documentação Chirp 3: HD](https://cloud.google.com/text-to-speech/docs/chirp3-hd)):**
  - **`Chirp 3: HD`:** suporte oficial documentado para **`Portuguese (Brazil)` (`pt-BR`)**, com cota gratuita mensal de **`0` a `1 milhão` de caracteres** (excedente de `US$ 30` por 1M caracteres; voz customizada instantânea sem cota gratuita a `US$ 60`/1M). Busca web em fóruns/documentação técnica indica ausência de suporte a *tags* SSML em requisições *streaming* e limitações de marcações/controle fino em síntese de áudio longo (exigindo requisições síncronas padrão e validação por idioma `pt-BR`) — **não verificado** em ensaio direto na API do GCP nesta rodada.
  - **`WaveNet` e `Standard`:** cota gratuita mensal de **`0` a `4 milhões` de caracteres** (excedente de `US$ 4` por 1M caracteres). **`Studio`:** **`0` a `1 milhão`** grátis (`US$ 160`/1M excedente). Requer conta de faturamento configurada no Google Cloud.
  - **`Gemini 3.8 Flash-Lite TTS (Preview)` e `Gemini 3.8 Flash TTS (Preview)`** *(sem cota gratuita; conversão documentada na página oficial de **`25` tokens de áudio por segundo**)*:
    - `Flash-Lite TTS`: `US$ 0,50`/1M tokens de texto + **`US$ 6,00`/1M tokens de áudio** até `2026-12-31` (`US$ 12,00`/1M a partir de `2027-01-01`), equivalente a **`US$ 0,009` por minuto de áudio** em 2026 (`US$ 0,018/min` em 2027);
    - `Flash TTS`: `US$ 0,50`/1M tokens de texto (`US$ 1,00` em 2027) + **`US$ 9,00`/1M tokens de áudio** até `2026-12-31` (`US$ 18,00`/1M em 2027), equivalente a **`US$ 0,0135` por minuto de áudio** em 2026 (`US$ 0,027/min` em 2027).
- **Microsoft Azure AI Speech ([Microsoft Q&A — tier `F0` e `S0`](https://learn.microsoft.com/en-us/answers/questions/1654938/text-to-speech-s0-standard-tier-0-5-million-charac)):**
  - Documentação de suporte em `learn.microsoft.com` confirma o tier gratuito **`F0`** com **`0,5 milhão` (`500.000`) de caracteres/mês grátis** em vozes neurais pré-construídas (via API oficial, com limite de requisições por minuto e bloqueio ao atingir a cota sem cobrança automática). Busca técnica indica que `F0` é uma faixa gratuita de preço (distinta de licença não-comercial, salvo quando vinculada a assinaturas promocionais como *Azure for Students*, com recomendação do fabricante de migrar ao tier `S0` em produção de maior porte por limites de concorrência) e que vozes neurais `pt-BR` oferecem eventos `WordBoundary` e `22` *viseme IDs* condicionados à matriz de cada voz; suporte específico de visemas por voz `pt-BR`, preços pagos `S0` (`US$ 15–22`/1M caracteres) e termos comerciais completos do `F0` permanecem **não verificado** diretamente na matriz/página de preços do Azure (que sofreu *timeout* na coleta anterior).
- **ElevenLabs ([Preços oficiais](https://elevenlabs.io/pricing)):**
  - **`Free` (`US$ 0/mês`):** `10.000` créditos/mês (sem acúmulo), **sem licença comercial**.
  - **`Starter` (`US$ 6/mês`):** `30.000` créditos/mês em *pool* único compartilhado entre voz, ***Text to Sound Effects* (`SFX`)** e **música**, incluindo **Licença Comercial** e **uso comercial de música**.
  - **`Creator` (`US$ 22/mês`, `US$ 11` no 1º mês):** `121.000` créditos/mês em *pool* compartilhado. *(Proporção exata de créditos por segundo em `SFX` e música não foi extraída integralmente — **não verificado**.)*
- **Google Lyria 3 (Música — documentação oficial `gemini-api-guides/pricing.md` via MCP `gemini-api-docs`):**
  - *Free Tier* indisponível; **`Lyria 3 Clip Preview (30s)` = `US$ 0,04` por música** e **`Lyria 3 Pro Preview` (música completa) = `US$ 0,08` por música**.
- **Referência interna atual do projeto ([alinhamento-ferramentas-producao-video-e-audio.md](alinhamento-ferramentas-producao-video-e-audio.md)):** o repositório utiliza atualmente `edge-tts` (`7.3.1`, API não-oficial gratuita sem garantia contratual de disponibilidade) para TTS `pt-BR`.
- **Outras opções citadas em busca web (**não verificado** diretamente nas páginas oficiais nesta rodada):**
  - `Cartesia Sonic` (suporte citado a 44 idiomas incl. `pt-BR`, baixa latência, Free / Pro ~`US$ 5/mês`);
  - `Fish Audio` (plano Free de teste e API paga citada em torno de `US$ 15`/1M caracteres);
  - `OpenAI TTS` (sem *free tier*; busca web indica desativação de `tts-1`/`gpt-4o-mini-tts` prevista para `2027-01-06` em favor da `Realtime API`);
  - `Suno AI` (`50` créditos/dia no Free **sem licença comercial** nem uso retroativo após upgrade; Pro citado a ~`US$ 10/mês` com direitos comerciais);
  - `Meta AudioGen / MusicGen` (pesos distribuídos tipicamente sob `CC-BY-NC 4.0`, uso não-comercial).

### 4. Geração de vídeo (*pay-per-use* em nuvem versus assinaturas)
- **Google Flow Web UI (`Omni Flash 1.2` e `Veo 3.1 Lite` — [Recursos do Flow](https://support.google.com/flow/answer/16352836?hl=en) e [Créditos do Flow](https://support.google.com/flow/answer/16526234?hl=pt-br&co=GENIE.Platform%3DDesktop)):**
  - Plano **Google AI Pro** já mantido pelo usuário inclui **`1.000` créditos/mês** na Web UI; em `Omni Flash 1.2 · 360p` (`1 crédito/s` até `10s`) com *upscale* a `1080p` (`0` crédito até `10s`), gera até **`125` clipes de `8s`/mês** sem gasto extra em dólar.
  - Via **Gemini Developer API** paga (`gemini-omni-1.1-flash`, MCP `pricing.md`), sem *Free Tier*: `US$ 1,50`/1M entrada e `US$ 17,50`/1M saída de vídeo (`5.792` tokens/s em `720p` ≈ `US$ 0,10/s`, cerca de `US$ 0,80` por `8s`).
- **`fal.ai` ([Preços oficiais](https://fal.ai/pricing)):**
  - Cobrança *serverless* *pay-per-use* por segundo/token de saída bem-sucedida, sem mensalidade fixa:
    - `Kling Video v2.5 Turbo Pro (Image-to-Video)` (`fal-ai/kling-video/v2.5-turbo/pro/image-to-video`): **`US$ 0,07/s`** (`US$ 0,56` por clipe de `8s`);
    - `Kling Video v3 Pro (Image-to-Video` e `Text-to-Video)`: **`US$ 0,14/s`** (`US$ 1,12` por clipe de `8s`);
    - `ByteDance Seedance 2.0 (Reference-to-Video` e `Image-to-Video)`: **`US$ 0,014` por `1.000` tokens**.
- **`Replicate` ([Preços oficiais](https://replicate.com/pricing)):**
  - Cobrança *pay-per-use* por segundo de GPU em uso ou por segundo de vídeo gerado conforme o modelo, sem mensalidade fixa.
- **Outros modelos citados no mercado (busca web — preços exatos **não verificado** diretamente nos *endpoints* nesta rodada):** `Wan` (~`US$ 0,05–0,28/s` entre `480p` e `1080p`), `Hailuo / MiniMax` (~`US$ 0,05–0,11/s`), `Vidu` (~`US$ 0,06–0,12/s`), `Runway Dev` (~`US$ 0,10–0,12/s` ou planos a partir de `US$ 15/mês`) e `Veo 3.1` em gateways terceiros (~`US$ 0,20–0,40/s`).

### 5. Avatares falantes e *lip-sync* em nuvem para mascote não-humano
- **Base interna atual do projeto ([0005-pipeline-hibrido-25d-e-flow.md](../decisoes/0005-pipeline-hibrido-25d-e-flow.md)):** o projeto prevê **Rig 2.5D local** animado em camadas PNG sobre a máquina local a custo adicional `US$ 0` por vídeo.
- **Limitação anatômica em personagens não-humanos (síntese técnica de busca web — **não verificado** em teste prático com [referencia-oficial.jpg](../../assets/personagem/referencia-oficial.jpg)):**
  - Ferramentas guiadas por marcos faciais humanos (**`LivePortrait`**, **`MuseTalk`**) tendem a deformar focinhos, texturas não-humanas e ângulos laterais quando o design foge de proporções humanas frontais;
  - Geradores de animação/vídeo completos (**`ByteDance OmniHuman 1.5/2.0`**, **`Kling Lip-Sync / Avatar`**, **`Hedra`**) lidam melhor com personagens 2D/3D estilizados quando há abertura ou contraste nítido na boca, movimentando cabeça e torso junto à fala.
- **Faixas de preço *pay-per-use* relatadas na web (**não verificado** diretamente nas páginas de tarifa nesta rodada):** `OmniHuman 1.5/2.0` (~`US$ 0,091–0,16/s` em `fal.ai`/provedores), `Sync.so` (~`US$ 0,04–0,133/s`), `Hedra API` (~`US$ 0,025–0,06+/s` em carteira pré-paga), `Kling Lip-Sync` (a partir de ~`US$ 0,0028/s` em modo específico básico até faixas de avatar completo) e `LivePortrait`/`MuseTalk` em GPU *serverless* (frações de centavo a poucos centavos por execução).

## Inferências

### Comparativo determinístico de custo por vídeo (`~50s` de fala / `~800` caracteres + `1` clipe externo de `8s` + `1` vetor/imagem + `1` trilha `30s`)

- **Inferência:** Estimativa construída combinando um roteiro padrão hipotético (`~50s` de fala ≈ `800` caracteres, `1` clipe externo de `8s`, `1` diagrama/vetor e `1` trilha `30s`) com os preços unitários e cotas observados acima:

| Frente do vídeo | Opção comparada | Modelo de cobrança e cota | Custo adicional estimado por vídeo | Risco ou restrição observada |
|---|---|---|---|---|
| **Imagem / Vetor `SVG`** | **`Recraft API` (`V4 Styles Vector` / `V4.1 Vector`)** | *Pay-per-use* (`US$ 1 = 1.000` unid., sem validade) | **`US$ 0,05` a `US$ 0,08`** por `SVG` | Free na web proíbe uso comercial; API exige compra pré-paga mínima de saldo. |
| **Imagem raster** | **`Gemini 3.1 Flash Image` (`0.5K` / `1K`)** | *Pay-per-use* API Gemini (ou já usado em sessão) | **`US$ 0,045` (`512px`) / `US$ 0,067` (`1K`)** | Saída apenas raster (`PNG`/`JPG`); vetores precisos dependem de código/SVG. |
| **Voz `pt-BR` (TTS)** | **`Google Cloud Chirp 3: HD`** | Gratuito **`0–1M` chars/mês** (`~1.250` vídeos/mês) | **`US$ 0`** na cota (`US$ 0,024` excedente) | API oficial estável com uso comercial; exige conta de faturamento ativa no GCP. |
| **Voz `pt-BR` (TTS)** | **`Microsoft Azure Speech F0`** | Gratuito **`0–500k` chars/mês** (`~625` vídeos/mês) | **`US$ 0`** na cota `F0` | API oficial das mesmas vozes neurais usadas via `edge-tts`, sujeita a teto de concorrência do `F0`. |
| **Voz `pt-BR` (TTS)** | **`Gemini 3.8 Flash-Lite TTS (Preview)`** | *Pay-per-use* (`25` tokens/s; sem *free tier*) | **`~US$ 0,008`** em 2026 (`~US$ 0,015` em 2027) | Voz controlável por *prompt* de estilo a custo de centavos; ainda rotulado *Preview*. |
| **Voz + `SFX` + Música** | **`ElevenLabs Starter`** | Assinatura **`US$ 6/mês`** (`30.000` créditos compartilhados) | **`~US$ 0,20/vídeo`** (estimando ~`1.000` créd./vídeo — **não verificado**) | Plano Free proíbe uso comercial; `Starter` unifica voz `pt-BR`, `SFX` e trilha sob licença comercial. |
| **Música de fundo** | **`Google Lyria 3 Clip (30s)`** | *Pay-per-use* API Gemini (`US$ 0,04`/música) | **`US$ 0,04`** por música reutilizável | Sem *free tier*; faixas instrumentais geradas podem ser reaproveitadas em vários vídeos. |
| **Vídeo externo (`8s`)** | **`Google Flow Web UI` (`Omni 1.2 · 360p -> 1080p`)** | Incluso no Google AI Pro (`1.000` créd./mês) | **`US$ 0` adicional** (`8` créditos até `125` vídeos/mês) | Consumo via Web UI; automação direta via Gemini API paga custaria `~US$ 0,80/8s` (`720p`). |
| **Vídeo externo (`8s`)** | **`fal.ai` (`Kling v2.5 Turbo Pro` / `v3 Pro`)** | *Pay-per-use* sem mensalidade | **`US$ 0,56`** (`v2.5 Turbo`) / **`US$ 1,12`** (`v3 Pro`) | Alternativa programática direta via API quando a cota Pro saturar ou exigir estética específica do `Kling`. |
| **Mascote falando (`40s`)** | **`Rig 2.5D` local vs. `OmniHuman 2.0` (`~40s`)** | Local gratuito vs. *pay-per-use* (`~US$ 0,091–0,16/s` — **não verificado**) | **`US$ 0`** (Rig local) vs. **`~US$ 3,64–6,40`** (**não verificado**) | `OmniHuman`/`Kling` trazem movimento orgânico completo de cabeça/corpo, mas a custo alto por minuto para falas longas. |

- **Inferência:** Em síntese de voz `pt-BR`, o mercado oferece alternativas oficiais comerciais gratuitas muito mais estáveis que o `edge-tts` não-oficial (**`Google Cloud Chirp 3: HD`** com `1M` chars/mês grátis e **`Azure Speech F0`** com `500k` chars/mês grátis) além de **`Gemini 3.8 Flash-Lite TTS`** abaixo de `US$ 0,01` por vídeo quando se deseja controle expressivo por *prompt*, enquanto o plano gratuito da `ElevenLabs` não serve para canal monetizado por vedar uso comercial.
- **Inferência:** Planos gratuitos na web de **ElevenLabs, Recraft, Suno e pesos `CC-BY-NC` (AudioGen)** compartilham restrições de **licenciamento comercial no modo gratuito**, porém continuam úteis na caixa de ferramentas para **provas de conceito e avaliação interna de ganho real** antes de assinar; para a **publicação comercial efetiva**, utilizam-se cotas gratuitas comerciais (`Google Cloud Chirp 3: HD`, `Azure Speech F0`) ou ativos já produzidos nos planos/APIs comerciais (`Recraft API` a `US$ 0,05–0,08` por `SVG`, `Google Lyria 3` a `US$ 0,04` por clipe de `30s`, `ElevenLabs Starter` a `US$ 6/mês`), respeitando que `Recraft` e `Suno` não licenciam retroativamente arquivos gerados no *Free*.
- **Inferência:** Para vídeos externos de `8s`, a assinatura **Google AI Pro** já mantida (`Omni Flash 1.2 · 360p → 1080p` a `0` crédito extra) permanece substancialmente mais barata que qualquer API *pay-per-use* (`fal.ai Kling` entre `US$ 0,56` e `US$ 1,12` por clipe de `8s`), embora gateways como **`fal.ai`** sejam úteis sob demanda sem assinatura fixa quando se precisar de API automatizada ou de um modelo específico além do Flow.
- **Inferência:** Para o mascote não-humano falando durante quase todo o vídeo (`40–50s`), o **Rig 2.5D local (`US$ 0`)** evita tanto o custo elevado por segundo de avatares generativos em nuvem (`~US$ 3,64–6,40` por `40s` em `OmniHuman`, estimativa secundária **não verificada**) quanto falhas geométricas em modelos focados em rosto humano (`LivePortrait`/`MuseTalk`), deixando eventual uso de `Kling Avatar` / `OmniHuman` restrito a testes curtos de gancho inicial (`3–5s`) caso se deseje comparar ganho real de retenção.
