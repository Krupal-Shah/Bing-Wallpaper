from PySide6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QPushButton, QSizePolicy, QMenu, QCheckBox, QMessageBox, QApplication, QSystemTrayIcon
from PySide6.QtGui import QIcon, QPixmap, QImage, QFont, QAction, QColor
from PySide6.QtCore import Qt, QRect, QSize, Slot
import subprocess

# Assume BingImage and BingCollection classes are in the extract module
from extract import BingCollection, BingImage, setWallpaper

class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Setup Window
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowTitle('Wallpaper')
        self.setWindowIcon(QIcon('icons/icon.png'))
        self.setFixedSize(350, 200)
        
        # Setup TrayIcon
        self.trayIcon = QSystemTrayIcon()
        self.trayIcon.setIcon(QIcon('icons/icon.png'))
        self.trayIcon.setToolTip('Wallpaper')
        self.trayIcon.setVisible(True)

        self.menu = QMenu()
        self.quit_action = QAction("Quit", self)
        self.quit_action.triggered.connect(self.quitApplication)
        self.menu.addAction(self.quit_action)
        self.trayIcon.setContextMenu(self.menu)
        self.trayIcon.activated.connect(self.on_tray_icon_activated)
        self.trayIcon.show()

        # Initialize variables
        self.image_width = 100
        self.image_height = 100
        self.icon_width = 20
        self.icon_height = 20
        self.curr_picture = 0
        self.is_dark_theme = None

        # Header
        self.headerLayout =QHBoxLayout()
        self.iconLabel = QLabel(self)
        self.iconLabel.setFixedSize(self.icon_width, self.icon_height)
        icon = QImage()
        icon.load('icons/icon.png')
        self.iconLabel.setPixmap(QPixmap.fromImage(icon).scaled(self.icon_width, self.icon_height, Qt.KeepAspectRatioByExpanding))
        self.iconLabel.show()

        self.minimizeButton = QPushButton()
        self.minimizeButton.setIconSize(QSize(self.icon_width, self.icon_height))
        self.minimizeButton.clicked.connect(self.minimizeApplication)

        self.closeButton = QPushButton()
        self.closeButton.setIconSize(QSize(self.icon_width, self.icon_height))
        self.closeButton.clicked.connect(self.quitApplication)

        # self.settingsButton = QPushButton()
        # self.settingsButton.setIcon(QIcon('icons/settings_dark.png'))
        # self.settingsButton.setIconSize(QSize(self.icon_width, self.icon_height))
        # self.menu = QMenu()
        # self.menu.addAction(QIcon("icons/theme_dark.png"), "Theme")
        # ----------------------------
        # self.themeAction = QAction(QIcon("icons/theme_dark.png"), "Theme (Dark)", self.menu)
        # self.themeAction.triggered.connect(self.toggleTheme)
        # self.menu.addAction(self.themeAction)
        # ----------------------------
        # self.menu.addSeparator()
        # self.menu.addAction("Quit")
        # self.settingsButton.setMenu(self.menu)

        # self.settingsButton.clicked.connect(self.showSettings)

        self.headerTitle = QLabel()
        self.headerTitle.setText(" Wallpaper")
        self.headerTitle.setStyleSheet("font-family: Verdana; text-transform: capitalize; font-weight: bold; font-size: 14px")
        self.headerLayout.addWidget(self.iconLabel)
        self.headerLayout.addWidget(self.headerTitle)
        self.headerLayout.addStretch()
        self.headerLayout.addWidget(self.minimizeButton)
        self.headerLayout.addWidget(self.closeButton)

        # Content
        self.title = QLabel(self)
        self.title.setWordWrap(True)
        self.title.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.title.setStyleSheet("font-family: Verdana; text-transform: capitalize; font-size: 18px; font-weight: bold;")

        self.description = QLabel(self)
        self.description.setWordWrap(True)
        self.description.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.description.setStyleSheet("font-family: Verdana; font-size: 16px;")

        self.textlayout = QVBoxLayout()
        self.textlayout.addWidget(self.title)
        self.textlayout.addWidget(self.description)
        # self.textlayout.setAlignment(Qt.AlignTop)
        self.textlayout.setContentsMargins(12, 7, 0, 0)
        self.textlayout.addStretch()

        self.image_label = QLabel(self)
        self.image_label.setFixedSize(self.image_width, self.image_height)
        # self.image_label.setStyleSheet("border-radius: 10px;")

        self.contentlayout = QHBoxLayout()
        self.contentlayout.addWidget(self.image_label)
        self.contentlayout.addLayout(self.textlayout)
        self.contentlayout.setStretch(0, 1)  # 1/3 for image
        self.contentlayout.setStretch(1, 4)  # 2/3 for text

        # Footer
        self.footerLayout = QHBoxLayout()
        self.back = QPushButton()
        self.back.clicked.connect(self.backButtonClicked)
        self.back.setText("Back")
        self.back.setFont(QFont("Verdana", 10))

        self.next = QPushButton()
        self.next.clicked.connect(self.nextButtonClicked)
        self.next.setText("Next")
        self.next.setFont(QFont("Verdana", 10))

        self.footerLayout.addWidget(self.back)
        self.footerLayout.addStretch()
        self.footerLayout.addWidget(self.next)
        self.checkButton()

        # Container
        self.mainlayout = QVBoxLayout()
        self.mainlayout.addLayout(self.headerLayout)
        self.mainlayout.addLayout(self.contentlayout)
        self.mainlayout.addLayout(self.footerLayout)
        self.mainlayout.setStretch(0, 1)  # 1/4 for content
        self.mainlayout.setStretch(1, 2)
        self.mainlayout.setStretch(2, 1)  # 1/4 for footer

        # Main Layout
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.mainlayout)
        self.setCentralWidget(self.central_widget)
        
        # Check theme
        self.checkTheme()
        self.setTheme()

        # Initialize the BingCollection object
        self.collection = BingCollection()
        self.load_image()

    @Slot(QSystemTrayIcon.ActivationReason)
    def on_tray_icon_activated(self, reason):
        """Handle the tray icon clicks and prevent window from opening."""
        if reason == QSystemTrayIcon.Trigger:  # Left-click
            print("Tray icon clicked, but window won't open.")
            # Prevent window from opening
            return


    def load_image(self, index=0):
        # Fetch the Bing data
        self.collection.request_data()  # Assume this method fetches the Bing image data
        self.collection.extract_images()  # Assume this method extracts the image details

        if self.collection.images:
            reply = self.collection.download_image(index)
            if reply:
                img_file_path = f'images/{index}.jpg'
                setWallpaper(img_file_path)
                img = QImage()
                img.load(img_file_path)
                self.image_label.setPixmap(QPixmap.fromImage(img).scaled(self.image_width, self.image_height, Qt.KeepAspectRatioByExpanding))
                self.image_label.show()
                self.title.setText(self.collection.images[index].title.upper())
                self.description.setText(self.collection.images[index].description)
            else:
                print("Error downloading the image")

        return

    def checkButton(self):
        if self.curr_picture >= 7:
            self.back.setEnabled(False)
        else:
            self.back.setEnabled(True)

        if self.curr_picture <= 0:
            self.next.setEnabled(False)
        else:
            self.next.setEnabled(True)

        return

    def backButtonClicked(self):
        self.curr_picture += 1
        self.load_image(self.curr_picture)
        self.checkButton()
        return

    def nextButtonClicked(self):
        self.curr_picture -= 1
        self.load_image(self.curr_picture)
        self.checkButton()
        return
    
    def quitApplication(self):
        reply = QMessageBox.question(self, 'Confirmation',
                                     "Are you sure you want to quit?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            # Force quit the application
            QApplication.quit()
    
    def minimizeApplication(self):
        self.close()
        return

    def checkTheme(self):
        # output = subprocess.run([
        #     "gsettings", "get", "org.gnome.desktop.interface", "gtk-theme"
        # ], stdout=subprocess.PIPE)
        # theme = output.stdout.decode().rstrip()
        # if "dark" in theme:
        #     self.is_dark_theme = True
        # else:
        #     self.is_dark_theme = False

        palette = self.palette()
        bgcolor = palette.color(self.backgroundRole())
        print(bgcolor.name())
        if bgcolor.name() > "#656565":
            self.is_dark_theme = False
        else:
            self.is_dark_theme = True
        return
    
    def setTheme(self):
        """Set light or dark theme."""
        if self.is_dark_theme:
            # Switch to light theme
            # self.setLightTheme()
            # self.themeAction.setText("Theme (Light)")
            # self.themeAction.setIcon(QIcon("icons/theme_light.png"))
            # self.quit_action.setIcon(QIcon('icons/close_dark.png'))
            self.minimizeButton.setIcon(QIcon('icons/minimize_dark.png'))
            self.closeButton.setIcon(QIcon('icons/close_dark.png'))
        else:
            # Switch to dark theme
            # self.setDarkTheme()
            # self.themeAction.setText("Theme (Dark)")
            # self.themeAction.setIcon(QIcon("icons/theme_dark.png"))
            # self.quit_action.setIcon(QIcon('icons/close_light.png'))
            self.minimizeButton.setIcon(QIcon('icons/minimize_light.png'))
            self.closeButton.setIcon(QIcon('icons/close_light.png'))

        # Toggle the theme state
        # self.is_dark_theme = not self.is_dark_theme

    # def setLightTheme(self):
    #     """Apply the light theme to the application."""

    #     self.settingsButton.setIcon(QIcon('icons/settings_light.png'))

    # def setDarkTheme(self):
    #     """Apply the dark theme to the application."""

    #     self.settingsButton.setIcon(QIcon('icons/settings_dark.png'))




