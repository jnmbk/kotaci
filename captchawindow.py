# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'captcha.ui'
#
# Created: Sun Nov  4 07:56:56 2007
#      by: PyQt4 UI code generator 4.3.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_CaptchaDialog(object):
    def setupUi(self, CaptchaDialog):
        CaptchaDialog.setObjectName("CaptchaDialog")
        CaptchaDialog.resize(QtCore.QSize(QtCore.QRect(0,0,318,207).size()).expandedTo(CaptchaDialog.minimumSizeHint()))

        self.gridlayout = QtGui.QGridLayout(CaptchaDialog)
        self.gridlayout.setObjectName("gridlayout")

        self.captcha = QtGui.QLabel(CaptchaDialog)
        self.captcha.setMinimumSize(QtCore.QSize(300,100))
        self.captcha.setAlignment(QtCore.Qt.AlignCenter)
        self.captcha.setWordWrap(True)
        self.captcha.setObjectName("captcha")
        self.gridlayout.addWidget(self.captcha,0,0,1,1)

        self.label = QtGui.QLabel(CaptchaDialog)
        self.label.setObjectName("label")
        self.gridlayout.addWidget(self.label,1,0,1,1)

        self.lineEdit = QtGui.QLineEdit(CaptchaDialog)
        self.lineEdit.setObjectName("lineEdit")
        self.gridlayout.addWidget(self.lineEdit,2,0,1,1)

        self.buttonBox = QtGui.QDialogButtonBox(CaptchaDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.NoButton|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridlayout.addWidget(self.buttonBox,3,0,1,1)

        self.retranslateUi(CaptchaDialog)
        QtCore.QObject.connect(self.buttonBox,QtCore.SIGNAL("accepted()"),CaptchaDialog.accept)
        QtCore.QObject.connect(self.buttonBox,QtCore.SIGNAL("rejected()"),CaptchaDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(CaptchaDialog)

    def retranslateUi(self, CaptchaDialog):
        CaptchaDialog.setWindowTitle(QtGui.QApplication.translate("CaptchaDialog", "Kotacı", None, QtGui.QApplication.UnicodeUTF8))
        self.captcha.setText(QtGui.QApplication.translate("CaptchaDialog", "Yükleniyor, lütfen bekleyin...", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("CaptchaDialog", "Aşağıdaki kutuya resimde gördüğünüzü yazın:", None, QtGui.QApplication.UnicodeUTF8))
