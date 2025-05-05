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
        msgBox = QMessageBox(self)
        msgBox.setIcon(QMessageBox.Icon.Information)
        msgBox.setWindowTitle("Success")
        msgBox.setText("Utility was successfully added")

        # Force non-native dialog so styles apply
        msgBox.setOption(QMessageBox.Option.DontUseNativeDialog, True)

        # Example stylesheet (dark mode)
        msgBox.setStyleSheet("""
        QDialog {
            background-color: #202020;
            font-family: "Urbanist";
            font-size: 16px;
            color: white;
        }
        QLabel {
            color: white;
        }
        QPushButton {
            background-color: #444444;
            color: white;
            padding: 6px 12px;
            border-radius: 4px;
        }
        QPushButton:hover {
            background-color: #666666;
        }
        """)

        msgBox.exec()
    