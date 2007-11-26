#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under GPL v2
# Copyright 2007, Ugur Cetin
# original version: http://forum.pardus-linux.org/viewtopic.php?t=11305
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

import signal, sys

from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4 import QtNetwork

import configwindow, captchawindow, statswindow, kotaci_rc

def byte2gb(bytes, rounding=3):
    return round(bytes/1073741824,rounding)

def getValues(results):
    months = [u'Ocak', u'\u015eubat', u'Mart', u'Nisan', u'May\u0131s', u'Haziran',
            u'Temmuz', u'A\u011fustos', u'Eyl\xfcl', u'Ekim', u'Kas\u0131m', u'Aral\u0131k']
    date = QtCore.QDate(int(results[0]), months.index(results[1])+1, 1)
    upload = int(results[2].replace('.', ''))
    download = int(results[5].replace('.', ''))
    return (date, download, upload)

class QuotaGrabber(QtCore.QObject):
    def __init__(self):
        QtCore.QObject.__init__(self)
        self.http = QtNetwork.QHttp("adslkota.ttnet.net.tr")
        self.header = QtNetwork.QHttpRequestHeader()
        self.header.setValue("Content-type", "application/x-www-form-urlencoded")
        self.header.setValue("Host", "adslkota.ttnet.net.tr")
        self.header.setValue("User-agent", "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)")

    def getCatpcha(self):
        url = '/adslkota/jcaptcha'
        QtCore.QObject.disconnect(self.http, QtCore.SIGNAL("done(bool)"), self.gotCaptcha)
        QtCore.QObject.connect(self.http, QtCore.SIGNAL("done(bool)"), self.gotCaptcha)
        self.header.setRequest("GET", url)
        self.header.removeValue("Cookie")
        self.http.request(self.header)

    def gotCaptcha(self, error):
        if error:
            print self.http.errorString()
        cookie = self.http.lastResponse().value("set-cookie")
        self.header.setValue("Cookie", cookie)
        self.emit(QtCore.SIGNAL("gotCaptcha"), self.http.readAll())

    def login(self, captcha, username, password):
        url= "/adslkota/loginSelf.do?"\
            "dispatch=login&userName=%s&password=%s&captchaResponse=%s"\
            % (username, password, captcha)
        self.header.setRequest("GET", url)
        QtCore.QObject.disconnect(self.http, QtCore.SIGNAL("done(bool)"), self.gotCaptcha)
        QtCore.QObject.connect(self.http, QtCore.SIGNAL("done(bool)"), self.acceptAgreenment)
        self.http.request(self.header)

    def acceptAgreenment(self, error):
        if error:
            print self.http.errorString()
        url = "/adslkota/confirmAgreement.do?dispatch=agree"
        self.header.setRequest("GET", url)
        QtCore.QObject.disconnect(self.http, QtCore.SIGNAL("done(bool)"), self.acceptAgreenment)
        QtCore.QObject.connect(self.http, QtCore.SIGNAL("done(bool)"), self.getResult)
        self.http.request(self.header)

    def getResult(self, error):
        if error:
            print self.http.errorString()
        url = "/adslkota/viewTransfer.do?dispatch=entry"
        self.header.setRequest("GET", url)
        QtCore.QObject.disconnect(self.http, QtCore.SIGNAL("done(bool)"), self.getResult)
        QtCore.QObject.connect(self.http, QtCore.SIGNAL("done(bool)"), self.gotResult)
        self.http.request(self.header)

    def gotResult(self, error):
        QtCore.QObject.disconnect(self.http, QtCore.SIGNAL("done(bool)"), self.gotResult)
        if error:
            print self.http.errorString()
        content = self.http.readAll()
        content = unicode(content, "windows-1254", errors="ignore")
        if u"Sistem Hatas" in content:
            content = "syserror"
        elif "tekrar" in content and "gerekmektedir" in content:
            content = "loginerror"
        else:
            start = content.find('<tr class="odd">')
            end = content.find('</tr></tbody></table>')
            content = content[start:end]
            content = content.replace('<tr class="odd">',"")
            content = content.replace('<tr class="even">',"")
            content = content.replace('<td width="100">',"").replace('<br>&nbsp;'," ")
            content = content.replace('</tr>'," ").replace("</td>","")
        self.emit(QtCore.SIGNAL("gotResults"), content)

