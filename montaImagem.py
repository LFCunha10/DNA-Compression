#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pickle
import png
from random import *
import numpy as np
from math import sqrt
import Huffman

def montaPNG(material, numDado, dadoDic, refImg):
    print 'montando'
    v = []
    v = Huffman.buildHuffman(material, dadoDic, numDado)
    

    with open('{}.txt'.format(dadoDic), 'rb') as myfile:
        arquivo = myfile.read()
    myfile.close()

    dado = arquivo.split(';')
    dict = {}

    
    for x in range(0, len(dado)-1, 2):
        dict[dado[x]] = dado[x+1]


    del dado, arquivo
    

    myFile = open('{}{}.txt'.format(material, numDado), 'rb')
    arq = myFile.read()
    if material == 'numero':
        arq = arq.split(';')
        ab = ''
        vec = []
        for x in range(len(arq)-1):
            ab += str(dict[arq[x]])
    else:
        del dict
        dict = {}
        for x in range(0, len(v)-1, 2):
            dict[v[x]] = v[x+1]
        print dict
        ab = ''
        vec = []
        for x in arq:
            ab += str(dict[x])

    for x in ab:
        vec.append(x)

    """Conta quantos ítens existe na base"""
    tamanhoDaSequencia = len(vec)

    """Define um "quadrado" onde a imagem será criada. Note que o +1 é para compensar o truncamento do int"""
    root = int(sqrt(tamanhoDaSequencia))
    tamX  = root+1
    tamY = root

    """Declara a matriz-imagem"""
    matriz = [[0 for i in range(tamX)] for j in range(tamY)]

    a=0
    """Laço para a adicionar à cada posição matriz uma cor, para gerar a imagem"""

    for i in range(tamY):
        for j in range(tamX):
            if(a<tamanhoDaSequencia):
                matriz[i][j] = int(vec[a])
                a=a+1
            else:
                break
    """Construtor da imagem"""
    s = map(lambda x: map(int, x), matriz)

    f = open('{}{}.png'.format(material, refImg), 'wb')
    w = png.Writer(len(matriz[0]), len(matriz), greyscale=True, bitdepth=1)
    w.write(f, s)
    f.close()
    del matriz, vec, ab, dict, tamX, tamY, arq, v








