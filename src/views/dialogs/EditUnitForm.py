from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import Qt

from src.views.widgets.BaseEditWidget import BaseEditWidget

from src.controllers.unitsController import UnitsController

class EditUnitForm(BaseEditWidget):
    def __init__(self, name: str, address: str, type: str):
        super().__init__(mainTitle="Edit Unit", iconPath="assets/icons/units.png")
        self.setWindowTitle("UtiliTrack - Edit Unit")
        self.setMinimumWidth(400)

        self.addSection("Unit Information")

        self.nameInput = self.addTextInput("Unit Name", placeholder="Enter name...", sectionTitle="Unit Information", defaultValue=name)
        self.addressInput = self.addTextInput("Address", placeholder="Enter address...", sectionTitle="Unit Information", defaultValue=address)
        self.unitTypeInput = self.addComboBox("Unit Type", ["Individual", "Shared"], sectionTitle="Unit Information", defaultValue=type)
        
    def onEditClicked(self, unitID):
        updatedData = self.getFormData()

        if not updatedData:
            self.setErrorMessage("Please complete all required fields.")
            return

        # Show confirmation dialog
        msgBox = QMessageBox(self)
        msgBox.setIcon(QMessageBox.Icon.Warning)
        msgBox.setWindowTitle("Confirm Update")
        msgBox.setText("Are you sure you want to update this unit?")
        msgBox.setStyleSheet("""
        QDialog {
            background-color: #202020;
            font-family: "Urbanist";
            font-size: 16px;
            color: white;
        }
        QLabel {
            color: white;
            font-family: "Urbanist";
            font-size: 16px;
        }
        """)
        
        yesButton = msgBox.addButton(QMessageBox.StandardButton.Yes)
        noButton = msgBox.addButton(QMessageBox.StandardButton.No)

        yesButton.setCursor(Qt.CursorShape.PointingHandCursor)
        noButton.setCursor(Qt.CursorShape.PointingHandCursor)

        yesButton.setStyleSheet("""
            QPushButton {
                background-color: #541111;
                color: white;
                padding: 6px 12px;
                border-radius: 4px;
                border: none;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #743131;
            }
        """)
        noButton.setStyleSheet("""
            QPushButton {
                background-color: #444444;
                color: white;
                padding: 6px 12px;
                border-radius: 4px;
                border: none;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #666666;
            }
        """)

        msgBox.exec()

        if msgBox.clickedButton() != yesButton:
            return

        name = updatedData["Unit Name"]
        address = updatedData["Address"]
        type = updatedData["Unit Type"]

        response = UnitsController.editUnit(unitID, name, address, type)

        if response == "Unit edited successfully":
            self.accept()
        else:
            self.setErrorMessage(response)

    def accept(self):
        super().accept()
        