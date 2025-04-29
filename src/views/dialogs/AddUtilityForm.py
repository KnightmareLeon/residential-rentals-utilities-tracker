from src.views.widgets.BaseCreateWidget import BaseCreateWidget

class AddUtilityForm(BaseCreateWidget):
    def __init__(self):
        super().__init__(mainTitle="Add Utility", iconPath="assets/icons/utilities.png")
        self.setWindowTitle("UtiliTrack - Add Utility")
        self.setMinimumWidth(400)

        #request all unit names from the database
        #unitNames = self.getUnitNames()  

        self.typeInput = self.addComboBox("Utility Type", ['Electricity','Water','Gas','Wifi','Trash','Maintenance','Miscellaneous'])
        self.unitNameInput = self.addComboBox("Unit of Utility", ['Unit 1','Unit 2','Unit 3','Unit 4'])
        self.installationDateInput = self.addDateInput("Installation Date")
        self.statusInput = self.addComboBox("Status", ['Active','Inactive'])
        self.billingInput = self.addComboBox("Billing Cycle", ['Monthly','Quarterly','Annually','Irregular'])