class CaptchaWindow(QtGui.QDialog, captchawindow.Ui_CaptchaDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)

    def displayCaptcha(self, byteArray):
        self.captcha.clear()
        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(byteArray)
        self.captcha.setPixmap(pixmap)


class StatsWindow(QtGui.QDialog, statswindow.Ui_StatsWindow):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        QtCore.QObject.connect(self.clearButton, QtCore.SIGNAL("clicked()"), self.clearStats)
        self.updateStats()

    def updateStats(self):
        self.stats.clear()
        settings = QtCore.QSettings()
        settings.beginGroup("Stats")
        for key in [i for i in settings.childKeys() if QtCore.QDate.fromString(i, "yyyyMM").isValid()]:
            list = settings.value(key).toList()
            item = QtGui.QTreeWidgetItem(self.stats)
            item.setText(0, QtCore.QDate.fromString(key, "yyyyMM").toString("MMMM yyyy"))
            item.setText(1, QtCore.QString("%L2 GB").arg(byte2gb(list[0].toDouble()[0])))
            item.setText(2, QtCore.QString("%L2 GB").arg(byte2gb(list[1].toDouble()[0])))
        settings.endGroup()
        item = QtGui.QTreeWidgetItem(self.stats)
        item.setText(0, settings.value("lastReport/date").toDate().toString("MMMM yyyy"))
        download = settings.value("lastReport/download").toDouble()[0]
        item.setText(1, QtCore.QString("%L2 GB").arg(byte2gb(download)))
        upload = settings.value("lastReport/upload").toDouble()[0]
        item.setText(2, QtCore.QString("%L2 GB").arg(byte2gb(upload)))

    def clearStats(self):
        settings = QtCore.QSettings()
        settings.remove("Stats")
        self.updateStats()

