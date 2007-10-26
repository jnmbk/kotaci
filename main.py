#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under GPL v2
# Copyright 2007, Uğur Çetin
# original version: http://forum.pardus-linux.org/viewtopic.php?t=11305
#TODO: parola, kullanıcı adı, okuma sıklığı ayarı ekranı
#TODO: okunduğu anda simgeyi yenileme
#TODO: geçmiş ayları da ayrıntılı olarak kaydet

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import commands, httplib2, os, time, signal, sys

def grabQuota(username=None, password=None):
    http = httplib2.Http()
    url = 'http://adslkota.ttnet.net.tr/adslkota/jcaptcha'
    request = {
        "Content-type": "application/x-www-form-urlencoded",
        # Firefox'u destekleyelim
        "User-agent": "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)"
        }
    response, content = http.request(url, headers=request)
    cookie = {'Cookie': response['set-cookie']}
    open("/tmp/captcha.jpg",'w').write(content)

    # captcha'yı oku
    #FIXME: temp kullanmadan ve tek komutla da yapılabilir
    os.system("convert /tmp/captcha.jpg "
        "-sharpen 7x7 -colors 5 /tmp/captcha.png")
    captcha = commands.getoutput("gocr /tmp/captcha.png")
    captcha = captcha.strip().replace(" ", "").replace("O", "0")

    # anlaşmayı kabul et
    url= "http://adslkota.ttnet.net.tr/adslkota/loginSelf.do?"\
        "dispatch=login&userName=%s&password=%s&captchaResponse=%s"\
        % (username, password, captcha)
    http.request(url, 'GET', headers=cookie)
    time.sleep(0.2)
    url = "http://adslkota.ttnet.net.tr/adslkota/"\
        "confirmAgreement.do?dispatch=agree"
    http.request(url, 'GET', headers=cookie)
    time.sleep(0.2)

    # sonucu oku
    url = "http://adslkota.ttnet.net.tr/adslkota/viewTransfer.do?dispatch=entry"
    response, content = http.request(url, 'GET', headers=cookie)
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

class TrayIcon(QSystemTrayIcon):
    def __init__(self):
        QSystemTrayIcon.__init__(self)
        self.pixmap = QPixmap(32, 32)
        self.setIcon(QIcon(self.pixmap))
        self.refreshQuota()

    def refreshQuota(self):
        settings = QSettings()
        quota = settings.value("lastreport/size", QVariant("?")).toString() + "\nGB"
        self.pixmap.fill(QColor("red"))
        painter = QPainter(self.pixmap)
        painter.setPen(QColor("white"))
        painter.setFont(QFont("", 10, QFont.Bold))
        painter.drawText(QRect(0, 0, 32, 32), Qt.AlignCenter, quota)

    def checkQuota(self):
        settings = QSettings()
        results = grabQuota(
                str(settings.value("username").toString()),
                str(settings.value("password").toString()))
        if results == "syserror":
            QMessageBox.critical(None, "Hata", u"Sistem Hatası")
        if results == "loginerror":
            #FIXME: catcpca yanlış okunmuş da olabilir
            QMessageBox.critical(None, "Hata", u"Giriş Hatası\nKullanıcı adı ve parolanızı kontrol edin.")
        else:
            lastReport = results.split("\n")[-1]
            lastReport = float(lastReport[:lastReport.index('(')-1].replace('.', ''))
            lastReport = round(lastReport/1024/1024/1024,2)
            settings.setValue("lastreport/size", QVariant(str(lastReport).replace('.',',')))
            QMessageBox.information(None, "Kota Bilgisi", results)
            self.refreshQuota()


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QApplication(sys.argv)
    app.setApplicationName("adslkota")
    app.setOrganizationName("adslkota")
    app.setQuitOnLastWindowClosed(False)
    settings = QSettings()

    menu = QMenu()
    actionCheckQuota = QAction(u"Şimdi Kontrol et", menu)
    actionQuit = QAction(u"Çıkış", menu)

    menu.addAction(actionCheckQuota)
    menu.addAction(actionQuit)

    trayIcon = TrayIcon()

    QObject.connect(actionQuit, SIGNAL("activated()"), app.quit)
    QObject.connect(actionCheckQuota, SIGNAL("activated()"), trayIcon.checkQuota)

    trayIcon.setContextMenu(menu)
    trayIcon.show()

    app.exec_()
