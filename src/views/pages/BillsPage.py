from src.views.pages.BasePageWidget import BasePageWidget
from src.views.components.BillsTable import BillsTable

class BillsPage(BasePageWidget):
    def __init__(self, mainWindow=None):
        self.buttonText = "Add Bill"
        
        super().__init__(BillsTable, self.buttonText, mainWindow=mainWindow)

    def handleAddButton(self):
        print("adding bill!")
