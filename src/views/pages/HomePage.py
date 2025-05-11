from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QSizePolicy, QPushButton, QMessageBox
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QSize

from src.utils.sampleDataGenerator import generateBillsDataFromUtility
from src.views.components.UtilityDashboard import UtilityDashboard
from src.views.components.BillsDashboard import BillsDashboard
from src.views.dialogs.AddBillForm import AddBillForm
from src.controllers.billsController import BillsController

class HomePage(QWidget):
    def __init__(self, parent=None, mainWindow=None):
        super().__init__(parent)
        self.mainWindow = mainWindow
        self.setupUI()

    def setupUI(self):
        mainLayout = QHBoxLayout()
        mainLayout.setContentsMargins(15, 20, 15, 20)
        mainLayout.setSpacing(15)
        self.setLayout(mainLayout)

        centerLayout = QVBoxLayout()
        centerLayout.setContentsMargins(0, 0, 0, 0)
        centerLayout.setSpacing(15)
        rightLayout = QVBoxLayout()
        mainLayout.addLayout(centerLayout, 4)
        mainLayout.addLayout(rightLayout, 2)

        # === Center Column ===
        self.utilityDashboard = UtilityDashboard(mainWindow=self.mainWindow)
        centerLayout.addWidget(self.utilityDashboard)

        # === Right Column ===
        billsData = generateBillsDataFromUtility()

        billsDashboard = BillsDashboard(billsData, self.mainWindow)
        billsDashboard.viewBills.connect(self.openBillsPage)

        bottomRightWidget = QFrame()
        bottomRightWidget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        bottomRightWidget.setFixedHeight(60)

        bottomRightLayout = QVBoxLayout(bottomRightWidget)
        bottomRightLayout.setContentsMargins(0, 0, 0, 0)
        bottomRightLayout.setSpacing(0)

        buttonLayout = QHBoxLayout() 

        addBillButton = QPushButton("Add Bill")
        addBillButton.setIcon(QIcon("assets/icons/bills.png"))
        addBillButton.setIconSize(QSize(24, 24))
        addBillButton.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        addBillButton.setCursor(Qt.CursorShape.PointingHandCursor)

        addBillButton.clicked.connect(self.handleAddBillButton)
        addBillButton.setStyleSheet("""
        QPushButton {
            background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #3500B0, stop:1 #9900A7);
            color: white;
            font-family: "Urbanist";
            font-size: 18px;
            font-weight: bold;
            padding: 6px 12px;
            border-radius: 12px;
        }
        QPushButton:hover {
            background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #4600E9, stop:1 #E200F7);
        }
        """)

        buttonLayout.addWidget(addBillButton)
        bottomRightLayout.addLayout(buttonLayout)

        rightLayout.addWidget(bottomRightWidget)
        rightLayout.addSpacing(5)
        rightLayout.addWidget(billsDashboard)
    
    def openBillsPage(self):
        self.mainWindow.updatePage(self.mainWindow.billsPage, self.mainWindow.billsButton, "Bills")
    
    def updateDashboards(self):
        self.utilityDashboard.updateWidgets()

    def handleAddBillButton(self):
        dialog = AddBillForm()
        if dialog.exec():
            billData = dialog.getFormData()
            if billData:
                unitID = billData["Unit"]
                utilityID = billData["Utility Type"]
                totalAmount = billData["Total Amount"]
                billPeriodStart = billData["Billing Period Start"]
                billPeriodEnd = billData["Billing Period End"]
                status = billData["Status"]
                dueDate = billData["Due Date"]

                response = BillsController.addBill(unitID, utilityID, totalAmount, billPeriodStart, billPeriodEnd, status, dueDate)
                
                if response:
                    self.mainWindow.updatePages()
                    self.showSuccessNotification()
    
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
            font-family: "Urbanist";
            font-size: 16px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #666666;
        }
        """)

        msgBox.exec()