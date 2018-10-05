# -*- coding: utf-8 -*-
#!/usr/bin/env python
from counterexample import Counterexample
from hit import TupleModelHash
from parser import parser

from itertools import permutations
from misc import indent
from collections import defaultdict


def main():
    model = parser()
    assert len(model.relations) == 1
    targets_rel = tuple(sym for sym in model.relations.keys() if sym[0] == "T")
    if not targets_rel:
        print("ERROR: NO TARGET RELATIONS FOUND")
        return
    print(isOpenDef(model, targets_rel[0]))


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
        self.partition = {} # indexado con tuplas, contiene la orbita
        self.types = {} # indexado con tipos, contiene la tupla
        for t in permutations(universe,r=Tg.arity): # sin repeticiones? TODO
            self.partition[t]=Orbit([t],t in Tg)

    def setType(self, Tuple, Type):
        assert Type not in self.types
        self.types[Type]=Tuple
    def __contains__(self, t):
        return t in self.types
        
    def propagar(self, gamma):
        cambio=False        
        while cambio:
            cambio=False
            for t in self.orbita:
                tp=gamma(t)
                self.unir(t,tp)
                cambio = True
                break
    
    def unir(self, t1, t2):
        o1 = self.partition[t1]
        del self.partition[t1]
        o2 = self.partition[t2]
        del self.partition[t2]
        union = o1+o2
        if union.t:
            self.types[union.t] = union.o
        for t in union.o:
            self.partition[t1]

class MicroPartition(object):
    def __init__(self,d=dict()):
        self.dict = d
        self.dictOfKeys = {k:k for k in d.keys()}
    def __contains__(self, h):
        return h in self.dict
    def representative(self, h):
        return self.dictOfKeys[h]
    def setType(self, t, h):
        self.dict[h]=t
        self.dictOfKeys[h]=h

def isOpenDef (A, Tg):
    Tg = A.relations[Tg]
    O = Partition(A.universe,Tg) #Inicialización de las orbitas
    S = [(A, permutations(A.universe,r=Tg.arity), MicroPartition())] #Inicializacion del stack
    while S:
        (E, l, r) = S.pop()
        for t in l:
            h = TupleModelHash(E,t)
            u = h.universe()
            if len(u) == len(E): # nos quedamos en el mismo tamaño
                if h in r: # es un tipo conocido (un automorfismo para checkear)
                    
                    gamma = h.iso(r.representative(h))
                    
                    if not O.propagar(gamma):
                        return False
                else: # es un tipo no conocido de potencial automorfismo
                    O.setType(t,h) #Etiqueto la orbita de t
                    r.setType(t,h)
            else: # Genera algo mas chico
                if h in O: # es de un tipo conocido (un subiso para checkear)
                    gamma = O[h].iso(t)
                    if not O.propagar(gamma):
                        return False
                else:
                    S.append((E,l,r))
                    S.append((h.structure(),permutations(h.universe(),r=Tg.arity) , MicroPartition({h:t})))
                    O.setType(t,h) # Etiqueto la orbita de t
                    break
    return True











if __name__ == "__main__":
    main()
