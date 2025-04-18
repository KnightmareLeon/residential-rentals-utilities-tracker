from src.views.pages.BasePageWidget import BasePageWidget
from src.views.components.UtilitiesTable import UtilitiesTable

class UtilitiesPage(BasePageWidget):
    def __init__(self, mainWindow=None):
        self.buttonText = "Add Utility"
        
        super().__init__(UtilitiesTable, self.buttonText, mainWindow=mainWindow)
    
    def handleAddButton(self):
        print("adding utility!")
