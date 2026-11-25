---
status: "proposed"
date: 2026-11-24
decision-makers: victor
---

# Publicação híbrida (API oficial + navegador autenticado), trava de 100% de links de afiliado antes do vídeo e desacoplamento de MP4 do Git

## Contexto e problema

As duas primeiras publicações reais do projeto — `IBG-001` (`ducha-eletronica-zagonel-nd-7700w`) e `IBG-002` (`fruta-liofilizada-davida`) — revelaram quatro lacunas arquiteturais e de governança no fechamento pós-Portão 3:

1. **Automação criada sem decisão arquitetural:** [0003-fluxo-aprovacao-e-publicacao.md](0003-fluxo-aprovacao-e-publicacao.md) previa envio manual na Fase 1 e [0009-vitrine-estatica-e-processo-de-publicacao.md](0009-vitrine-estatica-e-processo-de-publicacao.md) cobriu apenas a vitrine e o TTS, deixando `src/publish/` evoluir por tentativas sobre o DOM das plataformas (`5` commits corretivos na Zagonel e `4` na Fruta Liofilizada).
2. **Publicação de vídeos antes de 100% dos links de afiliado estarem prontos:** como a elegibilidade no Linkbuilder do Mercado Livre não era verificada no Portão 1 e `publish_all.py` prosseguia mesmo com conversões parciais (`3/5`), `IBG-002` subiu inicialmente com `2` URLs canônicas `/p/` sem comissão (`MLB2078372053` e `MLB56338512`), corrigidas somente após o envio aos canais.
3. **Retrabalho pós-aprovação do Portão 3:** `validate_gates.py --portao 3` validava o vídeo e a privacidade, porém deixava passar restrições sintáticas das redes (como `<` literal em `pacote.md`, rejeitado pelo YouTube) e instruções residuais de rascunho.
4. ** Acoplamento de binários `.mp4` (`30–75 MB`) ao repositório Git da vitrine (`4 KB`):** versionar vídeos finais e animatics diretamente na branch `master` causou timeouts `HTTP 408` no proxy HTTPS do GitHub e atrasou a atualização da vitrine estática no GitHub Pages.

Ao mesmo tempo, a pesquisa atualizada em [automacao-coleta-publicacao-e-dm.md](../pesquisa/automacao-coleta-publicacao-e-dm.md) demonstrou que **migrar cegamente 100% para APIs oficiais tem limitações funcionais reais**:
- A **YouTube Data API v3** (`videos.insert`) já permite uploads públicos sem auditoria de conformidade e suporta `containsSyntheticMedia` (`REQ-007`) nativamente;
- A **Instagram Graph API** (`rupload.facebook.com`) funciona em *Development Mode* para contas *Tester*, porém restringe a elegibilidade da aba Reels a **`5s–90s`**, carece de parâmetro documentado para o rótulo nativo *"AI info"* (`REQ-007`) e separa Instagram e Página do Facebook em dois uploads distintos;
- A **TikTok Content Posting API** restringe aplicativos não auditados a **`SELF_ONLY` (privado)** e exige que a própria conta criadora fique privada até concluir auditoria formal;
- O **Mercado Livre Afiliados** opera exclusivamente via Linkbuilder web (`/afiliados/linkbuilder`), sem API pública para gerar links `meli.la`.

## Opções consideradas

### Opção 1: Arquitetura híbrida orientada por capacidade de API + trava determinística de 100% de afiliados nos Portões 1/3 + `.mp4` fora do Git

