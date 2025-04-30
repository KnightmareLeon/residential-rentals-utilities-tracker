from src.views.widgets.BaseEditWidget import BaseEditWidget
from src.controllers.unitsController import UnitsController
from src.controllers.utilitiesController import UtilitiesController
from src.utils.constants import UTILITIES

class EditUtilityForm(BaseEditWidget):
    def __init__(self, type: str, unitName: str, status: str, billingCycle: str, installationDate: str):
        super().__init__(mainTitle="Edit Utility", iconPath="assets/icons/utilities.png")
        self.setWindowTitle("UtiliTrack - Edit Utility")
        self.setMinimumWidth(400)

        
        unitNames = UnitsController.getUnitNames()

        self.addSection("Utility Information")

        self.typeInput = self.addComboBox("Utility", UTILITIES, sectionTitle="Utility Information", defaultValue=type)
        self.unitNameInput = self.addComboBox("Unit", [name["UnitName"] for name in unitNames], sectionTitle="Utility Information")
        self.installationDateInput = self.addDateInput("Installation Date", sectionTitle="Utility Information")
        self.statusInput = self.addComboBox("Status", ['Active','Inactive'], sectionTitle="Utility Information")
        self.billingInput = self.addComboBox("Billing Cycle", ['Monthly','Quarterly','Annually','Irregular'], sectionTitle="Utility Information")