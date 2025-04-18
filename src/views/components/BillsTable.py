from src.views.components.BaseTableWidget import BaseTableWidget
from src.utils.constants import SortOrder
from src.controllers.billsController import BillsController

class BillsTable(BaseTableWidget):
    def __init__(self, parent=None, mainWindow=None):
        self.databaseHeaders = ["BillID", "UnitName", "Type", "TotalAmount", "DueDate", "Status"]
        self.headers = ["Bill ID", "Unit Name", "Type", "Total Amount", "Due Date", "Status", "Actions"]
        super().__init__(self.headers, self.databaseHeaders, parent=parent, mainWindow=mainWindow)

    def updateTable(self):
        currentPage = self.parentWidget().currentPage
        sortingOrder = self.columnSortStates[self.currentSortIndex]
        sortingField = self.databaseHeaders[self.currentSortIndex]
        searchValue = self.mainWindow.searchInputLineEdit.text().strip()

        if sortingOrder == SortOrder.ASC:
            sortingOrderStr = "ASC"
        elif sortingOrder == SortOrder.DESC:
            sortingOrderStr = "DESC"
        else:
            sortingOrderStr = "ASC"

        data, count = BillsController.fetchData(currentPage, sortingOrderStr, sortingField, searchValue)
        #self.populateTable(data)
        self.parentWidget().totalPages = count
        self.parentWidget().pageLabel.setText(f"Page {currentPage} of {count}")


    def handleViewButton(self, row_idx):
        item = self.item(row_idx, 0)
        if not item:
            return
    
        id = item.text()
        unitData = BillsController.viewRecord(id)

        if unitData:
            #open unit view dialog
            pass

        self.updateTable()

    def handleEditButton(self, row_idx):
        item = self.item(row_idx, 0)
        if not item:
            return
        
        id = item.text()
        #open unit edit dialog
        response = BillsController.editRecord(id, None)

        self.updateTable()

    def handleDeleteButton(self, row_idx):
        item = self.item(row_idx, 0)
        if not item:
            return
        
        id = item.text()
        #open unit delete dialog
        response = BillsController.deleteRecord(id)

        self.updateTable()