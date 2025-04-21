from src.views.widgets.BasePageWidget import BasePageWidget
from src.views.components.BillsTable import BillsTable
from src.controllers.billsController import BillsController

class BillsPage(BasePageWidget):
    def __init__(self, mainWindow=None):
        self.buttonText = "Add Bill"
        super().__init__(BillsTable, self.buttonText, mainWindow=mainWindow)

    def updatePage(self):
        self.table.updateTable()

    def handleAddButton(self):
        response = BillsController.addBill(None, None, None, None, None, None, None)
        self.table.updateTable()
