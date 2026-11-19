---
status: "accepted"
date: 2026-11-17
decision-makers: victor
---

# Identidade visual do Inspetor Bicho Grilo: animação 3D estilizada de trilha com engenhocas no chapéu

## Contexto e problema

Conforme [visao.md](../visao.md) e [0002-pipeline-personagem-e-video.md](0002-pipeline-personagem-e-video.md), o personagem **Inspetor Bicho Grilo** será produzido como um modelo 3D estilizado reutilizável no Blender, com *lip-sync* offline e animação fluida.

Para orientar a modelagem 3D antes da criação do arquivo-mestre no Blender, foram avaliados três conceitos visuais em `assets/personagem/conceitos/`:

- [conceito-1-animacao.jpg](../../assets/personagem/conceitos/conceito-1-animacao.jpg): grilo verde estilizado em meio-corpo de animação 3D, chapéu de explorador com lanterna, colete oliva com lupa no bolso e rosto expressivo.
- [conceito-2-toy-art.jpg](../../assets/personagem/conceitos/conceito-2-toy-art.jpg): corpo inteiro em estilo *toy-art* geométrico/vinil.
- [conceito-3-tecnico-campo.jpg](../../assets/personagem/conceitos/conceito-3-tecnico-campo.jpg): meio-corpo com boné, lupa de relojoeiro e colete técnico de oficina.

O usuário definiu que a identidade visual deve unir o caráter **"bicho grilo"** (estética rústica e despojada de trilha/natureza) à referência ao **"Inspetor Bugiganga"** (chapéu de trilha com lanterna e lupa articuladas saindo do chapéu).

## Opções consideradas

1. **Animação 3D estilizada em meio-corpo ("bicho grilo" de trilha + engenhocas no chapéu):** modelar o personagem da cintura para cima tomando como base estética o [conceito-1-animacao.jpg](../../assets/personagem/conceitos/conceito-1-animacao.jpg), com as seguintes especificações:
   - **Anatomia e *rig* de expressão:** grilo verde antropomórfico estilizado com olhos grandes (pálpebras para piscar e controle de direção do olhar), sobrancelhas independentes, boca articulada com *shape keys* de visemas para *lip-sync* offline (conforme [0002-pipeline-personagem-e-video.md](0002-pipeline-personagem-e-video.md)) e dois braços até a cintura com mãos de quatro dedos articuladas para apontar e gesticular.
   - **Vestimenta "bicho grilo":** chapéu de trilha de aba maleável em tom oliva/cáqui com cordão trançado, camisa folgada de linho em tom bege terroso sob colete utilitário de lona oliva com bolsos (sem lupa no bolso) e pulseira de corda trançada no pulso.
   - **Engenhocas "Inspetor Bugiganga" no chapéu:** duas antenas verdes segmentadas atravessando a frente/topo da copa do chapéu com ossos próprios para movimento expressivo, além de uma lanterna compacta e uma lupa redonda saindo das laterais da copa do chapéu por duas hastes metálicas articuladas (recolhidas junto ao chapéu em repouso, podendo estender para frente ou em direção ao olho/produto durante inspeções).
   - **Referência visual consolidada:** [referencia-oficial.jpg](../../assets/personagem/referencia-oficial.jpg).
   - **Saída de render:** fundo transparente (canal alfa) para composição sobre as imagens do produto no `ffmpeg`, e fundo sólido `#0f172a` apenas em *previews* isolados do personagem.
2. **Estilo *toy-art* colecionável ([conceito-2-toy-art.jpg](../../assets/personagem/conceitos/conceito-2-toy-art.jpg)):** adotar proporções de boneco plástico/vinil de corpo inteiro com juntas aparentes.
3. **Estilo técnico de oficina ([conceito-3-tecnico-campo.jpg](../../assets/personagem/conceitos/conceito-3-tecnico-campo.jpg)):** adotar boné com lanterna de cabeça, paquímetro e visual industrial de oficina.

## Decisão

Opção escolhida: **Opção 1 (Animação 3D estilizada em meio-corpo "bicho grilo" de trilha + engenhocas no chapéu)**, porque preserva o carisma e a amplitude de expressão facial necessários para *lip-sync* e gestos em vídeos `9:16` (diferente do *toy-art* rígido) e traduz diretamente os dois traços da marca definidos pelo usuário (trilha/rústico + engenhocas no chapéu), evitando o visual técnico genérico de oficina.

### Consequências

- **Bom:** consolida anatomia, vestimenta, engenhocas articuladas, controles faciais e saída com transparência em uma especificação única para modelagem e *rigging* no Blender.
- **Ruim:** a inclusão de braços, mãos articuladas, aba maleável e hastes mecânicas no chapéu aumenta a complexidade inicial do *rig* em relação a um busto estático ou estilo *toy-art*.
- **Nota de atualização (2026-11-18):** a especificação visual definida nesta decisão permanece vigente, porém a implementação técnica foi adaptada da modelagem 3D no Blender para o **Rig 2.5D em camadas PNG** conforme [0005-pipeline-hibrido-25d-e-flow.md](0005-pipeline-hibrido-25d-e-flow.md) e [0006-governanca-qualidade-finops-e-composicao-visual.md](0006-governanca-qualidade-finops-e-composicao-visual.md).
