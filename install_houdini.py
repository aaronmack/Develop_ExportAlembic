import os
import sys

def _onHoudini():
    srcpath = os.path.join(os.path.dirname("C:\\Users\\Your\\path\\"))
    if not os.path.exists(srcpath):
        raise IOError('Cannot find ' + srcpath)

    sys.path.insert(0, srcpath)

_onHoudini()

import your_module
your_module.run()
