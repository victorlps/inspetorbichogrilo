# Quais capacidades e limitações reais das ferramentas de áudio, lip-sync, vídeo por IA e composição local determinam a ordem dos portões e a arquitetura de produção?

Fontes lidas em 2026-11-18. Reverificar capacidades de modelos, bibliotecas e binários locais até 2027-02-18.

## Fatos observados

### 1. Google Flow (`Omni Flash 1.2` e `Veo 3.1 Lite`) versus Gemini Developer API
- **Recursos oficiais do `Omni Flash 1.2` no Google Flow ([Guia de criação no Google Flow](https://support.google.com/flow/answer/16352836?hl=en)):**
  - Para assinantes **Google AI Plus, Pro ou Ultra**, suporta proporções **`9:16`** e `16:9` com duração de **`3` a `15s`** em *Text to Video*, *Frames to Video* (na Web), *Ingredients/References to Video* e *Video-to-Video editing*;
  - Suporta extensão **`Omni Extend`** (`3` a `10s`, com até `3` imagens de referência, na Web) e **aumento de resolução (`Upscale Omni 360p`) até `1080p`** (`4K` no Ultra);
  - Confirma explicitamente que **`Omni 360p`** gera ou edita a partir de **texto, *frames* ou *ingredients*** por **1/3 do custo de créditos de `720p`**;
  - **`Veo 3.1 Lite`** suporta `4`, `6` ou `8s` em `720p` (*Ingredients/References* apenas em `8s`, sem edição nem extensão de vídeo);
  - **Desativação programada:** `Veo 3.1 Fast`, `Veo 3.1 Quality` e `Omni Flash 1.1` têm aposentadoria anunciada para **`2026-12-05`**.
- **Tabela de créditos na Web UI do Flow ([Ajuda do Google Flow — Créditos](https://support.google.com/flow/answer/16526234?hl=pt-br&co=GENIE.Platform%3DDesktop)):**
  - `Omni Flash 1.2` até `10s`: **`360p` = 1 crédito/s** e **`720p` = 3 créditos/s**;
  - **Upscale de `Omni 360p` para `720p` ou `1080p`** (Plus/Pro/Ultra): **`0` crédito para vídeos de `1` a `10s`** (`1 crédito/s` extra acima de `10s`);
  - Plano **Google AI Pro** concede **`1.000` créditos mensais** na **Web UI do Flow** (sem acúmulo para o mês seguinte).
- **Gemini Developer API paga (`gemini-omni-1.1-flash`, guia `pricing.md` consultado via documentação MCP oficial):** não oferece *Free Tier*; no *Paid Tier*, cobra **`US$ 1,50` por 1M de tokens de entrada** e **`US$ 17,50` por 1M de tokens de vídeo de saída** (`5.792` tokens/s em `720p`, equivalente aproximado a **`US$ 0,10/s`**). *(Nota: a disponibilidade e eventual tabela direta da versão `1.2` via API paga separada não foram listadas nessa consulta — **não verificado**.)*

### 2. Síntese de voz (`edge-tts` e `Piper pt_BR`) e sincronia labial (`Rhubarb Lip Sync`)
- **`Rhubarb Lip Sync` ([Repositório oficial `DanielSWolf/rhubarb-lip-sync`](https://github.com/DanielSWolf/rhubarb-lip-sync)):**
  - Documenta dois reconhecedores: **`pocketSphinx`** (padrão, indicado para gravações em inglês) e **`phonetic`** (indicado para gravações em idiomas não-ingleses, o qual **não** tenta compreender palavras inteiras nem aceita guia lexical equivalente ao fluxo nativo em inglês);
  - Relatos de comunidade encontrados em busca web sobre uso não-inglês apontam alternância entre pausas (*stalling*) e troca excessiva de poses de boca (*fluttering*) no modo fonético — comportamento prático em PT-BR **não verificado** em ensaio local.
  - Em inspeção direta da máquina local (`2026-11-18`), o executável `rhubarb` está ausente (`rhubarb not found`).
- **`edge-tts` ([Repositório oficial `rany2/edge-tts`](https://github.com/rany2/edge-tts)) e `Piper` ([Repositório `OHF-Voice/piper1-gpl`](https://github.com/OHF-Voice/piper1-gpl) e [Lista de vozes](https://github.com/OHF-Voice/piper1-gpl/blob/main/docs/VOICES.md)):**
  - No ambiente `.venv` local (`2026-11-18`), está instalada a versão **`edge-tts 7.3.1`**;
  - Resultados de busca web sobre `edge-tts` relatam instabilidades ocasionais em APIs não-oficiais da Microsoft (como erro `HTTP 403` em mudança de handshake WebSocket resultando em arquivos de `0 bytes`, corrigido em atualizações da biblioteca como `7.3.0+`) — incidência específica de cada issue **não verificado** diretamente nos tópicos individuais nesta rodada;
  - **`piper1-gpl`** é documentado como motor TTS neural rápido e local em CPU que utiliza `espeak-ng` para fonetização, listando vozes oficiais para **`Português, Brazil (Portuguese, pt_BR)`** em `docs/VOICES.md`. *(Qualidade perceptiva da voz `pt_BR` no `Piper` — **não verificado** em audição local nesta rodada.)*

### 3. Ambiente local de renderização e ativos no repositório (medição direta em `2026-11-18`)
- **`ffmpeg` e bibliotecas Python no Mac (`Intel Core i7-5557U`, 16 GB RAM, macOS):**
  - `/usr/local/bin/ffmpeg` (**`ffmpeg 9.0.2`**) possui o filtro **`overlay`** e suporte a **`videotoolbox`** e **`libx264`** habilitados; os filtros **`drawtext`**, **`subtitles`** e **`ass`** estão **ausentes** nessa compilação;
  - Na `.venv`, estão instalados **`Python 3.14`**, **`edge-tts 7.3.1`**, **`Pillow 13.0.0`** e **`numpy`**;
  - Os utilitários CLI **`rsvg-convert`**, **`cairosvg`** e **`inkscape`** estão **ausentes** (`not found`) no sistema;
  - Frameworks baseados em navegador como o [Remotion](https://v3.remotion.dev/) renderizam via Chromium *headless* + `ffmpeg` (relatos de busca web sobre *throttling* térmico e sobrecarga de memória com Chromium *headless* em Macs Intel sem GPU dedicada permanecem **não verificado** em benchmark próprio nesta máquina).
- **Ativos do personagem em `assets/personagem/`:** diretório contém apenas `referencia-oficial.jpg` e `conceitos/`, sem pacote fatiado de camadas PNG (boca/visemas, olhos, braços, lupa, lanterna) criado até esta data.

## Inferências

- **Inferência:** Como o consumo de créditos no Google Flow acontece ao gerar o clipe **`Omni 360p`** (e *upscale* até `1080p` para clipes de até `10s` no Pro custa `0` crédito), o orçamento de créditos precisa ser aprovado **no Portão 2** junto ao plano de cenas — e o **Portão 3** deixa de ser um rascunho descartável (herança da fase Blender) para validar áudio, ritmo, legendas e os clipes `360p` definitivos promovíveis a `1080p` sem custo adicional.
- **Inferência:** Substituir `Rhubarb Lip Sync` por um mapeador determinístico PT-BR em Python (grafema→visema guiado pelo texto original, marcas `WordBoundary` do `edge-tts` e amplitude RMS do áudio) elimina uma dependência ausente no sistema e evita distorções do reconhecedor fonético inglês sobre português brasileiro.
- **Inferência:** Sem filtros `drawtext`/`ass` no `ffmpeg` local e sem `rsvg-convert`/`cairosvg` instalados, compor camadas, legendas dinâmicas, diagramas e o Rig 2.5D em **Python (`Pillow`/`numpy`) + `ffmpeg` (`overlay`/`videotoolbox`)** executa diretamente com o ambiente já instalado no Mac Intel, evitando a sobrecarga de Chromium *headless* do Remotion.
- **Inferência:** Checar deterministicamente `tamanho > 0 bytes` e presença de `WordBoundary` logo após chamar o `edge-tts`, mantendo **`Piper pt_BR`** em CPU como plano B offline, garante resiliência caso o serviço não-oficial da Microsoft sofra nova alteração de protocolo.
- **Inferência:** Extrair uma única vez as camadas PNG do Rig 2.5D a partir de `assets/personagem/referencia-oficial.jpg` é pré-requisito estrutural único antes de rodar o fluxo produtivo dos Portões 3 e 4 para qualquer produto.
