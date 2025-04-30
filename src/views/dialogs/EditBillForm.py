from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, QSpinBox,
    QPushButton, QWidget, QSizePolicy, QFrame, QDateEdit
)

from src.views.widgets.BaseEditWidget import BaseEditWidget
from src.controllers.unitsController import UnitsController
from src.controllers.utilitiesController import UtilitiesController

class EditBillForm(BaseEditWidget):
    def __init__(self, unitName: str, utilityType: str, totalAmount: str, billingPeriodStart, billingPeriodEnd, status: str, dueDate):
        super().__init__(mainTitle="Edit Bill", iconPath="assets/icons/utilities.png")
        self.setWindowTitle("UtiliTrack - Edit Bill")
        self.setMinimumWidth(400)

        self.unitNames = UnitsController.getUnitNames()
        self.unitID = None

        unitNameList = [unit["UnitName"] for unit in self.unitNames]

        self.addSection("Bill Information")
        self.addSection("Bill Details") 

        self.unitNameInput = self.addComboBox("Unit", unitNameList, sectionTitle="Bill Information", defaultValue=unitName)
        self.unitNameInput.currentTextChanged.connect(self.onUnitNameChanged)
        self.typeInput = self.addComboBox("Utility Type", ['Electricity', 'Water', 'Gas', 'Wifi', 'Trash', 'Maintenance', 'Miscellaneous'], sectionTitle="Bill Information", defaultValue=utilityType)
        
        self.statusInput = self.addComboBox("Status", ['Active', 'Inactive'], sectionTitle="Bill Details", defaultValue=status)
        self.totalAmountInput = self.addFloatInput("Total Amount", defaultValue=float(totalAmount), sectionTitle="Bill Details")
        self.dueDateInput = self.addDateInput("Due Date", defaultDate=dueDate, sectionTitle="Bill Details")
        self.billingStartInput = self.addDateInput("Billing Start", defaultDate=billingPeriodStart, sectionTitle="Bill Details")
        self.billingEndInput = self.addDateInput("Billing End", defaultDate=billingPeriodEnd, sectionTitle="Bill Details")
    
    def onUnitNameChanged(self, unitName: str):
        for unit in unitName in self.unitNames:
            if unit["UnitName"] == unitName:
                self.unitID = unit["UnitID"]
                break

        utilityTypes = UtilitiesController.getUtilitiesByUnitID(self.unitID)
        self.typeInput.clear()
        self.typeInput.addItems([utility["Type"] for utility in utilityTypes])

    def getFormData(self) -> dict:
        data = {}
        for label, widget in self.fields.items():
            if isinstance(widget, QLineEdit):
                data[label] = widget.text()
            elif isinstance(widget, QComboBox):
                data[label] = widget.currentText()
            elif isinstance(widget, QSpinBox):
                data[label] = widget.value()
            elif isinstance(widget, QDateEdit):
                data[label] = widget.date().toString("yyyy-MM-dd")
            else:
                data[label] = None
        return data