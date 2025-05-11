from src.views.widgets.BaseCreateWidget import BaseCreateWidget

from src.controllers.unitsController import UnitsController

class AddUnitForm(BaseCreateWidget):
    def __init__(self):
        super().__init__(mainTitle="Add Unit", iconPath="assets/icons/units.png")
        self.setWindowTitle("UtiliTrack - Add Unit")
        self.setMinimumWidth(400)

        self.addSection("Unit Information")

        self.nameInput = self.addTextInput("Unit Name", placeholder="Enter name...", sectionTitle="Unit Information")
        self.addressInput = self.addTextInput("Address", placeholder="Enter address...", sectionTitle="Unit Information")
        self.unitTypeInput = self.addComboBox("Unit Type", ["Individual", "Shared"], sectionTitle="Unit Information")
    
    def onAddClicked(self):
        unitData = self.getFormData()
        if unitData:
            name = unitData["Unit Name"]
            address = unitData["Address"]
            type = unitData["Unit Type"]

            response = UnitsController.addUnit(name, address, type)

            if response == "Unit added successfully":
                self.accept()
            else:
                self.setErrorMessage(response)
        else:
            self.setErrorMessage("Please complete all required fields.")