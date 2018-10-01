from itertools import product
from collections import defaultdict
from misc import indent
from isomorphisms import Isomorphism

def int2base(x, base, size=None):
    valor = x
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
            raise ValueError("%s en base %s da %s, que no entra en %s digitos" % (valor,base,digits,size))
        else:
            digits = ([0] * (size-len(digits))) + digits
    return digits

def base2int(x,base):
    result = 0
    for i,value in enumerate(reversed(x)):
        result+=value*base**i
    return result

def permute(l,perm):
    return [l[perm[i]] for i in range(len(l))]
    
class TupleModelHash(object):
    """
    Clase de HIT, toma un modelo ambiente y la tupla generadora
    """
    def __init__(self,model, generators, TH = None):
        # input model, generators
        generators = list(generators)
        self.generators = generators
        self.model = model
        if TH:
            self.T,self.H = TH
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
            self.T = {k:frozenset(self.T[k]) for k in self.T}
            self.H.pop(-1)
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

    def structure(self):
        return self.model.restrict(self.universe())
    
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
        H=[]
        for Ha in self.H: # Ha historia actual
            if not Ha:
                continue
            H.append(sorted(Ha,key=lambda x:perm[min(self.T[x])]))
            for op in self.model.operations:
                n+=len(sigma)**self.model.operations[op].arity
                b_1 = len(perm) # final del bloque anterior
                for i in range(b_1,n):
                    s_i = int2base(i-b_1,len(sigma),self.model.operations[op].arity)
                    s_i = [sigma[x] for x in s_i]
                    s_i = base2int(s_i,len(sigma)) + b_1
                    perm.append(s_i)
            sigma+=[Ha.index(e)+len(sigma) for e in H[-1]]
        T = dict()
        for e in self.T:
             T[e]= frozenset(perm[i] for i in self.T[e])
        
        return TupleModelHash(self.model, permute(self.generators, perm), TH = (T,H))



if __name__ == "__main__":
    from parser import parser
    model = parser("./suma4.model")
    ta = [1,2]
    tb = [2,1]
    fa = TupleModelHash(model,ta)
    fb = TupleModelHash(model,tb).hit_p([1,0])
    print (fa)
    print (fb)
