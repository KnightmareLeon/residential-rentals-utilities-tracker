import re

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
            utilityData = dialog.getFormData()
            if utilityData:
                type = utilityData["Utility Type"]
                unit = ' '.join(utilityData["Unit"].split(' ')[:-1])
                sharedUnits = [re.sub(r'\s*\(.*?\)', '', unit).strip() for unit in utilityData["Shared with Unit(s)"]]
                status = utilityData["Status"]
                billing = utilityData["Billing Cycle"]

                response = UtilitiesController.addUtility(type, unit, sharedUnits, status, billing)
                self.table.updateTable()
