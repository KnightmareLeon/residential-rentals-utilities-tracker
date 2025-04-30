from src.views.widgets.BaseViewWidget import BaseViewWidget

class BillView(BaseViewWidget):
    def __init__(self, id: str, unitData: dict, headers: list, databaseHeaders: list, parent=None):
        super().__init__("Bill Details", parent=parent, iconPath="assets/icons/bills.png")
        self.setMinimumSize(600, 400)
        self.setMaximumSize(600, 700)

        # Create "Bill Information" card and add details
        billInfoCard = self.createCard("Bill Information")
        billInfoLayout = billInfoCard.layout()
        for i in range(4):
            self.addDetail(billInfoLayout, headers[i], unitData[databaseHeaders[i]])
        billInfoLayout.addStretch()

        # Create "Bill Details" card and add details
        billDetailsCard = self.createCard("Bill Details")
        billDetailsLayout = billDetailsCard.layout()
        for i in range(4, 9):
            self.addDetail(billDetailsLayout, headers[i], unitData[databaseHeaders[i]])
        billDetailsLayout.addStretch()

        # Add cards to the main grid layout
        self.addWidgetToGrid(0, 0, billInfoCard)
        self.addWidgetToGrid(0, 1, billDetailsCard)
