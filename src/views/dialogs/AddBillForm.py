import re
from PyQt6.QtWidgets import QLineEdit, QComboBox, QSpinBox, QDateEdit
from pyqt6_multiselect_combobox import MultiSelectComboBox

from src.views.widgets.BaseCreateWidget import BaseCreateWidget
from src.controllers.unitsController import UnitsController
from src.controllers.utilitiesController import UtilitiesController

class AddBillForm(BaseCreateWidget):
    def __init__(self):
        super().__init__(mainTitle="Add Bill", iconPath="assets/icons/bills.png")
        self.setWindowTitle("UtiliTrack - Add Bill")
        self.setMinimumWidth(400)

        self.unitNames = UnitsController.getUnitNames()
        self.unitNameMap = {unit["UnitName"]: unit["UnitID"] for unit in self.unitNames}
        self.utilityTypeMap = {}

        if not hasattr(self, 'sections'):
            self.sections = {}

        self.addSection("Bill Information")
        self.addSection("Bill Details")
        
        self.unitNameInput = self.addComboBox("Unit", [f"{name['UnitName']} ({name['Type']})" for name in self.unitNames], "Bill Information")
        self.unitNameInput.currentTextChanged.connect(self.handleUnitChange)
        
        self.utilityInput = self.addComboBox("Utility Type", [], "Bill Information")
        
        self.totalAmountInput = self.addFloatInput("Total Amount", 0, 999999999, "Bill Details")
        self.billingPeriodStartInput = self.addDateInput("Billing Period Start", sectionTitle="Bill Details")
        self.billingPeriodEndInput = self.addDateInput("Billing Period End", sectionTitle="Bill Details")
        self.statusInput = self.addComboBox("Status", ['Unpaid', 'Paid', 'Partially Paid', 'Overdue'], "Bill Details")
        self.dueDateInput = self.addDateInput("Due Date", sectionTitle="Bill Details")

        self.handleUnitChange()
        
    def getFormData(self) -> dict:
        data = {}
        for label, (labelWidget, widget) in self.fields.items():
            if isinstance(widget, QLineEdit):
                data[label] = widget.text()
            elif isinstance(widget, QComboBox) and labelWidget.text().strip() == "Unit":
                currentText = widget.currentText().strip()

                match = re.match(r'^(.*)\s+\((.*?)\)$', currentText)
                if match:
                    unitName = match.group(1).strip()
                else:
                    unitName = currentText

                unitID = self.unitNameMap.get(unitName)

                if unitID is None:
                    print(f"Warning: Unit ID not found for '{unitName}'")
                
                data[label] = unitID
            
            elif isinstance(widget, QComboBox) and labelWidget.text().strip() == "Utility Type":
                utilityType = widget.currentText().strip()
                utilityID = self.utilityTypeMap.get(utilityType)
                if utilityID is None:
                    print(f"Warning: Utility ID not found for '{utilityType}'")
                data[label] = utilityID

            elif isinstance(widget, MultiSelectComboBox):
                data[label] = widget.currentData()
            elif isinstance(widget, QComboBox):
                data[label] = widget.currentText()
            elif isinstance(widget, QSpinBox):
                data[label] = widget.value()
            elif isinstance(widget, QDateEdit):
                data[label] = widget.date()
        return data

    def handleUnitChange(self):
        currentText = self.unitNameInput.currentText()
        match = re.match(r'^(.*)\s+\((.*?)\)$', currentText)
        if not match:
            print(f"Warning: Could not parse unit from '{currentText}'")
            return

        unitName = match.group(1)
        unitID = None
        for unit in self.unitNames:
            if unit["UnitName"] == unitName:
                unitID = unit["UnitID"]
                break

        if unitID is None:
            print(f"Warning: Unit ID not found for '{unitName}'")
            return

        self.utilities = UtilitiesController.getUtilitiesByUnitID(unitID)
        self.utilityTypeMap = {utility["Type"]: utility["UtilityID"] for utility in self.utilities}

        self.utilityInput.clear()
        self.utilityInput.addItems([utility["Type"] for utility in self.utilities])