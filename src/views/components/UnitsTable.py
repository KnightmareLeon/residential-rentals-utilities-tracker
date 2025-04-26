import datetime
from dateutil.relativedelta import relativedelta

from src.views.widgets.BaseTableWidget import BaseTableWidget
from src.views.widgets.BaseViewWidget import BaseViewWidget
from src.views.widgets.UtilityChartWidget import UtilityChartWidget
from src.utils.constants import SortOrder
from src.controllers.unitsController import UnitsController

class UnitsTable(BaseTableWidget):
    def __init__(self, parent=None, mainWindow=None):
        self.databaseHeaders = ["UnitID", "Name", "Address", "Type"]
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

        data, count = UnitsController.fetchUnits(currentPage, sortingOrderStr, sortingField, searchValue)
        #self.populateTable(data)
        self.parentWidget().totalPages = count
        self.parentWidget().pageLabel.setText(f"Page {currentPage} of {count}")

    def handleViewButton(self, row_idx):
        item = self.item(row_idx, 0)
        if not item:
            return
    
        id = item.text()
        unitData, unitBillsData = UnitsController.viewUnit(id)
        print(id)
        if unitData:
            self.viewWindow = BaseViewWidget("Unit Details", iconPath="assets/icons/units.png")
            unitInfoSection = self.viewWindow.addSection("Unit Information")
            self.viewWindow.addDetail(unitInfoSection, self.headers[0], unitData[self.databaseHeaders[0]])
            self.viewWindow.addDetail(unitInfoSection, self.headers[1], unitData[self.databaseHeaders[1]])
            self.viewWindow.addDetail(unitInfoSection, self.headers[2], unitData[self.databaseHeaders[2]])
            self.viewWindow.addDetail(unitInfoSection, self.headers[3], unitData[self.databaseHeaders[3]])
            billInfoSection = self.viewWindow.addSection("Unit Bills")
            chartWidget = UtilityChartWidget(unitBillsData, "Total Utilities Cost of Unit " + id)
            self.viewWindow.addWidgetToSection(billInfoSection, chartWidget)
            self.viewWindow.show()
            pass

        self.updateTable()

    def handleEditButton(self, row_idx):
        item = self.item(row_idx, 0)
        if not item:
            return
        
        id = item.text()
        #open unit edit dialog
        response = UnitsController.editUnit(id, None, None, None, None)

        self.updateTable()

    def handleDeleteButton(self, row_idx):
        item = self.item(row_idx, 0)
        if not item:
            return
        
        id = item.text()
        #open unit delete dialog
        response = UnitsController.deleteUnit(id)

        self.updateTable()