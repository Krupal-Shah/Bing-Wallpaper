[app]
title = Bing Wallpaper for Linux
project_dir = .
input_file = bingwallpaper.py
project_file = bingwallpaper.pyproject
exec_directory = releases/bing_wallpaper_1.0/usr/bin
icon = /home/krupal/Documents/bingwallpaper/Bing-Wallpaper/icons/icon.png

[python]
python_path = /home/krupal/Documents/bingwallpaper/Bing-Wallpaper/venv/bin/python3
packages = Nuitka==2.3.2
android_packages = 

[qt]
qml_files = 
excluded_qml_plugins = 
modules = Gui,Core,Widgets,DBus
plugins = styles,platforms/darwin,iconengines,egldeviceintegrations,accessiblebridge,imageformats,platformthemes,platforminputcontexts,generic,xcbglintegrations,platforms

[android]
wheel_pyside = 
wheel_shiboken = 
plugins = 

[nuitka]
macos.permissions = 
extra_args = --quiet --noinclude-qt-translations

[buildozer]
mode = release
recipe_dir = 
jars_dir = 
ndk_path = 
sdk_path = 
local_libs = 
arch = 

