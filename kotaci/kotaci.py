#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under GPL v2
# Copyright 2007, Uğur Çetin
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

import configwindow, captchawindow

class icons:
    path = "/usr/share/icons/Tulliana-2.0/16x16/"
    exit = path + "actions/exit.png"
    configure = path + "actions/configure.png"
    check = path + "actions/ok.png"

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

    def getResults(self, captcha):
        settings = QSettings()
        username = settings.value("username").toString()
        password = settings.value("password").toString()

        # anlaşmayı kabul et
        url= "http://adslkota.ttnet.net.tr/adslkota/loginSelf.do?"\
            "dispatch=login&userName=%s&password=%s&captchaResponse=%s"\
            % (username, password, captcha)
        self.http.request(url, headers=self.cookie)
        time.sleep(0.2)
        url = "http://adslkota.ttnet.net.tr/adslkota/"\
            "confirmAgreement.do?dispatch=agree"
        self.http.request(url, headers=self.cookie)
        time.sleep(0.2)

        # sonucu oku
        url = "http://adslkota.ttnet.net.tr/adslkota/viewTransfer.do?dispatch=entry"
        response, content = self.http.request(url, headers=self.cookie)
        content = unicode(content, "windows-1254", errors="ignore")
        if u"Sistem Hatası" in content:
            content = "syserror"
        elif u"tekrar giriş yapmanız gerekmektedir" in content:
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


class TrayIcon(QSystemTrayIcon):
    def __init__(self):
        QSystemTrayIcon.__init__(self)
        self.refreshQuota()
        self.captchaWindow = CaptchaWindow()
        self.grabber = QuotaGrabber()
        QObject.connect(self.captchaWindow, SIGNAL("accepted()"), self.continueCheckQuota)
        QObject.connect(self.grabber, SIGNAL("captchaWritten"), self.captchaWindow.displayCaptcha)
        QObject.connect(self.grabber, SIGNAL("gotResults"), self.continueCheckQuota)

    def refreshQuota(self):
        settings = QSettings()
        quota = settings.value("lastreport/size", QVariant("?")).toString() + "\nGB"
        pixmap = QPixmap(32, 32)
        pixmap.fill(QColor("red"))
        painter = QPainter(pixmap)
        painter.setPen(QColor("white"))
        painter.setFont(QFont("", 10, QFont.Bold))
        painter.drawText(QRect(0, 0, 32, 32), Qt.AlignCenter, quota)
        painter.end()
        icon = QIcon(pixmap)
        self.setIcon(icon)
        if settings.contains("lastreport/bytes"):
            self.setToolTip(
                u"Kullanılan kota: %s GB\nSon Güncelleme: %s" %\
                (str(round(settings.value("lastreport/bytes").toInt()[0]/1024.0/1024/1024,3)).replace('.',','),
                settings.value("lastreport/date").toDateTime().toString("d MMMM dddd hh.mm")))
        else:
            self.setToolTip(u"Lütfen sağ tıklayıp kotanızı kontrol ediniz.")

    def checkQuota(self):
        self.captchaWindow.show()
        self.captchaWindow.captcha.clear()
        self.captchaWindow.lineEdit.clear()
        self.captchaWindow.captcha.setText(u"Yükleniyor, lütfen bekleyin...")
        thread.start_new_thread(self.grabber.getCatpcha, ())

    def continueCheckQuota(self, results = None):
        if results == None:
            if self.captchaWindow.lineEdit.text() == "":
                self.captchaWindow.show()
            else:
                thread.start_new_thread(self.grabber.getResults, (self.captchaWindow.lineEdit.text(),))
        else:
            if results == "syserror":
                QMessageBox.critical(None, "Hata", u"Sistem Hatası")
            if results == "loginerror":
                QMessageBox.critical(None, "Hata",
                    u"Giriş Hatası. Eğer tercihlerden kullanıcı adınızı ve "\
                    "parolanızı belirlemediyseniz önce bunları belirleyin. "\
                    "Ayrıca resimdeki yazıyı da yanlış yazmış olabilirsiniz.")
            else:
                lastReport = results.split("\n")[-1]
                lastReport = float(lastReport[:lastReport.index('(')-1].replace('.', ''))
                settings.setValue("lastReport/bytes", QVariant(lastReport))
                lastReport = round(lastReport/1024/1024/1024,2)
                settings.setValue("lastreport/size", QVariant(str(lastReport).replace('.',',')))
                settings.setValue("lastReport/date", QVariant(QDateTime.currentDateTime()))
                QMessageBox.information(None, "Kota Bilgisi", results)
                self.refreshQuota()

class ConfigWindow(QDialog, configwindow.Ui_Dialog):
    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)
        QObject.connect(self, SIGNAL("accepted()"), self.saveSettings)
        QObject.connect(self, SIGNAL("rejected()"), self.loadSettings)
        self.loadSettings()

    def saveSettings(self):
        settings = QSettings()
        settings.setValue("username", QVariant(self.username.text()))
        settings.setValue("password", QVariant(self.password.text()))

    def loadSettings(self):
        settings = QSettings()
        self.username.setText(settings.value("username").toString())
        self.password.setText(settings.value("password").toString())

def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QApplication(sys.argv)
    app.setApplicationName("kotacı")
    app.setOrganizationName("kotacı")
    app.setQuitOnLastWindowClosed(False)
    settings = QSettings()

    menu = QMenu()
    actionCheckQuota = QAction(QIcon(icons.check), u"Şimdi Kontrol et", menu)
    actionConfigure = QAction(QIcon(icons.configure), u"Yapılandır...", menu)
    actionQuit = QAction(QIcon(icons.exit), u"Çıkış", menu)

    menu.addAction(actionCheckQuota)
    menu.addAction(actionConfigure)
    menu.addAction(actionQuit)

    trayIcon = TrayIcon()
    configWindow = ConfigWindow()
    captchaWindow = CaptchaWindow()

    QObject.connect(actionQuit, SIGNAL("activated()"), app.quit)
    QObject.connect(actionConfigure, SIGNAL("activated()"), configWindow.show)
    QObject.connect(actionCheckQuota, SIGNAL("activated()"), trayIcon.checkQuota)

    trayIcon.setContextMenu(menu)
    trayIcon.show()

    app.exec_()

if __name__ == "__main__":
    main()
