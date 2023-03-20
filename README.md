# Efeitos-em-Video-APS
Por Alexandre Magno e Pedro Pertusi

## Descrição
O projeto consiste em um processador de vídeo desenvolvido para permitir que os usuários apliquem filtros em tempo real aos feeds de suas câmeras. Ele é construído usando a biblioteca OpenCV e implementado em Python. O processador aplica transformações de matrizes para obter efeitos de zoom e rotação.

## Como utilizar
* Para utilizar: 
  - Para instalar a aplicação existem dois caminhos:
    - Clonagem do repositório utilizando o seguinte comando no terminal: **git clone https://github.com/PedroPertusi/Efeitos-em-Video-APS.git**.
    - Ou baixar o arquivo zip desse repositório em `Code > Download Zip`. E descompactá-lo onde preferir.
  - Depois execute o comando: **pip install -r requirements.txt** no diretório principal do projeto clonado.
  - Execute o programa com o seguinte **comando: python demo.py**

## Implementação
Por meio da bibloteca OpenCV, foi possível capturar a câmera do usuário e converter sua imagem para uma matriz. Em seguida, foi criada uma matriz de destino para receber os pixels alterados. Foram realizadas diversas transformações matriciais, descritas no item abaixo, para criar o efeto de rotação da imagem em relação ao seu eixo. Esse processo é realizado frame-a-frame resultando em um filtro de câmera em tempo real. 

## Transformações
Com auxílio do NumPy, inserimos 3 tipos de transformações matriciais: Translação, Rotação e Expansão. 
- A primeira delas, a translação, foi utilizada para conduzir o vertice superior esquerdo da imagem para o centro da tela. **[[1, 0, -height/2], [0, 1, -width/2], [0, 0, 1]]**
- A rotação representada por: **[[np.cos(math.radians(ang)), -np.sin(math.radians(ang)), 0], [np.sin(math.radians(ang)), np.cos(math.radians(ang)), 0], [0, 0, 1]]**, foi responsável por girar a imagem, levando em consideração o ângulo que é incrementado a cada frame.
- Expansão: **[[2, 0, 0], [0, 2, 0], [0, 0, 1]]**. Usado para gerar efeito de Zoom 2X no centro da imagem.
- Por fim a imagem recebeu novamente uma translação, mas agora para retorná-la para a posicão inicial.

## Funcionalidades Adicionais
| --- | --- |
| Ação | Tecla | 
| Zoom IN & OUT | Z |
| Rotacionar Esquerda | A |
| Rotacionar Direita | D |
| Aumentar velocidade | Mouse Botão Esquerdo |
| Reduzir velocidade | Mouse Botão Direito |
| Salvar vídeo | S |
| Sair | Q |

