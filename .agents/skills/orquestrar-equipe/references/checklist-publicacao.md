# Checklist Repetível de Publicação — Inspetor Bicho Grilo

Guia operacional padrão para fechar o **Portão 3 ("Pronto para Publicar")**, ativar a **vitrine na bio** com `100%` de links comissionados verificados e publicar cada episódio nas plataformas conforme [0009](../../../../docs/decisoes/0009-vitrine-estatica-e-processo-de-publicacao.md) e [0011](../../../../docs/decisoes/0011-publicacao-hibrida-trava-afiliados-e-midia-fora-do-git.md).

---

## 1. Revisão Única de Perfis e Credenciais (Setup Inicial)

- **Identidade dedicada da marca (`REQ-011`):** utilizar exclusivamente nome, handle, avatar e e-mail/canal oficiais do projeto na bio e descrições públicas (`Inspetor Bicho Grilo` | `@inspetorbichogrilo` | [avatar-perfil-1024.png](../../../../assets/personagem/avatar-perfil-1024.png)).
- **Bio padrão e Link único:**
  > Como as coisas funcionam por dentro 🔍⚙️
  > Exemplares auditados por código na vitrine 👇
  > `https://<usuario>.github.io/<repo>/`
- **Sessões autenticadas e tokens opcionais de API:**
  1. **Perfil persistente Chrome (`YouTube`, `Meta`, `TikTok`, `Mercado Livre Afiliados`, `Amazon Associados`):**
     ```bash
     PYTHONPATH=. .venv/bin/python src/publish/playwright_publish.py --login
     ```
  2. **YouTube Data API v3 (caminho primário HTTP resumível):** tendo `.env.youtube_client_secret.json` na raiz (com tela OAuth publicada no Google Cloud Console para manter o `refresh_token` perene), autenticar uma única vez o canal `UCgIp02Q0H3rXsNwL-kDdFbA`:
     ```bash
     PYTHONPATH=. .venv/bin/python src/publish/youtube_upload.py --auth-only
     ```
  3. **Instagram Graph API (opcional para Reels `≤ 90s` isentos de toggle exclusivo de UI):** configurar `IG_USER_ID` e `IG_ACCESS_TOKEN` no `.env` (`src/publish/meta_graph_upload.py`).

---

## 2. Prontidão Integral Antes do Aceite (`Portão 1` → `Portão 3`)

1. **Portão 1 — Elegibilidade de afiliado verificada na origem:** `@Curador` testa os anúncios candidatos com `src/publish/affiliate_links.py --verify-urls <url1> <url2> ...` (`--headless=new` invisível), selecionando em `ficha.md` anúncios com estoque ativo que geram link comissionado (`https://meli.la/...`, `https://amzn.to/...` ou `?tag=`).
2. **Portão 3 — Áudio comercial, binários locais leves e pré-cadastro da vitrine (`"ativo": false`):**
   - `@Steve` renderiza `video_final_1080p.mp4` com `--tts-engine azure` (`REQ-006`), mantendo os `.mp4` locais fora do versionamento Git (`.gitignore`) para preservar pushes instantâneos na vitrine. Cortes `--ml-clips` (`≤ 60s`) são gerados sob demanda quando solicitados.
   - `@Steve`/`@Mike` pré-cadastra o card `IBG-XXX` em `vitrine/catalogo.json` com `"ativo": false` (`REQ-008`) e roda `src/publish/affiliate_links.py --code IBG-XXX --product-dir produtos/<slug>` convertendo `100%` das variações em links curtos comissionados antes da revisão.
3. **Validação determinística completa (mídia + sintaxe das redes + `100%` links de afiliado):**
   ```bash
   PYTHONPATH=. .venv/bin/python src/video/validate_gates.py produtos/<slug> --portao 1 --portao 2 --portao 3
   ```
   Confirma resolução, área segura, orçamento de palavras em tela, limites e caracteres aceitos em cada rede (`‹`/`›` no lugar de colchetes angulares no YouTube, `#shorts`, código `IBG-XXX` nas legendas) e `100%` de links comissionados em `catalogo.json`.
4. **Parecer do `@Curador`, Espectador frio (`REQ-014`) e Aceite do usuário no chat.**

---

## 3. Publicação Pós-Aceite com Trava de `100%` de Afiliados (`src/publish/publish_all.py`)

Após o `"Sim"` do usuário no Portão 3, `@Mike` executa em comando único:
```bash
PYTHONPATH=. .venv/bin/python src/publish/publish_all.py --product-dir produtos/<slug> --platform all
```

Sequência determinística executada por `publish_all.py`:
1. **Trava local de `100%` de links comissionados:** ativa `"ativo": true` no card `IBG-XXX` e valida que **todas** as variações possuem link curto/parametrizado de afiliado antes de prosseguir.
2. **Deploy instantâneo da vitrine (`~4 KB`):** realiza `git push` leve e consulta `https://<usuario>.github.io/<repo>/catalogo.json` até confirmar o card ativo e `100%` comissionado no ar antes de iniciar o envio de qualquer vídeo.
3. **Despacho híbrido por plataforma (conforme [0011](../../../../docs/decisoes/0011-publicacao-hibrida-trava-afiliados-e-midia-fora-do-git.md)):**

| Plataforma | Caminho Primário | Fallback / Caso de Duração Estendida ou UI | Rótulo de IA (`REQ-007`) |
|---|---|---|---|
| **YouTube Shorts** (`≤ 3 min`) | **YouTube Data API v3** (`youtube_upload.py`, HTTP resumível) quando `.env.youtube_token.json` está presente | `playwright_publish.py` no YouTube Studio | `status.containsSyntheticMedia=True` (API) ou seletor sintético (Studio) |
| **Instagram & Facebook Reels** | **Meta Graph API** (`meta_graph_upload.py`, `rupload.facebook.com`) para episódios `≤ 90s` sem toggle exclusivo de UI | **Meta Business Suite** (`playwright_publish.py`, suporta `> 90s`, postagem simultânea FB+IG e `REQ-007`) | Seletor de IA no composer + transparência na legenda |
| **TikTok** | **TikTok Studio** (`playwright_publish.py` em perfil persistente, público imediato `Everyone`) | TikTok Content Posting API após eventual auditoria formal do App no portal | Chave `"Conteúdo gerado por IA"` acionada pelo publicador |
| **Mercado Livre Clips** *(opcional)* | App mobile (afiliados) ou Vídeo Studio usando variante dedicada `--ml-clips` (`≤ 60s`) | — | Variante 100% determinística/real |

---

## 4. Encerramento e Retro Consolidada (`REQ-013`)

Após confirmar as URLs publicadas (e inspecionar visualmente capturas de tela sempre que o caminho Playwright tiver sido acionado), `@Mike` conduz a retro curta com a equipe, classifica os aprendizados na fonte única correspondente (`biblia.md`, skill/agente ou `docs/`), submete um único diff consolidado ao `@Revisor-Skills` e registra o commit isolado no Git.
