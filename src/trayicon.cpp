/*
 * kotaci, ADSL quota viewer for Turkey
 * Copyright (C) 2007-2009, Uğur Çetin
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * Please read the COPYING file.
 */

#include <QAction>
#include <QColor>
#include <QDateTime>
#include <QDebug>
#include <QFont>
#include <QIcon>
#include <QInputDialog>
#include <QLineEdit>
#include <QList>
#include <QMessageBox>
#include <QPainter>
#include <QPixmap>
#include <QRect>
#include <QRegExp>
#include <QSettings>
#include <QStringList>
#include <QVariant>
#include "trayicon.h"

TrayIcon::TrayIcon(QWidget *parent)
    : QSystemTrayIcon(parent)
{
    actionCheckQuota = new QAction(QIcon(":icons/ok.png"), tr("Check now..."), &menu);
    actionConfigure = new QAction(QIcon(":icons/configure.png"), tr("Configure..."), &menu);
    actionStatistics = new QAction(QIcon(":icons/today.png"), tr("Statistics..."), &menu);
    actionAbout = new QAction(QIcon(":icons/help1.png"), tr("About..."), &menu);
    actionExit = new QAction(QIcon(":icons/exit.png"), tr("Exit"), &menu);

    menu.addAction(actionCheckQuota);
    menu.addAction(actionConfigure);
    menu.addAction(actionStatistics);
    menu.addAction(actionAbout);
    menu.addSeparator();
    menu.addAction(actionExit);
    setContextMenu(&menu);

    refreshQuota();
    connect(&captchaWindow, SIGNAL(accepted()), this, SLOT(continueCheckQuota()));
    connect(captchaWindow.changePicture, SIGNAL(clicked()), this, SLOT(checkQuota()));
    connect(&quota, SIGNAL(gotCaptcha(QByteArray)), &captchaWindow, SLOT(displayCaptcha(QByteArray)));
    connect(&quota, SIGNAL(gotResults(QString)), this, SLOT(finishCheckQuota(QString)));
    connect(&quota, SIGNAL(error(QString, QString)), this, SLOT(showError(QString, QString)));
    connect(this, SIGNAL(activated(QSystemTrayIcon::ActivationReason)), this, SLOT(on_activated(QSystemTrayIcon::ActivationReason)));

    this->configWindow = new ConfigWindow(0, this);

    connect(actionCheckQuota, SIGNAL(activated()), this, SLOT(checkQuota()));
    connect(actionConfigure, SIGNAL(activated()), configWindow, SLOT(show()));
    connect(actionStatistics, SIGNAL(activated()), &statsWindow, SLOT(show()));
    connect(actionAbout, SIGNAL(activated()), this, SLOT(about()));
    connect(actionExit, SIGNAL(activated()), qApp, SLOT(quit()));
}

void TrayIcon::showError(QString title, QString message)
{
    showMessage(title, message, Critical);
}

void TrayIcon::on_activated(QSystemTrayIcon::ActivationReason activationReason)
{
    if (activationReason == DoubleClick) checkQuota();
}

void TrayIcon::refreshQuota()
{
    QSettings settings;
    QString quota;
    QString lastMonth = "Stats/";
    lastMonth += QDate::currentDate().toString("yyyyMM");
    if (settings.contains(lastMonth)) {
        quota = QString("%L1").arg(settings.value(lastMonth).toList()[0].toDouble()/1073741824, 0, 'f', 2);
        //make it fit into tray icon
        if (quota.size() == 5)
            quota = quota.left(4);
        else if (quota.size() > 5)
            quota = QString("%1").arg(settings.value(lastMonth).toList()[0].toDouble()/1073741824, 0, 'f', 0);
    } else
        quota = QString("?");
    quota += QString("\nGB");
    QPixmap pixmap(32, 32);
    pixmap.fill(QColor(settings.value("TrayIcon/backgroundColor", "red").toString()));
    QPainter painter(&pixmap);
    painter.setPen(QColor(settings.value("TrayIcon/textColor", "white").toString()));
    painter.setFont(QFont("", settings.value("TrayIcon/fontSize", 8).toInt(), QFont::Bold));
    painter.drawText(QRect(0,0,32,32), Qt::AlignCenter, quota);
    painter.end();
    setIcon(QIcon(pixmap));
    if (settings.contains(lastMonth)) {
        setToolTip(tr("Used Quota: %L1 GB\nLatest Update: %2").arg(
            settings.value(lastMonth).toList()[0].toDouble()/1073741824).arg(
            settings.value("LastReport/date").toDateTime().toString("d MMMM dddd hh.mm")));
    } else {
        setToolTip(tr("Double click to check quota."));
    }
}

