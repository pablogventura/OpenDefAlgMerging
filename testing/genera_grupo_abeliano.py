from itertools import product
from random import sample
import sys


def clean_print(value,universe):
    print(" ".join(str(universe.index(v)) for v in value))
        


def generador(numeros):
    universe = list(product(*list(range(i) for i in numeros)))
    print(" ".join(str(i) for i in range(len(universe))))
    print("")
    print("Sum 2")
    for a, b in product(universe, universe):
        r = []
        for i in range(len(a)):
            r.append((a[i]+b[i]) % numeros[i])
        clean_print((a, b, tuple(r)),universe)
    print("")
    print("Neg 1")
    for a in universe:
        r = []
        for i in range(len(a)):
            r.append((-a[i]) % numeros[i])
        clean_print((a, tuple(r)),universe)
    print("")
    print("Zero 0")
    clean_print([(0,)*len(numeros)],universe)
    print("")
    print("T0 %s %s" % (len(universe)**2, 2))
    for i in product(universe, universe):
        clean_print(i,universe)


def main():
    try:
        numeros = [int(i) for i in sys.argv[1:]]
    except:
        print("Toma los numeros de los Z")
        sys.exit(1)

    generador(numeros)


if __name__ == "__main__":
    main()
