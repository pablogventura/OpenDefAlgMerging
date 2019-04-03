from genera_ret import closure
from random import sample
import sys

def main():
    try:
        ancho = int(sys.argv[1])
    except:
        print("Toma un numero de ancho de las tuplas,")
        sys.exit(1)
    try:
        muestra = int(sys.argv[2])
    except:
        muestra = 2**ancho
    generators = sample(range(2**ancho), muestra)
    closure(generators)


if __name__ == "__main__":
    main()
