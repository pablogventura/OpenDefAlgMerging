from itertools import product
import sys


def clean_print(value):
    value = value.replace("(", "'(")
    value = value.replace(")", ")'")
    while ", " in value:
        value = value.replace(", ", ",")
    print(value)


def compose(a,b):
    assert len(a)==len(b)
    r = []
    for i in range(len(a)):
        r.append(b[a[i]])
    return tuple(r)

def generador(perm, gens):
    universe = list(product(*list(range(i) for i in numeros)))
    clean_print(" ".join(str(e) for e in universe))
    clean_print("")
    clean_print("Sum 2")
    for a, b in product(universe, universe):
        r = []
        for i in range(len(a)):
            r.append((a[i]+b[i]) % numeros[i])
        clean_print("%s %s %s" % (a, b, tuple(r)))
    clean_print("")
    clean_print("Neg 1")
    for a in universe:
        r = []
        for i in range(len(a)):
            r.append((-a[i]) % numeros[i])
        clean_print("%s %s" % (a, tuple(r)))
    clean_print("")
    clean_print("Zero 1 1")
    clean_print("(" + ",".join("0"*len(numeros)) + ",)")
    clean_print("")
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
