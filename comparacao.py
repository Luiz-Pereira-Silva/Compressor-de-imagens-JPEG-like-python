import numpy as np
from transformada import dct_2d, dct_2d_biblioteca, idct_2d, idct_2d_biblioteca

def dct_implementada_e_biblioteca(imagem):
    imagem_y_deslocada = imagem.astype(np.int16) - 128

    linhas, colunas = imagem_y_deslocada.shape

    padding_linhas = (8 - linhas % 8) % 8
    padding_colunas = (8 - colunas % 8) % 8

    imagem_com_padding = np.pad(
        imagem_y_deslocada,
        ((0, padding_linhas), (0, padding_colunas)),
        mode="constant",
        constant_values=0
    )

    imagem_transformada_implementada, tempo_dct_implementada = medir(dct_2d, imagem_com_padding)
    imagem_transformada_biblioteca, tempo_dct_biblioteca = medir(dct_2d_biblioteca, imagem_com_padding)
    erro_maximo_dct = np.max(np.abs(
        imagem_transformada_implementada - imagem_transformada_biblioteca)
    )

    imagem_destransformada_implementada, tempo_idct_implementada = medir(idct_2d, imagem_transformada_implementada)
    imagem_pela_implementacao = imagem_destransformada_implementada
    imagem_pela_biblioteca, tempo_idct_biblioteca = medir(idct_2d_biblioteca, imagem_transformada_biblioteca)
    imagem_pela_biblioteca = imagem_pela_biblioteca
    erro_maximo_idct = np.max(np.abs(imagem_pela_implementacao - imagem_pela_biblioteca))

    return (erro_maximo_dct, erro_maximo_idct, tempo_dct_implementada,
            tempo_dct_biblioteca, tempo_idct_implementada, tempo_idct_biblioteca)

def medir(funcao, imagem):
    nova_imagem = np.zeros_like(imagem)
    numero_de_aquecimento = 2
    numero_de_medicoes = 20
    medicoes = []
    for i in range (numero_de_aquecimento):
        nova_imagem, medicao_descartada = funcao(imagem)
    for i in range (numero_de_medicoes):
        nova_imagem, medicao = funcao(imagem)
        medicoes.append(medicao)
    medicao_mediana = np.median(medicoes)
    return nova_imagem, medicao_mediana
