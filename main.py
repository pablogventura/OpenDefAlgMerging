# -*- coding: utf-8 -*-

#!/usr/bin/env python
from itertools import permutations, chain, combinations

from parser import parser
from counterexample import CounterexampleTuples
from hit import TupleModelHash
from misc import indent
import sys

def main():
    model = parser(sys.argv[1])
    targets_rels = tuple(sym for sym in model.relations.keys() if sym[0] == "T")
    if not targets_rels:
        print("ERROR: NO TARGET RELATIONS FOUND")
        return
    print(isOpenDef(model, targets_rels))


class Orbit():
    def __init__(self, o, p, t=None):  # orbita, polaridad, tipo
        self.o = o
        self.p = p
        self.t = t

    def __contains__(self, t):
        return t in self.o

    def __add__(self, other):
        if self.p != other.p:
            raise CounterexampleTuples(self, other)
        if self.t is not None:
            t = self.t
        elif other.t is not None:
            t = other.t
        else:
            t = None
        return Orbit(self.o+other.o, self.p, t)

    def __repr__(self):
        if self.t is not None:
            return "(%s,%s,%s)" % (self.o, self.p, str(hash(self.t))[-4:])
        return "(%s,%s,%s)" % (self.o, self.p, self.t)



class Partition():
    def __init__(self, universe, arity, Tgs):  # universo y relacion a definir, Tgs debe venir ordenado
        self.universe = universe
        self.arity = arity
        self.partition = {}  # indexado con tuplas, contiene la orbita
        self.types = {}  # indexado con tipos, contiene la tupla
        for t in permutations(universe, r=arity):  # TODO solo cuando la aridad coincide con la relacion
            #import ipdb;ipdb.set_trace()
            self.partition[t] = Orbit([t], tuple(t in Tg for Tg in Tgs)) #TODO hacer durante el parseo, si esta en la relacion queda con true y el resto false

    def setType(self, Tuple, Type):
        #assert Type not in self.types
        self.types[Type] = Tuple
        self.getOrbit(Tuple).t = Type

    def getOrbit(self, Tuple):
        for representative in self.partition:
            if Tuple in self.partition[representative]:
                return self.partition[representative]
        raise ValueError(Tuple)

    def delOrbit(self, Tuple):
        assert self.partition
        for representative in self.partition:
            if Tuple in self.partition[representative]:
                break
        del self.partition[representative]

    def __repr__(self):
        result = "[\n"
        for representante in self.partition:
            result += "\t" + repr(self.partition[representante]) + "\n"
        result += "]\n"
        return result

    def getType(self, Tuple):
        for h in self.types:
            if Tuple in self.types[h]:
                return h
        return None

    def __len__(self):
        return len(self.partition)

    def __contains__(self, t):
        return t in self.types

    def propagar(self, gamma):
        for t in list(self.partition.keys()):
            tp = gamma.vcall(t)
            if None not in tp:
                self.unir(t, tp)

    def unir(self, t1, t2):
        if t1 == t2:
            return
        o1 = self.getOrbit(t1)
        o2 = self.getOrbit(t2)

        if o1 == o2:
            return
        self.delOrbit(t1)
        self.delOrbit(t2)
        union = o1+o2
        if union.t:
            self.types[union.t] = union.o
        self.partition[t1] = union

    def __getitem__(self, key):
        for h in self.types:
            if h == key:
                return h
        return None

    def hasKnowType(self, t):
        return self.getType(t) is not None

def propagarGrosa(Os, gamma):
    for k in Os:
        Os[k].propagar(gamma)

class MicroPartition():
    def __init__(self, d=dict()):
        self.dict = d
        self.dictOfKeys = {k: k for k in d.keys()}
    def union(self, other):
        #TODO union de microparticiones
        self.dict = dict(self.dict, **other.dict)
        self.dict = dict(self.dictOfKeys, **dictOfKeys.dict)
    def __contains__(self, h):
        return h in self.dict

    def representative(self, h):
        return self.dictOfKeys[h]

    def newType(self, t, h):
        self.dict[h] = t
        self.dictOfKeys[h] = h

def permutations_star(iterable, r=None):
    """
    Permutaciones con el orden estrella
    """
    if not r:
        r=len(iterable)
    for s in combinations(iterable, r=r):
        for t in permutations(s):
            yield t

