# -*- coding: utf-8 -*-

#!/usr/bin/env python
from itertools import permutations

from parser import parser
from counterexample import CounterexampleTuples
from hit import TupleModelHash
from misc import indent


def main():
    model = parser()
    assert len(model.relations) == 1
    targets_rel = tuple(sym for sym in model.relations.keys() if sym[0] == "T")
    if not targets_rel:
        print("ERROR: NO TARGET RELATIONS FOUND")
        return
    print(isOpenDef(model, targets_rel[0]))


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
        return Orbit(self.o+other.o, self.p, self.t or self.t)

    def __repr__(self):
        if self.t is not None:
            return "(%s,%s,%s)" % (self.o, self.p, str(hash(self.t))[-4:])
        return "(%s,%s,%s)" % (self.o, self.p, self.t)


class Partition():
    def __init__(self, universe, Tg):  # universo y relacion a definir
        self.universe = universe
        self.Tg = Tg
        self.partition = {}  # indexado con tuplas, contiene la orbita
        self.types = {}  # indexado con tipos, contiene la tupla
        for t in permutations(universe, r=Tg.arity):  # sin repeticiones? TODO
            #import ipdb;ipdb.set_trace()
            self.partition[t] = Orbit([t], t in Tg)

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
        print("unir %s con %s" % (t1, t2))
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


class MicroPartition():
    def __init__(self, d=dict()):
        self.dict = d
        self.dictOfKeys = {k: k for k in d.keys()}

    def __contains__(self, h):
        return h in self.dict

    def representative(self, h):
        return self.dictOfKeys[h]

    def newType(self, t, h):
        self.dict[h] = t
        self.dictOfKeys[h] = h


def isOpenDef(A, Tg):
    Tg = A.relations[Tg]
    O = Partition(A.universe, Tg)  # Inicialización de las orbitas
    # Inicializacion del stack
    S = [(A, permutations(A.universe, r=Tg.arity), MicroPartition())]
    while S:
        (E, l, r) = S.pop()
        print(O)
        print("pop")
        for t in l:
            print(t)
            if not O.hasKnowType(t):
                h = TupleModelHash(E, t)
                u = h.universe()
                if len(u) == len(E):  # nos quedamos en el mismo tamaño
                    # es un tipo conocido (un automorfismo para checkear)
                    if h in r:

                        gamma = h.iso(r.representative(h))

                        O.propagar(gamma)
                    else:  # es un tipo no conocido de potencial automorfismo
                        O.setType(t, h)  # Etiqueto la orbita de t
                        r.newType(t, h)
                else:  # Genera algo mas chico
                    # es de un tipo conocido (un subiso para checkear)
                    if h in O:
                        gamma = O[h].iso(h)
                        O.propagar(gamma)
                    else:
                        S.append((E, l, r))
                        S.append(
                            (A, permutations(h.universe(), r=Tg.arity), MicroPartition({h: t})))
                        print("append")
                        O.setType(t, h)  # Etiqueto la orbita de t
                        break
    print(O)
    return True


if __name__ == "__main__":
    main()
