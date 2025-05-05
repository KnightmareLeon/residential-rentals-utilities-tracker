from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import Qt

from src.views.widgets.BaseTableWidget import BaseTableWidget
from src.views.dialogs.UnitView import UnitView
from src.views.dialogs.EditUnitForm import EditUnitForm
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
        self.populateTable(data)
        self.parentWidget().totalPages = count
        self.parentWidget().pageLabel.setText(f"Page {currentPage} of {count}")

    def handleViewButton(self, row_idx):
        item = self.item(row_idx, 0)
        if not item:
            return
    
        id = item.text()
        unitData, unitUtilities, unitBillsData = UnitsController.viewUnit(id)

        if unitData:
            self.viewWindow = UnitView(id, unitData, unitUtilities, unitBillsData, self.headers, self.databaseHeaders)
            self.viewWindow.show()

    def handleEditButton(self, row_idx):
        item = self.item(row_idx, 0)
        if not item:
            return
        
        unitID = item.text()
        unit, _, _ = UnitsController.viewUnit(unitID)

        dialog = EditUnitForm(name=unit["Name"], address=unit["Address"], type=unit["Type"])

        if dialog.exec():
            updatedData = dialog.getFormData()
            
            UnitsController.editUnit(
                unitID,
                updatedData["Unit Name"],
                updatedData["Address"],
                updatedData["Unit Type"]
            )

            self.updateTable()

    def handleDeleteButton(self, row_idx):
        item = self.item(row_idx, 0)
        if not item:
            return

        unitID = item.text()

        msgBox = QMessageBox(self)
        msgBox.setIcon(QMessageBox.Icon.Warning)
        msgBox.setWindowTitle("Confirm Delete")
        msgBox.setText(f"Are you sure you want to delete Unit '{unitID}'?")
        yesButton = msgBox.addButton(QMessageBox.StandardButton.Yes)
        noButton = msgBox.addButton(QMessageBox.StandardButton.No)

        yesButton.setCursor(Qt.CursorShape.PointingHandCursor)
        noButton.setCursor(Qt.CursorShape.PointingHandCursor)

        yesButton.setStyleSheet("""
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
        noButton.setStyleSheet("""
QPushButton {
    background-color: #444444;
    color: white;
    padding: 6px 12px;
    border-radius: 4px;
}
QPushButton:hover {
    background-color: #666666;
}
""")
        
        msgBox.exec()

        if msgBox.clickedButton() == yesButton:
            success = UnitsController.deleteUnit(unitID)
            if success:
                QMessageBox.information(self, "Success", f"Unit '{unitID}' was deleted.")
            else:
                QMessageBox.warning(self, "Error", f"Failed to delete Unit '{unitID}'.")

            self.updateTable()