import numpy as np

#Definição da transformacao e dos offsets
transformacao = [
    [0.299    ,0.587    ,0.114    ],
    [0.500    ,-0.418688,-0.081312],
    [-0.168736,-0.331264,0.500    ]
]
offset = [0, 128, 128]

#Testado
def converter_para_ycbcr(imagem_rgb):
    assert len(transformacao[0]) == 3
    altura, largura, comprimento = imagem_rgb.shape
    imagem_ycrcb = np.zeros((altura, largura, comprimento), dtype=np.uint8)
    for i in range(len(imagem_rgb)):
        for j in range(len(imagem_rgb[0])):
            imagem_ycrcb[i][j] = transformacao_linear(transformacao, imagem_rgb[i][j]) + offset
    return imagem_ycrcb

#Testado
def transformacao_linear(matriz, vetor):
    assert len(matriz[0]) == len(vetor)
    novo_vetor = np.zeros(len(matriz))
    for i in range(len(matriz)):
        somatorio = 0
        for j in range(len(matriz[0])):
            somatorio += matriz[i][j] * vetor[j]
        novo_vetor[i] = somatorio
    return novo_vetor

#Testado
def dividir_8x8(imagem, altura, largura):
    assert altura >= 0 and largura >= 0
    altura_imagem, largura_imagem = imagem.shape
    maior_indice_altura = (altura_imagem+7)//8
    maior_indice_largura = (largura_imagem+7)//8
    if altura >= maior_indice_altura or largura >= maior_indice_largura:
        raise ValueError("Index out of bounds")
    bloco = np.zeros((8, 8))
    indice_y_bloco = altura * 8
    indice_x_bloco = largura * 8
    parte = imagem[indice_y_bloco:indice_y_bloco + 8, indice_x_bloco:indice_x_bloco + 8]
    bloco[:parte.shape[0], :parte.shape[1]] = parte
    return bloco

def converter_para_ycbcr_teste(transformacao, imagem_rgb):
    matriz = np.array(transformacao, dtype=np.float32)
    imagem_ycbcr = imagem_rgb.astype(np.float32) @ matriz.T
    imagem_ycbcr[:, :, 0] += 0
    imagem_ycbcr[:, :, 1] += 128
    imagem_ycbcr[:, :, 2] += 128
    return imagem_ycbcr
