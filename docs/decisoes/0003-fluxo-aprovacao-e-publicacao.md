---
status: "accepted"
date: 2026-11-17
decision-makers: victor
---

# Fluxo de aprovação em portões e publicação assistida na Fase 1

## Contexto e problema

Em [visao.md](../visao.md), o usuário definiu que atua como revisor de qualidade, decisor e fonte de critério técnico para calibrar a curadoria, cabendo à IA pausar antes de publicar e em decisões estratégicas. O usuário informou nesta sessão, a partir da experiência no projeto anterior (`~/Dev/vendas_online`), que precisará intervir até calibrar a curadoria de produtos e a produção de vídeo, buscando reduzir retrabalho nas etapas mais caras em tokens de IA e tempo de renderização.

Na frente de publicação programática, [automacao-coleta-publicacao-e-dm.md](../pesquisa/automacao-coleta-publicacao-e-dm.md) registrou que a TikTok Content Posting API restringe aplicativos não auditados ao modo privado (`SELF_ONLY`) para até 5 usuários/dia, que a YouTube Data API exige auditoria de conformidade para aumento de cotas acima do padrão e que a Instagram Graph API possui limite móvel de publicações em 24 horas.

## Opções consideradas

1. **Funil de aprovação em 4 portões + publicação manual pelo usuário na Fase 1:** estruturar a produção do menor para o maior custo de recurso — (1) **Ficha de curadoria** (produto, problema real, loja/link principal e ângulo técnico), (2) **Roteiro cronometrado + lista de cenas** (fala exata e indicação visual por trecho), (3) **Áudio TTS + *preview* leve do Blender** (render em baixa resolução/viewport para validar ritmo, dicção e enquadramento), e (4) **Render final `9:16` e pacote de publicação** (arquivo final, legenda, tags e link) — com o usuário realizando o envio manual às plataformas na Fase 1. Se um portão for reprovado, o fluxo retorna apenas à etapa corrente sem executar TTS ou render final; após o usuário considerar calibrados a dicção e o enquadramento do personagem, o Portão 3 torna-se opcional por decisão explícita dele.
2. **Funil compacto em 2 portões (curadoria + roteiro juntos → vídeo final):** reduzir interações intermediárias desde o início, assumindo eventuais re-renderizações completas quando houver ajustes de ritmo ou dicção.
3. **Publicação automática via APIs desde a Fase 1:** configurar aplicativos e passar pelos processos de auditoria (TikTok e YouTube) antes de validar a cadência dos primeiros vídeos.

## Decisão

Opção escolhida: **Opção 1 (Funil de aprovação em 4 portões + publicação manual pelo usuário na Fase 1)**, porque bloqueia erros de curadoria e de roteiro antes da geração de áudio e renderização 3D (reduzindo retrabalho de tokens e tempo de máquina) e evita investir esforço em auditorias de APIs de publicação antes de validar o formato e a cadência dos primeiros vídeos.

### Consequências

- **Bom:** minimiza desperdício de tokens e re-renders em 3D durante a fase de calibração, mantendo controle editorial direto sobre rigor técnico e gancho.
- **Bom:** permite iniciar as publicações imediatamente após o Portão 4 sem bloquear a operação por auditorias de APIs externas.
- **Ruim:** exige intervenção humana em até 4 pontos por vídeo nos primeiros ciclos (reduzindo para 3 quando o usuário dispensar o Portão 3) e envio manual do pacote final às plataformas até que se decida automatizar a publicação em fase posterior.
- **Nota de atualização (2026-11-18):** em [0006-governanca-qualidade-finops-e-composicao-visual.md](0006-governanca-qualidade-finops-e-composicao-visual.md), o papel técnico do Portão 3 (originalmente *preview/viewport* do Blender) foi atualizado para validação de narração TTS verificada, ritmo, legendas e clipes `Omni 360p` já prontos para aumento gratuito de resolução para `1080p` no Portão 4, mantendo o caráter opcional após calibração.
- **Nota de atualização (2026-11-22 e 2026-11-24):** a estrutura de 4 portões foi consolidada em 3 portões por [0008-sala-de-producao-coautoria-e-tres-portoes.md](0008-sala-de-producao-coautoria-e-tres-portoes.md), e a substituição do envio manual pela publicação automatizada híbrida com trava prévia de `100%` de links de afiliado encontra-se formalizada para aceite em [0011-publicacao-hibrida-trava-afiliados-e-midia-fora-do-git.md](0011-publicacao-hibrida-trava-afiliados-e-midia-fora-do-git.md).
