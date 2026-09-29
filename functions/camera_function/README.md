# Identificador de Cor via Câmera

Este é um projeto em Python focado em visão computacional em tempo real. Ele utiliza a webcam do computador para detectar e rastrear objetos de cores específicas, circulando-os na tela e exibindo seus respectivos nomes de acordo com limites de cor pré-estabelecidos.

## Objetivo
Fornecer um script capaz de realizar rastreamento de cor ao vivo (Real-time Color Tracking). O projeto utiliza o espaço de cor HSV, máscaras e análise de contornos para separar os objetos do fundo e focar nas cores que foram programadas para serem detectadas.

## Funcionalidades
- **Detecção ao Vivo**: Acessa a câmera (webcam) e processa os quadros dinamicamente.
- **Processamento HSV**: Converte as imagens para o modelo HSV, aplicando limiares de cor (Lower e Upper) para identificar objetos específicos.
- **Rastreamento Visual**: Ao encontrar áreas que correspondam às cores configuradas, o programa desenha um círculo ao redor do objeto e adiciona um texto indicando a cor reconhecida.

## Bibliotecas Utilizadas
- **OpenCV (`cv2`)**: Biblioteca principal responsável pela captura de vídeo da webcam, conversão de espaços de cor, operações morfológicas (abertura e fechamento de máscaras) e cálculo/desenho de contornos.
- **NumPy**: Para estruturar os limites das cores em matrizes (arrays) compatíveis com os filtros matemáticos do OpenCV.
- **Imutils**: Utilizada como facilitadora para operações de redimensionamento dos quadros de vídeo, melhorando a performance de leitura.

## Como Executar

1. Instale as dependências necessárias:
```bash
pip install opencv-python numpy imutils
```

2. Execute o arquivo principal (certifique-se de que a webcam não está sendo usada por outro app):
```bash
python main.py
```
