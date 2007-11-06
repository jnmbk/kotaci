# -*- coding: utf-8 -*-
#
# Copyright (C) 2007, Uğur Çetin <ugur.jnmbk at gmail.com>
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

from distutils.core import setup
from distutils.command.build import build
from distutils.command.clean import clean

try:
    import PyQt4
except:
    print "\033[31mWarning: You have to install PyQt4 on your system\033[0m"

try:
    import httplib2
except:
    print "\033[31mWarning: You have to install httplib2 module on your system\033[0m"

class myClean(clean):
    def run(self):
        clean.run(self)

class myBuild(build):
    def run(self):
        build.run(self)
        os.system("pyrcc4 kotaci/kotaci.qrc -o kotaci/kotaci_rc.py")
        os.system("pyuic4 kotaci/configwindow.ui -o kotaci/configwindow.py")
        os.system("pyuic4 kotaci/captchawindow.ui -o kotaci/captchawindow.py")

datas = [('share/applications', ['data/kotaci.desktop'])]

setup(name = "kotaci",
      version = "0.1",
      description = "ADSL quota checking tool for Turkey.",
      author = "Uğur Çetin",
      author_email = "ugur.jnmbk@gmail.com",
      license = "GNU General Public License, Version 2",
      url = "http://code.google.com/p/kotaci/",
      packages = ["kotaci"],
      data_files = datas,
      scripts = ['data/kotaci'],
      cmdclass = {"build" : myBuild,
                  "clean" : myClean}
      )
