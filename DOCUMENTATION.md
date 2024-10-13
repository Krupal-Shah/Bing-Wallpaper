## How to make changes to the code
1. Create a python environment as follows:
```
python3 -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
```
2. Make changes to the code.
3. File structure is as follows. If any folder is missing, create the folders for it. Some files will get created during the deployment step.
```
.
├── bingwallpaper.py
├── bingwallpaper.pyproject
├── DOCUMENTATION
├── extract.py
├── icons
│   ├── close_dark.png
│   ├── close_light.png
│   ├── icon.png
|   ├── icon_big.png
│   ├── refresh_dark.png
│   └── refresh_light.png
├── install.sh
├── LICENSE
├── pysidedeploy.spec
├── README.md
├── releases
│   └── bing_wallpaper_1.0
│       ├── DEBIAN
│       │   └── control
│       └── usr
│           ├── bin
│           │   └── bingwallpaper.bin
│           └── share
│               └── applications
│                   └── bing_wallpaper_1.0.desktop
├── requirements.txt
├── uninstall.sh
├── venv
└── window.py
```
4. Run the following code to create an executable of the code
   ```
   pyside6-deploy -c pysidedeploy.spec
   ```
5. Then create another folder separate from the current directory with the following structure
```
.
├── icons
│   ├── close_dark.png
│   ├── close_light.png
│   ├── icon.png
│   ├── refresh_dark.png
│   └── refresh_light.png
├── install.sh
├── uninstall.sh
└── usr
    ├── bin
    │   └── bingwallpaper.bin
    └── share
        └── applications
            └── bing_wallpaper_1.0.desktop
```
6. Then run install.sh to install the executable to the system.
