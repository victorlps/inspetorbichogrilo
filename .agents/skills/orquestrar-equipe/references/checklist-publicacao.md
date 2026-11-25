# Checklist Repetível de Publicação — Inspetor Bicho Grilo

Guia operacional padrão para fechar o **Portão 3**, atualizar a **vitrine na bio** e publicar cada novo episódio nas plataformas.

---

## 1. Revisão Única de Perfis (Validar Antes do 1º Upload ou ao Abrir Nova Conta)

- **Identidade dedicada da marca (`REQ-011`):** utilizar exclusivamente nome, handle, avatar e e-mail/canal oficiais do projeto na bio e descrições públicas.
- **Nome:** `Inspetor Bicho Grilo` | **Handle:** `@inspetorbichogrilo`
- **Foto de perfil (`1:1`):** usar [avatar-perfil-1024.png](../../../../assets/personagem/avatar-perfil-1024.png).
- **Bio padrão:**
  > Como as coisas funcionam por dentro 🔍⚙️
  > Exemplares auditados por código na vitrine 👇
- **Link na bio:** URL pública da vitrine no GitHub Pages (`https://<usuario>.github.io/<repo>/`).
- **Configurações por plataforma:**
  1. **Instagram:** Conta Profissional (*Criador de Conteúdo* ou *Empresa*) vinculada a uma **Página do Facebook** dedicada (habilita automação gratuita de comentários→DM e publicação de Reels via Meta Business Suite / Graph API). *Nota:* o campo de link na bio é editado pelo app mobile (verificado em `2026-11-23`).
  2. **TikTok:** Conta *Criador/Pessoal* para acesso integral à biblioteca de áudio e distribuição orgânica.
  3. **YouTube:** Canal verificado em **Recursos Intermediários/Avançados** (habilita links clicáveis, fixação de comentários em Shorts e publicação direta).
  4. **Mercado Livre:** Cadastro ativo no **Programa de Afiliados (CPF)** e perfil **Mercado Livre Clips** configurado com o avatar e nome da marca.

---

## 2. Fechamento Técnico do Portão 3 (Por Episódio)

1. **Áudio comercial em cadência natural (`REQ-006`):** `@Steve` verifica a presença do `.env` via `test -f` e renderiza `video_final_1080p.mp4` com `--tts-engine azure` (ou `Piper pt_BR`) respeitando a duração orgânica do episódio.
2. **Corte derivado opcional para Mercado Livre Clips:** quando o usuário desejar publicar também no Mercado Livre Clips (que opera com teto próprio de `60s` e ativos determinísticos/reais), `@Steve` gera sob demanda o corte enxuto dedicado (`--ml-clips`), mantendo `video_final_1080p.mp4` livre de qualquer amarra de tempo para Reels, TikTok e YouTube Shorts.
3. **Validação determinística:** `@Mike` executa a checagem local de conformidade:
   ```bash
   python3 src/video/validate_gates.py produtos/<slug> --portao 3
   ```
4. **Parecer, Espectador frio (`REQ-014`) e Aceite no chat:** `@Curador` registra o parecer final de fidelidade científica e física; `@Mike` aciona um **Espectador frio** em instância limpa sobre `video_final_1080p.mp4` e obtém o aceite explícito do usuário no chat antes de ativar o card na vitrine (`REQ-008`).

---

## 3. Automação de Links de Afiliado, Vitrine e Publicação Multiplataforma (`REQ-007` a `REQ-010`)

- **Setup único das 5 sessões no perfil persistente (`YouTube`, `Meta`, `TikTok`, `Mercado Livre Afiliados` e `Amazon Associados`):**
  ```bash
  PYTHONPATH=. .venv/bin/python src/publish/playwright_publish.py --login
  ```
- **Fluxo autônomo pós-aceite em comando único (`src/publish/publish_all.py`):**
  1. `@Mike` ativa o card em `vitrine/catalogo.json` com `"ativo": true`, código sequencial (`IBG-001`, `IBG-002`...) e URLs verificadas de `ficha.md`, mantendo nos textos públicos de `pacote.md` o endereço permanente da vitrine (`https://<usuario>.github.io/<repo>/?c=IBG-XXX`, conforme `REQ-008` e `REQ-009`).
  2. `@Mike` executa o orquestrador ponta a ponta:
     ```bash
     PYTHONPATH=. .venv/bin/python src/publish/publish_all.py --product-dir produtos/<slug> --platform all
     ```
     O orquestrador valida deterministicamente o Portão 3 (incluindo integridade de links em `pacote.md`), aciona `src/publish/affiliate_links.py` no perfil Playwright para converter URLs canônicas em links curtos (`https://meli.la/...` e `https://amzn.to/...`) quando a sessão de afiliado está autenticada, realiza `git push` incremental para publicar a vitrine via `.github/workflows/deploy-vitrine.yml`, confirma `IBG-XXX` online no GitHub Pages e envia o vídeo para **YouTube Shorts**, **Instagram Reels** e **TikTok** aplicando automaticamente a marcação `REQ-007`.
  3. Quando uma sessão de afiliado for renovada posteriormente no perfil, basta rodar `src/publish/affiliate_links.py --code IBG-XXX` e `git push` para atualizar `vitrine/catalogo.json` preservando intacta a URL já publicada nos vídeos (`REQ-009`).

