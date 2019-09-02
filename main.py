#!/usr/bin/python
# -*- coding: utf-8 -*-
from PySide2 import QtWidgets

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


class MyMaintainWindow(object):
    def __init__(self):
        self.main_object = MainWindow.run()
        # print("hou_qt_mainwindow", hou_qt_mainwindow)
        print("self.main_object", self.main_object)
        print("MyMaintainWindow self", self)
        print(sys.modules[__name__])


def run_houdini():
    my_main_win = None
    temp = MyMaintainWindow()

    if temp == None:
        my_main_win = MyMaintainWindow()
    if my_main_win == None:
        my_main_win = temp
    if my_main_win == temp:
        temp.main_object.show()
        pass
    print("\n\n")


def run():
    my_main_win = MyMaintainWindow()
    my_main_win.main_object.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    run()
    sys.exit(app.exec_())
