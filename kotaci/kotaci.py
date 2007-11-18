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

import commands, httplib2, os, time, signal, sys, thread

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import configwindow, captchawindow, statswindow, kotaci_rc

def byte2gb(bytes, rounding=3):
    return round(bytes/1024/1024/1024,rounding)

def getValues(results):
    months = [u'Ocak', u'\u015eubat', u'Mart', u'Nisan', u'May\u0131s', u'Haziran',
            u'Temmuz', u'A\u011fustos', u'Eyl\xfcl', u'Ekim', u'Kas\u0131m', u'Aral\u0131k']
    date = QDate(int(results[0]), months.index(results[1])+1, 1)
    upload = int(results[2].replace('.', ''))
    download = int(results[5].replace('.', ''))
    return (date, upload, download)

class QuotaGrabber(QObject):
    def __init__(self):
        QObject.__init__(self)
        self.http = httplib2.Http()

    def getCatpcha(self):
        url = 'http://adslkota.ttnet.net.tr/adslkota/jcaptcha'
        request = {
            "Content-type": "application/x-www-form-urlencoded",
            "User-agent": "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)"
            }
        response, content = self.http.request(url, headers=request)
        self.cookie = {'Cookie': response['set-cookie']}
        open("/tmp/captcha.jpg",'w').write(content)
        self.emit(SIGNAL("captchaWritten"), "/tmp/captcha.jpg")

    def getResults(self, captcha, password=None, username=None):
        settings = QSettings()
        if username is None:
            username = settings.value("username").toString()
        if password is None:
            password = settings.value("password").toString()

        # accept agreenment
        url= "http://adslkota.ttnet.net.tr/adslkota/loginSelf.do?"\
            "dispatch=login&userName=%s&password=%s&captchaResponse=%s"\
            % (username, password, captcha)
        self.http.request(url, headers=self.cookie)
        time.sleep(0.2)
        url = "http://adslkota.ttnet.net.tr/adslkota/"\
            "confirmAgreement.do?dispatch=agree"
        self.http.request(url, headers=self.cookie)
        time.sleep(0.2)

        # read result
        url = "http://adslkota.ttnet.net.tr/adslkota/viewTransfer.do?dispatch=entry"
        response, content = self.http.request(url, headers=self.cookie)
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
        self.emit(SIGNAL("gotResults"), content)

class CaptchaWindow(QDialog, captchawindow.Ui_CaptchaDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)

    def displayCaptcha(self, fileName):
        self.captcha.clear()
        self.captcha.setPixmap(QPixmap(fileName))


class StatsWindow(QDialog, statswindow.Ui_StatsWindow):
    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)
        QObject.connect(self.clearButton, SIGNAL("clicked()"), self.clearStats)
        self.updateStats()

    def updateStats(self):
        self.stats.clear()
        settings = QSettings()
        for i in range(settings.beginReadArray("stats")):
            settings.setArrayIndex(i)
            item = QTreeWidgetItem(self.stats)
            item.setText(0, settings.value("date").toDate().toString("MMMM yyyy"))
            download = settings.value("download").toDouble()[0]
            item.setText(1, QString("%L2 GB").arg(byte2gb(download)))
            upload = settings.value("upload").toDouble()[0]
            item.setText(2, QString("%L2 GB").arg(byte2gb(upload)))
        settings.endArray()
        item = QTreeWidgetItem(self.stats)
        item.setText(0, QDate.currentDate().toString("MMMM yyyy"))
        download = settings.value("lastReport/bytes").toDouble()[0]
        item.setText(1, QString("%L2 GB").arg(byte2gb(download)))
        upload = settings.value("lastReport/upload").toDouble()[0]
        item.setText(2, QString("%L2 GB").arg(byte2gb(upload)))

    def clearStats(self):
        settings = QSettings()
        settings.remove("stats")
        self.updateStats()

