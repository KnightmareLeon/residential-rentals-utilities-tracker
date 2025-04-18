from src.views.pages.BasePageWidget import BasePageWidget
from src.views.components.UtilitiesTable import UtilitiesTable
from src.controllers.utilitiesController import UtilitiesController

class UtilitiesPage(BasePageWidget):
    def __init__(self, mainWindow=None):
        self.buttonText = "Add Utility"
        super().__init__(UtilitiesTable, self.buttonText, mainWindow=mainWindow)
    
    def updatePage(self):
        self.table.updateTable()

    def handleAddButton(self):
        response = UtilitiesController.addRecord(None)
        self.table.updateTable()
