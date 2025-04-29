from src.views.widgets.BaseCreateWidget import BaseCreateWidget

class AddBillForm(BaseCreateWidget):
    def __init__(self):
        super().__init__(mainTitle="Add Utility", iconPath="assets/icons/utilities.png")
        self.setWindowTitle("UtiliTrack - Add Utility")
        self.setMinimumWidth(400)

        #request all unit names from the database
        #unitNames = self.getUnitNames()  

        #request all utilities of unit from the database
        #utilities = self.getUtilitiesByUnit()

        if not hasattr(self, 'sections'):
            self.sections = {}  

        self.addSection("Bill Information")
        self.addSection("Bill Details")
        
        self.unitNameInput = self.addComboBox("Unit of Utility", ['Unit 1','Unit 2','Unit 3','Unit 4'], "Bill Information")
        self.utilityInput = self.addComboBox("Utility Type", ['Electricity','Water','Gas','Wifi','Trash','Maintenance','Miscellaneous'], "Bill Information")
        
        self.totalAmountInput = self.addFloatInput("Total Amount", 0, 999999999, "Bill Details")
        self.billingPeriodStartInput = self.addDateInput("Billing Period Start", sectionTitle="Bill Details")
        self.billingPeriodEndInput = self.addDateInput("Billing Period End", sectionTitle="Bill Details")
        self.statusInput = self.addComboBox("Status", ['Unpaid', 'Paid', 'Partially Paid', 'Overdue'], "Bill Details")
        self.dueDateInput = self.addDateInput("Due Date", sectionTitle="Bill Details")