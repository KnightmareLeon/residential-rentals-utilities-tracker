from PyQt6.QtWidgets import QMessageBox

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
                unitID = utilityData["Unit"]
                sharedUnitIDs = utilityData["Shared with Unit(s)"]
                status = utilityData["Status"]
                billing = utilityData["Billing Cycle"]

                response = UtilitiesController.addUtility(type, unitID, sharedUnitIDs, status, billing)
                if response:
                    self.table.updateTable()
                    self.showSuccessNotification()
    
    def showSuccessNotification(self):
        QMessageBox.information(self, "Success", f"Utility was successfully added")
