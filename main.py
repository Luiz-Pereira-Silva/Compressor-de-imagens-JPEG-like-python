from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

from codec import codec, tornar_preto_e_branco
from comparacao import dct_implementada_e_biblioteca
from transformada import dividir_8x8

# Carrega, transpõe e reduz a imagem
imagem = Image.open("Judy_Koda.jpg").convert("RGB")
imagem_rgb = np.array(imagem).transpose(1, 0, 2)
imagem_menor_rgb = imagem_rgb[::10, ::10]

print("Fim da Conversão em RGB")

#Executa o codec
imagem_inicial = tornar_preto_e_branco(imagem_menor_rgb)
print("Fim da conversão em ycbcr")
print("\n\nValores de medições numéricas baseados na escala de quantização: \n")
testes = [0.5, 1, 1.5, 2.0, 2.5, 3.0, 3.5, 4]
lista_bpp = []
lista_psnr = []
lista_ssim = []
lista_imagens = []
lista_imagens.append(imagem_inicial)
print("|s       |bpp      |zeros%   |psnr      |ssim     |")
for i in testes:
    imagem_reconstruida, porcentagem_zeros, bpp, erro_psnr, erro_ssim = codec(imagem_inicial, escala= i)
    lista_bpp.append(bpp)
    lista_psnr.append(erro_psnr)
    lista_ssim.append(erro_ssim)
    lista_imagens.append(imagem_reconstruida)
    print(f"|{i:.1f}     |{bpp:04.2f}     |{porcentagem_zeros:04.2f}     |{erro_psnr:2.2f}     |{erro_ssim:.2f}     |")

print("\n\nValidacao numérica entre a dct rápida e da dct matricial implementada: ")
(erro_maximo_dct, erro_maximo_idct, tempo_dct_implementada,
 tempo_dct_biblioteca, tempo_idct_implementada, tempo_idct_biblioteca) = dct_implementada_e_biblioteca(imagem_inicial)
print(f"    Erro máximo da dct: {erro_maximo_dct:.4e}, Erro maximo da idct: {erro_maximo_idct:.4e}")
print(f"    Tempo de execucao dct pela implementacao x biblioteca: "
      f"{tempo_dct_implementada:.4f}s, {tempo_dct_biblioteca:.4f}s, speedup: {tempo_dct_implementada/tempo_dct_biblioteca:.4f}")
print(f"    Tempo de execucao idct pela implementacao x biblioteca: "
      f"{tempo_idct_implementada:.4f}s, {tempo_idct_biblioteca:.4f}s, speedup: {tempo_idct_implementada/tempo_idct_biblioteca:.4f}")

#Plota os gráficos de psnr e ssim por bpp
fig1, eixos1 = plt.subplots(1, 2, figsize=(9, 9))
eixos1[0].plot(lista_bpp, lista_psnr, marker="o")
eixos1[0].set_title("PSNR/BPP")
eixos1[0].set_xlabel("BPP")
eixos1[0].set_ylabel("PSNR")
eixos1[0].grid(True)
eixos1[1].plot(lista_bpp, lista_ssim, marker="o")
eixos1[1].set_title("SSIM/BPP")
eixos1[1].set_xlabel("BPP")
eixos1[1].set_ylabel("SSIM")
eixos1[1].grid(True)

#Printa e plota as imagens iniciais e finais
fig2, eixos2 = plt.subplots(3, 3, figsize=(9, 9))
eixos2[0][0].imshow(lista_imagens[0], cmap="gray")
eixos2[0][0].set_title("Imagem original em Y")
eixos2[0][1].imshow(lista_imagens[1], cmap="gray")
eixos2[0][1].set_title("s = 0.5")
eixos2[0][2].imshow(lista_imagens[2], cmap="gray")
eixos2[0][2].set_title("s = 1.0")
eixos2[1][0].imshow(lista_imagens[3], cmap="gray")
eixos2[1][0].set_title("s = 1.5")
eixos2[1][1].imshow(lista_imagens[4], cmap="gray")
eixos2[1][1].set_title("s = 2.0")
eixos2[1][2].imshow(lista_imagens[5], cmap="gray")
eixos2[1][2].set_title("s = 2.5")
eixos2[2][0].imshow(lista_imagens[6], cmap="gray")
eixos2[2][0].set_title("s = 3.0")
eixos2[2][1].imshow(lista_imagens[7], cmap="gray")
eixos2[2][1].set_title("s = 3.5")
eixos2[2][2].imshow(lista_imagens[8], cmap="gray")
eixos2[2][2].set_title("s = 4.0")

fig3, eixos3 = plt.subplots(1, 2, figsize=(9, 9))
eixos3[0].imshow(lista_imagens[0], cmap="gray")
eixos3[0].set_title("Imagem original em Y")
eixos3[1].imshow(lista_imagens[8], cmap="gray")
eixos3[1].set_title("s = 4.0")

plt.show()

