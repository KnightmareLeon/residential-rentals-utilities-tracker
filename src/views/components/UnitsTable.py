from src.views.components.BaseTableWidget import BaseTableWidget
from src.utils.constants import SortOrder
from src.controllers.unitsController import UnitsController

class UnitsTable(BaseTableWidget):
    def __init__(self, parent=None, mainWindow=None):
        self.databaseHeaders = ["UnitID", "Name", "Address", "UnitType"]
        self.headers = ["Unit ID", "Unit Name", "Address", "Unit Type", "Actions"]
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

        data, count = UnitsController.fetchData(currentPage, sortingOrderStr, sortingField, searchValue)
        #self.populateTable(data)
        self.parentWidget().totalPages = count
        self.parentWidget().pageLabel.setText(f"Page {currentPage} of {count}")

    def handleViewButton(self, row_idx):
        item = self.item(row_idx, 0)
        if not item:
            return
    
        id = item.text()
        unitData = UnitsController.viewRecord(id)

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
        response = UnitsController.editRecord(id, None)

        self.updateTable()

    def handleDeleteButton(self, row_idx):
        item = self.item(row_idx, 0)
        if not item:
            return
        
        id = item.text()
        #open unit delete dialog
        response = UnitsController.deleteRecord(id)

        self.updateTable()