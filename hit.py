from itertools import product
from collections import defaultdict
from misc import indent
from isomorphisms import Isomorphism

class TupleModelHash(object):
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
                    import ipdb;ipdb.set_trace()
                    if any(t in o for t in tup):
                        for sym_i,f in enumerate(sorted(ops[ar],key=lambda f: f.sym)):
                            x = f(*tup)
                            V.append(x)
                            self.T[x].add(i)
                            if all(x not in h for h in self.H):
                                self.H[-1].append(x)
            O = self.H[-1]
        self.H.pop()
        self.T = {k:frozenset(self.T[k]) for k in self.T}
    def __eq__(self,other):
        return set(self.T.values()) == set(other.T.values())
    
    def __hash__(self):
        return hash(frozenset(self.T))
    
    def iso(self,other):
        if self == other:
            flatSelfh = [item for sublist in self.H for item in sublist]
            flatOtherh = [item for sublist in other.H for item in sublist]
            d={(flatSelfh[i]):flatOtherh[i] for i in range(len(flatSelfh))}
            return Isomorphism(d,self.model.restrict(self.universe()),other.model.restrict(other.universe()),None)
        else:
            return None
    
    def tuple(self):
        return self.generators
    
    def universe(self):
        return set([item for sublist in self.H for item in sublist])
    
    def __repr__(self):
        result = "TupleModelHash(\n"
        result += indent("Tuple=%s,\n" % self.generators)
        result += indent("History=%s,\n" % self.H)
        result += indent("Type=%s,\n" % dict(self.T))
        result += ")"
        return result
    
    def hit_p(self,perm):
        n=B[-1]
        pi = perm 
        s = perm
        for h in range(1,len(H)):
            n=1+sum(len(self.generators)**self.model.operations[op].arity for op in self.model.operations)
            def pi(i):
                b = "{0:b}".format(i-(n+1))
                b = map(int, list(("0" * (len(self.generators) - len(b))) + b))
                b = map(perm,b)
                b = int("".join(b),2)
                return b
            s_old = s
            def s(i):
                if min(T[alpha]) in H[h-1] and i == min(j for j in T[alpha]):
                    return pi(i)
                else:
                    return s_old(i)
        for alpha in T.keys():
            for i in T[alpha]:
                TT[alpha].append(s(i))
        
        return TT


if __name__ == "__main__":
    from parser import parser
    model = parser()
    ta = [2,1]
    tb= [1,2]
    print(TupleModelHash(model,ta))
    print(TupleModelHash(model,tb))
    print(TupleModelHash(model,ta)==TupleModelHash(model,tb))
