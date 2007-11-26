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

#include <QTextCodec>
#include "quota.h"

Quota::Quota(QObject *parent)
    : QObject(parent)
{
    http.setHost("adslkota.ttnet.net.tr");
    requestHeader.setValue("Host", "adslkota.ttnet.net.tr");
}

void Quota::getCaptcha()
{
    requestHeader.setRequest("Get", "/adslkota/jcaptcha");
    requestHeader.removeValue("Cookie");
    http.disconnect();
    http.connect(&http, SIGNAL(done(bool)), this, SLOT(gotCaptcha(bool)));
    http.request(requestHeader);
}

void Quota::gotCaptcha(bool error)
{
    requestHeader.setValue("Cookie", http.lastResponse().value("set-cookie"));
    emit gotCaptcha(http.readAll());
}

void Quota::login(QString *captcha, QString *username, QString *password)
{
    QString page;
    page = "/adslkota/loginSelf.do?dispatch=login&userName=%1&password=%2&captchaResponse=%3";
    page = page.arg(*username, *password, *captcha);
    requestHeader.setRequest("GET", page);
    http.disconnect();
    http.connect(&http, SIGNAL(done(bool)), this, SLOT(acceptAgreenment(bool)));
    http.request(requestHeader);
}

void Quota::acceptAgreenment(bool error)
{
    requestHeader.setRequest("GET", "/adslkota/confirmAgreement.do?dispatch=agree");
    http.disconnect();
    http.connect(&http, SIGNAL(done(bool)), this, SLOT(getResult(bool)));
    http.request(requestHeader);
}

void Quota::getResult(bool error)
{
    requestHeader.setRequest("GET", "/adslkota/viewTransfer.do?dispatch=entry");
    http.disconnect();
    http.connect(&http, SIGNAL(done(bool)), this, SLOT(gotResult(bool)));
    http.request(requestHeader);
}

void Quota::gotResult(bool error)
{
    QTextCodec *codec = QTextCodec::codecForName("Windows-1254");

    http.disconnect();
    QString content = codec->toUnicode(http.readAll());
    if (content.contains("Sistem Hatası")) {
        content = "syserror";
    } else if (content.contains("tekrar giriş yapmanız gerekmektedir")) {
        content = "loginerror";
    } else {
        int start = content.indexOf("<tr class=\"odd\">");
        int end = content.indexOf("</tr></tbody></table>");
        content = content.mid(start, end - start);
        content = content.remove("<tr class=\"odd\">").remove("<tr class=\"even\">");
        content = content.remove("<td width=\"100\">").remove("<br>&nbsp;");
        content = content.remove("</tr>").remove("</td>");
    }
    emit gotResults(content);
}
