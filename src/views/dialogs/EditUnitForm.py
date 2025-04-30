from src.views.widgets.BaseEditWidget import BaseEditWidget

class EditUnitForm(BaseEditWidget):
    def __init__(self, name: str, address: str, type: str):
        super().__init__(mainTitle="Edit Unit", iconPath="assets/icons/units.png")
        self.setWindowTitle("UtiliTrack - Edit Unit")
        self.setMinimumWidth(400)

        self.addSection("Unit Information")

        self.nameInput = self.addTextInput("Unit Name", placeholder="Enter name...", sectionTitle="Unit Information", defaultValue=name)
        self.addressInput = self.addTextInput("Address", placeholder="Enter address...", sectionTitle="Unit Information", defaultValue=address)
        self.unitTypeInput = self.addComboBox("Unit Type", ["Individual", "Shared", "Common"], sectionTitle="Unit Information", defaultValue=type)