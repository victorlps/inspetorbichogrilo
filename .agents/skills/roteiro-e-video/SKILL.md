---
name: roteiro-e-video
description: Como estruturar roteiro com narrativa de ação (Portão 2), gerar imagens de apoio em resolução econômica e entregar preview.mp4 (Portão 3) e pacote final (Portão 4). Use ao criar ou revisar roteiros, imagens de conceito e vídeos de produtos.
---

# Roteiro e Vídeo (Portões 2 a 4)

Fluxo de produção derivado de [0002-pipeline-personagem-e-video.md](../../../docs/decisoes/0002-pipeline-personagem-e-video.md), [0003-fluxo-aprovacao-e-publicacao.md](../../../docs/decisoes/0003-fluxo-aprovacao-e-publicacao.md), [0004-identidade-visual-personagem.md](../../../docs/decisoes/0004-identidade-visual-personagem.md) e [fase-1.md](../../../docs/requisitos/fase-1.md) (`REQ-003` a `REQ-007`, `REQ-012`).

## 1. Roteiro com narrativa de ação (Portão 2)

- Estruture cada cena em `produtos/<slug>/roteiro.md` com **ação física do personagem Inspetor Bicho Grilo** (lupa articulada descendo do chapéu, lanterna iluminando, expressão de sobrancelha, gestos) e **demonstração visual em movimento sincronizada com a fala** (como vapor crescente, câmara enchendo de água ou comparação visual de componentes).
- Exiba em tela apenas o **produto real anunciado** (`REQ-003`), utilizando recortes de imprensa ou fontes oficiais quando precisar dar prova visual a fatos históricos.
- Registre as falas exatas cronometradas e a indicação de elegibilidade ao Mercado Livre Clips (ausência de preço variável falado e presença de trecho real de uso do produto).
- Incorpore as miniaturas/links das referências visuais diretamente em `roteiro.md` para revisão no *preview* de Markdown e aguarde a aprovação no chat antes de gerar áudio ou renderização (`REQ-004`).

## 2. Geração de imagens por IA (`REQ-012`)

- Solicite a menor resolução útil (`512px` / `0.5K`, ~747 tokens) em provas de conceito, rascunhos e exploração visual.
- Reserve resoluções maiores (`1K+`) exclusivamente para a arte final aprovada.

## 3. *Preview* leve (Portão 3) e Pacote Final (Portão 4)

- Enquanto o Portão 3 estiver ativo, gere a narração em áudio (`edge-tts`) e um único arquivo `preview.mp4` leve em baixa resolução/viewport já com áudio e imagem sincronizados para reprodução direta no player padrão do sistema (`REQ-005`).
- Após a aprovação do *preview* (ou do roteiro, quando o Portão 3 estiver dispensado pelo usuário), execute o render final `9:16` em alta definição no Blender com *lip-sync* offline (`rhubarb`) e composição no `ffmpeg`, entregando o MP4 final sem marca d'água e `pacote.md` com legenda, palavras-chave/tags, código curto da vitrine, link principal de afiliado, palavra-chave de DM (`REQ-010`) e eventuais avisos de marcação de IA (`REQ-006`, `REQ-007`).
- Atualize a vitrine estática na bio somente após a aprovação final do Portão 4 no chat (`REQ-008`).
