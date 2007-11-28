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

#include <QDate>
#include <QSettings>
#include "statswindow.h"

StatsWindow::StatsWindow(QWidget *parent)
    : QDialog(parent)
{
    setupUi(this);
    connect(clearButton, SIGNAL(clicked()), this, SLOT(clearStats()));
    updateStats();
}

void StatsWindow::clearStats()
{
    QSettings settings;
    settings.remove("Stats");
    updateStats();
}

void StatsWindow::updateStats()
{
    stats->clear();
    QSettings settings;
    settings.beginGroup("Stats");
    QStringListIterator i(settings.childKeys());
    while (i.hasNext()) {
        QString key(i.next());
        if (QDate::fromString(key, "yyyyMM").isValid()) {
            QStringList list(settings.value(key).toStringList());
            QTreeWidgetItem *item = new QTreeWidgetItem(stats);
            item->setText(0, QDate::fromString(key, "yyyyMM").toString("MMMM yyyy"));
            item->setText(1, tr("%L2 GB").arg(list[0].toDouble()/1073741824, 0, 'f', 3));
            item->setText(2, tr("%L2 GB").arg(list[1].toDouble()/1073741824, 0, 'f', 3));
        }
    }
    settings.endGroup();
}
