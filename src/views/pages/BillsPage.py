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
            response = BillsController.addBill(None, None, None, None, None, None, None)
            self.table.updateTable()
