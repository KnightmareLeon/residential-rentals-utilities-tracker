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
        
        