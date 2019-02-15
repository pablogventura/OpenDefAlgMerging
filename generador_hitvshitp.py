import datetime
from random import sample, choice, randint
import random
from itertools import product, permutations
from os import mkdir
import time

from main import isOpenDef
from parser import parser
from hit import TupleModelHash

seed = 0
random.seed(seed)
def generador(tA, t, c, fs):
    # tA es el tamaño de la estructura ambiente
    # t es la cantidad de subconjuntos
    # c es el tamaño de esos subconjuntos
    # fs es una lista de aridades de funciones
    result = '# Generated {0:%Y-%m-%d %H:%M:%S}\n'.format(datetime.datetime.now())
    result += '# Parameters: |A| = %s, |MaxSubs| = %s, |ms| = %s with ms in MaxSubs, Arities = %s\n' % (tA,t,c,fs)

    result += "# Random Seed: %s\n" % seed
    universe = set(range(tA))
    result += " ".join(str(e) for e in universe) + "\n"
    # TODO no hay que agregar al universo ambiente como subuniverso maximal?
    maxSubuniverses=[set(universe)]
    for i in range(t):
        maxSubuniverses.append(set(sample(universe, c)))
    #print(maxSubuniverses)
    #para calcular f(a,b) tomo los conjuntos que tengan a "a" y b y hago la interseccion y de ese conjunto elijo uno al azar
    # quiza conviene que f se pueda hacer conmutativa para tener una forma barata de generar mas rapdido y tener funciones que son mas rigidas
    # aca arriba se corre hit secuencial contra hit p
    for i,arity in enumerate(fs):
        result += "f%s %s\n" % (i,arity)
        for values in product(universe, repeat= arity):
            sets = [m for m in maxSubuniverses if set(values).issubset(m)]
            intersection = sets.pop()
            while sets:
                intersection = intersection & sets.pop()
            fvalues = choice(list(intersection))
            result += " ".join(str(e) for e in values) + " %s\n" % fvalues
    tarity = 3
    result += "T0 %s %s\n" % (tarity, tA**tarity)
    for i in product(universe, repeat=tarity):
        result += " ".join(map(str,i))
        result += "\n"
    return result
    

def permutador(lista, permutacion):
    result = dict()
    for i,j in enumerate(permutacion):
        result[j] = lista[i]
    return tuple(result[i] for i in range(len(lista)))


path ="testhitvshitp"
try:
    mkdir(path)
except:
    pass
for i in range(10):
    for tA in [10,20,30]:
        for t in [2,4,8]:
            for c in [3,5]:
                fs = [1,2,3]
                filename = "%s/sample_%s_%s_%s_%s.model" % (path,tA,t,c,i)
                with open(filename,"w") as f:
                    f.write(generador(tA, t, c, fs))
                model = parser(filename,False)
                targets_rels = tuple(sym for sym in model.relations.keys() if sym[0] == "T")
                if not targets_rels:
                    print("ERROR: NO TARGET RELATIONS FOUND")
                assert(isOpenDef(model, targets_rels))




















