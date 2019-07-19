#!/usr/bin/python
# -*- coding: utf-8 -*-
from PySide2 import QtWidgets

import Window_MainWindow as MainWindow
import sys
reload(MainWindow)


def run():
    MainWindow.run()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow.run()
    sys.exit(app.exec_())
