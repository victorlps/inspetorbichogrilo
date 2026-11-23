---
status: "accepted"
date: 2026-11-17
decision-makers: victor
---

# Identidade visual do Inspetor Bicho Grilo: personagem estilizado de trilha com engenhocas no chapéu

## Contexto e problema

Conforme [visao.md](../visao.md) e [0002-pipeline-personagem-e-video.md](0002-pipeline-personagem-e-video.md), o personagem **Inspetor Bicho Grilo** precisa de uma especificação visual única e reutilizável, com *lip-sync* e animação fluida para vídeos verticais (`9:16`).

O usuário definiu que a identidade visual une o caráter **"bicho grilo"** (estética rústica e despojada de trilha/natureza) à referência ao **"Inspetor Bugiganga"** (chapéu de trilha com lanterna e lupa articuladas saindo da copa do chapéu), consolidada em [referencia-oficial.jpg](../../assets/personagem/referencia-oficial.jpg).

## Opções consideradas

1. **Personagem estilizado em meio-corpo ("bicho grilo" de trilha + engenhocas no chapéu):** usar como base estética única [referencia-oficial.jpg](../../assets/personagem/referencia-oficial.jpg), com as seguintes especificações:
   - **Anatomia e *rig* de expressão:** grilo verde antropomórfico estilizado da cintura para cima, com olhos grandes (pálpebras para piscar e controle de direção do olhar), sobrancelhas independentes, boca articulada com visemas para *lip-sync* e dois braços até a cintura com mãos de quatro dedos articuladas para apontar e gesticular.
   - **Vestimenta "bicho grilo":** chapéu de trilha de aba maleável em tom oliva/cáqui com cordão trançado, camisa folgada de linho em tom bege terroso, colete utilitário de lona oliva com bolsos frontais limpos (reservando a lupa e a lanterna exclusivamente para as hastes do chapéu) e pulseira de corda trançada no pulso.
   - **Engenhocas "Inspetor Bugiganga" no chapéu:** duas antenas verdes segmentadas atravessando a frente/topo da copa do chapéu com movimento expressivo, além de uma lanterna compacta e uma lupa redonda saindo das laterais da copa do chapéu por duas hastes metálicas articuladas (recolhidas junto ao chapéu em repouso, podendo estender para frente ou em direção ao olho/produto durante inspeções).
   - **Saída de render:** fundo transparente (canal alfa) para composição sobre as imagens do produto no `ffmpeg`, e fundo sólido `#0f172a` apenas em *previews* isolados do personagem.

## Decisão

Opção escolhida: **Opção 1 (Personagem estilizado em meio-corpo "bicho grilo" de trilha + engenhocas no chapéu)**, porque preserva o carisma e a amplitude de expressão facial necessários para *lip-sync* e gestos em vídeos `9:16` e traduz diretamente os dois traços da marca definidos pelo usuário (trilha/rústico + engenhocas articuladas no chapéu).

### Consequências

- **Bom:** consolida anatomia, vestimenta, engenhocas articuladas, controles faciais e saída com transparência em uma especificação única e alinhada a [referencia-oficial.jpg](../../assets/personagem/referencia-oficial.jpg).
- **Ruim:** a inclusão de braços, mãos articuladas, aba maleável e hastes mecânicas no chapéu aumenta a complexidade inicial do *rig* em relação a um busto estático.
- **Nota de atualização (2026-11-18):** a especificação visual definida nesta decisão permanece vigente, porém a implementação técnica foi adaptada da modelagem 3D no Blender para o **Rig 2.5D em camadas PNG** conforme [0005-pipeline-hibrido-25d-e-flow.md](0005-pipeline-hibrido-25d-e-flow.md) e [0006-governanca-qualidade-finops-e-composicao-visual.md](0006-governanca-qualidade-finops-e-composicao-visual.md).
