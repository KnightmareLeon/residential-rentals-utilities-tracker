import sys

from PyQt6.QtWidgets import QApplication
from src.views.mainWindow import MainWindow

if __name__ == "__main__":
	app = QApplication(sys.argv)
	window = MainWindow()
	window.setWindowTitle("UtiliTrack")
	window.show()
	sys.exit(app.exec())