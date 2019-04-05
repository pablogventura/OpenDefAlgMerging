"""
Toma como argumento el directorio donde estan los modelos
"""

import os
for f in  [os.path.join(dp, f) for dp, dn, fn in os.walk("testing") for f in fn]:
    if f.endswith(".model") and not os.path.exists(f.replace(".model",".hvm")):
        os.system('python3 test_minion_vs_hit.py "%s" > "%s"' % (f,f.replace(".model",".hvm")))
    
    
