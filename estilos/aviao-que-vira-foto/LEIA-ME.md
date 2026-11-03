# Avião que vira foto

A peça é um A-29 Super Tucano feito só com código (Three.js, geometria própria) num hangar com painel de controles; um controle chamado Realismo transforma o desenho na foto do avião de verdade, e ele decola.
Mecanismo: a foto entra por baixo do desenho, do desfoque para o foco, e na decolagem uma fronteira orgânica anda por dentro do avião, com o traço de tinta chegando antes da cor.
O que se costuma trocar: o objeto (qualquer coisa que exista em 3D e em foto), os textos do painel e do cartão final ("Do código ao real"), a pintura e a cor de acento, e a foto final com as camadas recortadas em `assets/reais/`.
Os scripts em `preparo/` recriam as camadas (corpo, asa, pás, sombra, fundo) a partir de uma foto nova; os caminhos dentro deles são os da pasta de trabalho original.
O que quebra o estilo: 1) trocar o desenho por foto num corte seco, sem a fronteira orgânica; 2) um modelo 3D baixado no lugar da geometria em código; 3) tirar o cartão final com o crédito da foto.
Ritmo medido: variação 7,6x, 33 % em quase-parada.
Nada ficou de fora da cópia do projeto (o maior arquivo, cada PNG de `assets/reais/`, tem cerca de 6 MB). `index-desenho.html` é a variante só-desenho, não validada; a peça de partida é `index.html`.
Crédito obrigatório: a foto do A-29B da FAB é CC BY 2.0, de André Gustavo Stumpf (ver `CREDITOS.md` ao lado desta ficha); o crédito está no cartão final. Aparecem marcas da FAB e da Embraer: não apresentar como material apoiado por elas.
Sem imagem gerada por IA, sem gravação ou foto real de ninguém. Sem som.
Para renderizar de novo, dentro de `projeto/`: `npx hyperframes@0.8.181 render . -o final.mp4 -q high`.
