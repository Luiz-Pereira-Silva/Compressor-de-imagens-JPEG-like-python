import numpy as np

def psnr(imagem1, imagem2):
    assert imagem1.shape == imagem2.shape
    imagem1 = imagem1.astype(np.float32)
    imagem2 = imagem2.astype(np.float32)
    linhas, colunas = imagem1.shape
    somatorio_final = 0
    for i in range(linhas):
        somatorio_linha = 0
        for j in range(colunas):
            somatorio_linha += (imagem1[i, j] - imagem2[i, j]) ** 2
        somatorio_final += somatorio_linha
    mse =  somatorio_final * (1/ (linhas*colunas))
    if mse == 0:
        return float('inf')
    return 10 * np.log10((255 ** 2) / mse)
