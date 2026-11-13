Discussões sobre uma implementação de codec para arquivos jpeg em python e suas medições e comparações.

Introdução:

O objetivo desta atividade é implementar um encoder/decoder de imagens jpeg visando a compressão desses arquivos de forma a serem representados com a uma quantidade menor de bits, administrado um tradeoff entre a informação que é perdida na etapa de quantização e a compressão da imagem medida em bpp (bits por pixel).  O codec foi implementado de forma a realizar todas as etapas da compressão da imagem e executado apenas para a componente Y da imagem, como foi solicitada pela atividade, e a arquitetura do código foi desenvolvida de forma modular utilizando 9 arquivos python para agrupar as funções de acordo com a etapa e o tipo de função executado. Entre elas, duas são exclusivas para as funções que não participam da etapa de compressão, mas assumem a função de realizar os testes e as comparações necessárias e a implementação do teste de qualidade PSNR.

Metodologia

A primeira etapa do compressor foi realizada sobre a componente Y da imagem depois de ela passar pela conversão matricial do formato RGB para o formato YCbCr e depois do número de pixels dela ser reduzido em 10x por razões de tempo de execução do código que serão discutidas posteriormente. Sobre a imagem original que pode pode ser vista na figura 1, operações de conversão realizadas se encontram no arquivo converter_imagem.py, feitas para tornar o arquivo compatível com a implementação. Sobre ela foi aplicada a matriz de transformação C em blocos de 8 bits por 8 bits, utilizando funções implementadas manualmente exercendo o papel de multiplicação de vetores e multiplicação de matrizes que executam a DCT em cima dos blocos através dessa matriz. Toda a implementação matricial é feita dentro do arquivo transformada.py e o arquivo também contêm as versões dos algoritmos utilizando os métodos e bibliotecas prontas. 

Figura 1:


Após tirar a DCT dos blocos da imagem, é então realizada a quantização, utilizando o arquivo quantizador.py cuja agressividade da quantização é realizada através de uma escala definida anteriormente que será essencial para verificarmos como a compressão dos dados pode apagar informações do arquivo original. Posteriormente é realizada uma varredura utilizando o algoritmo utilizado para imagens jpeg que está dentro do arquivo zigzag.py que cria uma matriz onde cada coordenada corresponde à um bloco de 8x8 da imagem original e seu conteúdo nada mais é do que os bytes que representam cada elemento da matriz 8x8. Portando uma imagem de tamanho (x, y) é convertida em um bloco de dimensões (x/8, y/8, 64). A metodologia adotada foi essa porque foi uma forma fácil de recuperar as dimensões da imagem depois, visto que toda a implementação gira em torno de dividir a imagem completa em blocos 8x8. Dentro do arquivo zigzag.py também foi feita a parte de compressão dos dados utilizando o algoritmo RLE e o cálculo de bpp para representar o nível de compressão da imagem depois de sua execução. 

Todos os métodos relacionados à compressão e descompressão da imagem são encontrados dentro do arquivo codec.py, que é quem efetivamente executa todos os métodos enquanto main.py foca em plotar e printar os resultados para o usuário. Enquanto isso, os métodos relacionados à comparar o tempo de execução do algoritmo implementado com métodos prontos estão no arquivo comparacao.py e os métodos relacionados à controle de qualidade, mais especificamente o método PSNR, estão em qualidade.py. O arquivo teste.py serviu apenas para realização de testes durante o desenvolvimento e pode ser ignorado.

Resultados:

Em questão de qualidade de imagem, os métodos implementados tiveram diferença quase nula comparado aos métodos prontos das bibliotecas scipy e da utilização do método de multiplicação matricial @, no entanto em questão de tempo de processamento o código implementado teve um resultado “ridículo” comparado a esses métodos que possuem um speedup relativo chegando a mais de 27 vezes considerando os resultados obtidos no console do programa na figura 2:

Figura 2:


Esses resultados foram obtidos através da obtenção da mediana de uma lista de amostras de tempo de execução de tamanho 20 com 3 execuções de aquecimento. Isso se deve primariamente ao fato de que esses métodos e operações que podem ser utilizados pelo python são código compilado, muitos feitos na linguagem C, que devido a não precisarem de um interpretador que reduz consideravelmente o tempo de execução conseguem um desempenho estrondoso comparado ao código implementado. Além da ausência do interpretador, os métodos prontos utilizam também instruções vetoriais da própria CPU e de bibliotecas otimizadas de álgebra linear para atingir esse resultado.

Fora essas medições, foram feitas também comparações entre o mesmo programa, mas com valores de escala de quantização diferentes (s) para verificação de métricas como PSNR e SSIM, que medem a quantidade de informação perdida na compressão em relação à imagem original, a porcentagem de zeros na imagem depois de passar pela etapa de quantização da imagem (zeros%), e o número de bpp que representam a imagem depois da etapa da compressão na figura 3. 

Observando portanto a variação dos valores em função de s é possível perceber uma relação inversamente proporcional entre ele e as medidas de qualidade e de bpp representadas tanto na figura 3 quanto no gráfico da figura 4 que descrevem que quanto menor mais agressiva a compressão de imagem maior quantidade de informação da imagem original é perdida e menor fica o arquivo comprimido, chegando ao ponto de o bpp chegar à 1.39 bpp com escala de quantização igual a 4, ou seja, para cada 100 pixels são necessários apenas 139 bits para representá-los enquanto as métricas de qualidade da imagem apenas diminuem. 


Figura 3:













Figura 4:




Em questão da qualidade visual da imagem chega a ser imperceptível a diferença entre escalas de quantização mais baixas e mais altas, embora que ela seria muito mais evidente se fosse utilizado uma tela maior para a exibição das imagens completas na figura 5. Mas ela fica muito clara quando conseguimos isolar as mesmas coordenadas de um dos blocos de 8x8 das imagens e ver os efeitos da quantização quando o valor de s sobe principalmente para valores maiores que 2.5, que praticamente apaga os dados daquele bloco, como pode ser visto na figura 6.

Figura 5:


Figura 6:


Discussão:

Fica evidente que uma boa implementação é perfeitamente capaz de executar os algoritmos de compressão de imagens jpeg, apesar das limitações da linguagem utilizada. O fato da implementação ter sido realizada em matrizes 8x8 adicionou um pouco de complexidade ao utilizar uma imagem grande como entrada, e mesmo imagens relativamente pequenas sem muita qualidade ainda levam muito tempo para serem processadas pelo código ao ponto de que mesmo reduzido em 100x o número de pixels da imagem, ainda assim a aplicação leva alguns segundos para processar a imagem, principalmente no seu formato original em RGB que triplicava o tamanho da imagem comparado com a componente Y da conversão dela em YCbCr utilizada no projeto.
