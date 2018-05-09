from itertools import product
from collections import defaultdict
from misc import indent

def tuple_number(t,order):
    flath = [item for sublist in order for item in sublist]
    return tuple(flath.index(e) for e in t)

class SubmodelHash(object):
    """
    Clase de HIT, toma un modelo ambiente y la tupla generadora
    """
    def __init__(self,model, generators):
        # input model, generators
        generators = list(generators)
        self.generators = generators
        self.model = model
        ops = model.operations
        ops =defaultdict(set)
        for op in model.operations:
            ops[model.operations[op].arity].add(model.operations[op])
        
        self.H = [generators]
        i = len(generators)-1
        self.T = defaultdict(set, {a:{i}  for i, a in enumerate(generators)})
        O = self.H[-1]
        V=list(generators)

        while O:
            self.H.append([])
            for ar in sorted(ops):
            
                flath = [item for sublist in self.H for item in sublist]
                o = self.H[-2]
                for tup in product(flath, repeat=ar):
                    i += 1  
                    if any(t in o for t in tup):
                        for sym_i,f in enumerate(sorted(ops[ar],key=lambda f: f.sym)):
                            x = f(*tup)
                            V.append(x)
                            self.T[x].add(i)
                            if all(x not in h for h in self.H):
                                self.H[-1].append(x)
            O = self.H[-1]
    def __eq__(self,other):
        return self.self.T == other.self.T
    def __repr__(self):
        result = "TupleModelHash(\n"
        result += indent("Tuple=%s,\n" % self.generators)
        result += indent("History=%s,\n" % self.H)
        result += indent("Type=%s,\n" % dict(self.T))
        result += ")"
        return result
    

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