class TrayIcon(QtGui.QSystemTrayIcon):
    def __init__(self):
        QtGui.QSystemTrayIcon.__init__(self)
        self.refreshQuota()
        self.captchaWindow = CaptchaWindow()
        self.grabber = QuotaGrabber()
        self.statsWindow = StatsWindow()
        QtCore.QObject.connect(self.captchaWindow, QtCore.SIGNAL("accepted()"), self.continueCheckQuota)
        QtCore.QObject.connect(self.captchaWindow.changePicture, QtCore.SIGNAL("clicked()"), self.checkQuota)
        QtCore.QObject.connect(self.grabber, QtCore.SIGNAL("gotCaptcha"), self.captchaWindow.displayCaptcha)
        QtCore.QObject.connect(self.grabber, QtCore.SIGNAL("gotResults"), self.continueCheckQuota)
        QtCore.QObject.connect(self, QtCore.SIGNAL("activated(QSystemTrayIcon::ActivationReason)"), self.on_activated)

    def on_activated(self, activationReason):
        # check quota on double click
        if activationReason == self.DoubleClick:
            self.checkQuota()

    def refreshQuota(self):
        # reads quota information from settings, and changes tray icon accordingly
        settings = QtCore.QSettings()
        if settings.contains("lastReport/download"):
            quota = self.tr("%L1\nGB").arg(byte2gb(settings.value("lastReport/download").toDouble()[0], 2))
        else:
            quota = self.tr("?\nGB")
        pixmap = QtGui.QPixmap(32, 32)
        pixmap.fill(QtGui.QColor(settings.value("trayIcon/backgroundColor", QtCore.QVariant("red")).toString()))
        painter = QtGui.QPainter(pixmap)
        painter.setPen(QtGui.QColor(settings.value("trayIcon/textColor", QtCore.QVariant("white")).toString()))
        painter.setFont(QtGui.QFont("", 10, QtGui.QFont.Bold))
        painter.drawText(QtCore.QRect(0, 0, 32, 32), QtCore.Qt.AlignCenter, quota)
        painter.end()
        icon = QtGui.QIcon(pixmap)
        self.setIcon(icon)
        if settings.contains("lastReport/download"):
            self.setToolTip(
                self.tr("Used Quota: %L1 GB\nLatest Update: %2").arg(
                byte2gb(settings.value("lastReport/download").toDouble()[0])).arg(
                settings.value("lastReport/date").toDateTime().toString("d MMMM dddd hh.mm")))
        else:
            self.setToolTip(self.tr("Double click to check quota."))

    def checkQuota(self):
        self.captchaWindow.show()
        self.captchaWindow.captcha.clear()
        self.captchaWindow.lineEdit.clear()
        self.captchaWindow.captcha.setText(self.tr("Loading, plase wait..."))
        self.grabber.getCatpcha()

    def continueCheckQuota(self, results = None):
        #TODO: That's not cool, fix this mess some time
        if results == None:
            if self.captchaWindow.lineEdit.text() == "":
                self.captchaWindow.show()
            else:
                settings = QtCore.QSettings()
                username = settings.value("username").toString()
                password = settings.value("password").toString()
                if settings.value("savePassword").toInt()[0] != QtCore.Qt.Checked:
                    password = QtGui.QInputDialog.getText(None, self.tr("Enter Password"), self.tr("Enter your TTnet password:"), QtGui.QLineEdit.Password)[0]
                self.grabber.login(self.captchaWindow.lineEdit.text(),username,password)
        else:
            if results == "syserror":
                self.showMessage(self.tr("Error"), self.tr("System Error"), self.Critical)
            if results == "loginerror":
                self.showMessage(self.tr("Error"),
                    self.tr("Login error. Be sure you wrote it correctly "\
                    "and have specified a username in configuration."), self.Critical)
            else:
                # write previous two months to stats
                values = []
                values.append(getValues(results.split()[:8]))
                values.append(getValues(results.split()[8:16]))
                settings = QtCore.QSettings()
                settings.beginGroup("Stats")
                for value in values:
                    settings.setValue(value[0].toString("yyyyMM"), QtCore.QVariant([QtCore.QVariant(value[1]), QtCore.QVariant(value[2])]))
                settings.endGroup()

                lastReport = results.split("\n")[-1]
                lastReport = int(lastReport[:lastReport.index('(')-1].replace('.', ''))
                settings.setValue("lastReport/download", QtCore.QVariant(lastReport))
                settings.setValue("lastReport/upload", QtCore.QVariant(getValues(results.split()[16:])[2]))
                settings.setValue("lastReport/date", QtCore.QVariant(QtCore.QDateTime.currentDateTime()))
                self.refreshQuota()
                self.showMessage(self.tr("Quota Information"), self.tr("%L1 bytes\n(%L2 GB)").arg(lastReport).arg(
                    byte2gb(float(lastReport))))
                self.statsWindow.updateStats()

class ConfigWindow(QtGui.QDialog, configwindow.Ui_Dialog):
    def __init__(self, trayIcon):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        self.trayIcon = trayIcon
        QtCore.QObject.connect(self, QtCore.SIGNAL("accepted()"), self.saveSettings)
        QtCore.QObject.connect(self, QtCore.SIGNAL("rejected()"), self.loadSettings)
        # for the color selector
        for color in QtGui.QColor.colorNames():
            pixmap = QtGui.QPixmap(16, 16)
            pixmap.fill(QtGui.QColor(color))
            icon = QtGui.QIcon(pixmap)
            self.textColor.addItem(icon, color)
            self.backgroundColor.addItem(icon, color)
        self.loadSettings()

    def saveSettings(self):
        settings = QtCore.QSettings()
        settings.setValue("username", QtCore.QVariant(self.username.text()))
        settings.setValue("password", QtCore.QVariant(self.password.text()))
        settings.setValue("savePassword", QtCore.QVariant(self.savePassword.checkState()))
        settings.setValue("trayIcon/textColor", QtCore.QVariant(self.textColor.currentText()))
        settings.setValue("trayIcon/backgroundColor", QtCore.QVariant(self.backgroundColor.currentText()))
        self.trayIcon.refreshQuota()
        if self.savePassword.checkState() == QtCore.Qt.Unchecked:
            settings.remove("password")

    def loadSettings(self):
        settings = QtCore.QSettings()
        self.username.setText(settings.value("username").toString())
        self.password.setText(settings.value("password").toString())
        self.savePassword.setCheckState(QtCore.Qt.CheckState(settings.value("savePassword", QtCore.QVariant(QtCore.Qt.Checked)).toInt()[0]))
        self.textColor.setCurrentIndex(self.textColor.findText(settings.value("trayIcon/textColor", QtCore.QVariant("white")).toString()))
        self.backgroundColor.setCurrentIndex(self.textColor.findText(settings.value("trayIcon/backgroundColor", QtCore.QVariant("red")).toString()))
        if self.savePassword.checkState() == QtCore.Qt.Unchecked:
            self.password.setEnabled(False)

