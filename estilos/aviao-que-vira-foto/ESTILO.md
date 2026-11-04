# Avião que vira foto
id: aviao-que-vira-foto
Melhor para: "do código ao real" (produto, carro, prédio ou objeto 3D que vira foto), transição desenho→foto no meio de um vídeo, abertura sobre 3D feito em código, apresentação de produto com painel de controles, cartão final com crédito
Formato: 1920×1080, 22 s, sem som
Vídeo na galeria: galeria/videos/aviao-que-vira-foto.mp4
Peça de partida: projeto/index.html

## Como usar esta referência
1. O Claude lê esta ficha inteira antes de abrir qualquer arquivo de `projeto/`.
2. Parte dos cards (o que acontece em cada batida), não do código: a peça nova nasce em cards estáticos, batida a batida, aprovados antes de animar.
3. Mantém o mecanismo, a paleta e o ritmo medidos aqui (amplitude, quase-parada, picos, cortes).
4. Troca o assunto, os textos e as cores de acento para o pedido da pessoa; o que é só desta peça (tema, desenhos, frases) não se copia.
5. O código em `projeto/` é apoio para ver como um truque foi feito, não molde para preencher.

> Nesta ficha ficou só o que vale para a versão real (`aviao-1920x1080.mp4`): a seção da versão só-desenho saiu. O `projeto/` ainda traz `index-desenho.html`, porque é o mesmo código com um atributo a mais, mas a peça validada aqui é a real.

---

# Perícia: avião em código que vira real (A-29 Super Tucano)

Referência: vídeo "Three.js Skyraider aircraft model", de @BuildFastWithAI, em prompt-motion.com (39 s). Analisada pelos quadros no navegador; o arquivo não foi baixado, então não há comparação de ritmo direta com ela. Mistura pedida pelo Felipe: a transição sutil do vídeo de exemplo `video-particle-teste`.

## Mecanismo
Um cursor mexe em um painel e um avião feito só com código responde; um controle chamado Realismo transforma o desenho no avião de verdade, e na decolagem desenho e real se misturam dentro do mesmo avião.

## Batidas
| Tempo | O que acontece |
|---|---|
| 0 a 8,4 s | A-29 em 3D no hangar de código: hélice, capota, flaps, comandos e troca de pintura (Fumaça para Operacional), com câmera em órbitas |
| 8,4 a 11,5 s | Pausa, depois o controle Realismo: a foto entra por baixo do desenho, do desfoque para o foco, com a câmera avançando e uma faixa de luz no avião |
| 11,5 a 13 s | A interface sai; o motor acelera |
| 13 a 20,1 s | Decolagem real: corrida, nariz sobe nas rodas principais, rodas saem do chão, subida rasa. Duas vezes, uma fronteira orgânica anda por dentro do avião e do cenário: o desenho entra pela cauda, o real volta pelo nariz com luz quente, e o traço de tinta chega antes da cor |
| 20,1 a 22 s | Cartão final "Do código ao real" |

## Como foi feito
- **3D:** Three.js com geometria própria do A-29 (`plane.js`), sem modelo baixado.
- **Real:** uma foto real do A-29B 5950 da FAB, recortada em camadas (corpo, asa de perto, pás, sombra e fundo limpo). Hélice, rodas e borrão de velocidade são feitos em código.
- **Desenho da decolagem:** tirado da própria foto (`preparo/desenho.py`), por isso ocupa exatamente o mesmo lugar do real.
- **Sem imagem gerada por IA.** As tentativas com o Higgsfield foram descartadas e não estão nesta skill.

## Resultado medido
22 s, 1920 x 1080, 30 fps, sem áudio. Variação de ritmo (pico ÷ mediana) 7,6x; 33% do tempo em quase-parada.


## Para renderizar de novo
Dentro de `projeto/`: `npx hyperframes@0.8.181 render . -o final.mp4 -q high` (versão real) ou `npx hyperframes@0.8.181 render . -c index-desenho.html -o final.mp4 -q high` (versão só desenho). As duas usam o mesmo código; a diferença é o atributo `data-variante="desenho"` no `index-desenho.html`. O projeto foi testado renderizando as duas e comparando quadro a quadro: idênticas às salvas. Os scripts de `preparo/` recriam as camadas a partir da foto; os caminhos dentro deles são os da pasta de trabalho original e precisam ser ajustados antes de rodar.

## Pontos em aberto
- **Crédito obrigatório:** a foto é CC BY 2.0 (ver `CREDITOS.md`); o crédito está no cartão final das duas versões, porque a ilustração também foi feita a partir dela.
- **Marcas:** aparecem a FAB e o nome Embraer; não apresentar como material apoiado por elas.
