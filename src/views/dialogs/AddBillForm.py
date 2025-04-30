from src.views.widgets.BaseCreateWidget import BaseCreateWidget
from src.controllers.unitsController import UnitsController
from src.controllers.utilitiesController import UtilitiesController

class AddBillForm(BaseCreateWidget):
    def __init__(self):
        super().__init__(mainTitle="Add Utility", iconPath="assets/icons/utilities.png")
        self.setWindowTitle("UtiliTrack - Add Utility")
        self.setMinimumWidth(400)


        unitNames = UnitsController.getUnitNames()
        utilities = UtilitiesController.getUtilitiesByUnitID("0")

        if not hasattr(self, 'sections'):
            self.sections = {}

        self.addSection("Bill Information")
        self.addSection("Bill Details")
        
        self.unitNameInput = self.addComboBox("Unit", [name["UnitName"] for name in unitNames], "Bill Information")

        self.utilityInput = self.addComboBox("Utility Type", [utility["Type"] for utility in utilities], "Bill Information")
        
        self.totalAmountInput = self.addFloatInput("Total Amount", 0, 999999999, "Bill Details")
        self.billingPeriodStartInput = self.addDateInput("Billing Period Start", sectionTitle="Bill Details")
        self.billingPeriodEndInput = self.addDateInput("Billing Period End", sectionTitle="Bill Details")
        self.statusInput = self.addComboBox("Status", ['Unpaid', 'Paid', 'Partially Paid', 'Overdue'], "Bill Details")
        self.dueDateInput = self.addDateInput("Due Date", sectionTitle="Bill Details")