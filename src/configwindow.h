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

#ifndef CONFIGWONDOW_H
#define CONFIGWONDOW_H

#include <QDialog>

#include "ui_configwindow.h"

class ConfigWindow : public QDialog, private Ui::ConfigWindow
{
    Q_OBJECT

    public:
        ConfigWindow(QWidget *parent = 0);
};

#endif
