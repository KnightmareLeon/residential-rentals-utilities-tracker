from src.views.widgets.BasePageWidget import BasePageWidget
from src.views.components.UtilitiesTable import UtilitiesTable
from src.views.dialogs.AddUtilityForm import AddUtilityForm
from src.controllers.utilitiesController import UtilitiesController

class UtilitiesPage(BasePageWidget):
    def __init__(self, mainWindow=None):
        self.buttonText = "Add Utility"
        super().__init__(UtilitiesTable, self.buttonText, mainWindow=mainWindow)
    
    def updatePage(self):
        self.table.updateTable()

    def handleAddButton(self):
        dialog = AddUtilityForm()
        if dialog.exec():
            response = UtilitiesController.addUtility(None, None, None)
            self.table.updateTable()
