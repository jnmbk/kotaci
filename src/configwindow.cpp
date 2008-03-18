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

#include <QIcon>
#include <QPixmap>
#include <QSettings>
#include <QString>
#include <QStringListIterator>
#include <QVariant>
#include "configwindow.h"

ConfigWindow::ConfigWindow(QWidget *parent, TrayIcon *trayIcon)
    : QDialog(parent)
{
    setupUi(this);
    this->trayIcon = trayIcon;
    connect(this, SIGNAL(accepted()), this, SLOT(saveSettings()));
    connect(this, SIGNAL(rejected()), this, SLOT(loadSettings()));
    QStringListIterator i(QColor::colorNames());
    while(i.hasNext()) {
        QString color = i.next();
        QPixmap pixmap(16, 16);
        pixmap.fill(QColor(color));
        QIcon icon(pixmap);
        textColor->addItem(icon, color);
        backgroundColor->addItem(icon, color);
    }
    loadSettings();
}

void ConfigWindow::loadSettings()
{
    QSettings settings;
    username->setText(settings.value("username").toString());
    password->setText(settings.value("password").toString());
    savePassword->setCheckState(Qt::CheckState(settings.value("savePassword", QVariant(Qt::Checked)).toInt()));
    textColor->setCurrentIndex(textColor->findText(settings.value("TrayIcon/textColor", "white").toString()));
    backgroundColor->setCurrentIndex(textColor->findText(settings.value("TrayIcon/backgroundColor", "red").toString()));
    if (savePassword->checkState() == Qt::Unchecked)
        password->setEnabled(false);
}

void ConfigWindow::saveSettings()
{
    username->setText(username->text().remove("@ttnet"));

    QSettings settings;
    settings.setValue("username", QVariant(username->text()));
    settings.setValue("password", QVariant(password->text()));
    settings.setValue("savePassword", QVariant(savePassword->checkState()));
    settings.setValue("TrayIcon/textColor", QVariant(textColor->currentText()));
    settings.setValue("TrayIcon/backgroundColor", QVariant(backgroundColor->currentText()));

    trayIcon->refreshQuota();
    if (savePassword->checkState() == Qt::Unchecked)
        settings.remove("password");
}
