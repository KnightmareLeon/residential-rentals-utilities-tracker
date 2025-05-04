from PyQt6.QtWidgets import QMessageBox

from src.views.widgets.BasePageWidget import BasePageWidget
from src.views.components.UnitsTable import UnitsTable
from src.views.dialogs.AddUnitForm import AddUnitForm
from src.controllers.unitsController import UnitsController

class UnitsPage(BasePageWidget):
    def __init__(self, mainWindow=None):
        self.buttonText = "Add Unit"
        super().__init__(UnitsTable, self.buttonText, mainWindow=mainWindow)

    def updatePage(self):
        self.table.updateTable()

    def handleAddButton(self):
        dialog = AddUnitForm()
        
        if dialog.exec():
            unitData = dialog.getFormData()
            if unitData:
                name = unitData["Unit Name"]
                address = unitData["Address"]
                type = unitData["Unit Type"]

                response = UnitsController.addUnit(name, address, type)
                if response:
                    self.table.updateTable()
                    self.showSuccessNotification()
    
    def showSuccessNotification(self):
        QMessageBox.information(self, "Success", f"Utility was successfully added")
        
        