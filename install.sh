#!/bin/bash

## Bing Wallpaper

# Path
DIR=$(pwd)
DES="/usr"

## Make dirs
mkdir_dw() {
    echo "Installing Bing Wallpaper for Linux..."
    if [[ -d "$DES"/share/bingwallpaper ]]; then
        # delete old directory
        sudo rm -rf "$DES"/share/bingwallpaper
    fi
    # create new directory
    sudo mkdir -p "$DES"/share/bingwallpaper
}

## Copy files
copy_files() {
    # copy icons, binaries, and desktop file
    sudo cp -r "$DIR"/icons/ "$DES"/share/bingwallpaper/ &&
    sudo cp "$DIR"/usr/bin/bingwallpaper.bin "$DES"/bin/bingwallpaper &&
    sudo cp "$DIR"/usr/share/applications/bing_wallpaper.desktop "$DES"/share/applications/bingwallpaper.desktop
    # make the binary executable
    sudo chmod +x "$DES"/bin/bingwallpaper
    echo -e "Installed Successfully. Execute 'bingwallpaper' to Run."
}

## Add to Startup
add_startup() {
    echo "Adding Bing Wallpaper to startup..."
    mkdir -p "$HOME/.config/autostart"
    
    # Copy the .desktop file to autostart directory
    cp "$DIR/usr/share/applications/bing_wallpaper.desktop" "$HOME/.config/autostart/bingwallpaper.desktop"
    chmod +x ~/.config/autostart/bingwallpaper.desktop
    
    echo "Added to startup successfully!"
}

## Main Installation Function
install_bingwallpaper() {
    mkdir_dw
    copy_files

    # Check if the user passed the --add-startup argument
    if [[ "$1" == "--add-startup" ]]; then
        add_startup
    fi
}

## Run the installation
install_bingwallpaper "$1"
