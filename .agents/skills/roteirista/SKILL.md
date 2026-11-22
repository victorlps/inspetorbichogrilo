---
name: roteirista
description: >-
  Como estruturar a camada narrativa de roteiro.md (3 ganchos de abertura, fala cronometrada,
  intenção vocal, dicionário fonético TTS, elegibilidade ML Clips) e os textos editoriais de
  pacote.md em coautoria com Steve e Curador na sala de produção.
---

# Roteirista e Retenção (Camada Narrativa e `pacote.md`)

Fluxo editorial derivado de [0008-sala-de-producao-coautoria-e-tres-portoes.md](../../../docs/decisoes/0008-sala-de-producao-coautoria-e-tres-portoes.md), [fase-1.md](../../../docs/requisitos/fase-1.md) (`REQ-003`, `REQ-004`, `REQ-006`, `REQ-010`, `REQ-014`) e da fonte única [.agents/formato/biblia.md](../../formato/biblia.md).

## 1. Coautoria da camada narrativa (`roteiro.md`, Portão 2)

- Leia `produtos/<slug>/ficha.md` e [.agents/formato/biblia.md](../../formato/biblia.md) (além de [references/guia-roteirista.md](references/guia-roteirista.md)).
- Na **sala de produção (Swarm enxuto)**, alinhe com `@Steve` (dono da decupagem visual e motores) e `@Curador` (guardião factual) o arco de cada cena antes de fechar o texto, mantendo foco exclusivo na sua camada:
  1. **Cabeçalho narrativo e elegibilidade ML Clips:** produto, variações essenciais cobertas, duração falada estimada, elegibilidade ao Mercado Livre Clips (fala isenta de preço variável e de redirecionamento externo direto na fala principal) e palavra-chave de DM (`REQ-010`).
  2. **`## Opções de Gancho (0–3s)`:** 3 aberturas concorrentes por ângulos distintos — (A) Dor Cotidiana, (B) Mistério / Bastidor e (C) Quebra de Expectativa — indicando a adotada e sua costura direta com o benefício principal.
  3. **Coluna narrativa do `## 1. Mapa de Cenas`:** tempo contínuo iniciado em `00s`, **Intenção Vocal** entre colchetes e **Fala Exata (Narração PT-BR)** respeitando o teto de palavras por frase da bíblia (inclusive na forma expandida) e traduzindo termos técnicos por analogias cotidianas claras ao público leigo. A descrição visual detalhada, o HUD, os motores e o orçamento Flow pertencem à camada do `@Steve` na mesma tabela.
  4. **`## 2. Dicionário Fonético de TTS`:** mapeamento completo de siglas, marcas estrangeiras e unidades técnicas para pronúncia natural em `pt-BR`.
- Baseie cada afirmação exclusivamente em `ficha.md` (consultando `@Curador` no mural quando surgir dúvida factual) e cubra todas as variações essenciais do produto.

## 2. Textos editoriais de `pacote.md` (Portão 3)

Quando `@Steve` iniciar a montagem de `produtos/<slug>/pacote.md` (`REQ-006`, `REQ-010`), forneça na sala de produção:
- **Legenda adaptável por plataforma** alinhada ao gancho e à dor prática (respeitando regras de link/preço do ML Clips);
- **Palavras-chave / tags** fiéis ao modelo e às variações essenciais;
- **Palavra-chave de DM e resposta automática** para o Meta Business Suite (Instagram Reels), com direcionamento à vitrine na bio como *fallback*.

## 3. Ajustes em sala e retro

- Diante de apontamento do `@Curador`, do relato do **Espectador frio** ou de crítica do usuário, refine a fala, o gancho ou as analogias diretamente na mesma instância em `roteiro.md` ou `pacote.md`.
- Anote lições recorrentes de storytelling ou formato para a retro consolidada ao fim do produto.
