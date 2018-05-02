from itertools import product
from collections import defaultdict

def tuple_number(t,order):
    flath = [item for sublist in order for item in sublist]
    return tuple(flath.index(e) for e in t)


def submodel_hash(model, generators):
    # input model, generators
    generators = list(sorted(generators))
    ops = model.operations
    ops =defaultdict(set)
    for op in model.operations:
        ops[model.operations[op].arity].add(op)
    
    H = [generators]
    i = len(generators)
    T = defaultdict(set, {a:{(len(H)-1,-1,(i,))}  for i, a in enumerate(generators)})
    O = H[-1]

    while O:
        H.append([])
        for ar in sorted(ops):
            for tup in TupAd(H, ar):
                i += 1  
                for sym_i,f in enumerate(sorted(ops[ar],key=lambda f:f[0])):
                    f=f[1]
                    x = f(*tup)
                    if any(x in h for h in H):
                        T[x].add((i,sym_i,tuple_number(tup,H)))
                    else:
                        T[x].add((i,sym_i,tuple_number(tup,H)))
                        H[-1].append(x)
            i = 0
        O = H[-1]
    return H, T


class SubmodelHash(object):
    """
    Clase de HIT, toma un modelo ambiente y los elementos generadores
    """
    def __init__(self,model, generators):
        generators = list(sorted(generators))
        ops = model.operations
        H = [generators]
        i = len(generators)
        T = defaultdict(set, {a:{(len(H)-1,-1,(i,))}  for i, a in enumerate(generators)})
        O = H[-1]

        while O:
            H.append([])
            for ar in sorted(ops):
                for tup in TupAd(H, ar):
                    i += 1  
                    for sym_i,f in enumerate(sorted(ops[ar],key=lambda f:f[0])):
                        f=f[1]
                        x = f(*tup)
                        if any(x in h for h in H):
                            T[x].add((i,sym_i,tuple_number(tup,H)))
                        else:
                            T[x].add((i,sym_i,tuple_number(tup,H)))
                            H[-1].append(x)
                i = 0
            O = H[-1]
        self.H = H
        self.T = T
    def __eq__(self,other):
        return self.T == other.T
    

def TupAd(h, k):
    # devuelve una tupla de largo k con por lo menos un obligatorio
    # que estan en el penultimo lugar de h

    flath = [item for sublist in h for item in sublist]
    # print flath
    o = h[-2]
    print((flath,k))
    for tup in product(flath, repeat=k):
        if any(t in o for t in tup):
            yield tup


if __name__ == "__main__":
    from parser import stdin_parser
    model = stdin_parser()
    print(submodel_hash(model,[0,1,2]))