1. **Validação antecipada e trava inegociável de `100%` de links de afiliado antes de qualquer upload:**
   - No **Portão 1**, `@Curador` verifica a elegibilidade dos anúncios candidatos (`affiliate_links.py --verify-urls` em `--headless=new` invisível), selecionando desde a origem anúncios que geram link comissionado ativo (`meli.la/...`, `amzn.to/...` ou `?tag=`).
   - No **Portão 3**, `@Steve`/`@Mike` registra localmente o card do produto em `vitrine/catalogo.json` com `"ativo": false` (mantendo a vitrine pública no GitHub Pages inalterada antes da aprovação do usuário e filtrada por `ativo === true` em `vitrine/app.js`, em total conformidade com `REQ-008`), já com `100%` das variações convertidas em links curtos de afiliado, e `validate_gates.py --portao 3` valida deterministicamente: (a) `100%` de URLs comissionadas no card, (b) ausência de `<` e `>` no bloco YouTube, limites de caracteres por rede e presença do código `IBG-XXX` nas legendas.
   - Após o aceite do usuário no chat, `publish_all.py` muda `"ativo": false → true`, faz o `git push` leve (`~4 KB`), confirma no ar (`https://victorlps.github.io/inspetorbichogrilo/catalogo.json`) que **100% das variações públicas estão ativas e comissionadas**, e **bloqueia (`exit 2/3`) o envio de vídeos** se houver qualquer link não monetizado.
2. **Despacho híbrido API-First com fallback transparente em perfil autenticado Playwright:**
   - **YouTube Shorts:** usa prioritariamente a **YouTube Data API v3 oficial** (`src/publish/youtube_upload.py`, upload HTTP resumível com `containsSyntheticMedia` e trava de `channel_id`) sempre que `.env.youtube_token.json` estiver presente, mantendo `playwright_publish.py` como fallback imediato.
   - **Instagram / Facebook Reels:** usa a **Instagram Graph API oficial** (`src/publish/meta_graph_upload.py`, protocolo `rupload.facebook.com`) quando `IG_USER_ID` e `IG_ACCESS_TOKEN` estiverem configurados, a duração do episódio for `≤ 90s` e não houver exigência de toggle exclusivo de UI; para episódios orgânicos `> 90s`, postagem cruzada simultânea FB+IG ou `REQ-007` visual, despacha pelo composer endurecido do Meta Business Suite no perfil Playwright.
   - **TikTok e Mercado Livre Linkbuilder:** operam pelo perfil persistente do Chrome (`~/.cache/inspetorbichogrilo-pw-profile`) até eventual auditoria formal de App no TikTok Developers Portal.
3. **Desacoplamento de binários `.mp4` da árvore Git (`.gitignore`):**
   - Ignorar `produtos/*/*.mp4` e `produtos/*/assets/*.mp4` no `.gitignore` para os próximos produtos (`IBG-003+`), mantendo versionados todos os artefatos textuais, especificações determinísticas (`episode_spec.json`), códigos e imagens leves (com arquivamento opcional de vídeos mestre em *GitHub Releases* fora dos packfiles da branch `master`).

#### Viabilidade de custo (FinOps — `REQ-016`)

1. **Inventário de recursos por publicação:**
   - **YouTube Data API v3 (`videos.insert`):** `1` unidade por episódio no *bucket* dedicado de `100` uploads/dia (`~3.000` uploads/mês gratuitos por projeto Google Cloud, `US$ 0,00`).
   - **Instagram Graph API (`rupload.facebook.com`, quando elegível `≤ 90s` sem `REQ-007`) / Meta Business Suite:** até `1` chamada `media_publish` na cota gratuita de `100` publicações/24h (`3.000`/mês no Instagram; `0` consumo de API quando despachado pelo Meta Business Suite local, `US$ 0,00`).
   - **Playwright local (`Linkbuilder ML`, `TikTok Studio` e fallback Meta/YouTube):** execução local em CPU (`~45–120s` por publicação), `0` tokens de LLM e `US$ 0,00`.
   - **GitHub Pages, GitHub Actions (`build` → `deploy`) e *GitHub Releases* opcional:** commit de `~4 KB` em `catalogo.json`, ~`25s` de runner Linux em repositório público (minutos gratuitos ilimitados no GitHub Actions público e anexos gratuitos de até `2 GiB`/arquivo em *Releases*, `US$ 0,00`).
