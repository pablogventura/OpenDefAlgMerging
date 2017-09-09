from itertools import combinations,product

def subuniverso(A,f,B):
    #fija A,f(ternaria)
    #input B<=A


    V=set()
    N=set()
    O=set(B)
    Ex={}
    RotExAc=set()

    while O:
        for k in range(1,4):#tiene que ver con la aridad
            for r in conjuntos_adecuados(V,O,k):#al menos un elemento en O y el resto en V
                Ex[r] = r 
                for s in Ex:
                    if s <= r:
                        Ex[r] = Ex[r] | Ex[s]
                RotExAc = {s for s in Ex if r <= s}
                for tup in (t for t in product(r,repeat=3) if set(t)==r):
                    x = f(*tup)
                    if x not in V | O:
                        N = N | {x}
                    for s in RotExAc:
                        Ex[s] = Ex[s] | {x}
        V=V | O
        O = N
        N = set()
    return Ex

def conjuntos_adecuados(V,O,k):
    for i in range(1,k+1): #cantidad de obligatorios
        for pv in combinations(V,k-i): #la parte vieja
            for po in combinations(O,i): # la parte obligatoria
                yield(frozenset(pv+po))
                
def es_sub(A,f,B):
    for t in product(B,repeat=3):
        if f(*t) not in B:
            return False
    return True
     
