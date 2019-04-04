
import os


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

        os.system("python " + script + " " + argumentos + " > " + filename)

generar("grupo_abeliano",2,3,4)
generar("grupo_no_abeliano",3,2)
generar("boole",3)
generar("ret",4,4)
generar("alg_random",10,2,2,[2,3],[False,True],3)