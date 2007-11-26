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

#ifndef TRAYICON_H
#define TRAYICON_H

#include <QSystemTrayIcon>
#include "captchawindow.h"
#include "configwindow.h"
#include "quota.h"
#include "statswindow.h"

class TrayIcon : public QSystemTrayIcon
{
    Q_OBJECT

    public:
        TrayIcon(QWidget *parent = 0);
        CaptchaWindow captchaWindow;
        ConfigWindow configWindow;
        Quota quota;
        StatsWindow statsWindow;

    private slots:
        void on_activated(QSystemTrayIcon::ActivationReason);
        void checkQuota();
        void refreshQuota();
        void continueCheckQuota();
};

#endif
