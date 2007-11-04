#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under GPL v2
# Copyright 2007, Uğur Çetin
# original version: http://forum.pardus-linux.org/viewtopic.php?t=11305
#TODO: Use QHttp instead of httplib2

import commands, httplib2, os, time, signal, sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import configwindow, captchawindow

class QuotaGrabber:
    def __init__(self):
        self.http = httplib2.Http()

    def getCatpcha(self):
        url = 'http://adslkota.ttnet.net.tr/adslkota/jcaptcha'
        request = {
            "Content-type": "application/x-www-form-urlencoded",
            # Firefox'u destekleyelim
            "User-agent": "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)"
            }
        response, content = self.http.request(url, headers=request)
        self.cookie = {'Cookie': response['set-cookie']}
        open("/tmp/captcha.jpg",'w').write(content)
        return "/tmp/captcha.jpg"

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
            return "syserror"
        elif u"tekrar giriş yapmanız gerekmektedir" in content:
            return "loginerror"
        else:
            start = content.find('<tr class="odd">')
        end = content.find('</tr></tbody></table>')
        content = content[start:end]
        content = content.replace('<tr class="odd">',"")
        content = content.replace('<tr class="even">',"")
        content = content.replace('<td width="100">',"").replace('<br>&nbsp;'," ")
        content = content.replace('</tr>'," ").replace("</td>","")
        return content

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

    def checkQuota(self):
        settings = QSettings()
        self.captchaWindow.show()
        self.captchaWindow.displayCaptcha(self.grabber.getCatpcha())

    def continueCheckQuota(self):
        results = self.grabber.getResults(self.captchaWindow.lineEdit.text())
        if results == "syserror":
            QMessageBox.critical(None, "Hata", u"Sistem Hatası")
        if results == "loginerror":
            QMessageBox.critical(None, "Hata", u"Giriş Hatası\nKullanıcı adı ve parolanızı kontrol edin.")
        else:
            lastReport = results.split("\n")[-1]
            lastReport = float(lastReport[:lastReport.index('(')-1].replace('.', ''))
            lastReport = round(lastReport/1024/1024/1024,2)
            settings.setValue("lastreport/size", QVariant(str(lastReport).replace('.',',')))
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
        #settings.setValue("checkInterval", QVariant(self.checkInterval.value()))

    def loadSettings(self):
        settings = QSettings()
        self.username.setText(settings.value("username").toString())
        self.password.setText(settings.value("password").toString())
        #self.checkInterval.setValue(settings.value("checkInterval", QVariant(2)).toInt()[0])

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QApplication(sys.argv)
    app.setApplicationName("kotacı")
    app.setOrganizationName("kotacı")
    app.setQuitOnLastWindowClosed(False)
    settings = QSettings()

    menu = QMenu()
    actionCheckQuota = QAction(u"Şimdi Kontrol et", menu)
    actionConfigure = QAction(u"Yapılandır...", menu)
    actionQuit = QAction(u"Çıkış", menu)

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
