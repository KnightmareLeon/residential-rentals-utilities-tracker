from PyQt6.QtWidgets import QLabel, QMessageBox, QGroupBox

from src.views.widgets.BaseViewWidget import BaseViewWidget
from src.views.dialogs.EditBillForm import EditBillForm
from src.controllers.billsController import BillsController

class ViewBill(BaseViewWidget):
    def __init__(self, id: str, billData: dict, headers: list, databaseHeaders: list, parent=None, hasEdit = True, mainWindow = None):
        super().__init__("Bill Details", parent=parent, iconPath="assets/icons/bills.png", hasEdit=hasEdit, mainWindow=mainWindow)
        self.setMinimumSize(600, 400)
        self.setMaximumSize(800, 700)

        self.mainWindow = mainWindow
        self.billID = id
        
        # Create "Bill Information" card and add details
        billInfoCard = self.createCard("Bill Information")
        billInfoLayout = billInfoCard.layout()
        for i in range(4):
            self.addDetail(billInfoLayout, headers[i], billData[databaseHeaders[i]])
        billInfoLayout.addStretch()

        # Create "Bill Details" card and add details
        billDetailsCard = self.createCard("Bill Details")
        billDetailsLayout = billDetailsCard.layout()
        for i in range(4, 9):
            self.addDetail(billDetailsLayout, headers[i], billData[databaseHeaders[i]])
        billDetailsLayout.addStretch()

        # Add cards to the main grid layout
        self.addWidgetToGrid(0, 0, billInfoCard)
        self.addWidgetToGrid(0, 1, billDetailsCard)

    def handleEditClicked(self):
        if not self.billID:
            msgBox = QMessageBox(self)
            msgBox.setIcon(QMessageBox.Icon.Warning)
            msgBox.setWindowTitle("Error")
            msgBox.setText("Bill ID not found")

            msgBox.setOption(QMessageBox.Option.DontUseNativeDialog, True)
            msgBox.setStyleSheet("""
            QDialog {
                background-color: #202020;
                font-family: "Urbanist";
                font-size: 16px;
                color: white;
            }
            QLabel {
                color: white;
            }
            QPushButton {
                background-color: #541111;
                color: white;
                padding: 6px 12px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #743131;
            }
            """)

            msgBox.exec()
            return
    
        bill = BillsController.viewBill(self.billID)
        dialog = EditBillForm(bill["UnitName"], bill["Type"], bill["TotalAmount"], bill["BillingPeriodStart"], bill["BillingPeriodEnd"], bill["Status"], bill["DueDate"])

        if dialog.exec():
            updatedData = dialog.getFormData()
            
            BillsController.editBill(
                self.billID,
                updatedData["UnitID"],
                updatedData["Utility Type"],
                updatedData["Status"],
                updatedData["Total Amount"],
                updatedData["Due Date"],
                updatedData["Billing Period Start"],
                updatedData["Billing Period End"]
            )

            self.close()

            self.mainWindow.updatePages()
            

