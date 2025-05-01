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
                name = ' '.join(billData["Unit"].split(' ')[:-1])
                type = billData["Utility Type"]
                totalAmount = billData["Total Amount"]
                billPeriodStart = billData["Billing Period Start"]
                billPeriodEnd = billData["Billing Period End"]
                status = billData["Status"]
                dueDate = billData["Due Date"]

                response = BillsController.addBill(name, type, totalAmount, billPeriodStart, billPeriodEnd, status, dueDate)
                self.table.updateTable()
