from heapq import heappush, heappop, heapify
from collections import defaultdict
import compression


def encode(symb2freq):
    """Huffman encode the given dict mapping symbols to weights"""
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
    return sorted(heappop(heap)[1:], key=lambda p: (len(p[-1]), p))





def buildHuffman(dado, nomeDic, numDado):

    k = open('{}{}.txt'.format(dado, numDado), 'rb')
    txt = k.read()
    
    
    if dado == 'numero':
        txt = txt.split(';')
        vec2 = []
        vec = []
        for x in range(len(txt)-1):
            vec2.append(int(txt[x]))
        vec = compression.compactacaoPorDiferenca(vec2)
        del txt
        txt = vec[:]
        k.close()
        k = open('{}{}.txt'.format(dado, numDado), 'wb')
        for x in txt:
            k.write('{};'.format(x))

    k.close()
    k = open('{}.txt'.format(nomeDic), 'wb')

    if dado == 'metadados':
        vec2 = []
        for x in range(len(txt)-1):
            if x != '':
                vec2.append(txt[x])
        del txt
        txt = vec2[:]


    symb2freq = defaultdict(int)
    for ch in txt:
        if x != '':
            symb2freq[ch] += 1

    huff = encode(symb2freq)
    #print "Symbol\tWeight\tHuffman Code"
    v = []
    for p in huff:
        v.append(p[0])
        v.append(p[1])
        #print "%s\t%s\t%s" % (p[0], symb2freq[p[0]], p[1])

    for x in v:
        k.write("%s;" % x)

    k.close()

    if(dado != 'metadados'):
        with open('metadados{}.txt'.format(numDado), 'rb') as myfile:
            arquivo = myfile.read()
        myfile.close()

        myfile = open('metadados{}.txt'.format(numDado), 'wb')
        temp = open('{}.txt'.format(nomeDic), 'rb')
        metaHuff = temp.read()

        myfile.write('{}\nmetaHuff\n{}\n{}'.format(arquivo,dado,metaHuff))

        myfile.close()

    del p, vec2, txt, symb2freq
    return v


    
#buildHuffman('numero', 'simbDic', 0)


