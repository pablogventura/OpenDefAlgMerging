from itertools import product
from collections import defaultdict
from misc import indent
from isomorphisms import Isomorphism

def int2base(x, base, size=None):
    assert x>=0
    if x == 0:
        digits = [0]
    else:
        digits = []
        while x:
            digits.append(x % base)
            x = int(x / base)
        digits.reverse()
    if size:
        if size < len(digits):
            raise ValueError
        else:
            digits = ([0] * (size-len(digits))) + digits
    return digits

def base2int(x,base):
    result = 0
    for i,value in enumerate(reversed(x)):
        result+=value*base**i
    return result
    
class TupleModelHash(object):
    """
    Clase de HIT, toma un modelo ambiente y la tupla generadora
    """
    def __init__(self,model, generators, THV = None):
        # input model, generators
        generators = list(generators)
        self.generators = generators
        self.model = model
        if THV:
            self.T,self.H,self.V = THV
        else:
            ops = model.operations
            ops =defaultdict(set)
            for op in model.operations:
                ops[model.operations[op].arity].add(model.operations[op])
            
            self.H = [generators]
            i = len(generators)-1
            self.T = defaultdict(set, {a:{i}  for i, a in enumerate(generators)})
            O = self.H[-1]
            self.V=list(generators)

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
                                self.V.append(x)
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
        sigma = list(perm)
        n = len(perm)
        for b in range(len(self.H)):
            for op in self.model.operations:
                n+=n**self.model.operations[op].arity
                b_1 = len(perm) # final del bloque anterior
                for i in range(b_1,n):
                    s_i = int2base(i-b_1,len(self.generators),self.model.operations[op].arity)
                    s_i = [sigma[x] for x in s_i]
                    s_i = base2int(s_i,len(self.generators)) + b_1
                    perm.append(s_i)
        VV = [perm[i] for i in self.V]
        
        return perm

if __name__ == "__main__":
    from parser import parser
    model = parser("./retrombo.model")
    ta = [2,1]
    f = TupleModelHash(model,ta).hit_p([1,0])
    print (f)
