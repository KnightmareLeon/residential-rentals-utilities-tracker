from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QPushButton, QWidget, QHBoxLayout, QHeaderView
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QIcon, QColor, QBrush

from src.views.components.BaseTableWidget import BaseTableWidget
from src.utils.constants import SortOrder

class UtilityTable(BaseTableWidget):
    def __init__(self, parent=None, mainWindow=None):
        self.databaseHeaders = ["UtilityID", "Type", "Status", "BillingCycle"]
        self.headers = ["Utility ID", "Type", "Status", "Billing Cycle", "Actions"]
        super().__init__(self.headers, self.databaseHeaders, parent=parent, mainWindow=mainWindow)

    def updateTable(self):
        sortingOrder = self.columnSortStates[self.currentSortIndex]
        sortingField = self.databaseHeaders[self.currentSortIndex]
        searchValue = self.mainWindow.searchInputLineEdit.text().strip()

        if sortingOrder == SortOrder.ASC:
            sortingOrderStr = "ASC"
        elif sortingOrder == SortOrder.DESC:
            sortingOrderStr = "DESC"
        else:
            sortingOrderStr = "ASC"

        print("UTILITIES TABLE |", "search:", searchValue, "| sort by:", sortingField, sortingOrderStr)

    def handleViewButton(self, row_idx):
        print("UTILITIES TABLE | view", row_idx)

    def handleEditButton(self, row_idx):
        print("UTILITIES TABLE | edit", row_idx)
    
    def handleDeleteButton(self, row_idx):
        print("UTILITIES TABLE | delete", row_idx)