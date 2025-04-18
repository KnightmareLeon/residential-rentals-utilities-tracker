from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QPushButton, QWidget, QHBoxLayout, QHeaderView
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QIcon, QColor, QBrush

from src.views.components.BaseTableWidget import BaseTableWidget
from src.utils.constants import SortOrder

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

        print("UNITS TABLE |", "search:", searchValue, "| sort by:", sortingField, sortingOrderStr, "| page:", currentPage)

    def handleViewButton(self, row_idx):
        print("UNITS TABLE | view", row_idx)

    def handleEditButton(self, row_idx):
        print("UNITS TABLE | edit", row_idx)
    
    def handleDeleteButton(self, row_idx):
        print("UNITS TABLE | delete", row_idx)