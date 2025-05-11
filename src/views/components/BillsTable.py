from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import Qt

from src.views.widgets.BaseTableWidget import BaseTableWidget
from src.views.dialogs.ViewBill import ViewBill
from src.utils.constants import SortOrder, billDataDatabaseHeaders, billDataHeaders
from src.views.dialogs.EditBillForm import EditBillForm

from src.controllers.billsController import BillsController

class BillsTable(BaseTableWidget):
    def __init__(self, parent=None, mainWindow=None):
        self.databaseHeaders = ["BillID", "Name", "Type", "TotalAmount", "DueDate", "Status"]
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

        data, count = BillsController.fetchBills(currentPage, sortingOrderStr, sortingField, searchValue)
        self.populateTable(data)
        self.parentWidget().totalPages = count
        self.parentWidget().pageLabel.setText(f"Page {currentPage} of {count}")

    def handleViewButton(self, row_idx):
        item = self.item(row_idx, 0)
        if not item:
            return
    
        id = item.text()
        billData = BillsController.viewBill(id)

        if billData:
            self.viewWindow = ViewBill(id, billData, billDataHeaders, billDataDatabaseHeaders, mainWindow=self.mainWindow)
            self.viewWindow.show()

    def handleEditButton(self, row_idx):
        item = self.item(row_idx, 0)
        if not item:
            return

        billID = item.text()
        bill = BillsController.viewBill(billID)

        dialog = EditBillForm(
            bill["UnitName"],
            bill["Type"],
            bill["TotalAmount"],
            bill["BillingPeriodStart"],
            bill["BillingPeriodEnd"],
            bill["Status"],
            bill["DueDate"]
        )

        dialog.addButton.setText("Update Bill")
        dialog.addButton.clicked.disconnect()
        dialog.addButton.clicked.connect(lambda: dialog.onEditClicked(billID))

        if dialog.exec():
            self.mainWindow.updatePages()
            self.showSuccessNotification("Bill was updated successfully.")

    def handleDeleteButton(self, row_idx):
        item = self.item(row_idx, 0)
        if not item:
            return
        
        billID = item.text()

        msgBox = QMessageBox(self)
        msgBox.setIcon(QMessageBox.Icon.Warning)
        msgBox.setWindowTitle("Confirm Delete")
        msgBox.setText(f"Are you sure you want to delete Bill '{billID}'?")
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
            success = BillsController.deleteBill(billID)
            if success:
                self.showSuccessNotification(f"Bill '{billID}' was deleted.")
            else:
                self.showErrorNotification(f"Failed to delete Unit '{billID}'.")

            self.mainWindow.updatePages()
    
    def showSuccessNotification(self, message="Bill was successfully added"):
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
    