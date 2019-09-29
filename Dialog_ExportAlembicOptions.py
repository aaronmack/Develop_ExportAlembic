#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
from ui import export_abc_options
from PySide2 import QtCore
from PySide2.QtCore import QObject, Signal
from PySide2.QtWidgets import QDialog, QApplication


class ExportAbcOptionsDialog(QDialog, export_abc_options.Ui_Dialog_exportalembicoptions):
    class commu(QObject):
        someSignal = Signal()

    def __init__(self, parent=None):
        super(ExportAbcOptionsDialog, self).__init__(parent)
        self.setupUi(self)
        self.fileNameConfig = {}

        self.cm = self.commu()
        self.someSignal = self.cm.someSignal
        self.cm.someSignal.connect(self.print_msg)

        self.checkBox_uv.stateChanged.connect(self.EventTest)
        self.pushButton_cancle.clicked.connect(self.CancleDispose)
        self.pushButton_save.clicked.connect(self.SaveDispose)

        self.getAllOptions()

    def print_msg(self):
        # print("Debug info: Dialog Custom Signal is called")
        pass

    def getFileNameConfig(self):
        self.fileNameConfig['SceneName'] = self.lineEdit_scene.text()
        self.fileNameConfig['PropName'] = self.lineEdit_prop.text()
        self.fileNameConfig['CharacterName'] = self.lineEdit_character.text()
        self.fileNameConfig['CameraName'] = self.lineEdit_camera.text()
        return self.fileNameConfig

    def punch(self):
        try:
            self.someSignal.emit()
        except Exception as e:
            print("__init__:")
            print(e)

    def say_punched(self):
        print('Bag was punched.')

    def SaveDispose(self):
        self.hide()

    def CancleDispose(self):
        self.hide()

    def EventTest(self, index):
        print(index)

    def optionsFrameSet(self):
        # FrameMode StartFrame EndFrame Step
        optionsFrame = []
        for i in range(4):
            optionsFrame.append("")
        # init
        optionsFrame[0] = 0
        step = self.lineEdit_framestep.text()
        startFrame = self.lineEdit_framestart.text()
        endFrame = self.lineEdit_frameend.text()

        if len(step) != 0:
            optionsFrame[3] = int(filter(str.isdigit, step.encode("utf-8")))
        else:
            optionsFrame[3] = 1

        if len(startFrame) != 0 and len(endFrame) != 0:
            optionsFrame[0] = 1
            optionsFrame[1] = int(filter(str.isdigit, startFrame.encode("utf-8")))
            optionsFrame[2] = int(filter(str.isdigit, endFrame.encode("utf-8")))

        return optionsFrame


    def getAllOptions(self):
        checked = QtCore.Qt.CheckState.Checked
        options = []
        optionsFrame = self.optionsFrameSet()

        optionsLens = 9

        for i in range(optionsLens):
            options.append("")
        # default export abc format
        # options[0] = "ogawa"

        if self.radioButton_hdf5.isChecked():
            options[optionsLens-1] = "hdf"
        if self.radioButton_Ogawa.isChecked():
            options[optionsLens-1] = "ogawa"
        if self.checkBox_colorSet.checkState() == checked:  # 1
            options[0] = "-writeColorSets"
        if self.checkBox_worldSpace.checkState() == checked:  # 2
            options[1] = "-worldSpace"
        if self.checkBox_uvSets.checkState() == checked:  # 3
            options[2] = "-writeUVSets"
        if self.checkBox_visibility.checkState() == checked:  # 4
            options[3] = "-writeVisibility"
        if self.checkBox_creases.checkState() == checked:  # 5
            options[4] = "-autoSubd"
        if self.checkBox_faceSets.checkState() == checked:  # 6
            options[5] = "-writeFaceSets"
        if self.checkBox_uv.checkState() == checked:  # 7
            options[6] = "-uvWrite"
        options[optionsLens-2] = "-dataFormat"
        #print(options)
        return optionsFrame, options

    def closeEvent(self, event):
        # print("Debug info: The export alembic options dialog is closed")
        self.cm.someSignal.emit()
        #self.close()

    def mousePressEvent(self, event):
        '''re-implemented to suppress Right-Clicks from selecting items.'''

        if event.type() == QtCore.QEvent.MouseButtonPress:
            if event.button() == QtCore.Qt.RightButton:
                self.getAllOptions()
            else:
                super(ExportAbcOptionsDialog, self).mousePressEvent(event)

    def showDialog(self):
        self.show()

def run(object):
    dialog = ExportAbcOptionsDialog(object)
    #dialog.show()
    #dialog.exec_()
    return dialog


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = ExportAbcOptionsDialog()
    win.getAllOptions()
    win.show()
    sys.exit(app.exec_())
