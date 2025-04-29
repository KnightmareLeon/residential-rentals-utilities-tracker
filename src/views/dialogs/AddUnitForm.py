from src.views.widgets.BaseCreateWidget import BaseCreateWidget

class AddUnitForm(BaseCreateWidget):
    def __init__(self):
        super().__init__(mainTitle="Add Unit", iconPath="assets/icons/units.png")
        self.setWindowTitle("UtiliTrack - Add Unit")
        self.setMinimumWidth(400)

        self.nameInput = self.addTextInput("Unit Name", placeholder="Enter name...")
        self.addressInput = self.addTextInput("Address", placeholder="Enter address...")
        self.unitTypeInput = self.addComboBox("Unit Type", ["Individual", "Shared", "Common"])