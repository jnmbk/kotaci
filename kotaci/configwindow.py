# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/configwindow.ui'
#
# Created: Sun Nov 11 13:00:54 2007
#      by: PyQt4 UI code generator 4.3.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(QtCore.QSize(QtCore.QRect(0,0,264,188).size()).expandedTo(Dialog.minimumSizeHint()))

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setWindowIcon(QtGui.QIcon(":/icons/configure.png"))

        self.gridlayout = QtGui.QGridLayout(Dialog)
        self.gridlayout.setObjectName("gridlayout")

        self.tabWidget = QtGui.QTabWidget(Dialog)
        self.tabWidget.setObjectName("tabWidget")

        self.tab = QtGui.QWidget()
        self.tab.setObjectName("tab")

        self.gridlayout1 = QtGui.QGridLayout(self.tab)
        self.gridlayout1.setObjectName("gridlayout1")

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setObjectName("hboxlayout")

        self.vboxlayout = QtGui.QVBoxLayout()
        self.vboxlayout.setObjectName("vboxlayout")

        self.labelUsername = QtGui.QLabel(self.tab)
        self.labelUsername.setObjectName("labelUsername")
        self.vboxlayout.addWidget(self.labelUsername)

        self.labelPassword = QtGui.QLabel(self.tab)
        self.labelPassword.setObjectName("labelPassword")
        self.vboxlayout.addWidget(self.labelPassword)
        self.hboxlayout.addLayout(self.vboxlayout)

        self.vboxlayout1 = QtGui.QVBoxLayout()
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.username = QtGui.QLineEdit(self.tab)
        self.username.setObjectName("username")
        self.vboxlayout1.addWidget(self.username)

        self.password = QtGui.QLineEdit(self.tab)
        self.password.setEchoMode(QtGui.QLineEdit.Password)
        self.password.setObjectName("password")
        self.vboxlayout1.addWidget(self.password)
        self.hboxlayout.addLayout(self.vboxlayout1)
        self.gridlayout1.addLayout(self.hboxlayout,0,0,1,1)

        self.savePassword = QtGui.QCheckBox(self.tab)
        self.savePassword.setObjectName("savePassword")
        self.gridlayout1.addWidget(self.savePassword,1,0,1,1)

        spacerItem = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout1.addItem(spacerItem,0,1,1,1)
        self.tabWidget.addTab(self.tab,"")

        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName("tab_2")

        self.gridlayout2 = QtGui.QGridLayout(self.tab_2)
        self.gridlayout2.setObjectName("gridlayout2")

        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setObjectName("hboxlayout1")

        self.vboxlayout2 = QtGui.QVBoxLayout()
        self.vboxlayout2.setObjectName("vboxlayout2")

        self.labelTextColor = QtGui.QLabel(self.tab_2)
        self.labelTextColor.setObjectName("labelTextColor")
        self.vboxlayout2.addWidget(self.labelTextColor)

        self.labelBackgroundColor = QtGui.QLabel(self.tab_2)
        self.labelBackgroundColor.setObjectName("labelBackgroundColor")
        self.vboxlayout2.addWidget(self.labelBackgroundColor)
        self.hboxlayout1.addLayout(self.vboxlayout2)

        self.vboxlayout3 = QtGui.QVBoxLayout()
        self.vboxlayout3.setObjectName("vboxlayout3")

        self.textColor = QtGui.QComboBox(self.tab_2)
        self.textColor.setObjectName("textColor")
        self.vboxlayout3.addWidget(self.textColor)

        self.backgroundColor = QtGui.QComboBox(self.tab_2)
        self.backgroundColor.setObjectName("backgroundColor")
        self.vboxlayout3.addWidget(self.backgroundColor)
        self.hboxlayout1.addLayout(self.vboxlayout3)
        self.gridlayout2.addLayout(self.hboxlayout1,0,0,1,1)

        spacerItem1 = QtGui.QSpacerItem(20,40,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout2.addItem(spacerItem1,1,0,1,1)

        spacerItem2 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout2.addItem(spacerItem2,0,1,1,1)
        self.tabWidget.addTab(self.tab_2,"")
        self.gridlayout.addWidget(self.tabWidget,0,0,1,1)

        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.NoButton|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridlayout.addWidget(self.buttonBox,1,0,1,1)

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.buttonBox,QtCore.SIGNAL("accepted()"),Dialog.accept)
        QtCore.QObject.connect(self.buttonBox,QtCore.SIGNAL("rejected()"),Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Configure - Kotaci", None, QtGui.QApplication.UnicodeUTF8))
        self.labelUsername.setText(QtGui.QApplication.translate("Dialog", "Username:", None, QtGui.QApplication.UnicodeUTF8))
        self.labelPassword.setText(QtGui.QApplication.translate("Dialog", "Password:", None, QtGui.QApplication.UnicodeUTF8))
        self.username.setWhatsThis(QtGui.QApplication.translate("Dialog", "Enter your TTnet username here.", None, QtGui.QApplication.UnicodeUTF8))
        self.password.setWhatsThis(QtGui.QApplication.translate("Dialog", "Enter your TTnet password here.", None, QtGui.QApplication.UnicodeUTF8))
        self.savePassword.setWhatsThis(QtGui.QApplication.translate("Dialog", "Saves password to configuration file when selected. It may be unsafe to save the password.", None, QtGui.QApplication.UnicodeUTF8))
        self.savePassword.setText(QtGui.QApplication.translate("Dialog", "Save password", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtGui.QApplication.translate("Dialog", "Account", None, QtGui.QApplication.UnicodeUTF8))
        self.labelTextColor.setText(QtGui.QApplication.translate("Dialog", "Text color:", None, QtGui.QApplication.UnicodeUTF8))
        self.labelBackgroundColor.setText(QtGui.QApplication.translate("Dialog", "Background color:", None, QtGui.QApplication.UnicodeUTF8))
        self.textColor.setWhatsThis(QtGui.QApplication.translate("Dialog", "Select tray icon text color.", None, QtGui.QApplication.UnicodeUTF8))
        self.backgroundColor.setWhatsThis(QtGui.QApplication.translate("Dialog", "Select tray icon background color.", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QtGui.QApplication.translate("Dialog", "Tray Icon", None, QtGui.QApplication.UnicodeUTF8))

import kotaci_rc
