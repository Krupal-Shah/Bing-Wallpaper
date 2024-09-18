from PySide6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QPushButton, QSizePolicy
from PySide6.QtGui import QIcon, QPixmap, QImage, QFont
from PySide6.QtCore import Qt, QRect, QSize
import subprocess

# Assume BingImage and BingCollection classes are in the extract module
from extract import BingCollection, BingImage, set_wallpaper

class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowTitle('Wallpaper')
        self.setWindowIcon(QIcon(':/icon.ico'))
        self.setFixedSize(350, 200)

        self.image_width = 100
        self.image_height = 100
        self.icon_width = 20
        self.icon_height = 20
        self.currPicture = 0

        # Header
        self.headerLayout =QHBoxLayout()
        self.icon_label = QLabel(self)
        self.icon_label.setFixedSize(self.icon_width, self.icon_height)
        icon = QImage()
        icon.load('icons/icon.png')
        self.icon_label.setPixmap(QPixmap.fromImage(icon).scaled(self.icon_width, self.icon_height, Qt.KeepAspectRatioByExpanding))
        self.icon_label.show()

        self.minimizeButton = QPushButton()
        self.minimizeButton.setIcon(QIcon('icons/minimize_dark'))
        self.minimizeButton.setIconSize(QSize(self.icon_width, self.icon_height))
        self.minimizeButton.clicked.connect(self.showMinimized)

        self.settingsButton = QPushButton()
        self.settingsButton.setIcon(QIcon('icons/settings_dark'))
        self.settingsButton.setIconSize(QSize(self.icon_width, self.icon_height))
        self.settingsButton.clicked.connect(self.showSettings)

        self.headerTitle = QLabel()
        self.headerTitle.setText(" Wallpaper")
        self.headerTitle.setStyleSheet("font-family: Verdana; text-transform: capitalize; color: grey; font-weight: bold; font-size: 14px")
        self.headerLayout.addWidget(self.icon_label)
        self.headerLayout.addWidget(self.headerTitle)
        self.headerLayout.addStretch()
        self.headerLayout.addWidget(self.minimizeButton)
        self.headerLayout.addWidget(self.settingsButton)

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

        self.collection = BingCollection()
        self.load_image()

    def load_image(self, index=0):
        # Fetch the Bing data
        self.collection.request_data()  # Assume this method fetches the Bing image data
        self.collection.extract_images()  # Assume this method extracts the image details

        if self.collection.images:
            reply = self.collection.download_image(index)
            if reply:
                img_file_path = f'images/{index}.jpg'
                set_wallpaper(img_file_path)
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
        if self.currPicture >= 7:
            self.back.setEnabled(False)
        else:
            self.back.setEnabled(True)

        if self.currPicture <= 0:
            self.next.setEnabled(False)
        else:
            self.next.setEnabled(True)

        return

    def backButtonClicked(self):
        self.currPicture += 1
        self.load_image(self.currPicture)
        self.checkButton()
        return

    def nextButtonClicked(self):
        self.currPicture -= 1
        self.load_image(self.currPicture)
        self.checkButton()
        return
    
    def showSettings(self):
        return
    
    def showMinimized(self):
        return

    def set_wallpaper(self, file_path):
        subprocess.run([
            "gsettings", "set", "org.gnome.desktop.background", "picture-uri", f"file://{file_path}"
        ])
        return




