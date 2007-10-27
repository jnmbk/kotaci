# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'config.ui'
#
# Created: Sat Oct 27 10:04:26 2007
#      by: PyQt4 UI code generator 4.3-snapshot-20070811
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(QtCore.QSize(QtCore.QRect(0,0,483,229).size()).expandedTo(Dialog.minimumSizeHint()))

        self.gridlayout = QtGui.QGridLayout(Dialog)
        self.gridlayout.setObjectName("gridlayout")

        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setObjectName("groupBox")

        self.gridlayout1 = QtGui.QGridLayout(self.groupBox)
        self.gridlayout1.setObjectName("gridlayout1")

        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.gridlayout1.addWidget(self.label,0,0,1,1)

        self.username = QtGui.QLineEdit(self.groupBox)
        self.username.setObjectName("username")
        self.gridlayout1.addWidget(self.username,0,1,1,1)

        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.gridlayout1.addWidget(self.label_2,1,0,1,1)

        self.password = QtGui.QLineEdit(self.groupBox)
        self.password.setEchoMode(QtGui.QLineEdit.Password)
        self.password.setObjectName("password")
        self.gridlayout1.addWidget(self.password,1,1,1,1)
        self.gridlayout.addWidget(self.groupBox,0,0,1,1)

        self.groupBox_2 = QtGui.QGroupBox(Dialog)
        self.groupBox_2.setObjectName("groupBox_2")

        self.gridlayout2 = QtGui.QGridLayout(self.groupBox_2)
        self.gridlayout2.setObjectName("gridlayout2")

        self.label_3 = QtGui.QLabel(self.groupBox_2)
        self.label_3.setObjectName("label_3")
        self.gridlayout2.addWidget(self.label_3,0,0,1,1)

        self.checkInterval = QtGui.QSpinBox(self.groupBox_2)
        self.checkInterval.setMinimum(2)
        self.checkInterval.setMaximum(12)
        self.checkInterval.setSingleStep(1)
        self.checkInterval.setObjectName("checkInterval")
        self.gridlayout2.addWidget(self.checkInterval,0,1,1,2)

        self.label_5 = QtGui.QLabel(self.groupBox_2)
        self.label_5.setObjectName("label_5")
        self.gridlayout2.addWidget(self.label_5,1,0,1,2)

        self.retries = QtGui.QSpinBox(self.groupBox_2)
        self.retries.setMinimum(1)
        self.retries.setMaximum(10)
        self.retries.setObjectName("retries")
        self.gridlayout2.addWidget(self.retries,1,2,1,1)
        self.gridlayout.addWidget(self.groupBox_2,0,1,1,1)

        self.groupBox_3 = QtGui.QGroupBox(Dialog)
        self.groupBox_3.setObjectName("groupBox_3")

        self.gridlayout3 = QtGui.QGridLayout(self.groupBox_3)
        self.gridlayout3.setObjectName("gridlayout3")

        self.label_4 = QtGui.QLabel(self.groupBox_3)
        self.label_4.setObjectName("label_4")
        self.gridlayout3.addWidget(self.label_4,0,0,1,1)

        self.chars = QtGui.QSpinBox(self.groupBox_3)
        self.chars.setMinimum(1)
        self.chars.setMaximum(3)
        self.chars.setObjectName("chars")
        self.gridlayout3.addWidget(self.chars,0,1,1,1)
        self.gridlayout.addWidget(self.groupBox_3,1,0,1,2)

        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.NoButton|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridlayout.addWidget(self.buttonBox,2,0,1,2)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox,QtCore.SIGNAL("accepted()"),Dialog.accept)
        QtCore.QObject.connect(self.buttonBox,QtCore.SIGNAL("rejected()"),Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Ayarlar", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("Dialog", "Hesap Bilgileri", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setToolTip(QtGui.QApplication.translate("Dialog", "TTnet kullanıcı adınızı girin (sonuna @ttnet koymayın)", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Kullanıcı adı:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setToolTip(QtGui.QApplication.translate("Dialog", "TTnet parolanızı girin", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "Parola:", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("Dialog", "Kota Kontrolü", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setToolTip(QtGui.QApplication.translate("Dialog", "Kota bilgileriniz 6 saatte bir güncellenir. Bu yüzden kontrol etme sıklığının düşük olmasına gerek yoktur.", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Dialog", "Kontrol etme sıklığı:", None, QtGui.QApplication.UnicodeUTF8))
        self.checkInterval.setSuffix(QtGui.QApplication.translate("Dialog", " saat", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setToolTip(QtGui.QApplication.translate("Dialog", "Giriş başarısız olunca tekrar giriş yapılmaya çalışılır", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("Dialog", "Tekrar deneme sayısı:", None, QtGui.QApplication.UnicodeUTF8))
        self.retries.setSuffix(QtGui.QApplication.translate("Dialog", " defa", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_3.setTitle(QtGui.QApplication.translate("Dialog", "Görünüm", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setToolTip(QtGui.QApplication.translate("Dialog", "Daha az karakter daha az ayrıntı demektir. Fakat simgede daha kolay görülür.", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Dialog", "Simgede gösterilecek karakter sayısı:", None, QtGui.QApplication.UnicodeUTF8))

