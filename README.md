# IRIS - Intelligent Recognition & Identification System

[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-green.svg)](https://opencv.org/)
[![Tkinter](https://img.shields.io/badge/GUI-Tkinter-orange.svg)](https://docs.python.org/3/library/tkinter.html)
[![License](https://img.shields.io/badge/License-MIT-lightgrey.svg)](LICENSE)

O **IRIS** (*Intelligent Recognition & Identification System*) é uma aplicação modular desenvolvida em Python voltada para **Visão Computacional** e **Identificação Inteligente de Cores**. O sistema captura, analisa e classifica cores a partir de três fontes distintas de entrada: **Webcam ao vivo**, **Imagens locais** e **Área de trabalho (Desktop)**.

Para a rotulação das cores, o IRIS utiliza uma base padronizada com mais de 18.000 nomes indexada em uma árvore de busca multidimensional (**KD-Tree** via SciPy), garantindo consultas de vizinhos mais próximos de alta performance no espaço vetorial RGB.

---

## Sumario

- [Objetivo do Projeto](#objetivo-do-projeto)
- [Funcionalidades Principais](#funcionalidades-principais)
- [Arquitetura e Estrutura de Pastas](#arquitetura-e-estrutura-de-pastas)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Instalacao e Execucao](#instalacao-e-execucao)
- [Guia de Uso e Atalhos](#guia-de-uso-e-atalhos)
- [Licenca](#licenca)

---

## Objetivo do Projeto

O IRIS atua como ferramenta assistiva e analítica para identificação e quantificação de cores, com aplicações voltadas para:

- **Acessibilidade**: apoio a pessoas com daltonismo ou baixa visão na identificação precisa de tonalidades no mundo real, em fotos ou na interface gráfica.
- **Design e UI/UX**: extração de paletas dominantes, verificação de proporções cromáticas e captura rápida de valores de cor diretamente da tela.
- **Visão Computacional**: demonstração prática de segmentação HSV, filtragem morfológica, indexação espacial com KD-Tree e integração de eventos de interface entre OpenCV e Tkinter.

---

## Funcionalidades Principais

### 1. Modulo de Camera (Webcam)
- Transmissão de vídeo em tempo real via OpenCV.
- Identificação do nome da cor ao clicar em qualquer ponto do quadro.
- Rastreamento da cor selecionada por segmentação no espaço HSV com remoção de ruídos morfológicos.
- Exibição do rótulo e amostra em um painel flutuante arrastável.

### 2. Modulo de Imagem Estatica
- Seleção e abertura de arquivos locais nos formatos comuns (`PNG`, `JPG`, `JPEG`, `BMP`).
- Modos de demarcação geométrica: **Retângulo** e **Círculo**.
- Análise espectral da região demarcada com identificação das 5 cores predominantes e cálculo de percentuais relativos.

### 3. Modulo de Tela (Desktop)
- Widget flutuante arrastável para controle das ferramentas de inspeção do sistema.
- **Modo Click**: captura do pixel sob o cursor em qualquer janela ou aplicativo do sistema operacional.
- **Modo Cropped**: seleção de área retangular com overlay transparente na tela, calculando o ranking das 8 cores dominantes e suas porcentagens.

---

## Arquitetura e Estrutura de Pastas

O sistema adota um padrão modular coordenado pelo arquivo central `main.py` (`IRISApp`), compartilhando uma única instância em memória da base de dados (`ColorDataset` - Singleton).

```text
IRIS - Intelligent Recognition & Identification System/
|-- constants/                             # Configuracoes e constantes de cada modulo
|   |-- camera_constants.py
|   |-- image_constants.py
|   `-- screen_constants.py
|-- database/                              # Carregamento do CSV e indexacao KD-Tree
|   `-- github_database.py
|-- functions/                             # Modulos operacionais
|   |-- camera_function/                   # Streaming, clique e rastreamento HSV
|   |-- image_function/                    # Selecao de regioes e analise em imagens estaticas
|   `-- screen_function/                   # Captura pontual e por recorte da tela do sistema
|-- main.py                                # Interface central e gerenciador de modulos (Tkinter)
|-- requirements.txt                       # Dependencias do projeto
`-- README.md                              # Documentacao
```

---

## Tecnologias Utilizadas

| Tecnologia | Finalidade no Projeto |
| :--- | :--- |
| **Python 3.10+** | Linguagem base da aplicação. |
| **OpenCV (`opencv-python`)** | Captura de vídeo, conversões BGR/HSV, filtros morfológicos e renderização de janelas. |
| **SciPy** | Indexação espacial tridimensional via `KDTree` para busca de vizinho mais próximo em $\mathcal{O}(\log N)$. |
| **NumPy** | Manipulação de matrizes de imagem, operações vetorizadas e cálculos de média. |
| **Pandas** | Leitura e estruturação da base de dados de nomes de cores. |
| **Tkinter** | Interface principal, janela flutuante dock, overlays transparentes e painéis de resultado. |
| **MSS** | Captura de tela de alto desempenho para o módulo Desktop. |
| **Pynput** | Monitoramento de cliques e coordenadas globais do mouse no sistema operacional. |
| **Imutils** | Redimensionamento proporcional de frames de vídeo. |
| **Screeninfo** | Detecção da resolução do monitor para ajuste do overlay de recorte. |

---

## Instalacao e Execucao

### Pre-requisitos
- Python 3.10 ou superior.
- Conexão com a internet na primeira execução para download da base de cores (`colors.csv`).
- Webcam instalada e conectada (para utilização do módulo de câmera).

### Passo a Passo

1. **Acessar o diretório do projeto**:
   ```bash
   cd "IRIS - Intelligent Recognition & Identification System"
   ```

2. **Criar e ativar o ambiente virtual (recomendado)**:
   ```powershell
   # Windows (PowerShell)
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. **Instalar dependências**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Executar o programa**:
   ```bash
   python main.py
   ```

---

## Guia de Uso e Atalhos

### Janela Principal
- **Camera**: Ativa ou desativa a câmera ao vivo.
- **Image**: Abre o diálogo de seleção de arquivo de imagem.
- **Screen**: Ativa o dock flutuante de inspeção da área de trabalho.

### Modulo de Camera
- **Botão Esquerdo do Mouse**: Clica em um ponto da imagem para identificar a cor e ativar o rastreamento HSV.
- **Arrastar Painel**: Clique e arraste o card de resultados para movê-lo pela tela.
- **Tecla `q`**: Fecha a janela da câmera.

### Modulo de Imagem
- **Tecla `1`**: Seleciona modo de demarcação retangular.
- **Tecla `2`**: Seleciona modo de demarcação circular.
- **Clique e Arraste**: Delimita a região de interesse. Ao soltar, a janela de resultados é gerada.
- **Tecla `l`**: Limpa a seleção atual.
- **Tecla `q` ou `ESC`**: Fecha a visualização da imagem.

### Modulo de Tela
- **Botão Flutuante (Dock)**:
  - **Clique Simples**: Abre ou fecha o menu com as opções `Click` e `Cropped`.
  - **Clique e Arraste**: Move o botão flutuante para qualquer posição da tela.
  - **Clique com Botão Direito**: Encerra o módulo de tela.
- **Modo Click**: Com o modo ativo, clique em qualquer ponto da tela do sistema operacional para identificar o pixel selecionado.
- **Modo Cropped**: Com o modo ativo, clique e arraste para desenhar uma área retangular na tela; ao soltar, as 8 cores mais frequentes com suas respectivas porcentagens serão exibidas.

---

## Licenca

Projeto desenvolvido para fins acadêmicos e educacionais. Consulte o arquivo de licença do repositório para detalhes sobre redistribuição e uso.
