#!/bin/bash

# Variables
DES="/usr"
STARTUP_FILE="$HOME/.config/autostart/bing_wallpaper.desktop"

## Remove Installed Files
remove_files() {
    echo "Uninstalling Bing Wallpaper for Linux..."

    # Remove the installed binary, icons, and .desktop entry
    if [[ -d "$DES/share/bingwallpaper" ]]; then
        sudo rm -rf "$DES/share/bingwallpaper"
        echo "Removed $DES/share/bingwallpaper"
    else
        echo "$DES/share/bingwallpaper not found."
    fi

    if [[ -f "$DES/bin/bingwallpaper" ]]; then
        sudo rm "$DES/bin/bingwallpaper"
        echo "Removed $DES/bin/bingwallpaper"
    else
        echo "$DES/bin/bingwallpaper not found."
    fi

    if [[ -f "$DES/share/applications/bingwallpaper.desktop" ]]; then
        sudo rm "$DES/share/applications/bingwallpaper.desktop"
        echo "Removed $DES/share/applications/bingwallpaper.desktop"
    else
        echo "$DES/share/applications/bingwallpaper.desktop not found."
    fi
}

## Remove from Startup
remove_startup() {
    if [[ -f "$STARTUP_FILE" ]]; then
        rm "$STARTUP_FILE"
        echo "Removed startup entry: $STARTUP_FILE"
    else
        echo "No startup entry found."
    fi
}

## Main Uninstallation Function
uninstall_bingwallpaper() {
    remove_files

    # Check if the user passed the --remove-startup argument
    if [[ "$1" == "--remove-startup" ]]; then
        remove_startup
    fi

    echo "Uninstallation complete."
}

## Run the uninstallation
uninstall_bingwallpaper "$1"
