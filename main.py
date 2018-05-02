# -*- coding: utf-8 -*-
#!/usr/bin/env python
from counterexample import Counterexample
from hit import submodel_hash
from parser import stdin_parser

from itertools import chain
from misc import indent
from collections import defaultdict


def main():
    model = stdin_parser()
    assert len(model.relations) == 1
    targets_rel = tuple(sym for sym in model.relations.keys() if sym[0] == "T")
    if not targets_rel:
        print("ERROR: NO TARGET RELATIONS FOUND")
        return
    is_open_rel(model, targets_rel)


class SetSized(object):
    def __init__(self, values=[]):
        self.dict = defaultdict(set)
        for v in values:
            self.add(v)

    def add(self, e):
        self.dict[len(e)].add(e)

    def __iter__(self):
        print("WARNING: __iter__ SetSized")
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


def is_open_rel(model, target_rels):
    base_rels = tuple((r for r in model.relations if r not in target_rels))
    spectrum = sorted(model.spectrum(target_rels), reverse=True)
    if spectrum:
        size = spectrum[0]
    else:
        size = 0
    print("Spectrum = %s" % spectrum)
    isos_count = 0
    auts_count = 0
    S = SetSized()

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




def isOpenDef(A, R, F, Tg):

    global TP= set() # Tipos totalmente procesados

    T=set() # Tipos procesandose

    V=set() # Viejos

    for t in permutations(list(A),Tg.arity):
        if [v for v in V if t in v]:
            continue
        H=submodel_hash(A,t)
        for HH in T.union(TP):#Es un tipo conocido
            if H==HH:
                if H in TP: #Es un tipo totalmente procesado
                    V=V+H.universe() #Pasa a ser viejo
                if not H.iso(HH).iso_wrt(Tg) # no preserva Tg
                    return False
        else:  # Es un tipo nuevo

            if len(A)==len(H.universe): #Es un automorfismo}
                for HH in T:
                    if not H.iso(HH).iso_wrt(Tg): # Si T=set(), preserva trivialmente
                        return False
                T.add(H) #Pasa a ser un tipo en proceso}

            else: #Es un un subiso
                ts=isOpenDefR(H,V,R,F,Tg) #Baja en el árbol
                if ts:
                    V=V + H.universe() # Pasa a ser viejo
                    TP=TP + ts #Pasan a ser tipos procesados
                else:
                    return False
    return True


























if __name__ == "__main__":
    main()
