# Como produzir e animar um personagem consistente em vídeo (incluindo 3D e lip-sync) mantendo o custo controlado?

Fontes lidas em 2026-11-17. Reverificar preços, planos e limites de créditos até 2026-12-17.

## Fatos observados sobre abordagens e ferramentas

### 1. Pipeline 3D local com *rig* e *lip-sync* por fonemas
- **Blender + Auto Lip Sync (`auto-lip-sync`):** complemento gratuito e open-source para Blender que utiliza modelos locais leves de reconhecimento de fala (derivados de WhisperX e eSpeak NG) para gerar *keyframes* de visemas/boca na linha do tempo. Fonte: [Repositório auto-lip-sync](https://github.com/atongsak/auto-lip-sync).
- **Blender + Rhubarb Lip Sync:** complemento gratuito e offline para Blender que analisa áudio `.wav` e mapeia poses de boca ou *shape keys* em personagens 2D/3D estilizados. Fonte: [Repositório blender-rhubarb-lipsync](https://github.com/scaredyfish/blender-rhubarb-lipsync).
- **Licença do Blender:** software gratuito e open-source sob licença **GNU GPL** (v3 ou posterior); a licença cobre apenas o código do software, e as obras/animações geradas pertencem integralmente ao criador, inclusive para uso comercial. Fonte: [Licença oficial do Blender](https://www.blender.org/about/license/).

### 2. Animação neural local e *Image-to-3D* (restrição de hardware local)
- **Hardware local verificado (`2026-11-18`):** `Intel Core i7-5557U` (`x86_64`), 16 GB RAM e GPU integrada `Intel Iris Graphics 6100` (sem NVIDIA CUDA nem Apple Silicon). Em teste direto com Blender `4.5.16 LTS`, `BLENDER_EEVEE_NEXT` falhou em modo `--background` por ausência de contexto GPU, enquanto `CYCLES` em CPU levou **55 segundos por quadro** (`540×720`, 24 amostras).
- **MuseTalk / EchoMimic / LivePortrait / Hunyuan3D:** exigem GPU NVIDIA (CUDA) ou aceleração dedicada; em CPU Intel pura ficam inviáveis para produção local.
- **Image-to-3D em nuvem (Tripo AI / Meshy / Rodin):** geram malha `.glb` a partir de uma imagem de referência e oferecem *add-ons* para Blender e *auto-rigging* (Tripo/Meshy) — planos gratuitos têm limites de créditos e restrições de licença (ex.: Tripo *free* usa `CC BY 4.0`, detalhes completos de termos **não verificados** na íntegra).

### 3. Plataformas dedicadas de *lip-sync* / animação por imagem (2026)
- **Hedra (`Character-3`), Kling AI e Runway:** otimizadas para animar retratos e mascotes estilizados com áudio/vídeo, porém dependem de assinaturas pagas adicionais (ex.: Hedra Basic ~US$ 20/mês; Runway Standard US$ 15/mês; Kling Standard ~US$ 8,80/mês — valores secundários **não verificados** diretamente nos termos vigentes).

### 4. Geração de vídeo por IA com créditos já inclusos (Google Flow / Veo / Omni)
- **Custo por clipe e limites técnicos:** `Veo 3.1 Lite` (720p/1080p, clipes de 4s/6s/8s) consome 10 créditos por geração (5 no plano Ultra); `Veo 3.1 Fast` (20 créditos, 10 no Ultra) e `Veo 3.1 Quality` (100 créditos) têm aposentadoria prevista para 2026-12-05; `Omni Flash` tem consumo variável conforme duração e oferece modo **Omni 360p** a cerca de **1/3 do custo** de 720p para rascunhos/protótipos. O recurso **Ingredients to Video** aceita até 3 imagens de referência para manter consistência de personagem. Fonte: [Documentação de créditos e recursos do Google Flow](https://support.google.com/flow/answer/16526234?hl=en&co=GENIE.Platform%3DAndroid).
- **Preços e cotas mensais dos planos:** *Google AI Pro* por US$ 19,99/mês (R$ 96,99/mês no Brasil) inclui **1.000 créditos/mês** no Google Flow e US$ 10/mês em créditos de desenvolvedor/Cloud; *Google AI Ultra* varia de US$ 99,99 a US$ 200/mês conforme subnível (com 10.000 a 25.000 créditos/mês no Flow — faixa exata por subnível a confirmar na contratação). Fontes: [Assinaturas Google AI (Brasil)](https://gemini.google/br/subscriptions/?hl=pt-BR) e [Benefícios Google One AI](https://one.google.com/about/articles/google-one-ai-subscription-benefits/). Cotas exatas do plano *Free* (50 créditos diários) e *Google AI Plus* (US$ 4,99/mês) — **não verificado** nas páginas oficiais em português nesta rodada.
- **Consumo por resolução na geração de imagem (`gemini-3.1-flash-image`):** `512px` (`0.5K`) consome **747 tokens** de saída por imagem; `1K` consome **1.120 tokens** (+50%); `2K` consome **1.680 tokens** (2,25×); `4K` consome **2.520 tokens** (3,37×). Fonte: [Documentação de geração de imagens da Gemini API](https://ai.google.dev/gemini-api/docs/image-generation).

### 5. Observação do projeto anterior (`~/Dev/vendas_online`)
- No projeto anterior (`~/Dev/vendas_online`), a chave de API do AI Studio retornou erro `HTTP 402` por ausência de créditos pré-pagos na API, levando ao uso local de `edge-tts` + `ffmpeg` + HTML5 Canvas sem gasto de API (observação do projeto anterior).

## Inferências

- **Inferência:** Um modelo 3D (*rig*) em arquivo-mestre permite reutilizar o mesmo personagem entre vídeos e gerar *lip-sync* localmente sem custo marginal por minuto gerado, ao contrário de plataformas pagas por crédito mensal (como HeyGen ou consumo contínuo em ferramentas generativas).
