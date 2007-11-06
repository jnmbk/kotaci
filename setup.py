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

import os, shutil, sys
from distutils.core import setup
from distutils.command.build import build
from distutils.command.clean import clean

import kotaci

try:
    import PyQt4
except:
    print "\033[31mError: You have to install PyQt4 on your system\033[0m"
    sys.exit()

try:
    import httplib2
except:
    print "\033[31mWarning: You have to install httplib2 module on your system\033[0m"

def compileui(path, uiFile):
    compiled = os.system("pyuic4 %s%s.ui -o kotaci/%s.py" % (path, uiFile, uiFile))
    if compiled == 0:
        print "Compiled %s%s.ui -> kotaci/%s.py" % (path, uiFile, uiFile)
    else:
        print "Failed compiling %s%s.ui" % (path, uiFile)
        sys.exit()

def compileqrc(path, qrcFile):
    compiled = os.system("pyrcc4 %s%s.qrc -o kotaci/%s_rc.py" % (path, qrcFile, qrcFile))
    if compiled == 0:
        print "Compiled %s%s.qrc -> kotaci/%s_rc.py" % (path, qrcFile, qrcFile)
    else:
        print "Failed compiling %s%s.qrc" % (path, qrcFile)
        sys.exit()

class myClean(clean):
    def run(self):
        clean.run(self)
        try:
            os.remove("MANIFEST")
            print "removed MANIFEST"
        except:pass
        try:
            shutil.rmtree("build")
            print "removed build"
        except:pass

class myBuild(build):
    def run(self):
        build.run(self)
        for ui in (("ui/", "configwindow"), ("ui/", "captchawindow")):
            compileui(ui[0], ui[1])
        for qrc in (("data/", "kotaci"),):
            compileqrc(qrc[0], qrc[1])

datas = [('share/applications', ['data/kotaci.desktop'])]

setup(name = "kotaci",
      version = kotaci.__version__,
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
