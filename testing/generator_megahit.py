
import os
from random import randint
path_mega_hit = "mega_hit_test"
def generar(*args, cuantity=100):
    # genera alg random
    args = [str(i) for i in args]
    for i in range(cuantity):
        filename = os.path.join(path_mega_hit, args[0], '_'.join(args[1:] + [str(i)]))
        filename += ".model"
        if os.path.isfile(filename):
            continue
        filename = '"' + filename + '"'
        try:
            os.mkdir(os.path.join(path_mega_hit, args[0]))
        except:
            pass
        script = "genera_" + args[0] + ".py"
        argumentos = '" "'.join(args[1:])
        if argumentos:
            argumentos = '"' + argumentos + '"'

        os.system("python3 " + script + " " + argumentos + " > " + filename)

generar("boole",4)
generar("grupo_abeliano",2,2,4)
generar("alg_random",16,0,0,[2,2],[False,False],2)


