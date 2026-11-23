# Checklist Repetível de Publicação — Inspetor Bicho Grilo

Guia operacional padrão para fechar o **Portão 3**, atualizar a **vitrine na bio** e publicar cada novo vídeo nas 4 plataformas.

---

## 1. Revisão Única de Perfis (Validar Antes do 1º Upload ou ao Abrir Nova Conta)

- **Identidade *dark* (`REQ-011`):** nunca expor nome pessoal, telefone pessoal ou e-mail pessoal na bio ou descrição pública.
- **Nome:** `Inspetor Bicho Grilo` | **Handle:** `@inspetorbichogrilo`
- **Foto de perfil (`1:1`):** usar [avatar-perfil-1024.png](../../../../assets/personagem/avatar-perfil-1024.png).
- **Bio padrão:**
  > Raio-X técnico de produtos reais sem enrolação 🔍⚙️
  > Links verificados por código na vitrine 👇
- **Link na bio:** URL pública da vitrine no GitHub Pages (`https://<usuario>.github.io/<repo>/`).
- **Configurações por plataforma:**
  1. **Instagram:** Conta Profissional (*Criador de Conteúdo* ou *Empresa*) vinculada a uma **Página do Facebook** dedicada (necessário para automação de comentários→DM gratuita no Meta Business Suite).
  2. **TikTok:** Conta *Criador/Pessoal* (evita bloqueio de áudios e facilita alcance orgânico inicial).
  3. **YouTube:** Canal verificado em **Recursos Intermediários/Avançados** (libera links clicáveis e comentários fixados em Shorts).
  4. **Mercado Livre:** Cadastro ativo no **Programa de Afiliados (CPF)** e perfil **Mercado Livre Clips** configurado com o mesmo avatar/nome.

---

## 2. Fechamento Técnico do Portão 3 (Por Produto)

1. **Áudio comercial (`REQ-006`):** garantir `AZURE_SPEECH_KEY` e `AZURE_SPEECH_REGION` configurados no `.env` (sem ler ou imprimir no terminal) e renderizar o vídeo final com `--tts-engine azure`.
2. **Variante Mercado Livre Clips:** se o roteiro usar cena `flow_ia`, gerar também a variante limpa sem IA generativa:
   ```bash
   PYTHONPATH=. .venv/bin/python src/video/render_zagonel.py --mode final --skip-tts --ml-clips
   ```
3. **Validação determinística:**
   ```bash
   python3 src/video/validate_gates.py produtos/<slug> --portao 3
   ```
4. **Espectador frio (`REQ-014`) + Aceite no chat:** rodar subagente limpo sobre `video_final_1080p.mp4` e obter o aceite explícito do usuário no chat antes de ativar o produto na vitrine (`REQ-008`).

---

## 3. Links Curtos de Afiliado & Atualização da Vitrine (`REQ-008`, `REQ-009`)

1. Logado na conta de afiliado (**Mercado Livre Afiliados** / **Amazon Associados**), gerar o(s) link(s) curto(s) (`/sec/...`) de cada variação essencial (ex.: `127V` e `220V`).
2. Atualizar os links em `produtos/<slug>/pacote.md`.
3. Adicionar ou ativar o card em `vitrine/catalogo.json` com `"ativo": true` e código curto sequencial (`IBG-001`, `IBG-002`...).
4. Validar localmente antes do push:
   ```bash
   python3 -m json.tool vitrine/catalogo.json > /dev/null
   python3 -m http.server -d vitrine 8080
   ```
5. Fazer `git push` — o workflow `.github/workflows/deploy-vitrine.yml` publica a vitrine automaticamente no GitHub Pages.

---

## 4. Upload Assistido por Plataforma (`REQ-007`, `REQ-010`)

| Plataforma | Arquivo de Vídeo | Rótulo de IA (`REQ-007`) | Ação Obrigatória Pós-Upload |
|---|---|---|---|
| **Instagram Reels** | `video_final_1080p.mp4` | **Ativar** (se houver cena `flow_ia`) | Colar legenda de `pacote.md` (`2.1`) e ativar automação de DM no Meta Business Suite para a palavra-chave (ex.: `ZAGONEL`). |
| **TikTok** | `video_final_1080p.mp4` | **Ativar obrigatoriamente** ("Conteúdo gerado por IA") | Colar legenda de `pacote.md` (`2.2`) com o código `IBG-XXX`. |
| **YouTube Shorts** | `video_final_1080p.mp4` | **Marcar** conteúdo alterado/sintético (se houver `flow_ia`) | Colar título/descrição de `pacote.md` (`2.3`) e **fixar comentário** com os links curtos por variação. |
| **Mercado Livre Clips** | `video_final_ml_clips_1080p.mp4` | Não aplicável (versão sem `flow_ia`) | Vincular os anúncios oficiais do catálogo correspondentes ao produto. |

---

## 5. Encerramento e Retro (`REQ-013`)

Após publicar, conduzir a retro curta com `@Mike` e `@Revisor-Skills` para registrar eventuais ajustes na bíblia ou nas skills e commitar o ciclo do produto no Git.
