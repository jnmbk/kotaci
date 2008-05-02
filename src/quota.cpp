/*
 * kotaci, ADSL quota viewer for Turkey
 * Copyright (C) 2007, Uğur Çetin
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * Please read the COPYING file.
 */

#include "quota.h"

Quota::Quota(QObject *parent)
    : QObject(parent)
{
    http.setHost("adslkota.ttnet.net.tr");
    requestHeader.setValue("Host", "adslkota.ttnet.net.tr");
    codec = QTextCodec::codecForName("Windows-1254");
}

void Quota::getCaptcha()
{
    requestHeader.setRequest("GET", "/adslkota/jcaptcha");
    requestHeader.removeValue("Cookie");
    http.disconnect();
    http.connect(&http, SIGNAL(done(bool)), this, SLOT(gotCaptcha(bool)));
    http.request(requestHeader);
}

void Quota::gotCaptcha(bool connectionError)
{
    if (connectionError)
        emit(error(tr("Connection Error"), http.errorString()));
    else {
        requestHeader.setValue("Cookie", http.lastResponse().value("set-cookie"));
        emit gotCaptcha(http.readAll());
    }
}

void Quota::login(QString captcha, QString username, QString password)
{
    QString page;
    page = "/adslkota/loginSelf.do?dispatch=login&userName=%1&password=%2&captchaResponse=%3&lang=tr";
    page = page.arg(username, password, captcha);
    requestHeader.setRequest("GET", page);
    http.disconnect();
    http.connect(&http, SIGNAL(done(bool)), this, SLOT(acceptAgreenment(bool)));
    http.request(requestHeader);
}

void Quota::acceptAgreenment(bool connectionError)
{
    http.disconnect();
    QString content(codec->toUnicode(http.readAll()));
    if (connectionError)
        emit(error(tr("Connection Error"), http.errorString()));
    else if (content.contains(QString::fromUtf8("Güvenlik kodu doğru değil")))
        emit(error(tr("Code Error"), tr("You entered wrong code!")));
    else if (content.contains(QString::fromUtf8("Girilen şifre hatalıdır")))
        emit(error(tr("Password Error"), tr("You entered wrong password!")));
    else if (content.contains(QString::fromUtf8("Giriş başarısız")))
        emit(error(tr("Login Error"), tr("Please check your username from configuration.")));
    else {
        requestHeader.setRequest("GET", "/adslkota/confirmAgreement.do?dispatch=agree");
        http.connect(&http, SIGNAL(done(bool)), this, SLOT(getResult(bool)));
        http.request(requestHeader);
    }
}

void Quota::getResult(bool connectionError)
{
    http.disconnect();
    if (connectionError)
        emit(error(tr("Connection Error"), http.errorString()));
    else {
        requestHeader.setRequest("GET", "/adslkota/viewTransfer.do?dispatch=entry");
        http.connect(&http, SIGNAL(done(bool)), this, SLOT(gotResult(bool)));
        http.request(requestHeader);
    }
}

void Quota::gotResult(bool connectionError)
{
    http.disconnect();
    if (connectionError)
        emit(error(tr("Connection Error"), http.errorString()));
    else {
        QString content = codec->toUnicode(http.readAll());
        if (content.contains(QString::fromUtf8("İşlem hatası"))) {
            emit(error(tr("Error"), tr("TTnet System error")));
        } else {
            int start = content.indexOf("<tr class=\"odd\">");
            int end = content.indexOf("</tr></tbody></table>");
            content = content.mid(start, end - start);
            content = content.remove("<tr class=\"odd\">").remove("<tr class=\"even\">");
            content = content.remove("<td width=\"100\">").remove("<br>&nbsp;");
            content = content.remove("</tr>").remove("</td>");
            if (content.isEmpty())
                emit(error(tr("Unknown Error"), tr("TTnet site may be changed, "
                    "check for updates at http://kotaci.googlecode.com")));
            else
                emit gotResults(content);
        }
    }
}