2. **Projeção determinística de escala:**

   | Publicações/mês | Cota YouTube API (`~3.000`/mês grátis) | Cota Meta Graph API (teto `3.000`/mês grátis) | GitHub Actions público (`ilimitado`) & `git push` em `master` | Custo total (`US$`) |
   |---|---|---|---|---|
   | `1` | `0,03%` (`1` un.) | `≤ 0,03%` (`0–1` post) | `0%` de cota paga · `~4 KB` | `US$ 0,00` |
   | `30` | `1,00%` (`30` un.) | `≤ 1,00%` (`0–30` posts) | `0%` de cota paga · `~120 KB` | `US$ 0,00` |
   | `100` | `3,33%` (`100` un.) | `≤ 3,33%` (`0–100` posts) | `0%` de cota paga · `~400 KB` | `US$ 0,00` |
   | `300` | `10,00%` (`300` un.) | `≤ 10,00%` (`0–300` posts) | `0%` de cota paga · `~1,2 MB` | `US$ 0,00` |

   - **Ponto de saturação:** `100` uploads/dia (`~3.000`/mês) na YouTube Data API v3 e `100` Reels/24h na Meta Graph API — `10×` acima do horizonte de `300` execuções/mês a `US$ 0,00`.

### Opção 2: Migração integral imediata para APIs oficiais nas 3 redes

Exigir APIs REST puras para YouTube, Instagram e TikTok já na Fase 1, abandonando o Playwright nas redes sociais. Descartada porque bloquearia vídeos públicos no TikTok até aprovação em auditoria formal (`SELF_ONLY`), imporia teto artificial de `90s` aos episódios educativos na aba Reels da Graph API (contrariando a duração orgânica definida na bíblia) e inviabilizaria a geração automática de `meli.la` no Mercado Livre.

### Opção 3: Manter 100% Playwright UI e versionamento de `.mp4` no Git

Continuar subindo YouTube, Meta e TikTok apenas via cliques no navegador e versionando `.mp4` em `master`. Descartada porque perpetua o risco de `HTTP 408` a cada novo produto, desperdiça `youtube_upload.py` já implementado e mantém exposição desnecessária a mudanças de DOM no YouTube Studio.

## Decisão

Opção escolhida: **Opção 1 (Arquitetura híbrida orientada por capacidade de API + trava determinística de 100% de afiliados nos Portões 1/3 + `.mp4` fora do Git)**, porque resolve na raiz o vazamento de links sem comissão, o retrabalho pós-Portão 3 e os timeouts de `git push`, aproveitando APIs HTTP oficiais gratuitas onde elas têm paridade funcional completa (YouTube Data API v3 e Reels `≤ 90s` elegíveis) sem sacrificar a duração orgânica dos vídeos, a marcação `REQ-007` nem a publicação pública imediata no TikTok e no Linkbuilder do Mercado Livre.

Esta decisão atualiza e substitui, em [0003-fluxo-aprovacao-e-publicacao.md](0003-fluxo-aprovacao-e-publicacao.md), a previsão inicial de envio manual pelo usuário após o último portão.

### Consequências

- **Bom:** garante matematicamente que nenhum vídeo é publicado sem `100%` das variações na vitrine estarem comissionadas e online, reduz o `git push` da vitrine para `< 1s` (`~4 KB`) e zera o retrabalho de sintaxe após o aceite do Portão 3.
- **Bom:** preserva liberdade total de duração orgânica para os vídeos educativos *"Como as coisas funcionam?"* e mantém custo operacional de `US$ 0,00`.
- **Ruim:** para ativar o caminho primário da YouTube Data API v3 sem expiração semanal de token, requer `1` autenticação inicial (`youtube_upload.py --auth-only`) com a tela de consentimento OAuth publicada no Google Cloud Console; e os arquivos `.mp4` passam a residir localmente (ou em *GitHub Releases*), fora do clone `git` padrão.
