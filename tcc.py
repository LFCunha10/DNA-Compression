#!/usr/bin/env python
# -*- coding: utf-8 -*-

import compression
import montaImagem
import time

for x in range(0,1):

    ini = time.time()
    print 'Separa a base de dados em 2 arquivos'
    compression.separaMetadadosEGenomaEmArquivosDiferentes(x)
    print 'Codificação por referencia e divisão em 2 arquivos'
    compression.geraArquivosDeSimboloENumeros('genomaNormalizado0.txt', 0)
    print 'Gera png simbolo'
    compression.converteSequenciaEmImagemPNG('simbolo0.txt', 'dicionarioEncoderACTG.txt', 'simbolo{}.png'.format(x))
    print 'Gera png numero'
    montaImagem.montaPNG('numero',0,'numDic', x)
    print 'Gera png metadado'
    montaImagem.montaPNG('metadados', 0, 'metaDic', x)
    print 'limpa lixo'
    compression.startup()
    fim = time.time()

print fim-ini

