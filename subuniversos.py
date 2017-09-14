from itertools import combinations,product
from collections import defaultdict

def subuniverso(A,f,B):
    #fija A,f(ternaria)
    #input B<=A


    V=set()
    N=set()
    O=set(B)
    Ex={}
    RotExAc=set()
    Prod=defaultdict(set)

    while O:
        for k in range(1,4):#tiene que ver con la aridad
            for r in conjuntos_adecuados(V,O,k):#al menos un elemento en O y el resto en V
                Ex[r] = set(r)
                Ex[r]=clausurar(Ex[r],Prod)
                for s in Ex:
                    if s <= r:
                        Ex[r] = Ex[r] | Ex[s]
                        Ex[r]=clausurar(Ex[r],Prod)
                RotExAc = {s for s in Ex if r <= s}
                for tup in (t for t in product(r,repeat=3) if set(t)==r):
                    x = f(*tup)
                    Prod[x].add(frozenset(tup))
                    if x not in V | O:
                        N = N | {x}
                    for s in RotExAc:
                        Ex[s] = Ex[s] | {x}
                        Ex[s]=clausurar(Ex[r],Prod)
        V=V | O
        O = N
        N = set()
    return Ex#,Prod

def clausurar(ex,prod):
    cambie=True
    while cambie:
        cambie=False
        for elem in prod:
            if elem not in ex:
                if any(p <= ex for p in prod[elem]):
                    print("se agrega %s a %s" % (elem,ex))
                    ex.add(elem)
                    cambie=True
    return ex

def conjuntos_adecuados(V,O,k):
    for i in range(1,k+1): #cantidad de obligatorios
        for pv in combinations(V,k-i): #la parte vieja
            for po in combinations(O,i): # la parte obligatoria
                yield(frozenset(pv+po))
                
def es_sub(A,f,B):
    for t in product(B,repeat=3):
        if f(*t) not in B:
            print("no tiene a f(%s)=%s" % (t,f(*t)))
            return False
    return True
     
