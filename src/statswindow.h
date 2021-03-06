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

#ifndef STATSWONDOW_H
#define STATSWONDOW_H

#include <QDialog>

#include "ui_statswindow.h"

class StatsWindow : public QDialog, private Ui::StatsWindow
{
    Q_OBJECT

    public:
        StatsWindow(QWidget *parent = 0);

    public slots:
        void updateStats();
        void clearStats();
};

#endif
