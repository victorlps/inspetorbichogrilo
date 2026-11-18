# Como produzir e animar um personagem consistente em vídeo (incluindo 3D e lip-sync) mantendo o custo controlado?

Fontes lidas em 2026-11-17. Reverificar preços, planos e limites de créditos até 2026-12-17.

## Fatos observados sobre abordagens e ferramentas

### 1. Pipeline 3D local com *rig* e *lip-sync* por fonemas
- **Blender + Auto Lip Sync (`auto-lip-sync`):** complemento gratuito e open-source para Blender que utiliza modelos locais leves de reconhecimento de fala (derivados de WhisperX e eSpeak NG) para gerar *keyframes* de visemas/boca na linha do tempo. Fonte: [Repositório auto-lip-sync](https://github.com/atongsak/auto-lip-sync).
- **Blender + Rhubarb Lip Sync:** complemento gratuito e offline para Blender que analisa áudio `.wav` e mapeia poses de boca ou *shape keys* em personagens 2D/3D estilizados. Fonte: [Repositório blender-rhubarb-lipsync](https://github.com/scaredyfish/blender-rhubarb-lipsync).
- **Licença do Blender:** software gratuito e open-source sob licença **GNU GPL** (v3 ou posterior); a licença cobre apenas o código do software, e as obras/animações geradas pertencem integralmente ao criador, inclusive para uso comercial. Fonte: [Licença oficial do Blender](https://www.blender.org/about/license/).

### 2. Animação neural local de retrato 2D/3D pré-renderizado
- **MuseTalk / EchoMimic / LivePortrait:** ferramentas open-source citadas para sintetizar movimento facial e labial em vídeo a partir de uma imagem base e áudio/vídeo-guia, com exigência típica de GPU NVIDIA local — **não verificado** diretamente nos repositórios oficiais nem testado em Apple Silicon nesta rodada.

### 3. Avatar por foto / vídeo via plataforma paga (HeyGen)
- **Modelo de cobrança:** assinatura mensal baseada em créditos, com variação de resolução e recursos por plano. Fonte: [Planos baseados em créditos do HeyGen](https://help.heygen.com/en/articles/15125761-heygen-credit-based-pricing-plans-subscriptions-explained).
- **Planos pagos confirmados:** *Creator* a US$ 29/mês (ou US$ 24/mês no plano anual) com **600 créditos/mês** e exportação em 1080p sem marca d'água; *Pro* a partir de US$ 49/mês com **1.000+ créditos/mês** e exportação em 4K. Fonte: [Preços oficiais do HeyGen](https://www.heygen.com/pricing). Detalhes exatos dos planos *Free* e *Business* — **não verificado** na íntegra nesta rodada.

### 4. Geração de vídeo por IA com créditos (Google Flow / Veo)
- **Custo por clipe e limites técnicos:** `Veo 3.1 Lite` (720p/1080p, clipes de 4s/6s/8s) consome 10 créditos por geração (5 no plano Ultra); `Veo 3.1 Fast` (20 créditos, 10 no Ultra) e `Veo 3.1 Quality` (100 créditos) têm aposentadoria prevista para 2026-12-05; `Omni Flash` tem consumo variável conforme duração (tabela exata de valores por segundo não extraída na íntegra — **não verificado**). Fonte: [Documentação de créditos do Google Flow](https://support.google.com/flow/answer/16526234?hl=en&co=GENIE.Platform%3DAndroid).
- **Preços e cotas mensais dos planos:** *Google AI Pro* por US$ 19,99/mês (R$ 96,99/mês no Brasil) inclui **1.000 créditos/mês** no Google Flow e US$ 10/mês em créditos de desenvolvedor/Cloud; *Google AI Ultra* varia de US$ 99,99 a US$ 200/mês conforme subnível (com 10.000 a 25.000 créditos/mês no Flow — faixa exata por subnível a confirmar na contratação). Fontes: [Assinaturas Google AI (Brasil)](https://gemini.google/br/subscriptions/?hl=pt-BR) e [Benefícios Google One AI](https://one.google.com/about/articles/google-one-ai-subscription-benefits/). Cotas exatas do plano *Free* (50 créditos diários) e *Google AI Plus* (US$ 4,99/mês) — **não verificado** nas páginas oficiais em português nesta rodada.

### 5. Observação do projeto anterior (`~/Dev/vendas_online`)
- No projeto anterior (`~/Dev/vendas_online`), a chave de API do AI Studio retornou erro `HTTP 402` por ausência de créditos pré-pagos na API, levando ao uso local de `edge-tts` + `ffmpeg` + HTML5 Canvas sem gasto de API (observação do projeto anterior).

## Inferências

- **Inferência:** Um modelo 3D (*rig*) em arquivo-mestre permite reutilizar o mesmo personagem entre vídeos e gerar *lip-sync* localmente sem custo marginal por minuto gerado, ao contrário de plataformas pagas por crédito mensal (como HeyGen ou consumo contínuo em ferramentas generativas).
