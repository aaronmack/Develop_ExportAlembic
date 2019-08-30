#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
try:
    import hou
except ImportError:
    pass
sys.path.append('../ui')
try:
    from ui import import_alembic as ImAl
except Exception:
    # If have imported automation module
    from automation.ui import import_alembic as ImAl
import ViewAlembicListModel
import houdini_core as ho
from PySide2 import QtWidgets, QtCore


class HoudiniWidget_AlemImport(QtWidgets.QWidget, ImAl.Ui_Widget_ImportAlembic):
    def __init__(self, parent=None):
        super(HoudiniWidget_AlemImport, self).__init__()
        self.setupUi(self)
        try:
            self.setParent(hou.qt.mainWindow(), QtCore.Qt.Window)
        except NameError:
            pass
        self.data = None
        self.root_path = r""
        self.listWidget_alembiclist.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.set_connect()

    def set_connect(self):
        self.btn_searchpath.clicked.connect(self.setListWidget)
        self.lineEdit_alembicpath.textChanged.connect(self.setStatus)
        self.btn_alembic_single.clicked.connect(self.export_alembic_single)
        self.btn_alembic_archive.clicked.connect(self.export_alembic_archive)

    def setStatus(self):
        self.data = None
        self.listWidget_alembiclist.clear()

    def export_alembic_single(self):
        alem_sin_files = []
        alemsinfiles_dirc = {}

        # Get data
        for i in self.listWidget_alembiclist.selectedIndexes():
            alem_sin_files.append(i.data())
        # set dictionaries
        for i in range(len(alem_sin_files)):
            alemsinfiles_dirc[str(alem_sin_files[i]).split(".")[0]] = \
                self.root_path+os.sep+alem_sin_files[i]

        HoudiniWidget_AlemImport.judgeSelected(alem_sin_files)
        reload(ho)
        ho.create_alembic_single(alemsinfiles_dirc)

    def export_alembic_archive(self):
        alem_arc_files = []
        alemarcfiles_dirc = {}

        for i in self.listWidget_alembiclist.selectedIndexes():
            alem_arc_files.append(i.data())

        for i in range(len(alem_arc_files)):
            alemarcfiles_dirc[str(alem_arc_files[i]).split(".")[0]] = \
                self.root_path+os.sep+alem_arc_files[i]

        HoudiniWidget_AlemImport.judgeSelected(alem_arc_files)
        reload(ho)
        ho.create_alembic_archive(alemarcfiles_dirc)

    @staticmethod
    def judgeSelected(files):
        for i in range(len(files)):
            if not str(files[i]).endswith('.abc'):
                raise NameError("Select error")

    def setListWidget(self):
        if self.data == None:
            path = self.lineEdit_alembicpath.text()
            if not len(str(path)):
                try:
                    path = os.path.dirname(hou.hipFile.path())
                except NameError:
                    print( "NameError: Can not get hipFile path")
                    path = os.path.dirname('.')

            else:
                if not os.path.exists(path):
                    raise NameError("The path Error")

            reload(ViewAlembicListModel)

            model = ViewAlembicListModel.Houdini_Import_Alembic_FromDisk(path)
            ale_lists, ale_path_dir, dir_path = model.getList()
            self.root_path = dir_path

            self.listWidget_alembiclist.addItems(ale_lists)
            self.data = 1

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Return:
            self.setListWidget()
        if e.key() == QtCore.Qt.Key_Enter:
            self.setListWidget()


def run(object):
    win = HoudiniWidget_AlemImport(object)
    # win.show()
    return win


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = HoudiniWidget_AlemImport()
    win.show()
    sys.exit(app.exec_())
