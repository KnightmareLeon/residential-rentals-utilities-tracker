from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import Qt

from src.views.widgets.BaseTableWidget import BaseTableWidget
from src.views.dialogs.ViewUtility import ViewUtility
from src.views.dialogs.EditUtilityForm import EditUtilityForm
from src.utils.constants import SortOrder
from src.controllers.utilitiesController import UtilitiesController

from src.utils.constants import utilityDataHeaders, utilityDataDatabaseHeaders

class UtilitiesTable(BaseTableWidget):
    def __init__(self, parent=None, mainWindow=None):
        self.databaseHeaders = ["UtilityID", "Type", "Name", "Status", "BillingCycle"]
        self.headers = ["Utility ID", "Type", "Unit Name", "Status", "Billing Cycle", "Actions"]
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

        data, count = UtilitiesController.fetchUtilities(currentPage, sortingOrderStr, sortingField, searchValue)
        print(data, count)
        self.populateTable(data)
        self.parentWidget().totalPages = count
        self.parentWidget().pageLabel.setText(f"Page {currentPage} of {count}")


    def handleViewButton(self, row_idx):
        item = self.item(row_idx, 0)
        if not item:
            return
        
        self.mainWindow.setStatusBarText("Loading Utility Data....")
    
        id = item.text()
        utilityData, utilityUnits, utilityBillsData = UtilitiesController.viewUtility(id)

        if utilityData:
            self.viewWindow = ViewUtility(id, utilityData, utilityUnits, utilityBillsData, utilityDataHeaders, utilityDataDatabaseHeaders, mainWindow=self.mainWindow)
            self.viewWindow.show()
    
    def handleEditButton(self, row_idx):
        item = self.item(row_idx, 0)
        if not item:
            return

        utilityID = item.text()
        utility, units, _ = UtilitiesController.viewUtility(utilityID)

        dialog = EditUtilityForm(
            utility["Type"],
            units,
            utility["Status"],
            utility["BillingCycle"],
            utility["InstallationDate"]
        )

        dialog.addButton.setText("Update Utility")
        dialog.addButton.clicked.disconnect()
        dialog.addButton.clicked.connect(lambda: dialog.onEditClicked(utilityID))

        if dialog.exec():
            self.mainWindow.updatePages()
            self.mainWindow.setStatusBarText("Utility updated successfully.")
            self.showSuccessNotification("Utility was updated successfully.")

    def handleDeleteButton(self, row_idx):
        item = self.item(row_idx, 0)
        if not item:
            return

        utilityID = item.text()

        msgBox = QMessageBox(self)
        msgBox.setIcon(QMessageBox.Icon.Warning)
        msgBox.setWindowTitle("Confirm Delete")
        msgBox.setText(f"Are you sure you want to delete Utility '{utilityID}'?")
        msgBox.setStyleSheet("""
QDialog {
    background-color: #202020;
    font-family: "Urbanist";
    font-size: 16px;
    color: white;
}

QLabel {
    color: white;
    font-family: "Urbanist";
    font-size: 16px;
}

""")
        
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
            success = UtilitiesController.deleteUtility(utilityID)
            if success:
                self.mainWindow.setStatusBarText("Utility deleted succesfully.")
                self.showSuccessNotification(f"Utility '{utilityID}' was deleted.")
            else:
                self.mainWindow.setStatusBarText("Failed to delete Utility.")
                self.showErrorNotification(f"Failed to delete Utility '{utilityID}'.")

            self.mainWindow.updatePages()
    
    def showSuccessNotification(self, message="Utility was successfully added"):
        msgBox = QMessageBox(self)
        msgBox.setIcon(QMessageBox.Icon.Information)
        msgBox.setWindowTitle("Success")
        msgBox.setText(message)

        msgBox.setOption(QMessageBox.Option.DontUseNativeDialog, True)

        msgBox.setStyleSheet("""
        QDialog {
            background-color: #202020;
            font-family: "Urbanist";
            font-size: 16px;
            color: white;
        }
        QLabel {
            color: white;
        }
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
    
    def showErrorNotification(self, message="An error occurred"):
        msgBox = QMessageBox(self)
        msgBox.setIcon(QMessageBox.Icon.Warning)
        msgBox.setWindowTitle("Error")
        msgBox.setText(message)

        msgBox.setOption(QMessageBox.Option.DontUseNativeDialog, True)

        msgBox.setStyleSheet("""
        QDialog {
            background-color: #202020;
            font-family: "Urbanist";
            font-size: 16px;
            color: white;
        }
        QLabel {
            color: white;
        }
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

        msgBox.exec()
    