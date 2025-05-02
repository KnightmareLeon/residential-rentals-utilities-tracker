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
        self.utilities = UtilitiesController.getUtilitiesByUnitID("0")

        if not hasattr(self, 'sections'):
            self.sections = {}

        self.addSection("Bill Information")
        self.addSection("Bill Details")
        
        self.unitNameInput = self.addComboBox("Unit", [f"{name['UnitName']} ({name['Type']})" for name in self.unitNames], "Bill Information")

        self.utilityInput = self.addComboBox("Utility Type", [utility["Type"] for utility in self.utilities], "Bill Information")
        
        self.totalAmountInput = self.addFloatInput("Total Amount", 0, 999999999, "Bill Details")
        self.billingPeriodStartInput = self.addDateInput("Billing Period Start", sectionTitle="Bill Details")
        self.billingPeriodEndInput = self.addDateInput("Billing Period End", sectionTitle="Bill Details")
        self.statusInput = self.addComboBox("Status", ['Unpaid', 'Paid', 'Partially Paid', 'Overdue'], "Bill Details")
        self.dueDateInput = self.addDateInput("Due Date", sectionTitle="Bill Details")
    
    def getFormData(self) -> dict:
        data = {}
        for label, (labelWidget, widget) in self.fields.items():
            if isinstance(widget, QLineEdit):
                data[label] = widget.text()
            elif isinstance(widget, QComboBox) and labelWidget.text() == "Unit":
                unitName = ' '.join(widget.currentText().split(' ')[:-1])
                unitID = None
                for unit in self.unitNames:
                    if unit["UnitName"] == unitName:
                        unitID = unit["UnitID"]
                
                if unitID is None:
                    print(f"Warning: Unit ID not found for '{unitName}'")
                    
                data[label] = unitID
            elif isinstance(widget, MultiSelectComboBox):
                data[label] = widget.currentData()
            elif isinstance(widget, QComboBox):
                data[label] = widget.currentText()
            elif isinstance(widget, QSpinBox):
                data[label] = widget.value()
            elif isinstance(widget, QDateEdit):
                data[label] = widget.date()
        return data
