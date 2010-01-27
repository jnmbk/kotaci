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

#include <QPixmap>
#include "captchawindow.h"

CaptchaWindow::CaptchaWindow(QWidget *parent)
    : QDialog(parent)
{
    setupUi(this);
}

void CaptchaWindow::displayCaptcha(QByteArray captchaContent)
{
    captcha->clear();
    QPixmap pixmap;
    pixmap.loadFromData(captchaContent);
    captcha->setPixmap(pixmap);
}
