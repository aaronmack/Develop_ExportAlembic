#!/usr/bin/python
# -*- coding: utf-8 -*-

try:
    import hou
except Exception:
    print("----- import -----")
    print("Error: Can't import hou module")
try:
    import fnmatch
except Exception:
    print("----- import -----")
    print("Error: Can't import fnmatch module")

import os
import sys
import re
import time
import Dialog_ExportAlembic as DialogAlembicOptions
from myException import *
from switch import *
from utils.MyUtils import DebugInfo
from utils import MyUtils
from ui import mainwindow as mainwindow
from PySide2.QtWidgets import QMainWindow, QFileDialog
from PySide2 import QtCore, QtWidgets, QtGui


class AutomationStandard(QMainWindow, mainwindow.Ui_MainWindow):
    def __init__(self):
        super(AutomationStandard, self).__init__()
        self.setupUi(self)
        self.countTest = 0
        self.dialog = DialogAlembicOptions.run(self)

        self.comboBox_filterlist.setStyleSheet("font: 9pt \"Alef\";")

        try:
            self.setParent(hou.qt.mainWindow(), QtCore.Qt.Window)
        except Exception:
            print("Error: Can't setParent. self.setParent(hou.qt.mainWindow(), QtCore.Qt.Window)")
        self.checkBox_scene.setChecked(True)
        self.lineEdit_exportname.setEnabled(False)
        self.lineEdit_namespace.setEnabled(True)
        self.lineEdit_exportpath.setEnabled(True)

        # Init status (Scene)
        self.readyExportOption = ['Scene']
        self.TIME_LIMIT = 100
        self.ProCount = 0
        self.index = 0
        self.checkCamera = 0
        self.checkScene = 2
        self.checkCharacter = 0
        self.checkProp = 0
        self.rootFilepath = None
        self.exportName = ''
        self.exportPath = ''
        self.exportNamespace = ''
        self.thatAllNeed = {}
        self.setConnect()
        self.setProgressBar()

    def setProgressBar(self):
        self.progressBar.setGeometry(0, 0, 300, 25)
        self.progressBar.setValue(0)

    def onButtonClick(self):
        self.progressBar.setValue(0)
        self.ProCount = 0
        try:
            if self.selectdata != None:
                while self.ProCount < self.TIME_LIMIT:
                    self.ProCount += 1
                    time.sleep(0.0125)
                    self.progressBar.setValue(self.ProCount)
            else:
                pass
        except AttributeError:
            pass

    def setConnect(self):
        self.pushButton_search.clicked.connect(self.getStatus)
        self.pushButton_action.clicked.connect(lambda: self.readyMayaExportAbc())
        self.pushButton_action.clicked.connect(self.onButtonClick)
        self.pushButton_refresh.clicked.connect(self.StructureListView)
        self.pushButton_left.clicked.connect(self.SwitchToTopLevel)
        self.pushButton_right.clicked.connect(self.SwitchNextLevel)

        self.comboBox_export_mode.currentIndexChanged.connect(self.setExportMode)
        self.comboBox_filterlist.currentIndexChanged.connect(self.StructureListView)

        self.checkBox_camera.stateChanged.connect(self.onStateChange)
        self.checkBox_chracter.stateChanged.connect(self.onStateChange)
        self.checkBox_prop.stateChanged.connect(self.onStateChange)
        self.checkBox_scene.stateChanged.connect(self.onStateChange)

        self.lineEdit_exportname.textEdited.connect(self.exportNameEdit)
        self.lineEdit_exportpath.textEdited.connect(self.exportPathEdit)
        self.lineEdit_namespace.textEdited.connect(self.exportNameSpaceEdit)

        self.actionSetting.triggered.connect(self.getAlembicOptionsDialogStatus)

        self.listView.doubleClicked.connect(self.SwitchNextLevel)
        self.listView.clicked.connect(self.getListViewClicked)

        # or you can use lambda
        # self.checkBox3.stateChanged.connect(lambda: self.btnstate(self.checkBox3))

    # private slots
    def onStateChange(self, state):
        if self.comboBox_export_mode.currentText() == 'ByName':
            if state:
                if self.sender() == self.checkBox_camera:
                    DebugInfo("checked from checkBox_camera", 'SingleCheckBox', 0)
                    self.setCloseCheckBoxExceptSelf(self.checkBox_camera)
                elif self.sender() in (self.checkBox_scene, ):
                    DebugInfo("checked from checkBox_scene", 'SingleCheckBox', 0)
                    self.setCloseCheckBoxExceptSelf(self.checkBox_scene)
                elif self.sender() == self.checkBox_prop:
                    DebugInfo("checked from checkBox_prop", 'SingleCheckBox', 0)
                    self.setCloseCheckBoxExceptSelf(self.checkBox_prop)
                elif self.sender() == self.checkBox_chracter:
                    DebugInfo("checked from checkBox_chracter", 'SingleCheckBox', 0)
                    self.setCloseCheckBoxExceptSelf(self.checkBox_chracter)
        else:
            pass
    # private slots
    def SwitchToTopLevel(self):
        rootFilepath = os.path.abspath(os.path.join(self.rootFilepath, os.pardir))
        self.rootFilepath = rootFilepath
        self.lineEdit_filepath.setText(self.rootFilepath)
        self.getStatus()

    # private slots
    def SwitchNextLevel(self):
        if str(self.rootFilepath).endswith('\\'):
            curpath = self.rootFilepath + self.curentSelect
        else:
            curpath = self.rootFilepath+"\\"+self.curentSelect
        if os.path.isdir(curpath):
            self.rootFilepath = curpath
            self.lineEdit_filepath.setText(self.rootFilepath)
            self.getStatus()
        else:
            self.statusbar.showMessage("Select Error: None Directory.")

    # private slots
    def getAlembicOptionsDialogStatus(self):
        self.countTest += 1
        if self.dialog == None:
            self.AlembicOptionsDialog()
        else:
            self.AlembicOptionsDialog(mode=1)
        self.dialog.someSignal.connect(self.dialogObjectModifly)

    # private slots
    def dialogObjectModifly(self):
        #self.dialog = None
        pass

    # private slots
    def AlembicOptionsDialog(self, mode=0):
        if mode == 0:
            self.dialog.showDialog()
        if mode == 1:
            self.dialog.show()

    # private slots
    def exportNameEdit(self, data):
        if data != None:
            self.exportName = data
        else:
            self.exportName = ''

    # private slots
    def exportNameSpaceEdit(self, data):
        if data != None:
            self.exportNamespace = data
        else:
            self.exportNamespace = ''

    # private slots
    def exportPathEdit(self, data):
        if data != "" or data != None:
            self.exportPath = data
        else:
            self.exportPath = self.getCurrentHoudiniProjectPath()

    # private slots
    # Current Search frame status
    def getStatus(self):
        already = self.lineEdit_filepath.text()
        # print already == ""
        if len(already) != 0:
            self.search()
        else:
            self.showDialog()

    # private slots
    def setExportMode(self, index):
        # 0 - Option
        # 1 - ByName
        # 2 - All
        self.index = index
        for case in switch(self.index):
            if case(0):
                self.checkBox_camera.setEnabled(True)
                self.checkBox_prop.setEnabled(True)
                self.checkBox_chracter.setEnabled(True)
                self.checkBox_scene.setEnabled(True)
                self.lineEdit_exportname.setEnabled(False)
                self.lineEdit_namespace.setEnabled(True)
                self.lineEdit_exportpath.setEnabled(True)
                break
            if case(1):
                self.lineEdit_exportname.setEnabled(True)
                self.lineEdit_exportpath.setEnabled(True)
                self.lineEdit_namespace.setEnabled(True)
                self.checkBox_camera.setEnabled(True)
                self.checkBox_prop.setEnabled(True)
                self.checkBox_chracter.setEnabled(True)
                self.checkBox_scene.setEnabled(True)
                break
            if case(2):
                self.lineEdit_exportname.setEnabled(False)
                self.lineEdit_namespace.setEnabled(False)
                self.lineEdit_exportpath.setEnabled(True)
                self.checkBox_camera.setEnabled(False)
                self.checkBox_prop.setEnabled(False)
                self.checkBox_chracter.setEnabled(False)
                self.checkBox_scene.setEnabled(False)

                break
            if case():
                print "something else!"

    def getCurrentHoudiniProjectPath(self):
        try:
            tem_exportPath = ""
            tem_exportPath = os.path.dirname(hou.hipFile.path())
            exportPath = MyUtils.checkAbcPath(tem_exportPath)
            DebugInfo(exportPath, "geted Path", 1)
            return exportPath
        except Exception:

            print("Warning: Can't get the houdini project path, try to get Desktop folder")

            import _winreg
            key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER,
                                  r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
            tem_exportPath = _winreg.QueryValueEx(key, "Desktop")[0]
            exportPath = MyUtils.checkAbcPath(tem_exportPath)
            DebugInfo(exportPath, 'Export Path', 0)
            return exportPath

    def getOptionStatus(self):
        if self.comboBox_export_mode.currentText() == 'ByName':
            pass

        if self.checkBox_scene.checkState() == QtCore.Qt.CheckState.Checked:
            self.setExportOption_Scene(2)
        else:
            self.setExportOption_Scene(0)
        if self.checkBox_prop.checkState() == QtCore.Qt.CheckState.Checked:
            self.setExportOption_Prop(2)
        else:
            self.setExportOption_Prop(0)
        if self.checkBox_chracter.checkState() == QtCore.Qt.CheckState.Checked:
            self.setExportOption_Character(2)
        else:
            self.setExportOption_Character(0)
        if self.checkBox_camera.checkState() == QtCore.Qt.CheckState.Checked:
            self.setExportOption_Camera(2)
        else:
            self.setExportOption_Camera(0)

    # private slots
    def setExportOption_Camera(self, status):
        if status != 0:
            if "Camera" in self.readyExportOption:
                return

            self.readyExportOption.append("Camera")
        else:
            try:
                self.readyExportOption.remove("Camera")
            except Exception, e:
                pass
            self.checkCamera = status
        self.checkCamera = status

    # private slots
    def setExportOption_Character(self, status):
        if status != 0:
            if "Character" in self.readyExportOption:
                return
            self.readyExportOption.append("Character")
        else:
            try:
                self.readyExportOption.remove("Character")
            except Exception, e:
                pass
            self.checkCharacter = status
        self.checkCharacter = status

    # private slots
    def setExportOption_Prop(self, status):
        if status != 0:
            if "Prop" in self.readyExportOption:
                return
            self.readyExportOption.append("Prop")
        else:
            try:
                self.readyExportOption.remove("Prop")
            except Exception, e:
                pass
            self.checkProp = status
        self.checkProp = status

    # private slots
    def setExportOption_Scene(self, status):
        if status != 0:
            if "Scene" in self.readyExportOption:
                return
            self.readyExportOption.append("Scene")
        else:
            try:
                self.readyExportOption.remove("Scene")
            except Exception, e:
                pass
            self.checkScene = status
        self.checkScene = status

    def setCloseCheckBoxExceptSelf(self, exceptSelf):
        myCombox = [self.checkBox_chracter, self.checkBox_prop, self.checkBox_scene, self.checkBox_camera]
        for i in range(len(myCombox)):
            if myCombox[i] != exceptSelf:
                myCombox[i].setChecked(False)
            else:
                continue

    def StructureListView(self):
        self.listView.setModel(self.ViewModel())

    def ViewModel(self):
        mode = QtGui.QStandardItemModel()

        try:
            files, dirs = MyUtils.get_subLevel1_dirsAndFiles(self.rootFilepath)
        except Exception:
            self.statusbar.showMessage("Select Error: None Specified Path.")
            print("Warning: None Specified Path.")
            return
        objectNames = []
        dirNumber = len(dirs)
        fileNumber = len(files)
        filterLists = str(self.comboBox_filterlist.currentText()).split(';')
        filterListsMatched = [None for i in range(len(filterLists))]

        DebugInfo(filterLists, '', 0)

        if filterLists[0] != '*':
            for i in range(len(filterLists)):
                NoneStar = str(filterLists[i]).replace(r'*', '')

                # *.ma *.mb
                # ^.*\.ma$|^.*\.mb$
                com_temp = '\\' + NoneStar + '$'
                temp = str(filterLists[i]).replace(r'*', r'^.*').replace(NoneStar, com_temp)

                filterListsMatched[i] = temp
        else:
            filterListsMatched = ['.']

        # get FilterListsNoneStar list
        mat3 = ''
        lenFilter = len(filterListsMatched)
        for i in range(lenFilter):
            if i < lenFilter-1:
                mat3 += filterListsMatched[i]+'|'
            else:
                mat3 += filterListsMatched[i]
        DebugInfo(mat3, '', 0)
        reobj = re.compile(mat3)

        # get valid Number
        temp = []
        validNumber = 0
        for file in range(fileNumber):
            if reobj.search(files[file]) != None:
                validNumber += 1
                DebugInfo(file, '', 0)
                temp.append(files[file])
        DebugInfo(temp, '', 0)
        totalHaveValidNumber = dirNumber + validNumber
        fileNumber = validNumber

        # Init objectNames
        for i in MyUtils.fibList(totalHaveValidNumber):
            objectNames.append(None)

        # Set dirs
        for Num in range(dirNumber):
            objectNames[Num] = QtGui.QStandardItem(dirs[Num])
            #mode.appendRow(objectNames[Num])

        # Set files new
        for i in range(dirNumber, fileNumber + dirNumber):
            ori_index = i - dirNumber
            DebugInfo(ori_index, '', 0)
            _file = temp[ori_index]
            DebugInfo(_file, '', 0)
            DebugInfo(i, '', 0)
            objectNames[i] = QtGui.QStandardItem(temp[ori_index])

        # Set files
        # for Num in range(dirNumber, fileNumber + dirNumber):
        #     filename = files[Num - dirNumber]
        #     objectNames[Num] = QtGui.QStandardItem(files[Num - dirNumber])
        #     #mode.appendRow(objectNames[Num])

        # Append Mode
        for i in MyUtils.fibList(totalHaveValidNumber):
            mode.appendRow(objectNames[i])


        self.mode = mode
        self.ModeObject = objectNames
        self.selectdata = None
        return mode

    def EventTest_Index(self, index):
        print ("OK ---- > EventTest")
        print(index)

    def EventTest(self):
        print ("OK ---- > EventTest")

    def fixPath(self, path):
        return path.replace(os.sep, '/')

    def getListViewClicked(self, index):
        curRootPath = self.lineEdit_filepath.text()

        # final get (All path '/')
        fixCurRootPath = self.fixPath(curRootPath)

        self.curentSelect = self.ModeObject[index.row()].text()

        if str(fixCurRootPath).endswith('/'):
            selectdata = fixCurRootPath + self.curentSelect
        else:
            selectdata = fixCurRootPath + '/' + self.curentSelect

        if not os.path.isdir(selectdata):
            self.selectdata = selectdata
            self.statusbar.showMessage("Current select is: %s" % self.selectdata)
        else:
            self.selectdata = None
            self.statusbar.showMessage("Select Error: Please select a ready to export file.")

    def checkExportPath(self):
        exportPath = self.lineEdit_exportpath.text()
        if len(exportPath) != 0 and os.path.exists(exportPath):
            exportPath = str(exportPath).strip().rstrip("\\")
            exportPath = MyUtils.checkAbcPath(exportPath)
            return exportPath
        else:
            exportPath = self.getCurrentHoudiniProjectPath()
            return exportPath

    def checkExportName(self):
        name = self.lineEdit_exportname.text()
        if len(name) == 0:
            raise CUerror("None name, You must specified")
        else:
            return name

    def checkExportNamespace(self):
        namespace = self.lineEdit_namespace.text()
        if len(namespace) == 0:
            namespace = ''
        return namespace

    def showDialog(self):
        try:
            directory1 = MyUtils.convert_slash_type(QFileDialog.getExistingDirectory(self, "Select folder", "./"))
            # directory1 = hou.ui.selectFile(file_type=hou.fileType.Directory) # Use Houdini select mode
        except Exception:
            print "Warning: Can't get the Directory"
        else:
            self.lineEdit_filepath.setText(directory1)
            self.search()
        finally:
            pass

    def search(self):
        rootPath = str(self.lineEdit_filepath.text())
        pathSplit = rootPath.split('/')
        lens = len(pathSplit)
        if lens != 1 and pathSplit[lens-1] != '':
            rootPath = str(eval(repr(rootPath).replace('/', '\\')))
            rootPath = eval(repr(rootPath).replace('\\\\', '\\'))
            self.lineEdit_filepath.setText(rootPath)
            #print(rootPath)

        self.rootFilepath = rootPath
        self.StructureListView()

    def exportModeSetting(self, index):
        self.index = index
        for case in switch(self.index):
            if case(0):
                self.getOptionStatus()
                # check all (path name namespace)
                self.exportPath = self.checkExportPath()
                self.exportName = ''
                self.exportNamespace = self.checkExportNamespace()
                break
            if case(1):
                self.getOptionStatus()
                # check all (path name namespace)
                self.exportName = self.checkExportName()
                self.exportPath = self.checkExportPath()
                self.exportNamespace = self.checkExportNamespace()
                break
            if case(2):
                self.readyExportOption = ["Camera", "Character", "Prop", "Scene"]
                # check all (path name namespace)
                self.exportPath = self.checkExportPath()
                self.exportNamespace = ''
                self.exportName = ''
                break
            if case():
                break

    def readyMayaExportAbc(self):
        #try:
        if self.selectdata != None:
            reload(MyUtils)
            self.exportModeSetting(self.comboBox_export_mode.currentIndex())
            seleDat = self.selectdata.encode("utf-8") if (self.selectdata != None) else self.selectdata
            expoNa = self.exportName.encode("utf-8") if (self.exportName != None) else self.exportName
            expoNamespa = self.exportNamespace.encode("utf-8") if (self.exportNamespace != None) else self.exportNamespace
            expoPa = self.exportPath.encode("utf-8") if (self.exportPath != None) else self.exportPath

            optionsFrame, options = self.dialog.getAllOptions()

            # [0, '', '', 1]
            exportOptions_command = ' '.join(options)

            # update all file name options
            filenameoptions = self.dialog.getFileNameConfig()

            export_options = []
            # ['Camera', 'Character', 'Prop', 'Scene']
            # [['SceneName'], ['PropName'], ['CharacterName'], ['CameraName']]
            if "Camera" in self.readyExportOption:
                export_options.append(filenameoptions['CameraName'])
            if "Character" in self.readyExportOption:
                export_options.append(filenameoptions['CharacterName'])
            if "Prop" in self.readyExportOption:
                export_options.append(filenameoptions['PropName'])
            if "Scene" in self.readyExportOption:
                export_options.append(filenameoptions['SceneName'])

            DebugInfo(self.readyExportOption, "export options", 0)
            DebugInfo(filenameoptions, "filenameoptions", 0)
            DebugInfo(export_options, "export_options", 0)
            # Only one
            export_type = ''
            if self.comboBox_export_mode.currentText() in ('ByName', 'SelectCheck'):
                export_type = export_options[0]
                if expoNamespa != '' and expoNamespa != None:
                    expoNamespa += ":"
                else:
                    expoNamespa = ''

            DebugInfo(expoNamespa, "export namespace", 0)
            DebugInfo(self.exportNamespace, "self. namespace", 0)
            file_name, extension = os.path.splitext(str(self.curentSelect))
            self.thatAllNeed.update(allOptions=exportOptions_command,
                                    sel_file_name=file_name,
                                    mode=self.index,
                                    abcPath=expoPa,
                                    step=optionsFrame[-1],
                                    frameMode=optionsFrame[0],
                                    startTimeSet=optionsFrame[1],
                                    endTimeSet=optionsFrame[2],
                                    selectGeo=export_options,
                                    name=expoNa,
                                    type=export_type,
                                    maya_namespace=expoNamespa,
                                    )
            DebugInfo(self.thatAllNeed, 'getAllOptionsFromMain', 0)

            # import threading
            # t1 = threading.Thread(target=MyUtils.mayaExportAbc, args=(self.thatAllNeed, seleDat))
            # t1.start()

            import multiprocessing

            p1 = multiprocessing.Process(target=MyUtils.mayaExportAbc,
                                         args=(self.thatAllNeed, seleDat,))
            # p1.daemon(True)
            p1.start()
            print(p1.is_alive())

            # status = MyUtils.mayaExportAbc(self.thatAllNeed, seleDat, self)
        else:
            print("Error: Be not ready , No selected file")
            self.statusbar.showMessage("Error: Be not ready , No selected file")
        # except Exception, e:
        #     print(e)

    def event_notice(self):
        QtWidgets.QMessageBox.question(self, "Notice", "Ok!",
                                       QtWidgets.QMessageBox.Yes)

    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(self, "Warning", "Do you really want to quit?",
                                               QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            try:
                self.dialog.close()
            except Exception, e:
                print(e)
            event.accept()
        else:
            event.ignore()

    def mousePressEvent(self, event):
        '''re-implemented to suppress Right-Clicks from selecting items.'''

        if event.type() == QtCore.QEvent.MouseButtonPress:
            if event.button() == QtCore.Qt.RightButton:
                # print("Debug info: RightButtonClicked")
                pass
            else:
                super(AutomationStandard, self).mousePressEvent(event)


def run():
    win = AutomationStandard()
    win.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = AutomationStandard()
    win.show()
    sys.exit(app.exec_())
