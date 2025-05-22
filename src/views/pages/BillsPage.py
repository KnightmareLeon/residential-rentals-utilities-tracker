from PyQt6.QtWidgets import QMessageBox

from src.views.widgets.BasePageWidget import BasePageWidget
from src.views.components.BillsTable import BillsTable
from src.views.dialogs.AddBillForm import AddBillForm

class BillsPage(BasePageWidget):
    def __init__(self, mainWindow=None):
        self.buttonText = "Add Bill"
        super().__init__(BillsTable, self.buttonText, mainWindow=mainWindow)

        self.table.initializeSort()

    def updatePage(self):
        self.table.updateTable()

    def handleAddButton(self):
        dialog = AddBillForm()
        
        if dialog.exec():
            self.mainWindow.updatePages()
            self.mainWindow.setStatusBarText("Bill added succesfully.")
            self.showSuccessNotification()
    
    def showSuccessNotification(self):
        msgBox = QMessageBox(self)
        msgBox.setIcon(QMessageBox.Icon.Information)
        msgBox.setWindowTitle("Success")
        msgBox.setText("Bill was successfully added")

        # Force non-native dialog so styles apply
        msgBox.setOption(QMessageBox.Option.DontUseNativeDialog, True)

        # Example stylesheet (dark mode)
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
    