def isOpenDef(A, Tgs):
    Tgs = sorted([A.relations[Tg] for Tg in Tgs])
    spectrum = list(sorted({Tg.arity for Tg in Tgs},reverse=True))
    Os = {e:Partition(A.universe, e, Tgs) for e in spectrum}  # Inicialización de las orbitas
    # Inicializacion del stack
    S = [(A, chain(*[permutations_star(A.universe, r=e) for e in spectrum]),{e:MicroPartition() for e in spectrum})]
    while S:
        (E, l, rs) = S.pop()
        for t in l:
            r= rs[len(t)]
            O = Os[len(t)]
            if not O.hasKnowType(t):
                h = TupleModelHash(E, t)
                u = h.universe()
                if len(u) == len(E):  # nos quedamos en el mismo tamaño
                    # es un tipo conocido (un automorfismo para checkear)
                    if h in r:
                        gamma = h.iso(r.representative(h))
                        propagarGrosa(Os,gamma)
                    else:  # es un tipo no conocido de potencial automorfismo
                        O.setType(t, h)  # Etiqueto la orbita de t
                        r.newType(t, h)
                else:  # Genera algo mas chico
                    # es de un tipo conocido (un subiso para checkear)
                    if h in O:
                        gamma = O[h].iso(h)
                        propagarGrosa(Os,gamma)
                    else:
                        S.append((E, l, rs))
                        mps= {len(t):MicroPartition({h: t})}
                        for e in spectrum:
                            if e not in mps:
                                mps[e]=MicroPartition()
                        S.append((A, chain(*[permutations_star(h.universe(), r=e) for e in spectrum]),mps))
                        O.setType(t, h)  # Etiqueto la orbita de t
                        break
    print(Os)
    print(tuple(len(Os[O]) for O in Os))
    return True

def isOpenDefTodos(A, Tgs):
    Tgs = sorted([A.relations[Tg] for Tg in Tgs])
    spectrum = list(sorted({Tg.arity for Tg in Tgs},reverse=True))
    Os = {e:Partition(A.universe, e, Tgs) for e in spectrum}  # Inicialización de las orbitas
    # Inicializacion del stack
    S = [(A, chain(*[combinations(A.universe, r=e) for e in spectrum]),{e:MicroPartition() for e in spectrum})]
    while S:
        (E, l, rs) = S.pop()
        for t in l:
            r= rs[len(t)]
            O = Os[len(t)]
            if not O.hasKnowType(t):
                h = TupleModelHash(E, t)
                u = h.universe()
                if len(u) == len(E):  # nos quedamos en el mismo tamaño
                    # es un tipo conocido (un automorfismo para checkear)
                    if h in r:
                        gamma = h.iso(r.representative(h))
                        propagarGrosa(Os,gamma)
                    else:  # es un tipo no conocido de potencial automorfismo
                        O.setType(t, h)  # Etiqueto la orbita de t
                        r.newType(t, h)
                        #PROCESAR PERMUTACIONES Y AGREGARLAS EN O Y r
                        rr = procesarPermutaciones(h,E,O,Os)
                        r.union(rr)
                else:  # Genera algo mas chico
                    # es de un tipo conocido (un subiso para checkear)
                    if h in O:
                        gamma = O[h].iso(h)
                        propagarGrosa(Os,gamma)
                    else:
                        S.append((E, l, rs))
                        mps= {len(t):MicroPartition({h: t})}
                        for e in spectrum:
                            if e not in mps:
                                mps[e]=MicroPartition()
                        #PROCESAR PERMUTACIONES Y MANDARLAS EN mps
                        rr = procesarPermutaciones(h,E,O,Os)
                        mps.union(rr)
                        S.append((A, chain(*[combinations(h.universe(), r=e) for e in spectrum]),mps))
                        O.setType(t, h)  # Etiqueto la orbita de t
                        break
    print(Os)
    print(tuple(len(Os[O]) for O in Os))
    return True

def procesarPermutaciones(h,E,O,Os):
    t = h.generator_tuple
    ml = MicroPartition()
    ml.newType(t,h)
    for gamma in islice(permutations([0,1,2,3]),1,None): # salteo la primera que es la identidad
        gammaf = lambda x:tuple(x[i] for i in gamma)
        tt = gammaf(t)
        if not O.hasKnowType(tt):
            hh = TupleModelHash(E,tt)
            if hh in ml:
                iso = hh.iso(ml.representative(hh))
                propagarGrosa(Os,iso)
            else:
                O.setType(tt, hh)  # Etiqueto la orbita de t
                ml.newType(tt, hh)
    return ml
    
if __name__ == "__main__":
    main()
