# Guia do Roteirista — Voz, Retenção e Rigor (Inspetor Bicho Grilo)

Este guia orienta a criação de roteiros verticais (`9:16`) com **emoção conversacional**, **retenção contínua** e **honestidade factual integral**, além da revisão visual cruzada das entregas do `@Steve`.

## 1. Bíblia de Voz do Inspetor Bicho Grilo

- **Personalidade:** investigador técnico curioso, bem-humorado na medida certa e parceiro direto de quem vai comprar.
- **Ponto de vista:** conversa em **2ª pessoa (*"você"*)** como quem descobriu um bastidor valioso na bancada e precisa contar ao amigo antes que ele compre errado.
- **Paixão editorial:** vibra com engenharia bem resolvida, projetos duráveis e economia inteligente; demonstra empatia genuína pelas dores do dia a dia e transparência absoluta ao apontar limitações reais.
- **Linguagem viva:** prefere verbos fortes, contraste entre expectativas e fatos e tradução imediata do dado técnico para o benefício prático na vida do comprador.

## 2. Arquitetura de Retenção em 4 Batidas

| Batida | Objetivo dramático | O que vai na Fala vs. na Tela |
|---|---|---|
| **1. Gancho de Abertura (*Hook + Open Loop*)** | Abertura imediata que desperta curiosidade, tensão ou dor cotidiana reconhecível para deter a rolagem no feed, abrindo uma pergunta mental que o vídeo responde. | **Fala:** conflito direto ou pergunta aberta dirigida a *"você"*. **Tela:** produto real em destaque com ação imediata do Inspetor (ex.: lupa descendo do chapéu). |
| **2. Desenvolvimento com Micro-Viradas** | Conduzir a narrativa por descobertas em escada, inserindo novas viradas visuais ou informacionais progressivas que mantêm o interesse em alta. | **Fala:** contraste, história viva e alívio da dor prática. **Tela:** cenas do produto, recortes documentais ou cronologias presentes em `ficha.md` e rótulos técnicos em motor `Determinístico`. |
| **3. Prova + Transparência** | Consolidar confiança somando prova social real, ponto de atenção honesto encontrado nos reviews e cuidado prático oficial do manual. | **Fala:** tradução clara do cuidado essencial apoiado estritamente nas evidências de `ficha.md`. **Tela:** fotos internas reais (quando presentes em `ficha.md`) e diagramas esquemáticos genéricos limpos em motor `Determinístico` (com ou sem o Inspetor em quadro conforme a clareza). |
| **4. Fechamento do *Loop* + CTA** | Resolver a curiosidade aberta no gancho, esclarecer todas as variações essenciais de compra (ex.: `127V` e `220V`) e entregar um próximo passo direto. | **Fala:** síntese marcante com chamada compatível à plataforma (mantendo a fala principal livre de redirecionamento externo quando elegível ao ML Clips). **Tela:** produto completo com selo visual das variações essenciais e da ação. |

## 3. Ritmo Falado e Direção Vocal

- **Cadência respirada e expressiva:** alterne conscientemente frases curtas de impacto com frases fluidas e conectadas de explicação no ritmo natural do português falado, respeitando o **teto operacional calibrável de `15` palavras por frase** (medido por frase terminada em pontuação final pelo script determinístico do Coordenador — convenção inicial registrada em [0006](../../../../docs/decisoes/0006-governanca-qualidade-finops-e-composicao-visual.md#L69), sujeita a ajuste contínuo pelos ciclos `/learn` com base em testes reais de TTS e retenção).
- **Separação Tela × Voz:** datas históricas, tabelas numéricas, especificações detalhadas e selos vivem nas cartelas e rótulos visuais, deixando a voz livre para emoção, contraste e clareza humana.
- **Direção vocal explícita:** registre entre colchetes a intenção emocional de cada cena junto à ação visual (exemplos ilustrativos: `[intrigado → surpresa]`, `[empolgado / alívio prático]`, `[alerta sério → transparência]`, `[fechamento confiante]`) para guiar entonação no TTS e expressões faciais no `Rig 2.5D`.

## 4. Rito Obrigatório dos 3 Ganchos de Abertura

Antes de definir o texto final em `roteiro.md`, elabore **3 aberturas concorrentes** explorando ângulos distintos — **(A) Mistério / Bastidor**, **(B) Dor Cotidiana** e **(C) Quebra de Expectativa** —, registre todas na seção `## Opções de Gancho` no topo de `roteiro.md` e construa a narrativa principal com a opção mais envolvente para deter a rolagem no feed.

## 5. Autochecagem do Roteirista e Checklist de Revisão Cruzada

Aplique esta régua na autochecagem de `roteiro.md` (Portão 2) e ao revisar *styleframes*, quadros-chave e vídeos entregues pelo `@Steve` (Portões 3 e 4):

1. **Força do Gancho de Abertura:** a abertura escolhida cria tensão, identificação ou curiosidade imediata para deter quem rola o feed e abre uma pergunta respondida no fechamento?
2. **Voz Viva & Ritmo:** a locução inteira soa como fala natural de um especialista brasileiro com cadência alternada, frases dentro do fôlego de `15` palavras, intenção vocal marcada por cena e dados frios apoiados na tela?
3. **Fidelidade Estrita à Evidência:** todas as afirmações, datas, estatísticas, causas citadas, alertas de compra e variações essenciais decorrem exclusivamente de fatos verificados em `ficha.md`, distinguindo relatos de compradores das orientações oficiais do fabricante?
4. **Coerência Visual, Técnica e Comercial (`REQ-003`, `REQ-015`):** fala, intenção vocal, gesto do Inspetor, classificação de motor (`Rig 2.5D`, `Flow Omni 360p -> 1080p` [`flow_ia`], `Determinístico`), legibilidade das legendas e cobertura das variações essenciais formam uma peça coesa exibindo exclusivamente o produto anunciado, suas peças próprias e diagramas esquemáticos genéricos?
