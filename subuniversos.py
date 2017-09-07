fija A,f(ternaria)
input B>=A


V=set()
N=set()
O=B
Ex=set()
RotExAc=set()

while O:
    for k in range(1,4):#tiene que ver con la aridad
        for r <= conjuntos adecacuados de tamaño k#al menos un elemento en O y el resto en V
            Ex[r] = r union U{Ex[s]:s<=r}
            RotExAc = {Es:r<=Es}
            for tup in {t in r^3| set(t)=r}
                x = f(*tup)
                if x not in V u O:
                    N = N u {x}
                for s in RotExAc:
                    Es = Es u {x}
    V=V u O
    O = N
    
        
