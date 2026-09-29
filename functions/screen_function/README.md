# Identificador de Cor da Tela

Este é um projeto em Python para capturar e identificar cores exibidas na tela do computador. Ele analisa as cores de um pixel específico ou de uma área selecionada e retorna o nome da cor em português, a porcentagem de incidência e o código hexadecimal correspondente.

## Objetivo
Criar uma ferramenta prática e flutuante para identificar rapidamente os tons de cor na tela, utilizando uma base de dados de nomes de cores combinada com um algoritmo de busca de vizinhos mais próximos (KDTree) para garantir precisão.

## Modos de Uso
O programa abre um menu flutuante com dois modos de operação:
- **Modo Click**: Captura e identifica a exata cor do pixel onde o mouse clicou.
- **Modo Cropped**: Permite arrastar o mouse na tela para selecionar uma região. O programa então lista as 8 cores mais presentes na área selecionada, com suas porcentagens.

## Bibliotecas Utilizadas
- **Tkinter**: Interface gráfica (menu flutuante e painel de resultados).
- **mss**: Captura da tela (screenshot).
- **OpenCV / NumPy**: Leitura e manipulação das matrizes de imagem.
- **Pandas**: Carregamento da base de dados externa de cores.
- **SciPy (KDTree)**: Cálculo de distância espacial para encontrar a cor mais próxima no banco de dados.
- **Pynput**: Captura global dos cliques do mouse.

## Como Executar

1. Instale as dependências necessárias:
```bash
pip install mss numpy opencv-python pandas scipy pynput screeninfo
```

2. Execute o arquivo principal:
```bash
python main.py
```