class TrayIcon(QSystemTrayIcon):
    def __init__(self):
        QSystemTrayIcon.__init__(self)
        self.refreshQuota()
        self.captchaWindow = CaptchaWindow()
        self.grabber = QuotaGrabber()
        self.statsWindow = StatsWindow()
        QObject.connect(self.captchaWindow, SIGNAL("accepted()"), self.continueCheckQuota)
        QObject.connect(self.captchaWindow.changePicture, SIGNAL("clicked()"), self.checkQuota)
        QObject.connect(self.grabber, SIGNAL("captchaWritten"), self.captchaWindow.displayCaptcha)
        QObject.connect(self.grabber, SIGNAL("gotResults"), self.continueCheckQuota)
        QObject.connect(self, SIGNAL("activated(QSystemTrayIcon::ActivationReason)"), self.on_activated)

    def on_activated(self, activationReason):
        if activationReason == self.DoubleClick:
            self.checkQuota()

    def showStats(self):
        self.statsWindow.show()

    def refreshQuota(self):
        settings = QSettings()
        if settings.contains("lastReport/bytes"):
            quota = self.tr("%L1\nGB").arg(byte2gb(settings.value("lastReport/bytes").toDouble()[0], 2))
        else:
            quota = self.tr("?\nGB")
        pixmap = QPixmap(32, 32)
        pixmap.fill(QColor(settings.value("trayIcon/backgroundColor", QVariant("red")).toString()))
        painter = QPainter(pixmap)
        painter.setPen(QColor(settings.value("trayIcon/textColor", QVariant("white")).toString()))
        painter.setFont(QFont("", 10, QFont.Bold))
        painter.drawText(QRect(0, 0, 32, 32), Qt.AlignCenter, quota)
        painter.end()
        icon = QIcon(pixmap)
        self.setIcon(icon)
        if settings.contains("lastReport/bytes"):
            self.setToolTip(
                self.tr("Used Quota: %L1 GB\nLatest Update: %2").arg(
                byte2gb(settings.value("lastReport/bytes").toDouble()[0])).arg(
                settings.value("lastReport/date").toDateTime().toString("d MMMM dddd hh.mm")))
        else:
            self.setToolTip(self.tr("Double click to check quota."))

    def checkQuota(self):
        self.captchaWindow.show()
        self.captchaWindow.captcha.clear()
        self.captchaWindow.lineEdit.clear()
        self.captchaWindow.captcha.setText(self.tr("Loading, plase wait..."))
        thread.start_new_thread(self.grabber.getCatpcha, ())

    def continueCheckQuota(self, results = None):
        if results == None:
            if self.captchaWindow.lineEdit.text() == "":
                self.captchaWindow.show()
            else:
                settings = QSettings()
                if settings.value("savePassword").toInt()[0] != Qt.Checked:
                    password = QInputDialog.getText(None, self.tr("Enter Password"), self.tr("Enter your TTnet password:"), QLineEdit.Password)[0]
                    thread.start_new_thread(self.grabber.getResults, (self.captchaWindow.lineEdit.text(),password))
                else:
                    thread.start_new_thread(self.grabber.getResults, (self.captchaWindow.lineEdit.text(),))
        else:
            if results == "syserror":
                self.showMessage(self.tr("Error"), self.tr("System Error"), self.Critical)
            if results == "loginerror":
                self.showMessage(self.tr("Error"),
                    self.tr("Login error. Be sure you wrote it correctly "\
                    "and have specified a username in configuration."), self.Critical)
            else:
                values = []
                values.append(getValues(results.split()[:8]))
                values.append(getValues(results.split()[8:16]))
                settings = QSettings()
                # clean
                statCount = settings.beginReadArray("stats")
                j = 0
                while j < len(values):
                    for i in range(statCount):
                        settings.setArrayIndex(i)
                        if settings.value("date").toDate().__eq__(values[j][0]):
                            del(values[j])
                            j -= 1
                            break
                    j += 1
                settings.endArray()

                # write
                settings.beginWriteArray("stats")
                for i in range(len(values)):
                    settings.setArrayIndex(i+statCount)
                    settings.setValue("date", QVariant(values[i][0]))
                    settings.setValue("upload", QVariant(values[i][1]))
                    settings.setValue("download", QVariant(values[i][2]))
                settings.endArray()

                lastReport = results.split("\n")[-1]
                lastReport = int(lastReport[:lastReport.index('(')-1].replace('.', ''))
                settings.setValue("lastReport/bytes", QVariant(lastReport))
                settings.setValue("lastReport/upload", QVariant(getValues(results.split()[16:])[1]))
                settings.setValue("lastReport/date", QVariant(QDateTime.currentDateTime()))
                self.refreshQuota()
                self.showMessage(self.tr("Quota Information"), self.tr("%L1 bytes\n(%L2 GB)").arg(lastReport).arg(
                    byte2gb(float(lastReport))))
                self.statsWindow.updateStats()

