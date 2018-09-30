# -*- coding: utf-8 -*-
#!/usr/bin/env python
from counterexample import Counterexample
from hit import TupleModelHash
from parser import stdin_parser

from itertools import chain,permutations
from misc import indent
from collections import defaultdict


def main():
    model = stdin_parser()
    assert len(model.relations) == 1
    targets_rel = tuple(sym for sym in model.relations.keys() if sym[0] == "T")
    if not targets_rel:
        print("ERROR: NO TARGET RELATIONS FOUND")
        return
    print(isOpenDef(model, targets_rel))


class Orbit(object):
    def __init__(self, o,p,t=None): #orbita, polaridad, tipo
        self.o = o
        self.p = p
        self.t = t
    def __add__(self, other):
        if self.p != other.p:
            assert False, "Contraejemplo"
        else:
            return Orbit(self.o+other.o,self.p,self.t or self.t)

class Partition(object):
    def __init__(self, universe, Tg): # universo y relacion a definir
        self.universe = universe
        self.Tg = Tg
        self.partition = {} # indexado con tuplas, contiene la orbita y la polaridad
        self.types = {} # indexado con tipos, contiene la tupla
        for t in permutations(universe,repeat=Tg.arity): # sin repeticiones? TODO
            self.partition[t]=Orbit([t],t in Tg)
    def getOrbitByType(self, t):
        if t in self.types:
            return self.partition[self.types[t]]
        else:
            return None


def isOpenDef (A, Tg):
    O = Partition(A.universe,Tg) #Inicialización de las orbitas
    S = [(A, permutations(A.universe,repeat=Tg.arity), dict())] #Inicializacion del stack
    while S:
        (E, l, r) = S.pop()
        for t in l:
            h = hit(t)
            u = l.universe()
            if len(u) == len(E): # nos quedamos en el mismo tamaño
                if h in r: # es un tipo conocido (un automorfismo para checkear)
                    gamma = h.iso(r[h])
                    if not O.propagar(gamma):
                        return False
                else: # es un tipo no conocido de potencial automorfismo
                    O.setType(t,h) #Etiqueto la orbita de t
                    r[h] = t
            else: # Genera algo mas chico
                if h in O: # es de un tipo conocido (un subiso para checkear)
                    gamma = O[h].iso(t)
                    if not O.propagar(gamma):
                        return False
                else:
                    S.append((E,l,r))
                    S.append((h.structure(),permutations(h.universe(),repeat=Tg.arity) , {h:t}))
                    O.setType(t,h) # Etiqueto la orbita de t
                    break
    return True











if __name__ == "__main__":
    main()
