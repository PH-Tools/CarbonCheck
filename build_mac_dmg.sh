#!/bin/sh
# From root dir '.../00_PH_Tools/CarbonCheck/' run './build_mac_dmg.sh' in terminal
# From https://www.pythonguis.com/tutorials/packaging-pyqt6-applications-pyinstaller-macos-dmg/
# Create a folder (named dmg) to prepare our DMG in (if it doesn't already exist).
mkdir -p dist/dmg
# Empty the dmg folder.
rm -r dist/dmg/*
# Copy the app bundle to the dmg folder.
cp -r "dist/CarbonCheck.app" dist/dmg
# If the DMG already exists, delete it.
test -f "dist/CarbonCheck.dmg" && rm "dist/CarbonCheck.dmg"
create-dmg \
 --volname "CarbonCheck" \
 --volicon "CC_GUI/resources/logo_CarbonCheck_512x512.icns" \
 --window-pos 200 120 \
 --window-size 600 300 \
 --icon-size 100 \
 --icon "CarbonCheck.app" 175 120 \
 --hide-extension "CarbonCheck.app" \
 --app-drop-link 425 120 \
 "dist/CarbonCheck.dmg" \
 "dist/dmg/"