"""
Toma como argumento el directorio donde estan los modelos
"""
from shell_non_blocking import ShellProc
from time import sleep
cores = 6
procs = []
try:
    import os
    files = [os.path.join(dp, f) for dp, dn, fn in os.walk("testing") for f in fn]
    for i,f in enumerate(files):
        if f.endswith(".model") and not os.path.exists(f.replace(".model",".hvm")):
            print("%s%%" % (i / len(files)))
            
            procs = [p for p in procs if p.is_running()]
            if len(procs) < cores:
                procs.append(ShellProc('python3 test_minion_vs_hit_multiple_times.py "%s" > "%s"' % (f,f.replace(".model",".hvm"))))
            
except KeyboardInterrupt:
    pass
    
