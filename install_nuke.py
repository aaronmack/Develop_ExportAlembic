import os
import sys


def _onNuke():
    srcPath = os.path.abspath(os.path.join(os.path.join(os.path.dirname(__file__)), os.pardir))

    srcPath = os.path.normpath(srcPath)

    if not os.path.exists(srcPath):
        raise IOError('Cannot find ' + srcPath)

_onNuke()
