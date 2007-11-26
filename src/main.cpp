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

#include <QApplication>
#include <QLocale>
#include <QTranslator>

#include "captchawindow.h"
#include "configwindow.h"
#include "statswindow.h"

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    app.setOrganizationName(QString("kotaci"));
    app.setApplicationName(QString("kotaci"));

    QString locale = QLocale::system().name();
    QTranslator translator;
    translator.load(QString(":/kotaci_") + locale);
    app.installTranslator(&translator);

    return app.exec();
}
