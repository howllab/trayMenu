#!/bin/bash
# autostart dir
targetDir="$HOME/.config/autostart"
targetFile="$HOME/.config/autostart/trayMenu.desktop"
# git clone dir
srcDir="$HOME/git/trayMenu"
srcFile="$HOME/git/trayMenu/trayMenu.desktop"

if [ ! -f "$targetFile" ]; then
    mkdir -p "$targetDir"
    cp "$srcFile" "$targetDir"
    python "$srcDir"/trayMenu.py &
    echo 'trayMenu install'
fi
