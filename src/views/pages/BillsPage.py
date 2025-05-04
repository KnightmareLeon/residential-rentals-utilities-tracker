from PyQt6.QtWidgets import QMessageBox

from src.views.widgets.BasePageWidget import BasePageWidget
from src.views.components.BillsTable import BillsTable
from src.views.dialogs.AddBillForm import AddBillForm
from src.controllers.billsController import BillsController

class BillsPage(BasePageWidget):
    def __init__(self, mainWindow=None):
        self.buttonText = "Add Bill"
        super().__init__(BillsTable, self.buttonText, mainWindow=mainWindow)

    def updatePage(self):
        self.table.updateTable()

    def handleAddButton(self):
        dialog = AddBillForm()
        if dialog.exec():
            billData = dialog.getFormData()
            if billData:
                unitID = billData["Unit"]
                utilityID = billData["Utility Type"]
                totalAmount = billData["Total Amount"]
                billPeriodStart = billData["Billing Period Start"]
                billPeriodEnd = billData["Billing Period End"]
                status = billData["Status"]
                dueDate = billData["Due Date"]

                response = BillsController.addBill(unitID, utilityID, totalAmount, billPeriodStart, billPeriodEnd, status, dueDate)
                
                if response:
                    self.table.updateTable()
                    self.showSuccessNotification()
    
    def showSuccessNotification(self):
        QMessageBox.information(self, "Success", f"Bill was successfully added")