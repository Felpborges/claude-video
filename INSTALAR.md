# Instalar a skill claude-video

> **Para a pessoa:** cole o link deste repositório numa conversa do Claude Code e diga "instala essa skill".
> O resto é com o Claude. Ao terminar, abra uma conversa nova para a skill carregar.

## Instrução para o Claude Code

Instale esta skill na máquina da pessoa. Faça exatamente isto, nesta ordem, falando em português simples:

1. Confira se já existe `~/.claude/skills/claude-video/`. Se existir, pergunte se pode substituir; só siga com um sim.
2. Clone o repositório para lá:
   `git clone <url deste repositório> ~/.claude/skills/claude-video`
   Se `git` não existir, baixe o ZIP do repositório, descompacte e mova a pasta para `~/.claude/skills/claude-video`
   (o arquivo `~/.claude/skills/claude-video/SKILL.md` precisa existir no fim).
3. Dê permissão de execução aos scripts: `chmod +x ~/.claude/skills/claude-video/scripts/*.sh`.
4. Rode a checagem da máquina: `bash ~/.claude/skills/claude-video/scripts/checar.sh`.
   Para cada item que faltar, diga em uma linha o que é e o comando que vai rodar, e **peça confirmação antes de
   instalar**. Só instale depois do sim. Os itens possíveis são: Node 22 ou mais novo, ffmpeg (com ffprobe) e
   Python 3. O HyperFrames é baixado sozinho na primeira vez que renderizar (`npx hyperframes@0.8.181`); avise que a
   primeira execução demora alguns minutos.
5. Rode a checagem de novo até ela dizer "pronto".
6. Diga à pessoa que a instalação terminou e que ela precisa abrir uma conversa nova e dizer
   "faz um motion graphic pra mim".

Não instale nada que a checagem não pediu. Nunca peça nem registre chaves de API; a do Higgsfield é opcional e vai
num arquivo `.env` na pasta do projeto da pessoa, que ela mesma cria.

## Requisitos

- macOS ou Linux (testado no macOS). No Windows, use o Git Bash para os scripts `.sh`; ainda não testado.
- Node 22 ou mais novo (https://nodejs.org), ffmpeg (`brew install ffmpeg`), Python 3.
- Internet na primeira renderização (download do HyperFrames e das fontes).
