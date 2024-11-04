#!/env/bin/python3
import sys
from PySide6.QtWidgets import QApplication, QMessageBox, QSystemTrayIcon

from window import Window

if __name__ == "__main__":
    app = QApplication([])

    if not QSystemTrayIcon.isSystemTrayAvailable():
        QMessageBox.critical(
            None, "Systray", "I couldn't detect any system tray on this system."
        )
        sys.exit(1)

    QApplication.setQuitOnLastWindowClosed(False)

    window = Window()
    window.hide()
    sys.exit(app.exec())
