import numpy as np
import time

from converter_imagem import dividir_8x8
from scipy.fft import dctn, idctn

def alfa(altura):
    if altura == 0:
        return (1/8) ** (1/2)
    else:
        return (2/8) ** (1/2)

def gerar_transformacao():
    matriz_transformacao = np.zeros((8, 8))
    for k in range(8):
        for n in range(8):
            matriz_transformacao[k, n] = alfa(k) * np.cos((np.pi/8) *(n + (1/2)) * k)
    return matriz_transformacao

def multiplicacao_de_vetores(vetor1, vetor2):
    assert vetor1.shape[0] == vetor2.shape[0]
    somatorio = 0
    for n in range(vetor1.shape[0]):
        somatorio += vetor1[n] * vetor2[n]
    return somatorio

def multiplicacao_de_matrizes(matriz1, matriz2):
    assert matriz1.shape[1] == matriz2.shape[0]
    matriz_resultado = np.zeros((matriz1.shape[0], matriz2.shape[1]))
    for k in range(matriz1.shape[0]):
        for n in range(matriz2.shape[1]):
            matriz_resultado[k, n] = multiplicacao_de_vetores(matriz1[k, :], matriz2[:, n])
    return matriz_resultado

def dct_2d(imagem):
    altura, largura = imagem.shape
    altura_transformada = ((altura+7)//8)*8
    largura_transformada = ((largura+7)//8)*8
    imagem_transformada = np.zeros((altura_transformada, largura_transformada))
    n_blocos_vertical = (altura+7)//8
    n_blocos_horizontal = (largura+7)//8
    transformada = gerar_transformacao()
    inicio = time.perf_counter()
    for k in range(n_blocos_vertical):
        for n in range(n_blocos_horizontal):
            imagem_transformada[
                k*8:k*8+8,
                n*8:n*8+8
            ] = multiplicacao_de_matrizes(
                multiplicacao_de_matrizes(
                    transformada,
                    dividir_8x8(imagem, k, n)
                )
                , transformada.T)
    final = time.perf_counter()
    tempo_de_execucao = (final - inicio)
    return imagem_transformada, tempo_de_execucao

def dct_2d_biblioteca(imagem):
    linhas, colunas = imagem.shape
    padding_linhas = (8 - linhas % 8) % 8
    padding_colunas = (8 - colunas % 8) % 8
    imagem_com_padding = np.pad(
        imagem,
        ((0, padding_linhas), (0, padding_colunas)),
        mode="constant",
        constant_values=0
    )
    imagem_transformada_biblioteca = np.zeros_like(
        imagem_com_padding, dtype=np.float64
    )
    inicio = time.perf_counter()
    for i in range(0, imagem_com_padding.shape[0], 8):
        for j in range(0, imagem_com_padding.shape[1], 8):
            bloco = imagem_com_padding[i:i + 8, j:j + 8]

            imagem_transformada_biblioteca[i:i + 8, j:j + 8] = dctn(
                bloco, type=2, norm="ortho"
            )
    final = time.perf_counter()
    tempo_de_execucao = (final - inicio)
    return imagem_transformada_biblioteca, tempo_de_execucao

def idct_2d(imagem):
    altura, largura = imagem.shape
    altura_transformada = ((altura+7)//8)*8
    largura_transformada = ((largura+7)//8)*8
    imagem_transformada = np.zeros((altura_transformada, largura_transformada))
    n_blocos_vertical = (altura+7)//8
    n_blocos_horizontal = (largura+7)//8
    transformada = gerar_transformacao()
    inicio = time.perf_counter()
    for k in range(n_blocos_vertical):
        for n in range(n_blocos_horizontal):
            imagem_transformada[
                k*8:k*8+8,
                n*8:n*8+8
            ] = multiplicacao_de_matrizes(
                multiplicacao_de_matrizes(
                    transformada.T,
                    dividir_8x8(imagem, k, n)
                )
                , transformada)
    final = time.perf_counter()
    tempo_de_execucao = (final - inicio)
    return imagem_transformada, tempo_de_execucao

def idct_2d_biblioteca(imagem):
    imagem_reconstruida = np.zeros_like(imagem, dtype=np.float64)
    inicio = time.perf_counter()
    for i in range(0, imagem.shape[0], 8):
        for j in range(0, imagem.shape[1], 8):
            bloco = imagem[i:i+8, j:j+8]

            imagem_reconstruida[i:i+8, j:j+8] = idctn(
                bloco, type=2, norm="ortho"
            )
    final = time.perf_counter()
    tempo_de_execucao = (final - inicio)
    return imagem_reconstruida, tempo_de_execucao