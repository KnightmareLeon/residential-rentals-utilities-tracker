from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, QSpinBox,
    QPushButton, QWidget, QSizePolicy, QFrame, QDateEdit, QMessageBox
)
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import Qt

from src.views.widgets.BaseEditWidget import BaseEditWidget
from src.controllers.unitsController import UnitsController
from src.controllers.utilitiesController import UtilitiesController

from src.controllers.billsController import BillsController

class EditBillForm(BaseEditWidget):
    def __init__(self, unitName: str, utilityType: str, totalAmount: str, billingPeriodStart, billingPeriodEnd, status: str, dueDate):
        super().__init__(mainTitle="Edit Bill", iconPath="assets/icons/utilities.png")
        self.setWindowTitle("UtiliTrack - Edit Bill")
        self.setMinimumWidth(400)

        self.allUnits = UnitsController.getUnitNames()
        self.unitDisplayNames = [f"{unit['Name']} ({unit['Type']})" for unit in self.allUnits]
        self.unitDisplayToID = {f"{unit['Name']} ({unit['Type']})": unit["UnitID"] for unit in self.allUnits}
        self.unitIDToDisplay = {unit["UnitID"]: f"{unit['Name']} ({unit['Type']})" for unit in self.allUnits}

        unitDisplayDefault = self.unitIDToDisplay.get(
            next((unit["UnitID"] for unit in self.allUnits if unit["Name"] == unitName), None),
            self.unitDisplayNames[0]
        )

        self.addSection("Bill Information")
        self.addSection("Bill Details")

        allUtilities = ['Electricity', 'Water', 'Gas', 'Internet', 'Trash', 'Maintenance', 'Miscellaneous']

        self.unitNameInput = self.addComboBox("Unit", self.unitDisplayNames, sectionTitle="Bill Information", defaultValue=unitDisplayDefault)
        self.unitNameInput.currentTextChanged.connect(self.onUnitNameChanged)

        self.typeInput = self.addComboBox("Utility Type", allUtilities, sectionTitle="Bill Information", defaultValue=utilityType)
        self.typeInput.setPlaceholderText("")
        
        self.statusInput = self.addComboBox("Status", ['Unpaid', 'Paid', 'Partially Paid', 'Overdue'], sectionTitle="Bill Details", defaultValue=status)
        self.totalAmountInput = self.addFloatInput("Total Amount", defaultValue=float(totalAmount), sectionTitle="Bill Details")
        self.billingStartInput = self.addDateInput("Billing Period Start", defaultDate=billingPeriodStart, sectionTitle="Bill Details")
        self.billingEndInput = self.addDateInput("Billing Period End", defaultDate=billingPeriodEnd, sectionTitle="Bill Details")
        self.dueDateInput = self.addDateInput("Due Date", defaultDate=dueDate, sectionTitle="Bill Details")
        
        self.onUnitNameChanged(unitDisplayDefault)

        index = self.typeInput.findText(utilityType)
        if index != -1:
            self.typeInput.setCurrentIndex(index)
        else:
            self.typeInput.setCurrentIndex(-1)
    
    def onUnitNameChanged(self, displayName: str):
        unitID = self.unitDisplayToID.get(displayName)
        if not unitID:
            return

        self.unitID = unitID
        utilityTypes = UtilitiesController.getUtilitiesByUnitID(unitID)

        self.typeInput.clear()
        self.typeInput.addItems([utility["Type"] for utility in utilityTypes])
        self.typeInput.setCurrentIndex(0)

    def getFormData(self) -> dict:
        data = {}
        for label, (labelWidget, widget) in self.fields.items():
            if isinstance(widget, QLineEdit):
                data[label] = widget.text()
            elif isinstance(widget, QComboBox) and label == "Unit":
                data["UnitID"] = self.unitDisplayToID.get(self.unitNameInput.currentText())
            elif isinstance(widget, QComboBox):
                data[label] = widget.currentText()
            elif isinstance(widget, QSpinBox):
                data[label] = widget.value()
            elif isinstance(widget, QDateEdit):
                data[label] = widget.date().toString("yyyy-MM-dd")
            else:
                data[label] = None
        return data

    def onEditClicked(self, billID):
        updatedData = self.getFormData()

        if not updatedData:
            self.setErrorMessage("Please complete all required fields.")
            return

        # Show confirmation dialog
        msgBox = QMessageBox(self)
        msgBox.setIcon(QMessageBox.Icon.Warning)
        msgBox.setWindowTitle("Confirm Update")
        msgBox.setText("Are you sure you want to update this bill?")
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

        # Proceed with update after confirmation
        unitID = updatedData["UnitID"]
        utilityID = updatedData["Utility Type"]
        status = updatedData["Status"]
        totalAmount = updatedData["Total Amount"]
        dueDate = updatedData["Due Date"]
        billStart = updatedData["Billing Period Start"]
        billEnd = updatedData["Billing Period End"]

        response = BillsController.editBill(
            billID,
            unitID,
            utilityID,
            status,
            totalAmount,
            dueDate,
            billStart,
            billEnd
        )

        if response == "Bill edited successfully":
            self.accept()
        else:
            self.setErrorMessage(response)

    def accept(self):
        super().accept()