class ConfigWindow(QDialog, configwindow.Ui_Dialog):
    def __init__(self, trayIcon):
        QDialog.__init__(self)
        self.setupUi(self)
        self.trayIcon = trayIcon
        QObject.connect(self, SIGNAL("accepted()"), self.saveSettings)
        QObject.connect(self, SIGNAL("rejected()"), self.loadSettings)
        for color in QColor.colorNames():
            pixmap = QPixmap(16, 16)
            pixmap.fill(QColor(color))
            icon = QIcon(pixmap)
            self.textColor.addItem(icon, color)
            self.backgroundColor.addItem(icon, color)
        self.loadSettings()

    def saveSettings(self):
        settings = QSettings()
        settings.setValue("username", QVariant(self.username.text()))
        settings.setValue("password", QVariant(self.password.text()))
        settings.setValue("savePassword", QVariant(self.savePassword.checkState()))
        settings.setValue("trayIcon/textColor", QVariant(self.textColor.currentText()))
        settings.setValue("trayIcon/backgroundColor", QVariant(self.backgroundColor.currentText()))
        self.trayIcon.refreshQuota()
        if self.savePassword.checkState() == Qt.Unchecked:
            settings.remove("password")

    def loadSettings(self):
        settings = QSettings()
        self.username.setText(settings.value("username").toString())
        self.password.setText(settings.value("password").toString())
        self.savePassword.setCheckState(Qt.CheckState(settings.value("savePassword", QVariant(Qt.Checked)).toInt()[0]))
        self.textColor.setCurrentIndex(self.textColor.findText(settings.value("trayIcon/textColor", QVariant("white")).toString()))
        self.backgroundColor.setCurrentIndex(self.textColor.findText(settings.value("trayIcon/backgroundColor", QVariant("red")).toString()))
        if self.savePassword.checkState() == Qt.Unchecked:
            self.password.setEnabled(False)

def about():
    import __init__
    QMessageBox.about(None, QApplication.translate("TrayIcon", "About Kotaci", None, QApplication.UnicodeUTF8),
        QApplication.translate("TrayIcon",
        "<b>Kotaci %1</b> - ttnet ADSL quota displayer<br />Copyright (c) 2007, Ugur Cetin <ugur.jnmbk at gmail.com><br />"\
        "This software is licensed under the terms of GPL-2.<br /><a href=\"http://kotaci.googlecode.com\">"\
        "http://kotaci.googlecode.com</a><br /><br />Kotaci nor its authors are in any way affiliated or endorsed by Turk Telekom.", None,
        QApplication.UnicodeUTF8).arg(__init__.__version__))

def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QApplication(sys.argv)
    app.setApplicationName("kotaci")
    app.setOrganizationName("kotaci")
    app.setQuitOnLastWindowClosed(False)
    settings = QSettings()

    locale = QLocale.system().name()
    translator = QTranslator()
    translator.load(":/kotaci_%s.qm" % locale)
    app.installTranslator(translator)

    trayIcon = TrayIcon()
    configWindow = ConfigWindow(trayIcon)

    menu = QMenu()
    actionAbout = QAction(QIcon(":icons/help1.png"),
        QApplication.translate("TrayIcon", "About", None, QApplication.UnicodeUTF8), menu)
    actionCheckQuota = QAction(QIcon(":icons/ok.png"),
        QApplication.translate("TrayIcon", "Check now...", None, QApplication.UnicodeUTF8), menu)
    actionConfigure = QAction(QIcon(":icons/configure.png"),
        QApplication.translate("TrayIcon", "Configure...", None, QApplication.UnicodeUTF8), menu)
    actionStatistics = QAction(QIcon(":icons/today.png"),
        QApplication.translate("TrayIcon", "Statistics...", None, QApplication.UnicodeUTF8), menu)
    actionQuit = QAction(QIcon(":icons/exit.png"),
        QApplication.translate("TrayIcon", "Exit", None, QApplication.UnicodeUTF8), menu)

    menu.addAction(actionCheckQuota)
    menu.addAction(actionConfigure)
    menu.addAction(actionStatistics)
    menu.addAction(actionAbout)
    menu.addSeparator()
    menu.addAction(actionQuit)

    QObject.connect(actionQuit, SIGNAL("activated()"), app.quit)
    QObject.connect(actionConfigure, SIGNAL("activated()"), configWindow.show)
    QObject.connect(actionCheckQuota, SIGNAL("activated()"), trayIcon.checkQuota)
    QObject.connect(actionStatistics, SIGNAL("activated()"), trayIcon.showStats)
    QObject.connect(actionAbout, SIGNAL("activated()"), about)

    trayIcon.setContextMenu(menu)
    trayIcon.show()

    app.exec_()

if __name__ == "__main__":
    main()
