from src.views.widgets.BaseCreateWidget import BaseCreateWidget
from src.controllers.unitsController import UnitsController

class AddUtilityForm(BaseCreateWidget):
    def __init__(self):
        super().__init__(mainTitle="Add Utility", iconPath="assets/icons/utilities.png")
        self.setWindowTitle("UtiliTrack - Add Utility")
        self.setMinimumWidth(400)

        self.unitNames = UnitsController.getUnitNames()
        self.indivUnitNames = [f"{name['UnitName']} ({name['Type']})" for name in self.unitNames if name['Type'] != "Shared"]

        self.addSection("Utility Information")

        self.typeInput = self.addComboBox("Utility Type", ['Electricity','Water','Gas','Wifi','Trash','Maintenance','Miscellaneous'], sectionTitle="Utility Information")
        self.typeInput.currentTextChanged.connect(self.handleUtilityTypeChange)

        self.unitNameInput = self.addComboBox("Unit", [f"{name['UnitName']} ({name['Type']})" for name in self.unitNames], sectionTitle="Utility Information")
        self.unitNameInput.currentTextChanged.connect(self.handleUnitNameChange)

        self.multipleUnitInput = self.addMultiselectComboBox("Shared with Unit(s)", [], sectionTitle="Utility Information", isVisible=False)

        self.installationDateInput = self.addDateInput("Installation Date", sectionTitle="Utility Information")
        self.statusInput = self.addComboBox("Status", ['Active','Inactive', 'N/A'], sectionTitle="Utility Information")
        self.billingInput = self.addComboBox("Billing Cycle", ['Monthly','Quarterly','Annually','Irregular'], sectionTitle="Utility Information")
    
    def handleUnitNameChange(self, text: str):
        unitType = text.split(' ')[-1][1:-1]
        
        labelWidget, widget = self.fields["Shared with Unit(s)"]
    
        if unitType == "Shared":
            widget.clear()
            widget.addItems(self.indivUnitNames)
            labelWidget.setVisible(True)
            widget.setVisible(True)
        elif unitType == "Individual":
            widget.clear()
            labelWidget.setVisible(False)
            widget.setVisible(False)
    
    def handleUtilityTypeChange(self, text: str):
        labelWidget, widget = self.fields["Status"]
        
        if text == "Gas" or text == "Maintenance" or text == "Miscellaneous" or text == "Trash":
            widget.setCurrentIndex(2)
        else:
            widget.setCurrentIndex(0)
        # if text == "Gas" or text == "Maintenance" or text == "Miscellaneous" or text == "Trash":
        #     widget.clear()
        #     widget.addItems(['N/A'])
        #     labelWidget.setVisible(False)
        #     widget.setVisible(False)
        # else:
        #     widget.clear()
        #     widget.addItems(['Active','Inactive'])
        #     labelWidget.setVisible(True)
        #     widget.setVisible(True)