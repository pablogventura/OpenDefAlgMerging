
import os
from random import randint

def generar(*args, cuantity=100):
    # genera alg random
    args = [str(i) for i in args]
    for i in range(cuantity):
        filename = os.path.join(args[0], '_'.join(args[1:] + [str(i)]))
        filename += ".model"
        if os.path.isfile(filename):
            continue
        filename = '"' + filename + '"'
        try:
            os.mkdir(args[0])
        except:
            pass
        script = "genera_" + args[0] + ".py"
        argumentos = '" "'.join(args[1:])
        if argumentos:
            argumentos = '"' + argumentos + '"'

        os.system("python3 " + script + " " + argumentos + " > " + filename)

generar("grupo_abeliano",2,3,4)
for i in range(3):
    generar("grupo_abeliano",randint(2,5),randint(2,5),randint(2,5))

generar("grupo_abeliano",2,3,4)
generar("grupo_no_abeliano",3,2)
for i in range(3):
    generar("grupo_no_abeliano",randint(2,5),2)
generar("boole",3)
generar("boole",7)
generar("ret",4,4)
for i in range(3):
    generar("ret",randint(2,5),randint(2,5))
generar("alg_random",10,2,2,[2,3],[False,True],3)
generar("alg_random",20,2,2,[2,3],[False,True],3)
generar("alg_random",30,3,3,[2,3],[False,True],3)
