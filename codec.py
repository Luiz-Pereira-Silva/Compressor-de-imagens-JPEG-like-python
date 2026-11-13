import numpy as np
import matplotlib.pyplot as plt

from converter_imagem import converter_para_ycbcr, dividir_8x8
from transformada import dct_2d, idct_2d, dct_2d_biblioteca, idct_2d_biblioteca
from quantizador import quantizar_dct, desquantizar_dct
import zigzag as zig
from qualidade import psnr
from skimage.metrics import structural_similarity
from scipy.fft import dctn, idctn

def tornar_preto_e_branco(imagem):
    imagem_ycbcr = converter_para_ycbcr(imagem)
    return imagem_ycbcr[:, :, 0]

def plotar_imagens(imagem_inicial, imagem_y_deslocada, imagem_dct, imagem_quantizada, imagem_varrida,
                   imagem_comprimida, imagem_descomprimida, imagem_quantizada_recuperada,
                   imagem_desquantizada, imagem_destransformada, imagem_normalizada):
    # Plotando as imagens
    fig, eixos = plt.subplots(3, 3, figsize=(9, 9))
    eixos[0][0].imshow(imagem_inicial)
    eixos[0][0].set_title("Original")
    eixos[0][1].imshow(imagem_y_deslocada, cmap="gray")
    eixos[0][1].set_title("Y")
    eixos[0][2].imshow(imagem_y_deslocada, cmap="gray")
    eixos[0][2].set_title("Y_deslocada")
    eixos[1][0].imshow(imagem_dct, cmap="gray")
    eixos[1][0].imshow(dividir_8x8(imagem_dct, 17, 22), cmap="gray")
    eixos[1][0].set_title("DCT")
    eixos[1][1].imshow(imagem_quantizada, cmap="gray")
    eixos[1][1].imshow(dividir_8x8(imagem_quantizada, 17, 22), cmap="gray")
    eixos[1][1].set_title("DCT quantizada")
    eixos[1][2].imshow(imagem_quantizada_recuperada, cmap="gray")
    eixos[1][2].imshow(dividir_8x8(imagem_quantizada_recuperada, 17, 22), cmap="gray")
    eixos[1][2].set_title("Quantizada recuperada")
    eixos[2][0].imshow(imagem_desquantizada, cmap="gray")
    eixos[2][0].imshow(dividir_8x8(imagem_desquantizada, 17, 22), cmap="gray")
    eixos[2][0].set_title("Desquantizada")
    eixos[2][1].imshow(imagem_destransformada, cmap="gray")
    eixos[2][1].set_title("Imagem Destransformada")
    eixos[2][2].imshow(imagem_normalizada, cmap="gray")
    eixos[2][2].set_title("Imagem Normalizada")
    plt.show()

def codec(imagem_inicial, escala):
    imagem_y_deslocada = imagem_inicial.astype(np.int16) - 128
    imagem_dct, tempo_dct = dct_2d(imagem_y_deslocada)
    imagem_quantizada = quantizar_dct(imagem_dct, escala)
    imagem_varrida = zig.varredura_zigzag(imagem_quantizada)
    imagem_comprimida, bpp = zig.comprimir(imagem_varrida)
    imagem_descomprimida, porcentagem_zeros = zig.descomprimir(imagem_comprimida)
    imagem_quantizada_recuperada = zig.recuperar_imagem(imagem_descomprimida)
    imagem_desquantizada = desquantizar_dct(imagem_quantizada_recuperada, escala)
    imagem_destransformada, tempo_idct = idct_2d(imagem_desquantizada)
    imagem_normalizada = (imagem_destransformada + 128).astype(np.uint8)[:imagem_inicial.shape[0], :imagem_inicial.shape[1]]
    erro_psnr = psnr(imagem_inicial, imagem_normalizada)
    erro_ssim = structural_similarity(imagem_inicial, imagem_normalizada, multichannel=True, data_range=255)

    # plotar_imagens(imagem_inicial, imagem_y_deslocada, imagem_dct, imagem_quantizada, imagem_varrida,
    #         imagem_comprimida, imagem_descomprimida, imagem_quantizada_recuperada,
    #         imagem_desquantizada, imagem_destransformada, imagem_normalizada)


    return imagem_normalizada, porcentagem_zeros, bpp, erro_psnr, erro_ssim

def codec_v2(imagem_inicial, escala):
    imagem_y_deslocada = imagem_inicial.astype(np.int16) - 128
    imagem_dct, tempo_dct = dct_2d_biblioteca(imagem_y_deslocada)
    imagem_quantizada = quantizar_dct(imagem_dct, escala)
    imagem_varrida = zig.varredura_zigzag(imagem_quantizada)
    imagem_comprimida, bpp = zig.comprimir(imagem_varrida)
    imagem_descomprimida, porcentagem_zeros = zig.descomprimir(imagem_comprimida)
    imagem_quantizada_recuperada = zig.recuperar_imagem(imagem_descomprimida)
    imagem_desquantizada = desquantizar_dct(imagem_quantizada_recuperada, escala)
    imagem_destransformada, tempo_idct = idct_2d_biblioteca(imagem_desquantizada)
    imagem_normalizada = (imagem_destransformada + 128).astype(np.uint8)[:imagem_inicial.shape[0], :imagem_inicial.shape[1]]
    erro_psnr = psnr(imagem_inicial, imagem_normalizada)
    erro_ssim = structural_similarity(imagem_inicial, imagem_normalizada, multichannel=True, data_range=255)

    # plotar_imagens(imagem_inicial, imagem_y_deslocada, imagem_dct, imagem_quantizada, imagem_varrida,
    #                imagem_comprimida, imagem_descomprimida, imagem_quantizada_recuperada,
    #                imagem_desquantizada, imagem_destransformada, imagem_normalizada)

    return imagem_normalizada, porcentagem_zeros, bpp, erro_psnr, erro_ssim

