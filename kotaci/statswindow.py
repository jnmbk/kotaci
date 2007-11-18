# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/statswindow.ui'
#
# Created: Sun Nov 18 11:56:52 2007
#      by: PyQt4 UI code generator 4.3.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_StatsWindow(object):
    def setupUi(self, StatsWindow):
        StatsWindow.setObjectName("StatsWindow")
        StatsWindow.resize(QtCore.QSize(QtCore.QRect(0,0,332,311).size()).expandedTo(StatsWindow.minimumSizeHint()))
        StatsWindow.setWindowIcon(QtGui.QIcon(":/icons/today.png"))

        self.gridlayout = QtGui.QGridLayout(StatsWindow)
        self.gridlayout.setObjectName("gridlayout")

        self.stats = QtGui.QTreeWidget(StatsWindow)
        self.stats.setRootIsDecorated(False)
        self.stats.setSortingEnabled(False)
        self.stats.setAnimated(True)
        self.stats.setObjectName("stats")
        self.gridlayout.addWidget(self.stats,0,0,1,3)

        spacerItem = QtGui.QSpacerItem(16,27,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem,1,0,1,1)

        self.clearButton = QtGui.QPushButton(StatsWindow)
        self.clearButton.setObjectName("clearButton")
        self.gridlayout.addWidget(self.clearButton,1,1,1,1)

        self.closeButton = QtGui.QPushButton(StatsWindow)
        self.closeButton.setObjectName("closeButton")
        self.gridlayout.addWidget(self.closeButton,1,2,1,1)

        self.retranslateUi(StatsWindow)
        QtCore.QObject.connect(self.closeButton,QtCore.SIGNAL("clicked()"),StatsWindow.close)
        QtCore.QObject.connect(self.clearButton,QtCore.SIGNAL("clicked()"),self.stats.clear)
        QtCore.QMetaObject.connectSlotsByName(StatsWindow)

    def retranslateUi(self, StatsWindow):
        StatsWindow.setWindowTitle(QtGui.QApplication.translate("StatsWindow", "Kotaci - Statistics", None, QtGui.QApplication.UnicodeUTF8))
        self.stats.headerItem().setText(0,QtGui.QApplication.translate("StatsWindow", "Month", None, QtGui.QApplication.UnicodeUTF8))
        self.stats.headerItem().setText(1,QtGui.QApplication.translate("StatsWindow", "Download", None, QtGui.QApplication.UnicodeUTF8))
        self.stats.headerItem().setText(2,QtGui.QApplication.translate("StatsWindow", "Upload", None, QtGui.QApplication.UnicodeUTF8))
        self.clearButton.setText(QtGui.QApplication.translate("StatsWindow", "Clear Statistics", None, QtGui.QApplication.UnicodeUTF8))
        self.closeButton.setText(QtGui.QApplication.translate("StatsWindow", "Close", None, QtGui.QApplication.UnicodeUTF8))

import kotaci_rc
