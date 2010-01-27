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

#ifndef CAPTCHAWONDOW_H
#define CAPTCHAWONDOW_H

#include <QDialog>
#include <QByteArray>
#include <QPixmap>

#include "ui_captchawindow.h"

class CaptchaWindow : public QDialog, public Ui::CaptchaWindow
{
    Q_OBJECT

    public:
        CaptchaWindow(QWidget *parent = 0);

    public slots:
        void displayCaptcha(QByteArray captchaContent);
};

#endif
