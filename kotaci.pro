TEMPLATE = app
TARGET = kotaci
VERSION = "0.2_rc1"
DEFINES += \
#    KOTACI_VERSION=\\\"$$VERSION\\\"
    KOTACI_VERSION=\\\"$$VERSION\\\" \
    QT_NO_DEBUG_OUTPUT

# Input
FORMS += \
    ui/captchawindow.ui \
    ui/configwindow.ui \
    ui/statswindow.ui
HEADERS += \
    src/captchawindow.h \
    src/configwindow.h \
    src/quota.h \
    src/statswindow.h \
    src/trayicon.h
RESOURCES += \
    data/kotaci.qrc
SOURCES += \
    src/captchawindow.cpp \
    src/configwindow.cpp \
    src/main.cpp \
    src/quota.cpp \
    src/statswindow.cpp \
    src/trayicon.cpp
TRANSLATIONS += \
    data/qt4sozluk_tr_TR.ts

DESTDIR = bin
OBJECTS_DIR = build
MOC_DIR = build
UI_DIR = build
RCC_DIR = build

QT += \
    network
