# Checklist Repetível de Publicação — Inspetor Bicho Grilo

Guia operacional padrão para fechar o **Portão 3**, atualizar a **vitrine na bio** e publicar cada novo vídeo nas plataformas.

---

## 1. Revisão Única de Perfis (Validar Antes do 1º Upload ou ao Abrir Nova Conta)

- **Identidade *dark* (`REQ-011`):** usar exclusivamente nome, handle, avatar e e-mail/canal dedicados do projeto na bio e descrições públicas.
- **Nome:** `Inspetor Bicho Grilo` | **Handle:** `@inspetorbichogrilo`
- **Foto de perfil (`1:1`):** usar [avatar-perfil-1024.png](../../../../assets/personagem/avatar-perfil-1024.png).
- **Bio padrão:**
  > Raio-X técnico de produtos reais sem enrolação 🔍⚙️
  > Links verificados por código na vitrine 👇
- **Link na bio:** URL pública da vitrine no GitHub Pages (`https://<usuario>.github.io/<repo>/`).
- **Configurações por plataforma:**
  1. **Instagram:** Conta Profissional (*Criador de Conteúdo* ou *Empresa*) vinculada a uma **Página do Facebook** dedicada (necessário para automação de comentários→DM gratuita e publicação de Reels via Meta Business Suite / Graph API). *Nota:* o campo de link na bio requer edição pelo app mobile (Instagram Web manteve o campo bloqueado mesmo com emulação mobile; verificado em `2026-11-23`).
  2. **TikTok:** Conta *Criador/Pessoal* (evita bloqueio de áudios e facilita alcance orgânico inicial).
  3. **YouTube:** Canal verificado em **Recursos Intermediários/Avançados** (libera links clicáveis, fixação de comentários em Shorts e publicação direta).
  4. **Mercado Livre:** Cadastro ativo no **Programa de Afiliados (CPF)** e perfil **Mercado Livre Clips** configurado com o mesmo avatar e nome da marca.

---

## 2. Fechamento Técnico do Portão 3 (Por Produto)

1. **Áudio comercial (`REQ-006`):** `@Steve` garante `AZURE_SPEECH_KEY` e `AZURE_SPEECH_REGION` configurados no `.env` (sem ler ou imprimir no terminal) e renderiza o vídeo final com `--tts-engine azure` (ou fallback offline `Piper pt_BR`).
2. **Variante Mercado Livre Clips:** se o roteiro usar cena `flow_ia`, `@Steve` gera também a variante determinística sem IA generativa (`≤ 60s`):
   ```bash
   PYTHONPATH=. .venv/bin/python src/video/<render_produto>.py --mode final --skip-tts --ml-clips
   ```
   *(Exemplo no produto-piloto: `src/video/render_zagonel.py`.)*
3. **Validação determinística:** `@Mike` executa a checagem local de conformidade:
   ```bash
   python3 src/video/validate_gates.py produtos/<slug> --portao 3
   ```
4. **Parecer, Espectador frio (`REQ-014`) e Aceite no chat:** `@Curador` registra o parecer final de fidelidade; `@Mike` aciona um **Espectador frio** em instância limpa sobre `video_final_1080p.mp4` e obtém o aceite explícito do usuário no chat antes de ativar o produto na vitrine (`REQ-008`).

---

## 3. Links Curtos de Afiliado & Atualização da Vitrine (`REQ-008`, `REQ-009`)

1. Logado na conta de afiliado, o usuário gera o(s) link(s) curto(s) de cada variação essencial (`https://meli.la/...` ou `/sec/...` no **Mercado Livre Afiliados**, e formato equivalente no **Amazon Associados**).
2. `@Mike` atualiza os links em `produtos/<slug>/pacote.md` e ativa o card em `vitrine/catalogo.json` com `"ativo": true` e código curto sequencial (`IBG-001`, `IBG-002`...).
3. Validar localmente antes do push:
   ```bash
   python3 -m json.tool vitrine/catalogo.json > /dev/null
   python3 -m http.server -d vitrine 8080
   ```
4. Executar `git push` — o workflow `.github/workflows/deploy-vitrine.yml` publica a vitrine automaticamente no GitHub Pages.

---

## 4. Upload Automatizado (Playwright Local) / Assistido por Plataforma (`REQ-007`, `REQ-010`)

- **Setup único de sessão persistente:**
  ```bash
  PYTHONPATH=. .venv/bin/python src/publish/playwright_publish.py --login
  ```
- **Envio automático (YouTube + Instagram/Meta + TikTok) lendo `pacote.md`:**
  ```bash
  PYTHONPATH=. .venv/bin/python src/publish/playwright_publish.py --product-dir produtos/<slug> --platform all --publish --no-wait
  ```

| Plataforma | Arquivo de Vídeo | Rótulo de IA (`REQ-007`) | Ação Obrigatória Pós-Upload |
|---|---|---|---|
| **Instagram Reels** | `video_final_1080p.mp4` | **Ativar** (se houver cena `flow_ia`) | Legenda de `pacote.md` (`2.1`) e ativar automação de DM no Meta Business Suite para a palavra-chave do produto. |
| **TikTok** | `video_final_1080p.mp4` | **Ativar obrigatoriamente** ("Conteúdo gerado por IA") | Legenda de `pacote.md` (`2.2`) com o código `IBG-XXX`. |
| **YouTube Shorts** | `video_final_1080p.mp4` | **Marcar** conteúdo alterado/sintético (se houver `flow_ia`) | Título/descrição de `pacote.md` (`2.3`) e **fixar comentário** com os links curtos por variação. |
| **Mercado Livre Clips** | `video_final_ml_clips_1080p.mp4` (`≤ 60s`) | Não aplicável (versão sem `flow_ia`) | Enviar pelo app mobile (afiliados) ou Vídeo Studio (vendedores), vinculando os anúncios oficiais do catálogo. |

---

## 5. Encerramento e Retro (`REQ-013`)

Após publicar, `@Mike` conduz a retro curta com a sala (`@Curador`, `@Carlos`, `@Steve`), classifica os aprendizados em formato (`biblia.md`), ofício (skills/agentes) ou insumo, e submete o diff consolidado ao `@Revisor-Skills` antes do commit isolado no Git.
