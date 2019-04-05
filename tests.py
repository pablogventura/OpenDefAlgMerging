"""
Toma como argumento el directorio donde estan los modelos
"""

import os
files = [os.path.join(dp, f) for dp, dn, fn in os.walk("testing") for f in fn]
for i,f in enumerate(files):
    if f.endswith(".model") and not os.path.exists(f.replace(".model",".hvm")):
        print("%s%%" % (i / len(files)))
        os.system('python3 test_minion_vs_hit.py "%s" > "%s"' % (f,f.replace(".model",".hvm")))
    
    