| Plataforma | Arquivo de Vídeo | Rótulo de IA (`REQ-007`) | Automação / Ação Pós-Upload |
|---|---|---|---|
| **Instagram Reels** | `video_final_1080p.mp4` (duração orgânica) | **Ativado pelo publicador** (quando houver `flow_ia`) | Legenda de `pacote.md` (`2.1`) enviada via Meta Business Suite e palavra-chave de DM registrada na `§ 3`. |
| **TikTok** | `video_final_1080p.mp4` (duração orgânica) | **Ativado pelo publicador** ("Conteúdo gerado por IA" quando houver `flow_ia`) | Legenda + hashtags de `pacote.md` (`2.2` + `2.5`) com o código `IBG-XXX`. |
| **YouTube Shorts** | `video_final_1080p.mp4` (duração orgânica; YouTube Shorts suporta até `3 min` conforme [anúncio oficial do YouTube](https://blog.youtube/news-and-events/tall-updates-coming-to-shorts/), verificado em `2026-11-24`) | **Marcado pelo publicador** (`VIDEO_CONTAINS_SYNTHETIC_MEDIA_YES`) | Título/descrição de `pacote.md` (`2.3`) com link clicável da vitrine `?c=IBG-XXX`. |
| **Mercado Livre Clips** *(opcional sob demanda)* | `video_final_ml_clips_1080p.mp4` (corte dedicado `≤ 60s`) | Corte 100% determinístico/real | Enviar pelo app mobile (afiliados) ou Vídeo Studio quando desejado, vinculando os anúncios oficiais. |

---

## 4. Encerramento e Retro (`REQ-013`)

Após publicar, `@Mike` conduz a retro curta com a equipe (`@Curador`, `@Carlos`, `@Steve`), classifica os aprendizados em formato (`biblia.md`), ofício (skills/agentes) ou insumo, e submete o diff consolidado ao `@Revisor-Skills` antes do commit isolado no Git.

---

## 5. Padrões Técnicos Operacionais Consolidados (`IBG-001` e `IBG-002`)

- **Legendas dinâmicas e cadência Azure AI Speech (`src/video/web_engine/tts_audio.py`):** anexar `?`, `!` e `,` emitidos isoladamente em `WordBoundary` à palavra anterior, quebrar batidas nas fronteiras de frase (incluindo ponto e vírgula), ocultar o contêiner de legenda durante pausas respiratórias e espaçar chamadas consecutivas (`0.45s` com retentativa progressiva `1.8s × tentativa`) para operar dentro da cota gratuita `Azure F0`.
- **Mercado Livre Linkbuilder e Amazon SiteStripe (`src/publish/affiliate_links.py`):** sondar a sessão em modo `--headless=new` com `User-Agent` padrão de Chrome desktop para compatibilidade com o filtro CloudFront; caso alguma sessão exija login único inicial, abrir uma janela visível com abas independentes para Mercado Livre e Amazon preservando cada aba aberta até a autenticação. No Linkbuilder (`/afiliados/linkbuilder`), preencher especificamente `textarea#url-0` via `insert_text` puro (preservando todos os dígitos do identificador `MLB`/`MLBU`) para habilitar o botão Andes `Gerar`, mantendo em `vitrine/catalogo.json` exclusivamente variações com estoque elegível convertidas em `https://meli.la/...` ou `https://amzn.to/...`.
- **YouTube Studio (`src/publish/playwright_publish.py`):** converter colchetes angulares (`<` e `>` → `‹` e `›`) no título (`≤ 100` caracteres com `#shorts`) e na descrição para manter o botão `Avançar` habilitado na etapa `Detalhes`, dispensar eventual modal inicial (`Continuar`), validar o `channel_id` da marca (`UCgIp02Q0H3rXsNwL-kDdFbA`) e aguardar a conclusão integral do envio antes do fechamento da aba.
- **Meta Business Suite / Instagram Reels (`src/publish/playwright_publish.py`):** iniciar o Reels Composer a partir de `/latest/home?asset_id=<PAGE_ID>&business_id=<BUSINESS_ID>` acionando `get_by_text("Criar reel", exact=True)` após hidratação da página (com recarga automática se o composer abrir em branco), anexar o arquivo pelo seletor exato `get_by_text("Adicionar vídeo", exact=True)` com `expect_file_chooser`, preencher a legenda no editor Lexical com `insert_text`, confirmar a opção `Público` e acionar os textos exatos finais `get_by_text("Avançar", exact=True).last` e `get_by_text("Compartilhar", exact=True).last` após a liberação de direitos autorais.
- **TikTok Studio (`src/publish/playwright_publish.py`):** ativar o seletor `Conteúdo gerado por IA` (`REQ-007`), definir explicitamente a visibilidade `Everyone` / `Todos`, aguardar a confirmação de envio (`/content` ou `Publicado`, até `30s` no script) e conferir a liberação da análise inicial de conteúdo na listagem do TikTok Studio.
- **Git e GitHub Pages (`src/publish/publish_all.py` e `.github/workflows/deploy-vitrine.yml`):** manter commits binários enxutos (`≤ 20 MiB` com `libx264 -crf 22`), enviar commits incrementalmente com `git -c http.version=HTTP/1.1 push` para completar cada transferência dentro da janela de conexão HTTPS do GitHub e estruturar o workflow do GitHub Pages em dois jobs encadeados (`build` com `upload-pages-artifact@v4` e `deploy` com `needs: build` e `deploy-pages@v4`).
