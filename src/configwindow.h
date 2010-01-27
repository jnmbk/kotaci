/*
 * kotaci, ADSL quota viewer for Turkey
 * Copyright (C) 2007-2010, Uğur Çetin
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * Please read the COPYING file.
 */

#ifndef CONFIGWONDOW_H
#define CONFIGWONDOW_H

#include <QDialog>

#include "trayicon.h"
#include "ui_configwindow.h"

class TrayIcon;

class ConfigWindow : public QDialog, public Ui::ConfigWindow
{
    Q_OBJECT

    public:
        ConfigWindow(QWidget *parent, TrayIcon *trayIcon);
        TrayIcon *trayIcon;

    private slots:
        void loadSettings();
        void saveSettings();
};

#endif
