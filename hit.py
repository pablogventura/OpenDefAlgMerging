from itertools import product
from collections import defaultdict

def tuple_number(t,order):
    flath = [item for sublist in order for item in sublist]
    return tuple(flath.index(e) for e in t)


def submodel_hash(model, generators):
    # input model, generators
    generators = list(sorted(generators))
    #print(generators)
    ops = model.operations
    ops =defaultdict(set)
    for op in model.operations:
        ops[model.operations[op].arity].add(model.operations[op])
    
    H = [generators]
    i = len(generators)-1
    T = defaultdict(set, {a:{i}  for i, a in enumerate(generators)})
    print (T)
    O = H[-1]
    V=list(generators)

    while O:
        H.append([])
        for ar in sorted(ops):
        
            flath = [item for sublist in H for item in sublist]
            o = H[-2]
            for tup in product(flath, repeat=ar):
                i += 1  
                if any(t in o for t in tup):
                    for sym_i,f in enumerate(sorted(ops[ar],key=lambda f: f.sym)):
                        print(tup)
                        print(i)
                        x = f(*tup)
                        V.append(x)
                        T[x].add(i)
                        if all(x not in h for h in H):
                            H[-1].append(x)
        O = H[-1]
    return V,H,T


class SubmodelHash(object):
    """
    Clase de HIT, toma un modelo ambiente y los elementos generadores
    """
    def __init__(self,model, generators):
        pass
    def __eq__(self,other):
        return self.T == other.T
    

def TupAd(h, k):
    # devuelve una tupla de largo k con por lo menos un obligatorio
    # que estan en el penultimo lugar de h

    flath = [item for sublist in h for item in sublist]
    o = h[-2]
    for tup in product(flath, repeat=k):
        if any(t in o for t in tup):
            yield tup


if __name__ == "__main__":
    from parser import stdin_parser
    model = stdin_parser()
    print(submodel_hash(model,[0,1]))

