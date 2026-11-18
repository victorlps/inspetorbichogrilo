---
status: "accepted"
date: 2026-11-17
decision-makers: victor
---

# Pipeline de personagem 3D e produção de vídeo na Fase 1

## Contexto e problema

Conforme [visao.md](../visao.md), o personagem **Inspetor Bicho Grilo** precisa manter consistência visual em alta definição, animação fluida (incluindo avaliação de técnicas 3D) e operação com custo inicial mínimo usando ferramentas gratuitas/locais e assinaturas já mantidas pelo usuário (como o Google AI Pro).

As regras de monetização e transparência registradas em [regras-originalidade-e-monetizacao-dark.md](../pesquisa/regras-originalidade-e-monetizacao-dark.md) apontam que:

- O YouTube **não permite monetizar no YPP** produção em massa com *templates* repetitivos sem aporte humano original ("conteúdo inautêntico"), mas permite séries e *reviews* quando cada vídeo traz análise distinta.
- O YouTube exige marcação de conteúdo alterado/sintético apenas para mídia **realista**, isentando animações estilizadas claramente não realistas; o TikTok exige marcação para mídia realista (incluindo detecção via C2PA) e isenta edições rotineiras e assistência de roteiro, restando verificar diretamente nos termos do TikTok a abrangência exata sobre mascotes 3D estilizados.

A pesquisa em [personagem-consistente-e-animacao-3d.md](../pesquisa/personagem-consistente-e-animacao-3d.md) levantou plataformas pagas por créditos mensais (HeyGen a partir de US$ 24–29/mês; Google Flow com 1.000 créditos/mês inclusos no Google AI Pro) frente a um *rig* 3D local no Blender (licença GNU GPL, gratuito para uso comercial).

## Opções consideradas

1. **Pipeline local com personagem 3D no Blender + apoio pontual do Google AI Pro:** criar (por modelagem/rigging inicial dedicado antes da produção em série) um personagem 3D estilizado reutilizável no Blender e executar a produção na ordem: (a) gerar o áudio da narração em TTS gratuito/local (como `edge-tts` já usado no projeto anterior ou alternativa offline a definir na implementação), (b) gerar *lip-sync* offline no Blender a partir do áudio (`auto-lip-sync` ou `blender-rhubarb-lipsync`, a escolher na configuração do *rig*), (c) renderizar o personagem no Blender e (d) compor o vídeo vertical `9:16` no `ffmpeg` combinando o personagem com material visual do produto (obtido em fontes autorizadas/sessão do usuário, dado que a coleta automatizada tem termos **não verificado** em [automacao-coleta-publicacao-e-dm.md](../pesquisa/automacao-coleta-publicacao-e-dm.md)) e eventual *B-roll* pontual gerado nos 1.000 créditos/mês do Google AI Pro.
2. **Pipeline generativo via Google Flow (`Veo 3.1 Lite`):** gerar clipes do personagem diretamente pelos créditos inclusos no Google AI Pro (10 créditos por clipe de 4–8s), sem construir *rig* 3D no Blender.
3. **Avatar 2D simples por camadas + `ffmpeg`:** iniciar com poses 2D estáticas/trocadas e deixar a modelagem 3D no Blender para uma etapa posterior.

## Decisão

Opção escolhida: **Opção 1 (Pipeline local com personagem 3D no Blender + apoio pontual do Google AI Pro)**, porque um *rig* 3D reutilizável garante consistência visual do personagem entre vídeos com custo marginal zero por minuto produzido, atende ao padrão de animação fluida da visão e reduz o risco de enquadramento como conteúdo repetitivo de *template* 2D no YPP. O Google AI Pro já pago pelo usuário permanece como recurso complementar sem gerar nova despesa fixa.

### Consequências

- **Bom:** custo marginal zero por vídeo renderizado localmente, controle total sobre enquadramento, expressões e consistência do personagem, e isenção de marcação de IA realista no YouTube para a animação estilizada do mascote.
- **Ruim:** exige esforço inicial único para modelar/riggar o personagem no Blender e escolher entre `auto-lip-sync` e `blender-rhubarb-lipsync` antes de ganhar velocidade na produção em série.
- **Ruim:** caso sejam inseridos cenários ou *B-roll* fotorrealistas gerados no Google Flow, esses trechos ficam sujeitos às regras de marcação de conteúdo sintético realista das plataformas.
