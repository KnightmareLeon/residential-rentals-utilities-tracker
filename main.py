import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFontDatabase

from src.views.MainWindow import MainWindow

if __name__ == "__main__":    
	app = QApplication(sys.argv)

	fontId = QFontDatabase.addApplicationFont("assets/fonts/Urbanist-VariableFont_wght.ttf")
	if fontId == -1:
		print("Failed to load font.")
	else:
		print("Font loaded successfully!")
		
	window = MainWindow()
	window.setWindowTitle("UtiliTrack")
	window.show()
	sys.exit(app.exec())