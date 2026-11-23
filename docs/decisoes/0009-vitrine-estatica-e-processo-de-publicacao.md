---
status: "accepted"
date: 2026-11-23
decision-makers: victor
---

# Vitrine estática na bio, voz comercial oficial e processo de publicação

## Contexto e problema

Com o primeiro produto (`ducha-eletronica-zagonel-nd-7700w`) aprovado tecnicamente no Portão 3, surgiram três definições operacionais necessárias para publicar na Fase 1 e tornar o processo repetível para os próximos vídeos:

1. **Hospedagem da vitrine de links na bio (`REQ-008`, `REQ-009`, `REQ-011`):** o projeto precisa de uma página pública leve, com busca por código curto (`IBG-001`) e links separados por variação essencial, sem custo fixo mensal e sem misturar arquivos de site com `docs/` (reservado à documentação do projeto).
2. **Licenciamento comercial da locução (`REQ-006`):** a verificação jurídica e técnica confirmou que o `edge-tts` acessa o endpoint consumidor *Read Aloud* do Microsoft Edge, o qual **não concede direitos comerciais** para redistribuição ou monetização de vídeos, além de estar sujeito a bloqueios sem aviso.
3. **Publicação no Mercado Livre Clips (`0001`):** a versão principal do vídeo utiliza um clipe de uso prático gerado via Google Flow (`flow_ia`, Cena 02), exigindo uma variação determinística sem `flow_ia` para cumprir a diretriz de produto real do ML Clips, além de padronização dos perfis de todas as contas (`@inspetorbichogrilo`).

## Opções consideradas

### Vitrine estática na bio
1. **Pasta `vitrine/` dedicada + GitHub Pages (`actions/deploy-pages`) com `catalogo.json`:** mantém `docs/` exclusivo para documentação, publica HTML/CSS/JS estáticos a `US$ 0,00`, permite busca client-side por código curto (`IBG-001`) e atualiza links sem mudar a URL da bio (`REQ-009`).
2. **Serviço pago de Link-in-Bio (Linktree Pro / Beacons):** adiciona custo mensal recorrente ou limita busca por código curto e personalização.
3. **Publicar a partir de `docs/`:** mistura documentação interna do projeto com o site público da vitrine.

### Voz comercial final (`REQ-006`)
1. **Azure AI Speech (`F0` gratuito) com fallback `Piper pt_BR`:** usa a API oficial da Microsoft para a mesma voz `pt-BR-AntonioNeural` com direitos comerciais explícitos, `WordBoundary` e visemas nativos (`500.000` caracteres/mês grátis), mantendo `edge-tts` restrito ao rascunho/animatic do Portão 2.
2. **Manter `edge-tts` no vídeo final publicado:** viola os termos de serviço do endpoint consumidor e expõe o canal monetizado a risco de bloqueio.

## Decisão

Opções escolhidas:
- **Vitrine estática na pasta `vitrine/` publicada no GitHub Pages** via `.github/workflows/deploy-vitrine.yml`, alimentada por `vitrine/catalogo.json` (com códigos fixos `IBG-001`, `IBG-002`...).
- **Azure AI Speech (`F0`)** obrigatório para a síntese vocal do vídeo final (`Portão 3`), reservando `edge-tts` apenas para o animatic interno do Portão 2.
- **Padronização de perfis e variação `--ml-clips`:** todos os perfis (`@inspetorbichogrilo` no Instagram, TikTok, YouTube Shorts e Mercado Livre Clips) compartilham o mesmo avatar `1:1`, bio *dark* (`REQ-011`) e link único da vitrine; vídeos com cena `flow_ia` geram automaticamente a variante `video_final_ml_clips_1080p.mp4` sem IA generativa na cena de uso real.

### Viabilidade de custo (`FinOps` — `REQ-016`)

Inventário de recursos consumidos por publicação (além dos créditos Google Flow já orçados em `0006`):
- **Hospedagem da vitrine (GitHub Pages + GitHub Actions):** repositório público/Pages gratuito (`US$ 0,00/mês`, dentro da franquia padrão de `100 GB`/mês de banda).
- **Voz comercial (`Azure AI Speech F0`):** ~`1.100` caracteres por vídeo de `60s` na voz `pt-BR-AntonioNeural`.
- **Renderização da variante `--ml-clips`:** `100%` local em CPU/GPU (`Python + ffmpeg`), `US$ 0,00` e `0` crédito Flow.

| Volume mensal | Caracteres Azure Speech | Cota `F0` (`500k`/mês) | Custo Azure (`US$`) | Custo GitHub Pages (`US$`) | Total adicional (`US$`) |
|---|---|---|---|---|---|
| `1` vídeo/mês | `~1.100` | `0,22%` | `US$ 0,00` | `US$ 0,00` | `US$ 0,00` |
| `30` vídeos/mês | `~33.000` | `6,60%` | `US$ 0,00` | `US$ 0,00` | `US$ 0,00` |
| `100` vídeos/mês | `~110.000` | `22,00%` | `US$ 0,00` | `US$ 0,00` | `US$ 0,00` |
| `300` vídeos/mês | `~330.000` | `66,00%` | `US$ 0,00` | `US$ 0,00` | `US$ 0,00` |

- **Ponto de saturação:** `~450` vídeos/mês no tier `Azure AI Speech F0` (`500.000` caracteres/mês). Caso ultrapasse, o fallback offline `Piper pt_BR` ou `Azure S0` (`US$ 15/1M` chars) absorve o excedente.

### Consequências

- **Bom:** elimina risco de licença comercial na narração mantendo exatamente a mesma voz `pt-BR-AntonioNeural`, entrega vitrine própria com busca por código curto a `US$ 0,00` e habilita publicação simultânea no Mercado Livre Clips.
- **Ruim:** exige configuração única inicial da chave `AZURE_SPEECH_KEY` no `.env`, conexão de um repositório remoto no GitHub para Pages e manutenção de duas variantes de MP4 (`video_final_1080p.mp4` e `video_final_ml_clips_1080p.mp4`) quando houver cena `flow_ia`.
