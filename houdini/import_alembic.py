# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'import_alembic.ui',
# licensing of 'import_alembic.ui' applies.
#
# Created: Sun Jul 21 11:02:36 2019
#      by: pyside2-uic  running on PySide2 5.12.3
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Widget_ImportAlembic(object):
    def setupUi(self, Widget_ImportAlembic):
        Widget_ImportAlembic.setObjectName("Widget_ImportAlembic")
        Widget_ImportAlembic.resize(418, 341)
        Widget_ImportAlembic.setStyleSheet("background-color:rgb(70, 70, 70)")
        self.gridLayout = QtWidgets.QGridLayout(Widget_ImportAlembic)
        self.gridLayout.setObjectName("gridLayout")
        self.widget_leftmain = QtWidgets.QWidget(Widget_ImportAlembic)
        self.widget_leftmain.setObjectName("widget_leftmain")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.widget_leftmain)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.listWidget_alembiclist = QtWidgets.QListWidget(self.widget_leftmain)
        self.listWidget_alembiclist.setObjectName("listWidget_alembiclist")
        self.gridLayout_2.addWidget(self.listWidget_alembiclist, 2, 0, 1, 3)
        self.lineEdit_alembicpath = QtWidgets.QLineEdit(self.widget_leftmain)
        self.lineEdit_alembicpath.setObjectName("lineEdit_alembicpath")
        self.gridLayout_2.addWidget(self.lineEdit_alembicpath, 1, 1, 1, 1)
        self.label_path = QtWidgets.QLabel(self.widget_leftmain)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setWeight(50)
        font.setBold(False)
        self.label_path.setFont(font)
        self.label_path.setObjectName("label_path")
        self.gridLayout_2.addWidget(self.label_path, 1, 0, 1, 1)
        self.btn_searchpath = QtWidgets.QPushButton(self.widget_leftmain)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(20)
        sizePolicy.setVerticalStretch(20)
        sizePolicy.setHeightForWidth(self.btn_searchpath.sizePolicy().hasHeightForWidth())
        self.btn_searchpath.setSizePolicy(sizePolicy)
        self.btn_searchpath.setMinimumSize(QtCore.QSize(30, 20))
        self.btn_searchpath.setStyleSheet("QPushButton{background:rgb(94, 94, 94);border-radius:5px;}QPushButton:hover{background:rgb(15, 185, 25)}")
        self.btn_searchpath.setObjectName("btn_searchpath")
        self.gridLayout_2.addWidget(self.btn_searchpath, 1, 2, 1, 1)
        self.gridLayout.addWidget(self.widget_leftmain, 0, 0, 2, 1)
        self.widget_emptylock = QtWidgets.QWidget(Widget_ImportAlembic)
        self.widget_emptylock.setMinimumSize(QtCore.QSize(50, 125))
        self.widget_emptylock.setObjectName("widget_emptylock")
        self.gridLayout.addWidget(self.widget_emptylock, 0, 1, 1, 1)
        self.widget_rightdown = QtWidgets.QWidget(Widget_ImportAlembic)
        self.widget_rightdown.setObjectName("widget_rightdown")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget_rightdown)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.btn_alembic_single = QtWidgets.QPushButton(self.widget_rightdown)
        self.btn_alembic_single.setMinimumSize(QtCore.QSize(100, 20))
        self.btn_alembic_single.setStyleSheet("QPushButton{background:rgb(94, 94, 94);border-radius:5px;}QPushButton:hover{background:rgb(15, 185, 25)}")
        self.btn_alembic_single.setObjectName("btn_alembic_single")
        self.verticalLayout.addWidget(self.btn_alembic_single)
        spacerItem1 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        self.verticalLayout.addItem(spacerItem1)
        self.btn_alembic_archive = QtWidgets.QPushButton(self.widget_rightdown)
        self.btn_alembic_archive.setMinimumSize(QtCore.QSize(100, 20))
        self.btn_alembic_archive.setStyleSheet("QPushButton{background:rgb(94, 94, 94);border-radius:5px;}QPushButton:hover{background:rgb(125, 85, 15)}")
        self.btn_alembic_archive.setObjectName("btn_alembic_archive")
        self.verticalLayout.addWidget(self.btn_alembic_archive)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.gridLayout.addWidget(self.widget_rightdown, 1, 1, 1, 1)

        self.retranslateUi(Widget_ImportAlembic)
        QtCore.QMetaObject.connectSlotsByName(Widget_ImportAlembic)

    def retranslateUi(self, Widget_ImportAlembic):
        Widget_ImportAlembic.setWindowTitle(QtWidgets.QApplication.translate("Widget_ImportAlembic", "Alembic Import", None, -1))
        self.label_path.setText(QtWidgets.QApplication.translate("Widget_ImportAlembic", "Path", None, -1))
        self.btn_searchpath.setText(QtWidgets.QApplication.translate("Widget_ImportAlembic", "S", None, -1))
        self.btn_alembic_single.setText(QtWidgets.QApplication.translate("Widget_ImportAlembic", "Alembic Single", None, -1))
        self.btn_alembic_archive.setText(QtWidgets.QApplication.translate("Widget_ImportAlembic", "Alembic Archive", None, -1))

