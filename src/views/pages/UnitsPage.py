from src.views.pages.BasePageWidget import BasePageWidget
from src.views.components.UnitsTable import UnitsTable

class UnitsPage(BasePageWidget):
	def __init__(self, mainWindow=None):
		self.buttonText = "Add Unit"
		
		super().__init__(UnitsTable, self.buttonText, mainWindow=mainWindow)
	
	def handleAddButton(self):
		print("adding unit!")