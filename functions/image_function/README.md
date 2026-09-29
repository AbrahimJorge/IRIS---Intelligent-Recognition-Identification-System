# Identificador de Cor em Imagens

Este é um projeto em Python voltado para a análise e identificação de cores em imagens estáticas (arquivos locais). O programa permite que o usuário interaja diretamente com a imagem carregada, selecionando regiões específicas para capturar a informação das cores contidas nelas.

## Objetivo
Criar uma ferramenta simples onde o usuário possa carregar uma imagem e desenhar regiões de interesse (retângulos ou círculos) utilizando o mouse, para posterior processamento ou identificação visual das cores predominantes nessas áreas delimitadas.

## Modos de Uso
O script abre uma janela contendo a imagem especificada. A partir da interação com o mouse e teclado:
- **Teclas `1` e `2`**: Alternam o modo de desenho entre Retângulo e Círculo.
- **Mouse (Clique e Arraste)**: Desenha a forma selecionada diretamente sobre a imagem para delimitar a área de análise de cores.
- **Tecla `l`**: Limpa a seleção atual da tela.
- **Tecla `q` ou `ESC`**: Fecha o programa.

## Bibliotecas Utilizadas
- **OpenCV (`cv2`)**: Para carregamento da imagem, renderização da interface (janela), leitura dos eventos de mouse/teclado e desenho de formas geométricas.
- **NumPy**: Para manipulação eficiente de arrays, cálculos matemáticos (como o cálculo do raio do círculo) e estrutura de dados de imagem.

## Como Executar

1. Instale as dependências necessárias:
```bash
pip install opencv-python numpy
```

2. Execute o arquivo principal:
```bash
python main.py
```