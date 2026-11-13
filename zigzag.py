import numpy as np
import sys

from converter_imagem import dividir_8x8

def varredura_zigzag(imagem):
    altura, largura = imagem.shape
    assert altura % 8 == 0 and largura % 8 == 0
    tamanho_indices_x = altura // 8
    tamanho_indices_y = largura  // 8
    resultado = [[[] for _ in range(tamanho_indices_y)] for _ in range(tamanho_indices_x)]
    #Percorre os blocos
    for k in range(tamanho_indices_x):
        for n in range(tamanho_indices_y):
            bloco = dividir_8x8(imagem, k, n)
            #Percorre os índices dos blocos
            varredura = []
            tamanho = 8
            for diagonal in range(2 * tamanho - 1):
                inicio = max(0, diagonal - tamanho + 1)
                fim = min(diagonal, tamanho - 1)
                if diagonal % 2 == 0:
                    for i in range(fim, inicio - 1, -1):
                        j = diagonal - i
                        varredura.append(bloco[i, j])
                else:
                    for i in range(inicio, fim + 1):
                        j = diagonal - i
                        varredura.append(bloco[i, j])
            resultado[k][n] = varredura
    return resultado

def recuperar_imagem(imagem):
    altura, largura, comprimento = imagem.shape
    assert comprimento == 64
    imagem_recuperada = np.zeros((altura*8, largura*8))
    # Percorre os blocos
    for k in range(altura):
        for n in range(largura):
            tamanho = 8
            indice_descomprimido = 0
            bloco = np.zeros((tamanho, tamanho))
            for diagonal in range(tamanho * 2 - 1):
                inicio = max(0, diagonal - tamanho + 1)
                fim = min(diagonal, tamanho - 1)
                if diagonal % 2 == 0:
                    for i in range(fim, inicio - 1, -1):
                        j = diagonal - i
                        bloco[i, j] = imagem[k][n][indice_descomprimido]
                        indice_descomprimido += 1
                else:
                    for i in range(inicio, fim + 1):
                        j = diagonal - i
                        bloco[i, j] = imagem[k][n][indice_descomprimido]
                        indice_descomprimido += 1
            imagem_recuperada[k*8:k*8+8, n*8:n*8+8] = bloco
    return imagem_recuperada

def comprimir(imagem):
    linhas = len(imagem)
    colunas = len(imagem[0])
    assert all(len(imagem[i][j]) == 64 for i in range(linhas) for j in range(colunas))
    imagem_comprimida = [[[] for _ in range(colunas)] for _ in range(linhas)]
    numero_de_bits = 0
    for i in range(linhas):
        for j in range(colunas):
            numero_de_zeros = 0
            linha_atual = []
            for z in range(64):
                if imagem[i][j][z] != 0:
                    linha_atual.append((numero_de_zeros, imagem[i][j][z]))
                    numero_de_bits += 24
                    numero_de_zeros = 0
                else:
                    numero_de_zeros += 1
            linha_atual.append(0)
            numero_de_bits += 8
            imagem_comprimida[i][j] = linha_atual
    bpp = numero_de_bits / (linhas * colunas * 64)
    return imagem_comprimida, bpp

def tamanho_memoria(objeto):
    tamanho = sys.getsizeof(objeto)

    if isinstance(objeto, (list, tuple)):
        tamanho += sum(tamanho_memoria(item) for item in objeto)

    return tamanho

def descomprimir(imagem):
    linhas = len(imagem)
    colunas = len(imagem[0])
    imagem_descomprimida = np.zeros((linhas, colunas, 64))
    for i in range(linhas):
        for j in range(colunas):
            indice_descomprimido = 0
            z = 0
            while z < len(imagem[i][j]):
                if imagem[i][j][z] != 0:
                    numero_de_zeros, valor = imagem[i][j][z]
                    indice_descomprimido += numero_de_zeros
                    imagem_descomprimida[i][j][indice_descomprimido] = valor
                else:
                    break
                z += 1
                indice_descomprimido += 1
    porcentagem_zeros = (imagem_descomprimida.size - np.count_nonzero(imagem_descomprimida)) / imagem_descomprimida.size
    return imagem_descomprimida, porcentagem_zeros