def about():
    import __init__
    QtGui.QMessageBox.about(None, QtGui.QApplication.translate("TrayIcon", "About Kotaci", None, QtGui.QApplication.UnicodeUTF8),
        QtGui.QApplication.translate("TrayIcon",
        "<b>Kotaci %1</b> - ttnet ADSL quota displayer<br />Copyright (c) 2007, Ugur Cetin <ugur.jnmbk at gmail.com><br />"\
        "This software is licensed under the terms of GPL-2.<br /><a href=\"http://kotaci.googlecode.com\">"\
        "http://kotaci.googlecode.com</a><br />"\
        "<br />This program uses Tulliana 2.0 icon theme.<br />"\
        "Kotaci nor its authors are in any way affiliated or endorsed by Turk Telekom.", None,
        QtGui.QApplication.UnicodeUTF8).arg(__init__.__version__))

def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QtGui.QApplication(sys.argv)
    app.setApplicationName("kotaci")
    app.setOrganizationName("kotaci")
    app.setQuitOnLastWindowClosed(False)
    settings = QtCore.QSettings()

    locale = QtCore.QLocale.system().name()
    translator = QtCore.QTranslator()
    translator.load(":/kotaci_%s.qm" % locale)
    app.installTranslator(translator)

    trayIcon = TrayIcon()
    configWindow = ConfigWindow(trayIcon)

    menu = QtGui.QMenu()
    actionAbout = QtGui.QAction(QtGui.QIcon(":icons/help1.png"),
        QtGui.QApplication.translate("TrayIcon", "About...", None, QtGui.QApplication.UnicodeUTF8), menu)
    actionCheckQuota = QtGui.QAction(QtGui.QIcon(":icons/ok.png"),
        QtGui.QApplication.translate("TrayIcon", "Check now...", None, QtGui.QApplication.UnicodeUTF8), menu)
    actionConfigure = QtGui.QAction(QtGui.QIcon(":icons/configure.png"),
        QtGui.QApplication.translate("TrayIcon", "Configure...", None, QtGui.QApplication.UnicodeUTF8), menu)
    actionStatistics = QtGui.QAction(QtGui.QIcon(":icons/today.png"),
        QtGui.QApplication.translate("TrayIcon", "Statistics...", None, QtGui.QApplication.UnicodeUTF8), menu)
    actionQuit = QtGui.QAction(QtGui.QIcon(":icons/exit.png"),
        QtGui.QApplication.translate("TrayIcon", "Exit", None, QtGui.QApplication.UnicodeUTF8), menu)

    menu.addAction(actionCheckQuota)
    menu.addAction(actionConfigure)
    menu.addAction(actionStatistics)
    menu.addAction(actionAbout)
    menu.addSeparator()
    menu.addAction(actionQuit)

    QtCore.QObject.connect(actionQuit, QtCore.SIGNAL("activated()"), app.quit)
    QtCore.QObject.connect(actionConfigure, QtCore.SIGNAL("activated()"), configWindow.show)
    QtCore.QObject.connect(actionCheckQuota, QtCore.SIGNAL("activated()"), trayIcon.checkQuota)
    QtCore.QObject.connect(actionStatistics, QtCore.SIGNAL("activated()"), trayIcon.statsWindow.show)
    QtCore.QObject.connect(actionAbout, QtCore.SIGNAL("activated()"), about)

    trayIcon.setContextMenu(menu)
    trayIcon.show()

    app.exec_()

if __name__ == "__main__":
    main()
