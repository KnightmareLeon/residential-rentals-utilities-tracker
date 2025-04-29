from src.views.widgets.BaseViewWidget import BaseViewWidget

class BillView(BaseViewWidget):
    def __init__(self, id: str, unitData: dict, headers: list, databaseHeaders: list, parent=None):
        super().__init__("Bill Details", parent=parent, iconPath="assets/icons/bills.png")
        self.setMaximumSize(500, 700)

        billInfo = self.addSection("Bill Information")
        for i in range(4):
            self.addDetail(billInfo, headers[i], unitData[databaseHeaders[i]])
        
        billDetails = self.addSection("Bill Details")
        for i in range(4,9):
            self.addDetail(billDetails, headers[i], unitData[databaseHeaders[i]])