void TrayIcon::checkQuota()
{
    captchaWindow.show();
    captchaWindow.captcha->clear();
    captchaWindow.lineEdit->clear();
    captchaWindow.captcha->setText(tr("Loading, plase wait..."));
    quota.getCaptcha();
}

QList<QVariant> getValues(QStringList values)
{
    QStringList months;
    months << "Ocak" << QString::fromUtf8("Şubat") << "Mart" << "Nisan"
           << QString::fromUtf8("Mayıs") << "Haziran" << "Temmuz"
           << QString::fromUtf8("Ağustos") << "Eyl\xfcl" << "Ekim"
           << QString::fromUtf8("Kasım") << QString::fromUtf8("Aralık");
    QDate date(values[0].toInt(), months.indexOf(values[1])+1, 1);
    double upload = values[2].split('(')[0].remove('.').toDouble();
    double download = values[4].split('(')[0].remove('.').toDouble();
    QList<QVariant> list;
    list << QVariant(date) << QVariant(download) << QVariant(upload);
    return list;
}

void TrayIcon::continueCheckQuota()
{
    QSettings settings;
    if (captchaWindow.lineEdit->text().isEmpty()) {
        captchaWindow.show();
    } else {
        QString username = settings.value("username").toString();
        if (username.isEmpty())
            username = QInputDialog::getText(0, tr("Enter Username"), tr("Enter your TTnet username:"));
        username.remove("@ttnet"); // some users try to put this at the end, resulting username error
        /* following two line is for those who didn't write their username in config,
         * we need username because this application is intended for only one person's use */
        settings.setValue("username", QVariant(username));
        configWindow->username->setText(username);

        QString password = settings.value("password").toString();
        /* we don't have to save the password */
        if (settings.value("savePassword").toInt() == Qt::Unchecked)
            password = QInputDialog::getText(0, tr("Enter Password"), tr("Enter your TTnet password:"), QLineEdit::Password);
        quota.login(captchaWindow.lineEdit->text().toLower(), username, password);
    }
}

void TrayIcon::finishCheckQuota(QString content)
{
    QSettings settings;
    QList< QList <QVariant> > values;
    qDebug() << content;
    values << getValues(content.split(QRegExp("\\s+")).mid(1,6));
    values << getValues(content.split(QRegExp("\\s+")).mid(7,6));
    values << getValues(content.split(QRegExp("\\s+")).mid(13,6));
    qDebug() << "Date:" << content.right(19);
    settings.beginGroup("Stats");
    settings.setValue(values[0][0].toDate().toString("yyyyMM"), values[0].mid(1,2));
    settings.setValue(values[1][0].toDate().toString("yyyyMM"), values[1].mid(1,2));
    settings.setValue(values[2][0].toDate().toString("yyyyMM"), values[2].mid(1,2));
    settings.endGroup();
    /* 06.10.2008 11:33:26 or 06-10-2008 11:33:26 */
    QString dateMask;
    if (content.right(19).contains("."))
        dateMask = "dd.MM.yyyy HH:mm:ss";
    else
        dateMask = "dd-MM-yyyy HH:mm:ss";
    settings.setValue("LastReport/date", QDateTime::fromString(content.right(19), dateMask));
    refreshQuota();
    showMessage(tr("Quota Information"), tr("%L1 bytes\n(%L2 GB)\nLast Update:\n%3").arg(
                values[2][1].toDouble(), 0, 'f', 0).arg(values[2][1].toDouble()/1073741824).arg(
                settings.value("LastReport/date").toDateTime().toString("d MMMM dddd hh.mm")));
    statsWindow.updateStats();
}

void TrayIcon::about()
{
    QMessageBox::about(0, tr("About Kotaci"), tr(
        "<p><b>Kotaci %1</b> - ttnet ADSL quota displayer<br />Copyright (c) 2007-2009, Ugur Cetin - jnmbk at users.sourceforge.net<br />"
        "This software is licensed under the terms of GPL-2.<br /><a href=\"http://kotaci.googlecode.com\">"
        "http://kotaci.googlecode.com</a></p>"
        "<p>This program uses <a href=\"http://www.kde-look.org/content/show.php/show.php?content=38757\">"
        "Tulliana 2.0</a> icon theme.<br />"
        "Kotaci nor its authors are in any way affiliated or endorsed by Turk Telekom.</p>"
        ).arg(KOTACI_VERSION));
}
