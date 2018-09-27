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


class setSized(object):
    def __init__(self, values=[]):
        self.dict = defaultdict(set)
        for v in values:
            self.add(v)

    def add(self, e):
        self.dict[len(e)].add(e)

    def __iter__(self):
        print("WARNING: __iter__ setSized")
        for i in self.sizes():
            for v in self.iterate(i):
                yield v

    def __len__(self):
        return sum(self.len(s) for s in self.sizes())

    def len(self, size):
        return len(self.dict[size])

    def sizes(self):
        return sorted(self.dict.keys())

    def iterate(self, size):
        return iter(self.dict[size])


class GenStack(object):
    def __init__(self, generator):
        self.stack = [generator]
        self.history = set()

    def add(self, generator):
        self.stack.append(generator)

    def next(self):
        result = None
        while result is None or frozenset(result.universe) in self.history:
            try:
                result = next(self.stack[-1])
            except IndexError:
                raise StopIteration
            except StopIteration:
                del self.stack[-1]
        self.history.add(frozenset(result.universe))
        return result


def is_open_relold(model, target_rels):
    base_rels = tuple((r for r in model.relations if r not in target_rels))
    spectrum = sorted(model.spectrum(target_rels), reverse=True)
    if spectrum:
        size = spectrum[0]
    else:
        size = 0
    print("Spectrum = %s" % spectrum)
    isos_count = 0
    auts_count = 0
    S = setSized()

    genstack = GenStack(model.substructures(size))
    try:
        while True:
            try:
                current = genstack.next()
            except StopIteration:
                break
            iso = is_isomorphic_to_any(current, S, base_rels)
            if iso:
                isos_count += 1
                if not iso.iso_wrt(target_rels):
                    raise Counterexample(iso)
            else:
                for aut in automorphisms(current, base_rels):
                    auts_count += 1
                    if not aut.aut_wrt(target_rels):
                        raise Counterexample(aut)
                S.add(current)

                try:
                    # EL SIGUIENTE EN EL ESPECTRO QUE SEA MAS CHICO QUE LEN DE SUBUNIVERSE
                    size = next(x for x in spectrum if x < len(current))
                    genstack.add(current.substructures(size))
                except StopIteration:
                    # no tiene mas hijos
                    pass
        print("DEFINABLE")
        print("\nFinal state: ")

    except Counterexample as ce:
        print("NOT DEFINABLE")
        print("Counterexample:")
        print(indent(repr(ce.ce)))
        print("\nState before abort: ")
    except KeyboardInterrupt:
        print("CANCELLED")
        print("\nState before abort: ")

    print("  Diversity = %s" % len(S))
    for size in S.sizes():
        print("    %s-diversity = %s" % (size, S.len(size)))
    print("  #Auts = %s" % auts_count)
    print("  #Isos = %s" % isos_count)
    print("  %s calls to Minion" % MinionSol.count)



TP=set()
def isOpenDef(A, Tg):

    global TP 

    T=set() # Tipos procesandose

    V=set() # Viejos

    for t in permutations(list(A.universe),A.relations[Tg[0]].arity):
        print (V, t)
        if set(t).issubset(V):
            continue
        H=TupleModelHash(A,t)
        for HH in T.union(TP):#Es un tipo conocido
            if H==HH:
                if H in TP: #Es un tipo totalmente procesado
                    V=V.union(H.universe()) #Pasa a ser viejo
                if not H.iso(HH).iso_wrt(Tg): # no preserva Tg
                    print(H.iso(HH))
                    return False
                else:
                    return True
        # Es un tipo nuevo
        if len(A)==len(H.universe()): #Es un automorfismo
            for HH in T:
                if not H.iso(HH).iso_wrt(Tg): # Si T=set(), preserva trivialmente
                    print(H.iso(HH))
                    return False
            T.add(H) #Pasa a ser un tipo en proceso

        else: #Es un un subiso
            ts=isOpenDefR(H,V,A,Tg) #Baja en el árbol
            if ts:
                V=V.union(H.universe()) # Pasa a ser viejo
                TP=TP.union(ts) #Pasan a ser tipos procesados
            else:
                print("recursivo")
                return False
    return True






def isOpenDefR(H,V,A,Tg):

    global TP 

    T=set() # Tipos procesandose
    print (A.universe,H.universe())
    gen=permutations(H.tuple()+list(A.universe-H.universe()),A.relations[Tg[0]].arity)

    next(gen) #Se saltea la primer tupla que es \text{tupla}(H)

    for t in gen:

        if [v for v in V if set(t) in v]:
            continue

        H0=TupleModelHash(A,t)
        for HH in T.union(TP):#Es un tipo conocido
            if H0==HH:
                if H in TP: #Es un tipo totalmente procesado
                    V=V+H0.universe() #Pasa a ser viejo
                if not H0.iso(HH).iso_wrt(Tg): # no preserva Tg
                    print ( H0.iso(HH))
                    return set()
                else:
                    return T
        if len(H.universe())==len(H0.universe()): #Es un automorfismo
            if not H.iso(H0).iso_wrt(Tg): # no preserva Tg
                print(H.iso(H0))
                return set()
            T.add(H0) #Pasa a ser un tipo en proceso
        else: #Es un un subiso
            ts=isOpenDefR(H0,V,A,Tg) #Baja en el árbol
            if ts:
                V=V.union(H0.universe()) #Pasa a ser viejo
                TP.add(ts) # Pasan a ser tipos procesados
            else:
                print ("recursivo")
                return set()
    return T


class Orbit(object):
    class __init__(self, o,p,t=None): #orbita, polaridad, tipo
        self.o = o
        self.p = p
        self.t = t
    class __add__(self, other):
        if self.p != other.p:
            assert False, "Contraejemplo"
        else:
            return Orbit(self.o+other.o,self.p,self.t or self.t)

class Partition(object):
    class __init__(self, universe, Tg): # universo y relacion a definir
        self.universe = universe
        self.Tg = Tg
        self.partition = {}
        for t in permutations(universe,repeat=Tg.arity): # sin repeticiones? TODO
            self.partition[t]=Orbit([t],t in Tg, None)


def isOpenDef (A, Tg):
    O = Partition(A.universe,Tg) #Inicialización de las órbitas
    S = [(A, permutations(A.universe,repeat=Tg.arity), set())] #Inicializacion del stack
    while S:
        (E, l, r) = S.pop()
        for t in l:
            u = A.generateUniverse(l)
            if len(u) == len(E):
                if hay (t , e ) ∈ r con e = e then
                    γ = iso (t,t')
                    if ¬ propagar ( γ ,O) then
                        return False
                    end if
                else
                    (
                    (t,O)) = e
                    r = r ∪ {(t, e)}
                    . Etiqueto la orbita de t
                    tipo orbitaDe
                end if
            else
                if hay (T u, p, e 0 ) ∈ O con e = e 0
                    t = Tu[0]
                    γ = iso (t,t')
                    if ¬ propagar ( γ ,O) then
                        . Genera algo mas chico
                        then
                        . Tomo el primero como representante
                        return False
                    end if
                else
                    (E,l,r)
                     
                    (S, ( U k , {t, e}) )
                    tipo ( orbitaDe (t,O)) = e
                    push
                    push # Etiqueto la orbita de t
                    break
                end if
            end if
        end while
    end while
    return True
end function











if __name__ == "__main__":
    main()
