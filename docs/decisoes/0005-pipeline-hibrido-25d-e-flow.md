---
status: "accepted"
date: 2026-11-18
decision-makers: victor
---

# Pipeline híbrido de personagem (Rig 2.5D local + Google Flow) em substituição ao render 3D quadro a quadro

## Contexto e problema

A decisão anterior ([0002-pipeline-personagem-e-video.md](0002-pipeline-personagem-e-video.md)) previa modelar e renderizar o personagem 3D integralmente no Blender. Na validação prática com o hardware local (`Intel Core i7-5557U`, 16 GB RAM, `Intel Iris Graphics 6100` — sem GPU NVIDIA nem Apple Silicon) registrada em [personagem-consistente-e-animacao-3d.md](../pesquisa/personagem-consistente-e-animacao-3d.md):

- `BLENDER_EEVEE_NEXT` falhou em modo `--background` por ausência de contexto GPU no macOS headless;
- `CYCLES` em CPU levou **55 segundos por quadro** (`540×720`, 24 amostras), tornando inviável renderizar centenas de quadros de vídeo localmente em CPU;
- Ferramentas neurais locais (*LivePortrait*, *Hunyuan3D*, *MuseTalk*) exigem GPU NVIDIA dedicada.

É necessário redefinir a arquitetura de produção mantendo custo adicional zero, fidelidade à [referencia-oficial.jpg](../../assets/personagem/referencia-oficial.jpg), *lip-sync* preciso e tempo viável de geração, preservando as salvaguardas da decisão anterior contra conteúdo inautêntico no YPP e uso exclusivo de materiais de produto de fontes autorizadas ou da sessão do usuário.

## Opções consideradas

1. **Pipeline híbrido (Rig 2.5D local + Google Flow já pago + *Image-to-3D* apenas para quadros estáticos):**
   - **Cenas faladas e *lip-sync* (Rig 2.5D local):** decompor a [referencia-oficial.jpg](../../assets/personagem/referencia-oficial.jpg) em camadas PNG com fundo transparente (corpo/colete, cabeça, olhos/pálpebras, sobrancelhas independentes, visemas de boca, dois braços, duas antenas, lanterna e lupa) — por recorte/edição única respeitando `REQ-012` em rascunhos — e animar via Python (`Pillow` / HTML5 Canvas) + `ffmpeg` usando os tempos de áudio do `edge-tts` e o *lip-sync* offline do `Rhubarb Lip Sync`.
   - **Cenas de ação e *B-roll* (Google Flow):** utilizar os **1.000 créditos/mês já inclusos no Google AI Pro** apenas para clipes curtos complementares de ação (exibidos mudos sob a narração local ou com o Rig 2.5D sobreposto em PiP), usando **Omni 360p** (~1/3 do custo de 720p) como rascunho no Portão 3 quando aplicável e `Veo 3.1 Lite` / `Omni Flash` (720p/1080p) no Portão 4 *(custo exato por segundo do `Omni Flash` e compatibilidade de `Omni 360p` com *Ingredients to Video* ainda **não verificados** na documentação lida)*.
   - **Poses estáticas extras sob demanda (*Image-to-3D* + Blender):** quando faltar um ângulo específico do personagem, gerar um quadro estático único via *Image-to-3D* + Blender (`CYCLES` CPU em 1 quadro = ~55s) para alimentar o Rig 2.5D ou como imagem de referência, condicionado à verificação prévia de licença comercial limpa (evitando atribuição `CC BY 4.0` incompatível com canal *dark*).
   - **Impacto nos Portões 3 e 4:** no Portão 3 (`preview.mp4`), o Rig 2.5D + `edge-tts` + `rhubarb` valida dicção, sincronia labial e ritmo em baixa resolução sem gastar créditos pesados de vídeo; no Portão 4, gera-se o MP4 `9:16` final em alta definição (incorporando eventual clipe 720p/1080p do Flow).
   - **Mitigação de YPP e origem visual:** cada vídeo mantém análise técnica distinta, narração própria e composição personalizada (não *template* repetitivo em massa), com visuais do produto vindos apenas de fontes autorizadas ou da sessão do usuário.
2. **100% Google Flow:** gerar todas as cenas (inclusive falas) via *Veo 3.1 Lite* / *Omni Flash*, com menor controle quadro a quadro de *lip-sync* em português e risco de esgotar os 1.000 créditos/mês.
3. **100% Rig 2.5D local:** operar apenas com camadas 2.5D no `ffmpeg`/Python, sem aproveitar os créditos já pagos do Google AI Pro para cenas de ação e *B-roll*.

## Decisão

Opção escolhida: **Opção 1 (Pipeline híbrido: Rig 2.5D local + Google Flow + poses estáticas via *Image-to-3D* sob demanda)**, porque elimina o gargalo de 55s/quadro em vídeo no Blender CPU mantendo fidelidade visual à referência aprovada, *lip-sync* preciso em português a custo zero e opção de cenas de ação cinematográficas dentro da cota mensal do Google AI Pro já mantida pelo usuário.

### Consequências

- **Bom:** viabiliza a produção local em CPU Intel sem novas assinaturas pagas e permite validar o `preview.mp4` do Portão 3 rapidamente antes de consumir créditos 720p/1080p no Portão 4.
- **Ruim:** ao ser aceita, esta decisão substitui (`superseded by 0005`) a [0002-pipeline-personagem-e-video.md](0002-pipeline-personagem-e-video.md) e exige atualizar [0004-identidade-visual-personagem.md](0004-identidade-visual-personagem.md) e [fase-1.md](../requisitos/fase-1.md) (`REQ-004`, `REQ-005`, `REQ-006`) para refletir o Rig 2.5D em vez de renderização 3D completa.
- **Ruim:** exige preparar o conjunto de camadas/visemas do personagem e registrar em `pacote.md` (`REQ-007`) o aviso de marcação de IA sempre que houver cenas fotorrealistas geradas no Google Flow ou enquanto a isenção para o mascote estilizado no TikTok não estiver verificada.
