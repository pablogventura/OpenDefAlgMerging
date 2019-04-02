from itertools import product,permutations
from random import sample
import sys


def clean_print(value):
    value = value.replace("(", "'(")
    value = value.replace(")", ")'")
    while ", " in value:
        value = value.replace(", ", ",")
    print(value)

def inverse(a):
    
    r = []
    for i in range(len(a)):
        r.append(a.index(i))
    return tuple(r)

def compose(a,b):
    assert len(a)==len(b)
    r = []
    for i in range(len(a)):
        r.append(b[a[i]])
    return tuple(r)

def generador(perm, gens):
    """
    :param perm: toma el tamanno del del que van a ser las permutaciones
    :param gens: cantidad de generadores aleatorios
    """
    permutaciones = set(permutations(range(perm)))
    print("# Cantidad de permutaciones posibles: %s" % len(permutaciones))
    universe = set(sample(permutaciones,gens))

    sigo=True
    while sigo:
        sigo = False
        for a,b in product(universe,universe):
            
            r = compose(a,b)
            if r not in universe:
                universe.add(r)
                sigo = True
    universe.add(tuple(range(perm)))
    print("# Quedaron: %s" % len(universe))
    clean_print(" ".join(str(e) for e in universe))
    print("")
    print("Id 0")
    clean_print(str(tuple(range(perm))))
    print("")
    print("O 2")
    for a, b in product(universe, universe):
        r = compose(a, b)
        clean_print("%s %s %s" % (a,b,r))
    print("")
    print("I 1")
    for a in universe:
        r = inverse(a)
        clean_print("%s %s" % (a,r))
    print("")
    clean_print("T0 %s %s" % (len(universe)**2, 2))
    for i in product(universe, universe):
        clean_print(" ".join(map(str, i)))

def main():
    try:
        perm, gens = [int(i) for i in sys.argv[1:]]
    except:
        print("Toma los numeros de los Z")
        sys.exit(1)

    generador(perm, gens)


if __name__ == "__main__":
    main()
