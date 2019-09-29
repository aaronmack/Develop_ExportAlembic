#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import importlib
try:
    import hou
except ImportError:
    pass
try:
    from ui import import_alembic_v02
    from utils import MyUtils
except Exception:
    # If have imported automation module
    modulename = os.path.realpath(os.path.dirname(__file__)).split(os.sep)[-2]
    import_alembic_v02 = importlib.import_module("%s.ui.import_alembic_v02" % (modulename))
    MyUtils = importlib.import_module("%s.utils" % (modulename))
import ViewAlembicListModel
import houdini_core as ho

from PySide2 import QtWidgets, QtCore


class HoudiniWidget_AlemImport(QtWidgets.QWidget, import_alembic_v02.Ui_Widget_ImportAlembic):
    def __init__(self, parent=None):
        super(HoudiniWidget_AlemImport, self).__init__()
        self.setupUi(self)
        try:
            self.setParent(hou.qt.mainWindow(), QtCore.Qt.Window)
        except NameError:
            pass
        self.root_path = r""
        # set Item View
        self.listWidget_alembiclist.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        # set some styles

        self.set_connect()

    def set_connect(self):
        self.btn_alembic_single.clicked.connect(self.export_alembic_single)
        self.btn_alembic_archive.clicked.connect(self.export_alembic_archive)
        self.btn_searchpath.clicked.connect(self.setListWidget)
        self.btn_go_previous_level.clicked.connect(self.SwitchPreviousLevel)
        self.lineEdit_alembicpath.textChanged.connect(self.setStatus)
        self.listWidget_alembiclist.doubleClicked.connect(self.SwitchNextLevel)

    # Set next level's view
    def SwitchNextLevel(self):
        temp_seleted = ''
        for i in self.listWidget_alembiclist.selectedIndexes():
            temp_seleted = i.data()
        temp_path = self.root_path + temp_seleted
        MyUtils.DebugInfo(temp_path, theMessageFrom="NextLevel Path", show=1)
        if os.path.isdir(temp_path):
            self.setListWidget(IncomingPath=temp_path)

    # Set previous level's view
    def SwitchPreviousLevel(self):
        previous_path = MyUtils.get_previous_level_path(self.root_path)

        self.listWidget_alembiclist.clear()
        self.setListWidget(IncomingPath=previous_path)

    def setStatus(self):
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

    def setListWidget(self, IncomingPath=''):
        # clean has been exists view list
        self.listWidget_alembiclist.clear()
        # The default set
        path = self.lineEdit_alembicpath.text()
        if os.path.exists(IncomingPath):
            path = IncomingPath
        if not len(str(path)):
            try:
                path = os.path.dirname(hou.hipFile.path())
                MyUtils.DebugInfo(path, "Geted: Curent hip file path", show=1)
            except NameError:
                win_desktop_folder = MyUtils.get_windows_dekstopFolder()
                path = os.path.dirname(win_desktop_folder)
                MyUtils.DebugInfo("NameError: Not able to get the hipFile path, geted Desktop directory", show=1)
        elif os.path.exists(path):
            # Uniform backslashes
            if os.path.sep in path:  # win: \  ==> Instead of /
                path = str(path).replace(os.path.sep, '/')
        else:
            raise MyUtils.PathIrregularError("Irregular: %s " % (path, ))
        # Uniform slashes by different System
        path = os.path.normpath(path)
        # fix the path
        if not path.endswith(os.sep):
            path += os.sep

        # sync list weight's content with line edit's content same
        self.lineEdit_alembicpath.setText(path)
        reload(ViewAlembicListModel)
        model = ViewAlembicListModel.Houdini_Import_Alembic_FromDisk(path)
        ale_lists, dir_lists, ale_path_dir, dir_path = model.getList()
        self.root_path = path
        MyUtils.DebugInfo(self.root_path, theMessageFrom='From Sel List Weight  ==> root_path', show=0)

        self.listWidget_alembiclist.addItems(ale_lists)
        self.listWidget_alembiclist.addItems(dir_lists)

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
