name "Kotaci"
outFile "kotaci-1.1-win32.exe"
installDir $PROGRAMFILES32\kotaci

Page license
Page directory
Page instfiles
UninstPage uninstConfirm
UninstPage instfiles

LicenseData COPYING

SetCompressor lzma

section
    setOutPath $INSTDIR

    # files
    File kotaci.exe
    File *.dll
    File README
    File COPYING
    File AUTHORS
    File /r plugins

    writeUninstaller "$INSTDIR\uninstall.exe"
    CreateDirectory "$SMPROGRAMS\Kotaci"
    createShortCut "$SMPROGRAMS\Kotaci\Kotaci.lnk" "$INSTDIR\kotaci.exe"
    createShortCut "$SMPROGRAMS\Kotaci\Uninstall.lnk" "$INSTDIR\uninstall.exe"
sectionEnd

section "uninstall"
    # delete program files
    RMDir /r $INSTDIR

    # remove the links from the start menu
    Delete "$SMPROGRAMS\Kotaci\Kotaci.lnk"
    Delete "$SMPROGRAMS\Kotaci\Uninstall.lnk"
    RMDir "$SMPROGRAMS\Kotaci"
sectionEnd
