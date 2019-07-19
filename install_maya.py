#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys

try:
    import maya.mel
    import maya.cmds
    isMaya = True
except ImportError:
    isMaya = False

def _onMayaDropped():
    """Dragging and dropping this file into the scene executes the file."""

    srcPath = os.path.abspath(os.path.join(os.path.join(os.path.dirname(__file__)), os.pardir))

    iconPath = os.path.join(srcPath, 'automation', 'resource', 'icons', 'icon.png')

    srcPath = os.path.normpath(srcPath)
    iconPath = os.path.normpath(iconPath)

    if not os.path.exists(iconPath):
        raise IOError('Cannot find ' + iconPath)

    for path in sys.path:
        if os.path.exists(path + '/automation/__init__.py'):
            maya.cmds.warning('Automation is already installed at ' + path)


    command = '''
# -----------------------------------
# Automation
# -----------------------------------

import os
import sys

if not os.path.exists(r'{path}'):
    raise IOError(r'The source path "{path}" does not exist!')

if r'{path}' not in sys.path:
    sys.path.insert(0, r'{path}')

import automation.main as automation
automation.run()
'''.format(path=srcPath)

    shelf = maya.mel.eval('$gShelfTopLevel=$gShelfTopLevel')
    parent = maya.cmds.tabLayout(shelf, query=True, selectTab=True)
    maya.cmds.shelfButton(
        command=command,
        annotation='Automation',
        sourceType='Python',
        image=iconPath,
        image1=iconPath,
        parent=parent
    )


if isMaya:
    _onMayaDropped()
