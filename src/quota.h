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

#ifndef QUOTA_H
#define QUOTA_H

#include <QByteArray>
#include <QHttp>
#include <QHttpRequestHeader>
#include <QString>

class Quota : public QObject
{
    Q_OBJECT

    public:
        Quota(QObject *parent = 0);
        QHttp http;
        QHttpRequestHeader requestHeader;

    signals:
        void connectionError(QString errorString);
        void gotCaptcha(QByteArray captcha);
        void gotResults(QString content);

    private slots:
        void gotCaptcha(bool error);
        void acceptAgreenment(bool error);
        void getResult(bool error);
        void gotResult(bool error);

    public slots:
        void getCaptcha();
        void login(QString captcha, QString username, QString password);
};

#endif
