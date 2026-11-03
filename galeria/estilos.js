// Todos os estilos da galeria. id = a pasta em estilos/. familia agrupa os tiles. media = tem vídeo "com mídia real".
// Cada vídeo fica em galeria/videos/<id>.mp4 (cópia leve do original, que vive em estilos/<id>/).
window.ESTILOS = [
  // Apps com cursor de IA
  { id: 'editor-ia',           nome: 'Editor com cursor de IA',        familia: 'Apps com cursor de IA',  chamada: 'Uma IA edita o vídeo dentro do editor e o vídeo toma a tela', duracao: 18,   formato: '16:9', media: false },
  { id: 'app-de-design',       nome: 'App de design com cursor de IA', familia: 'Apps com cursor de IA',  chamada: 'O cursor monta uma thumbnail num app de design',            duracao: 15,   formato: '16:9', media: false },
  { id: 'app-de-motion',       nome: 'App de motion com cursor de IA', familia: 'Apps com cursor de IA',  chamada: 'Curvas e keyframes mexidos por uma IA',                      duracao: 16,   formato: '16:9', media: false },
  // Desenho que vira real
  { id: 'aviao-que-vira-foto', nome: 'Avião que vira foto',            familia: 'Desenho que vira real',  chamada: 'Um avião desenhado em código que vira foto real',           duracao: 22,   formato: '16:9', media: false },
  { id: 'festival-da-lua',     nome: 'Festival da lua',                familia: 'Desenho que vira real',  chamada: 'Nanquim e pincel seco; o desenho vira foto e anoitece',       duracao: 28,   formato: '16:9', media: false },
  { id: 'porto-de-nova-york',  nome: 'Porto de Nova York',             familia: 'Desenho que vira real',  chamada: 'Pôr do sol, barco e as luzes acendendo de baixo pra cima',   duracao: 30,   formato: '16:9', media: false },
  { id: 'barco-e-montanha',    nome: 'Barco e montanha',               familia: 'Desenho que vira real',  chamada: 'Camadas de papel, barco e montanha, versão premium',         duracao: 16,   formato: '16:9', media: false },
  // Lápis, giz e caneta
  { id: 'dirigivel-a-lapis',   nome: 'Dirigível a lápis',              familia: 'Lápis, giz e caneta',    chamada: 'Mascote em expedição a lápis que vira pintura de pôr do sol', duracao: 28.6, formato: '1:1',  media: false },
  { id: 'giz-de-cera',         nome: 'Giz de cera',                    familia: 'Lápis, giz e caneta',    chamada: 'Giz e canetinha no papel-cartão',                            duracao: 5,    formato: '16:9', media: false, loop: true },
  { id: 'rabisco-de-caneta',   nome: 'Rabisco de caneta',              familia: 'Lápis, giz e caneta',    chamada: 'Rabiscos de esferográfica na margem do caderno',             duracao: 5,    formato: '16:9', media: false, loop: true },
  { id: 'sessao-na-mesa',      nome: 'Sessão na mesa',                 familia: 'Lápis, giz e caneta',    chamada: 'O dia com o agente, em papel e aquarela',                    duracao: 58.7, formato: '16:9', media: false },
  // Tipografia e filme
  { id: 'showreel',            nome: 'Showreel em fundo claro',        familia: 'Tipografia e filme',     chamada: 'Pôster suíço que dança no compasso, sete capítulos',         duracao: 16,   formato: '16:9', media: false },
  { id: 'documento-vira-video',nome: 'Documento vira vídeo',           familia: 'Tipografia e filme',     chamada: 'O ponto final é um portal; a volta é vídeo',                 duracao: 32,   formato: '16:9', media: false },
];
