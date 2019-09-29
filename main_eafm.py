#!/usr/bin/python
# -*- coding: utf-8 -*-
from PySide2 import QtWidgets
import status as sa
import Window_MainWindow as MainWindow
import sys
reload(MainWindow)

# About Houdini
try:
    import hou
    hou_qt_mainwindow = hou.qt.mainWindow()
    # GLOBAL_MAIN_OBJECT = None
except Exception:
    pass


def run_none_application():
    if sa.ExportAlembicFromMaya == None:
        my_main_win = MainWindow.run()
        my_main_win.show()
        sa.ExportAlembicFromMaya = 1


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    my_main_win = MainWindow.run()
    my_main_win.show()
    sys.exit(app.exec_())
