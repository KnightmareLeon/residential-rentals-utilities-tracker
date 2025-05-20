from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QScrollArea, QPushButton, QFrame, QSizePolicy, QGridLayout
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, pyqtSignal

from src.utils.constants import categoryColors, defaultColor, billDataDatabaseHeaders, billDataHeaders
from src.views.widgets.BillEntry import BillEntry
from src.views.dialogs.ViewBill import ViewBill
from src.controllers.billsController import BillsController
from src.controllers.dashboardController import DashboardController

class BillsDashboard(QWidget):
    viewBills = pyqtSignal()

    def __init__(self, bills, mainWindow = None):
        super().__init__()

        self.mainWindow = mainWindow
        self.bills = bills

        self.setupUI(self.bills)

    def setupUI(self, bills):
        # Container frame to apply background & rounded corners
        container = QFrame()
        container.setObjectName("DashboardContainer")
        container.setStyleSheet("""
            #DashboardContainer {
                background-color: #1C1C1C;
                border-radius: 15px;
                padding: 10px;
            }
        """)
        container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        container.setMinimumWidth(300)

        outerLayout = QVBoxLayout(container)
        outerLayout.setContentsMargins(15, 15, 15, 15)
        outerLayout.setSpacing(10)

        title = QLabel("Urgent Bills")
        title.setFont(QFont("Urbanist", 15, QFont.Weight.Bold))
        title.setStyleSheet("color: white;")
        outerLayout.addWidget(title)

        scrollArea = QScrollArea()
        scrollArea.setWidgetResizable(True)
        scrollArea.setFrameShape(QFrame.Shape.NoFrame)

        contentWidget = QWidget()
        contentWidget.setStyleSheet("background-color: #1C1C1C; border-radius: 10px;")
        self.contentLayout = QVBoxLayout(contentWidget)
        self.contentLayout.setSpacing(0)
        self.contentLayout.setContentsMargins(0, 0, 0, 0)
        self.contentLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        headerLayout = QGridLayout()
        headerLayout.setContentsMargins(5, 10, 5, 10)
        headerLayout.setSpacing(5)

        headerLayout.setColumnStretch(0, 3)  # Type
        headerLayout.setColumnStretch(1, 2)  # Balance
        headerLayout.setColumnStretch(2, 2)  # Due Date
        headerLayout.setColumnStretch(3, 2)  # Status

        headers = ["Type", "Balance", "Due Date", "Status"]
        for i, text in enumerate(headers):
            label = QLabel(text)
            label.setFont(QFont("Urbanist", 10, QFont.Weight.Bold))
            label.setStyleSheet("color: #FFFFFF;")
            headerLayout.addWidget(label, 0, i)

        headerWidget = QWidget()
        headerWidget.setLayout(headerLayout)
        self.contentLayout.addWidget(headerWidget)

        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        line.setStyleSheet("background-color: #444;")
        self.contentLayout.addWidget(line)

        for index, bill in enumerate(self.bills[:15]):
            utility = bill["Type"]
            color = categoryColors.get(utility, defaultColor)
            balance = bill['TotalAmount']
            due = bill["DueDate"]
            status = bill["Status"]

            billEntry = BillEntry(index, utility, color, balance, due, status)
            billEntry.rowClicked.connect(self.handleRowClick) 

            self.contentLayout.addWidget(billEntry)

        scrollArea.setWidget(contentWidget)
        outerLayout.addWidget(scrollArea)

        viewAllButton = QPushButton("View All")
        viewAllButton.setStyleSheet("""
            QPushButton {
                background-color: #2b2b2b;
                font-family: Urbanist;
                font-size: 12px;
                font-weight: bold;
                color: white;
                border: 1px solid #333;
                padding: 10px 25px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #3b3b3b;
            }
        """)
        viewAllButton.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        viewAllButton.setCursor(Qt.CursorShape.PointingHandCursor)
        viewAllButton.clicked.connect(self.viewBills.emit)
        outerLayout.addWidget(viewAllButton)

        # Final layout for this widget
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(container)

    def handleRowClick(self, index):
        self.mainWindow.setStatusBarText("Loading Bill Data....")
        
        clickedBill = self.bills[index]
        billID = clickedBill["BillID"]
        billData = BillsController.viewBill(billID)

        if billData:
            self.viewWindow = ViewBill(billID, billData, billDataHeaders, billDataDatabaseHeaders, mainWindow=self.mainWindow)
            self.viewWindow.show()

    def updateDashboard(self):
        self.clearDashboard()

        self.bills = DashboardController.fetchUpcomingBills()
        
        for index, bill in enumerate(self.bills[:15]):
            utility = bill["Type"]
            color = categoryColors.get(utility, defaultColor)
            balance = bill['TotalAmount']
            due = bill["DueDate"]
            status = bill["Status"]

            billEntry = BillEntry(index=index, utility=utility, color=color, balance=balance, due=due, status=status)
            billEntry.rowClicked.connect(self.handleRowClick)
            self.contentLayout.addWidget(billEntry)
        
        self.contentLayout.addStretch()

    def clearDashboard(self):
        numStaticWidgets = 2

        for i in reversed(range(self.contentLayout.count())):
            if i < numStaticWidgets:
                break

            item = self.contentLayout.itemAt(i)

            if item.widget():
                item.widget().deleteLater()
            else:
                self.contentLayout.removeItem(item)
