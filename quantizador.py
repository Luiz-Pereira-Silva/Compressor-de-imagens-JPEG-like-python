import numpy as np

quantizador = np.array([
[16, 11, 10, 16, 24, 40, 51, 61],
[12, 12, 14, 19, 26, 58, 60, 55],
[14, 13, 16, 24, 40, 57, 69, 56],
[14, 17, 22, 29, 51, 87, 80, 62],
[18, 22, 37, 56, 68, 109, 103, 77],
[24, 35, 55, 64, 81, 104, 113, 92],
[49, 64, 78, 87,103, 121, 120, 101],
[72, 92, 95, 98,112, 100, 103, 99]
], dtype=np.float64)

def quantizar_dct(imagem, escala):
    altura, largura = imagem.shape
    imagem_quantizada = np.zeros(imagem.shape, dtype=np.float64)
    n_blocos_vertical = (altura + 7) // 8
    n_blocos_horizontal = (largura + 7) // 8
    for k in range(n_blocos_vertical):
        for n in range(n_blocos_horizontal):
            imagem_quantizada[
                k*8:k*8+8,
                n*8:n*8+8
            ] = np.round(
                imagem[
                    k*8:k*8+8,
                    n*8:n*8+8
                ] / (quantizador * escala)
            )
    return imagem_quantizada

def desquantizar_dct(imagem, escala):
    altura, largura = imagem.shape
    imagem_desquantizada = np.zeros(imagem.shape, dtype=np.float64)
    n_blocos_vertical = (altura + 7) // 8
    n_blocos_horizontal = (largura + 7) // 8
    for k in range(n_blocos_vertical):
        for n in range(n_blocos_horizontal):
            imagem_desquantizada[
                k * 8:k * 8 + 8,
                n * 8:n * 8 + 8
            ] = np.round(
                imagem[
                    k * 8:k * 8 + 8,
                    n * 8:n * 8 + 8
                ] * (quantizador * escala)
            )
    return imagem_desquantizada