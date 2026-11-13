from codec import codec_v2, tornar_preto_e_branco
from PIL import Image
import numpy as np

# Carrega, transpõe e reduz a imagem
imagem = Image.open("Judy_Koda.jpg").convert("RGB")
imagem_rgb = np.array(imagem).transpose(1, 0, 2)
imagem_menor_rgb = imagem_rgb[::10, ::10]
imagem_inicial = tornar_preto_e_branco(imagem_menor_rgb)

codec_v2(imagem_inicial, 1)