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

#include "trayicon.h"

TrayIcon::TrayIcon(QWidget *parent)
    : QSystemTrayIcon(parent)
{
    refreshQuota();
}

void TrayIcon::on_activated(QSystemTrayIcon::ActivationReason)
{

}

void TrayIcon::refreshQuota()
{

}

void TrayIcon::checkQuota()
{

}

void TrayIcon::continueCheckQuota()
{

}
