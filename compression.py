#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from random import randint
from tqdm import *
import pickle
import png
from math import sqrt
from shutil import copyfile
import os
from heapq import heappush, heappop, heapify
import collections
from collections import Counter
import sys
import math
import zlib
import struct

def separaMetadadosEGenomaEmArquivosDiferentes(arquivo):
    myFile          = open('genoma{}.fsa'.format(arquivo), "r")

    metadadosFile   = open('metadados0.txt',"a+")
    genomaFile      = open('genomaNormalizado0.txt',"a+")
    cont = 0
    
    for line in myFile:
        if(line[0] == '>'):
            metadadosFile.write("%s\n" % cont)
            metadadosFile.write(line[0:-1]+"\n")
        else:
            for x in line:
                if (x!='N' and x!= '\n'):
                    genomaFile.write(x)
        
            cont += len(line[0:-1])

    myFile.close()
    metadadosFile.close()
    genomaFile.close()

def selecionaStringDeReferencia(arquivo, tamanho):
    a = 0
    c = 0
    g = 0
    t = 0
    k = ''
    myFiles = open(arquivo, 'r')
    dado = myFiles.readline()
    myFiles.close()
    for x in dado:
        if x == 'A':
            a+=1
        if x == 'C':
            c+=1
        if x == 'G':
            g+=1
        if x == 'T':
            t+=1

    if a > c and a > g and a > t:
        k = 'A'
    if c > g and c > t and c > a:
        k = 'C'
    if g > t and g > a and g > c:
        k = 'G'
    if t > a and t > c and t > g:
        k = 'T'

    x = [k for z in range(4)]
    print x
    return x

def constroiArquivoTemporarioDeDadoCompactado(arquivo, referencia):
    myFiles = open(arquivo, 'r')
    dado = myFiles.readline()
    myFiles.close()

    cont = 0
    tamanho = len(referencia)
    contRecorrencia = 0
    copyfile(arquivo, arquivo + ".backup")

    myFiles = open(arquivo, 'wb')
    for x in range(len(dado)):
        if cont == tamanho:
            cont = 0
        if dado[x] == referencia[cont]:
            contRecorrencia+=1
        else:
            string = '{}.{}.'.format(contRecorrencia, dado[x])
            myFiles.write(string.encode('utf-8'))
            contRecorrencia+=1
        cont+=1
    string = '{}.{}.'.format(contRecorrencia, dado[x])
    myFiles.write(string.encode('utf-8'))
    myFiles.close()

def geraArquivosDeSimboloENumeros(arquivo, nivel):
    tamanho = 4
    referencia = selecionaStringDeReferencia(arquivo, tamanho)
    constroiArquivoTemporarioDeDadoCompactado(arquivo, referencia)

    myFiles = open(arquivo, 'r')
    dado = myFiles.readline()
    dado = dado.split(".")
    dado = dado[:-1]
    myFiles.close()

    cont = 0
    contRecorrencia = 0
    simboloStr = ""
    numeroStr = ""

    simbolo = open('simbolo{}.txt'.format(nivel), 'w')
    numero = open('numero{}.txt'.format(nivel), 'w')

    print(referencia)
    count = 0
    for x in dado:
        if count % 2 == 1:
            simbolo.write('{}'.format(x))
        else:
            
            numero.write('{};'.format(x))
        count += 1

    simbolo.close()
    numero.close()



def converteSequenciaEmImagemPNG(nomeSequencia, dicionarioArq, nomeDaImagemPNG):
    dicionario = open(dicionarioArq, 'rb')
    dicionarioEncoder = pickle.load(dicionario)
    dicionario.close()

    """ Abre o arquivo onde está a base de dados"""
    myFile = open(nomeSequencia, 'r')
    arquivo = myFile.readline()
        #if nomeSequencia == 'numero.txt':
    arquivo.split(';')
    
    myFile.close()
    tamanho = 4
    vec = np.empty(int(len(arquivo) / 4), dtype=int)
    count   = 0
    aux = ''
    for x in range(0, len(arquivo)-tamanho, tamanho):
        for k in range(4):
            aux += arquivo[x+k]
        vec[count] = dicionarioEncoder[aux]
        aux = ''
        count += 1

    del(arquivo)

    """Conta quantos itens existe na base"""
    tamanhoDaSequencia = len(vec)
    #for x in vec:
    #    tamanhoDaSequencia = tamanhoDaSequencia +1

    """Define um "quadrado" onde a imagem será criada. Note que o +1 é para compensar o truncamento do int"""
    root = int(sqrt(tamanhoDaSequencia))
    tamX = root+1
    tamY = root

    """Declara a matriz-imagem"""
    #matriz = [0] * tamX
    matriz = [[0 for i in range(tamX)] for j in range(tamY)]

    a=0
    """Laço para a adicionar à cada posição matriz uma cor, para gerar a imagem"""
    for i in range(tamY):
        for j in range(tamX):
            matriz[i][j] = int(vec[i * tamY + j])

    """Construtor da imagem"""
    s = map(lambda x: map(int, x), matriz)

    f = open(nomeDaImagemPNG, 'wb')
    w = png.Writer(len(matriz[0]), len(matriz), greyscale=True, bitdepth=8)
    w.write(f, s)
    f.close()


