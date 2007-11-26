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

#include <QColor>
#include <QDateTime>
#include <QFont>
#include <QIcon>
#include <QPainter>
#include <QPixmap>
#include <QRect>
#include <QSettings>
#include "trayicon.h"

TrayIcon::TrayIcon(QWidget *parent)
    : QSystemTrayIcon(parent)
{
    refreshQuota();
    connect(&captchaWindow, SIGNAL(accepted()), this, SLOT(continueCheckQuota()));
    connect(captchaWindow.changePicture, SIGNAL(clicked()), this, SLOT(checkQuota()));
    connect(&quota, SIGNAL(gotCaptcha(QByteArray)), &captchaWindow, SLOT(displayCaptcha(QByteArray)));
    connect(&quota, SIGNAL(gotResults(QString)), this, SLOT(continueCheckQuota(QString)));
    connect(this, SIGNAL(activated(QSystemTrayIcon::ActivationReason)), this, SLOT(on_activated(QSystemTrayIcon::ActivationReason)));
}

void TrayIcon::on_activated(QSystemTrayIcon::ActivationReason activationReason)
{
    if (activationReason == DoubleClick) checkQuota();
}

void TrayIcon::refreshQuota()
{
    QSettings settings;
    QString quota;
    if (settings.contains("lastReport/download"))
        quota = tr("%L1\nGB").arg(settings.value("lastReport/download").toDouble()/1073741824, 0, 'f', 2);
    else
        quota = tr("?\nGB");
    QPixmap pixmap(32, 32);
    pixmap.fill(QColor(settings.value("trayIcon/backgrounColor", "red").toString()));
    QPainter painter(&pixmap);
    painter.setPen(QColor(settings.value("trayIcon/textColor", "white").toString()));
    painter.setFont(QFont("", 10, QFont::Bold));
    painter.drawText(QRect(0,0,32,32), Qt::AlignCenter, quota);
    painter.end();
    setIcon(QIcon(pixmap));
    if (settings.contains("lastReport/download")) {
        setToolTip(tr("Used Quota: %L1 GB\nLatest Update: %2").arg(
            settings.value("lastReport/download").toDouble()/1073741824).arg(
            settings.value("lastReport/date").toDateTime().toString("d MMMM dddd hh.mm")));
    } else {
        setToolTip(tr("Double click to check quota."));
    }
}

void TrayIcon::checkQuota()
{

}

void TrayIcon::continueCheckQuota(QString content)
{

}
