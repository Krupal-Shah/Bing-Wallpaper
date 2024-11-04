import os
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

# Assume BingImage and BingCollection classes are in the extract module
from extract import BingCollection, BingImage, set_wallpaper, FavoriteCollection

ICONPATH = "//usr/share/bingwallpaper/icons/"
PATH = os.path.join(os.getenv("HOME"), ".cache", "bingwallpaper")

class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Setup Window
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
        self.setWindowTitle("Bing Wallpaper")
        self.setWindowIcon(QIcon(f"{ICONPATH}icon.png"))
        self.setFixedSize(350, 220)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Setup TrayIcon
        self.trayIcon = QSystemTrayIcon()
        self.trayIcon.setIcon(QIcon(f"{ICONPATH}icon.png"))
        self.trayIcon.setToolTip("Bing Wallpaper")
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
        self.current_image = None
        self.collectionButtonState = False

        # Header
        self.headerLayout = QHBoxLayout()
        self.iconLabel = QLabel(self)
        self.iconLabel.setFixedSize(self.icon_width, self.icon_height)
        icon = QImage()
        icon.load(f"{ICONPATH}icon.png")
        self.iconLabel.setPixmap(
            QPixmap.fromImage(icon).scaled(
                self.icon_width, self.icon_height, Qt.KeepAspectRatioByExpanding
            )
        )
        self.iconLabel.show()

        self.collectionButton = QPushButton()
        self.collectionButton.setIconSize(QSize(self.icon_width, self.icon_height))
        self.collectionButton.clicked.connect(self.favoriteCollection)

        self.refreshButton = QPushButton()
        self.refreshButton.setIconSize(QSize(self.icon_width, self.icon_height))
        self.refreshButton.clicked.connect(self.refreshApplication)

        self.closeButton = QPushButton()
        self.closeButton.setIconSize(QSize(self.icon_width, self.icon_height))
        self.closeButton.clicked.connect(self.minimizeApplication)

        self.headerTitle = QLabel()
        self.headerTitle.setText("Wallpaper")
        self.headerTitle.setStyleSheet(
            "font-family: Verdana; text-transform: capitalize; font-weight: bold; font-size: 14px"
        )
        self.headerLayout.addWidget(self.iconLabel)
        self.headerLayout.addWidget(self.headerTitle)
        self.headerLayout.addStretch()
        self.headerLayout.addWidget(self.collectionButton)
        self.headerLayout.addWidget(self.refreshButton)
        self.headerLayout.addWidget(self.closeButton)

        # Content
        self.title = QLabel(self)
        self.title.setWordWrap(True)
        self.title.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.title.setStyleSheet(
            "font-family: Verdana; text-transform: capitalize; font-size: 18px; font-weight: bold;"
        )

        self.description = QLabel(self)
        self.description.setWordWrap(True)
        self.description.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.description.setStyleSheet("font-family: Verdana; font-size: 16px;")

        self.textlayout = QVBoxLayout()
        self.textlayout.addWidget(self.title)
        self.textlayout.addWidget(self.description)
        self.textlayout.setContentsMargins(12, 10, 0, 0)
        self.textlayout.addStretch()

        self.image_label = QLabel(self)
        self.image_label.setFixedSize(self.image_width, self.image_height)
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

        self.favorite = QPushButton()
        self.favorite.clicked.connect(self.toggleFavorite)

        self.next = QPushButton()
        self.next.clicked.connect(self.nextButtonClicked)
        self.next.setText("Next")
        self.next.setFont(QFont("Verdana", 10))

        self.footerLayout.addWidget(self.back)
        self.footerLayout.addStretch()
        self.footerLayout.addWidget(self.favorite)
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

        # Set icons initially
        palette = self.palette()
        self.bgcolor = palette.color(self.backgroundRole())
        self.setButtonIcons()

        # Initialize the BingCollection object
        self.collection = BingCollection()
        self.load_image()

        self.favorites = FavoriteCollection()


        self.timer = QTimer(self)
        self.timer.timeout.connect(self.load_next_image if self.collectionButtonState else self.refreshApplication)
        self.timer.start(43200000)

    def setButtonIcons(self):
        """Set button icons based on the current background color."""
        try:
            if self.bgcolor.name() > "#656565":
                self.refreshButton.setIcon(QIcon(f"{ICONPATH}refresh_light.png"))
                self.closeButton.setIcon(QIcon(f"{ICONPATH}close_light.png"))
                self.collectionButton.setIcon(QIcon(f"{ICONPATH}collection_light.png"))

            else:
                self.refreshButton.setIcon(QIcon(f"{ICONPATH}refresh_dark.png"))
                self.closeButton.setIcon(QIcon(f"{ICONPATH}close_dark.png"))
                self.collectionButton.setIcon(QIcon(f"{ICONPATH}collection_dark.png"))

        except Exception as e:
            print("Error setting icons:", e)

    def paintEvent(self, event):
        # Initialize QPainter
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Set brush to fill background with the current background color
        palette = self.palette()
        bgcolor = palette.color(self.backgroundRole())
        brush = QBrush(QColor(bgcolor))  # Current background color
        painter.setBrush(brush)

        # Remove pen to avoid white border line (Qt.NoPen)
        painter.setPen(Qt.NoPen)

        # Draw the rounded rectangle
        painter.drawRoundedRect(self.rect(), 15.0, 15.0)

        # Adjust button icons based on background color
        self.bgcolor = palette.color(self.backgroundRole())
        self.setButtonIcons()

    def event(self, event):
        """Listen for palette change events to trigger repaint."""
        if event.type() == QEvent.PaletteChange:
            self.update()  # Trigger paintEvent to update the icons
        return super().event(event)

    @Slot(QSystemTrayIcon.ActivationReason)
    def on_tray_icon_activated(self):
        """Handle the tray icon clicks and prevent window from opening."""
        self.show()

    def load_image(self, index=0):
        if self.collectionButtonState:
            self.favorites.extract_images()
            if self.favorites.images:
                self.current_image = self.favorites.images[index]
                filename = os.path.join(
                    "favorites",
                    f"{self.current_image.startdate}-{self.current_image.enddate}.jpg",
                )
                reply = set_wallpaper(filename)
                print(reply)
                img = QImage()
                img.load(f"{PATH}/{filename}")
                self.image_label.setPixmap(
                    QPixmap.fromImage(img).scaled(
                        self.image_width,
                        self.image_height,
                        Qt.KeepAspectRatioByExpanding,
                    )
                )
                self.image_label.show()
                self.title.setText(self.favorites.images[index].title.upper())
                self.description.setText(self.favorites.images[index].description)
            else:
                self.image_label.hide()
                self.title.setText("")
                self.description.setText("No pictures saved in favorites")
        else:
            self.collection.request_data()  # Assume this method fetches the Bing image data
            self.collection.extract_images()  # Assume this method extracts the image details

            if self.collection.images:
                reply = self.collection.download_image(index)
                if reply:
                    self.current_image = self.collection.images[index]
                    filename = f"{self.current_image.startdate}-{self.current_image.enddate}.jpg"
                    reply = set_wallpaper(filename)
                    print(reply)
                    img = QImage()
                    img.load(f"{PATH}/{filename}")
                    self.image_label.setPixmap(
                        QPixmap.fromImage(img).scaled(
                            self.image_width,
                            self.image_height,
                            Qt.KeepAspectRatioByExpanding,
                        )
                    )
                    self.image_label.show()
                    self.title.setText(self.collection.images[index].title.upper())
                    self.description.setText(self.collection.images[index].description)
                else:
                    print("Error downloading the image")
        
        self.setFavoriteIcon()
        return

    def checkButton(self):
        if self.collectionButtonState:
            file_count = len(os.listdir(os.path.join(PATH, "favorites")))
            print("Favorites", file_count)
        else:
            file_count = 8

        self.back.setEnabled(self.curr_picture < file_count - 1)
        self.next.setEnabled(self.curr_picture > 0)

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
        reply = QMessageBox.question(
            self,
            "Confirmation",
            "Are you sure you want to quit?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            # Force quit the application
            QApplication.quit()

    def minimizeApplication(self):
        self.close()
        return

    def refreshApplication(self):
        self.collection = BingCollection()
        self.load_image()

    def favoriteCollection(self):
        self.collectionButtonState = not self.collectionButtonState
        if not self.collectionButtonState:
            self.curr_picture = 0
        self.load_image()
        self.checkButton()
            
    def setFavoriteIcon(self):
        if self.current_image and hasattr(self.current_image, 'favorite'):
            icon_path = f"{ICONPATH}favorite_"
            if self.current_image.favorite:
                icon_path += "light-fill.png" if self.bgcolor.name() > "#656565" else "dark-fill.png"
            else:
                icon_path += "light.png" if self.bgcolor.name() > "#656565" else "dark.png"
            
            self.favorite.setIcon(QIcon(icon_path))

    def toggleFavorite(self):
        if self.current_image:
            self.current_image.favorite = not self.current_image.favorite
            if self.current_image.favorite:
                self.favorites.add_favorite(self.current_image)
            else:
                self.favorites.remove_favorite(self.current_image)
        
        self.setFavoriteIcon()


    def load_next_image(self):
        self.curr_picture = (self.curr_picture + 1) % self.favorites.count()
        self.load_image(self.curr_picture)
        return