def compactacaoPorCarreira(vec):
    contRecorrencia = 1
    referencia = vec[0]
    vec2 = np.zeros(len(vec) * 2, dtype=np.int)

    cont = 0
    for x in range(1, len(vec)):
        if vec[x] == referencia:
            contRecorrencia += 1
        else:
            vec2[cont] = referencia
            vec2[cont + 1] = contRecorrencia
            referencia = vec[x]
            contRecorrencia = 1
            cont += 2

    cont = len(vec) - 1
    for x in range(len(vec) - 1, 1, -1):
        if(vec2[x] != 0):
            cont = x
            break

    return vec2[:cont + 1]

def compactacaoPorDiferenca(vec):
    vec2 = []
    vec2.append(vec[0])
    for x in range(1, len(vec)):
        vec2.append(vec[x] - vec[x - 1])
    return vec2

def codificaArquivoDeNumero(arquivo, saida):
    #copyfile(arquivo, arquivo + ".backup")

    myFile = open(arquivo, 'r')
    dad = myFile.readline()

    vec = np.zeros(len(dad), dtype=np.int)
    count = 0
    for x in dad:
        vec[count] = int(x)
        count+=1
    del dad
    myFile.close()

    #for i in range(0, 1):
    vec2 = compactacaoPorCarreira(vec)
    print(len(vec2), len(vec))
    input()
    del vec
    #vec = compactacaoPorCarreira(vec2)
    #del vec2

    myFile = open(saida, 'w')
    myFile.write(string)


    myFile.close()
    #del vec

def computaHuffman(arquivo, saida):
    file = open(arquivo, 'r')
    txt = file.read()
    txt = txt.split()

    symb2freq = Counter(txt)        

    heap = [[wt, [sym, ""]] for sym, wt in symb2freq.items()]
    heapify(heap)
    while len(heap) > 1:
        lo = heappop(heap)
        hi = heappop(heap)
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])

    huffmanList = sorted(heappop(heap)[1:], key=lambda p: (len(p[-1]), p))
    dictionary = {}

    for i in huffmanList:
        dictionary[i[0]] = i[1]

    del huffmanList
    
    txtNew = ""
    for x in txt:
        txtNew += dictionary[x]

    myFiles = open(saida, 'wb')
    for i in range(0, len(txtNew), 23):
        bitsToWrite = txtNew[i:i+23]
        myFiles.write('%s' % bitsToWrite)
    myFiles.close()



def computaLZ77(arquivo, saida):
    MESSAGE = b""
    with open(arquivo, 'rb') as myFile:
        MESSAGE = myFile.read()
    myFile.close()

    compressed_message = zlib.compress(MESSAGE)

    saida = open(saida, 'wb')
    saida.write(compressed_message)
    saida.close()

def startup():
    if os.path.exists("genomaNormalizado0.txt"):
        os.remove("genomaNormalizado0.txt")
    if os.path.exists("numero0.txt"):
        os.remove("numero0.txt")
    if os.path.exists("simbolo0.txt"):
        os.remove("simbolo0.txt")
    if os.path.exists("metadados0.txt"):
        os.remove("metadados0.txt")
    if os.path.exists("genomaNormalizado0.txt.backup"):
        os.remove("genomaNormalizado0.txt.backup")
    if os.path.exists("metaDic.txt"):
        os.remove("metaDic.txt")
    if os.path.exists("numDic.txt"):
        os.remove("numDic.txt")

#startup()
#separaMetadadosEGenomaEmArquivosDiferentes('genoma0.fsa')
#geraArquivosDeSimboloENumeros("genomaNormalizado0.txt", 0)
#converteSequenciaEmImagemPNG("genomaNormalizado0.txt", "dicionarioEncoderACTG.txt", "simbolo.png")
#converteSequenciaEmImagemPNG("numero0.txt", "dicionarioEncoder0123.txt", "simbolo0123.png")
#converteSequenciaEmImagemPNG("simbolo0.txt", "dicionarioEncoderACTG.txt", "simboloACTG.png")
#computaHuffman("numero0.txt", "NUMERO.txt")
#computaLZ77("numero0.txt", "NUMERO0.bin")
#computaHuffman("metadados0.txt", "METADADOS.bin")
