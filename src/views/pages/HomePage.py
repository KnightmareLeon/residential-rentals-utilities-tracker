from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QSizePolicy
from PyQt6.QtCore import Qt

from src.views.components.UtilityDashboard import UtilityDashboard
from src.views.components.BillsDashboard import BillsDashboard

class HomePage(QWidget):
    def __init__(self, parent=None, mainWindow=None):
        super().__init__(parent)
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
        utilityDashboard = UtilityDashboard()
        centerLayout.addWidget(utilityDashboard)

        # === Right Column ===
        billsData = [
        {
            "BillID": 1,
            "Type": "Electricity",
            "TotalAmount": "6021.90",
            "DueDate": "Mar 30",
            "Status": "Overdue"
        },
        {
            "BillID": 2,
            "Type": "Water",
            "TotalAmount": "1245.75",
            "DueDate": "Apr 05",
            "Status": "Unpaid"
        },
        {
            "BillID": 3,
            "Type": "Wifi",
            "TotalAmount": "1899.00",
            "DueDate": "Apr 02",
            "Status": "Paid"
        },
        {
            "BillID": 4,
            "Type": "Electricity",
            "TotalAmount": "5487.30",
            "DueDate": "Mar 28",
            "Status": "Overdue"
        },
        {
            "BillID": 5,
            "Type": "Water",
            "TotalAmount": "1320.50",
            "DueDate": "Apr 10",
            "Status": "Unpaid"
        },
        {
            "BillID": 6,
            "Type": "Wifi",
            "TotalAmount": "1799.00",
            "DueDate": "Apr 01",
            "Status": "Paid"
        },
        {
            "BillID": 7,
            "Type": "Electricity",
            "TotalAmount": "6100.00",
            "DueDate": "Apr 06",
            "Status": "Unpaid"
        },
        {
            "BillID": 8,
            "Type": "Water",
            "TotalAmount": "1100.80",
            "DueDate": "Apr 09",
            "Status": "Unpaid"
        },
        {
            "BillID": 9,
            "Type": "Wifi",
            "TotalAmount": "1999.00",
            "DueDate": "Apr 03",
            "Status": "Overdue"
        },
        {
            "BillID": 10,
            "Type": "Electricity",
            "TotalAmount": "5890.45",
            "DueDate": "Apr 08",
            "Status": "Unpaid"
        },
        {
            "BillID": 11,
            "Type": "Water",
            "TotalAmount": "1185.60",
            "DueDate": "Apr 07",
            "Status": "Paid"
        },
        {
            "BillID": 1,
            "Type": "Electricity",
            "TotalAmount": "6021.90",
            "DueDate": "Mar 30",
            "Status": "Overdue"
        },
        {
            "BillID": 2,
            "Type": "Water",
            "TotalAmount": "1245.75",
            "DueDate": "Apr 05",
            "Status": "Unpaid"
        },
        {
            "BillID": 3,
            "Type": "Wifi",
            "TotalAmount": "1899.00",
            "DueDate": "Apr 02",
            "Status": "Paid"
        },
        {
            "BillID": 4,
            "Type": "Electricity",
            "TotalAmount": "5487.30",
            "DueDate": "Mar 28",
            "Status": "Overdue"
        },
        {
            "BillID": 5,
            "Type": "Water",
            "TotalAmount": "1320.50",
            "DueDate": "Apr 10",
            "Status": "Unpaid"
        },
        {
            "BillID": 6,
            "Type": "Wifi",
            "TotalAmount": "1799.00",
            "DueDate": "Apr 01",
            "Status": "Paid"
        },
        {
            "BillID": 7,
            "Type": "Electricity",
            "TotalAmount": "6100.00",
            "DueDate": "Apr 06",
            "Status": "Unpaid"
        },
        {
            "BillID": 8,
            "Type": "Water",
            "TotalAmount": "1100.80",
            "DueDate": "Apr 09",
            "Status": "Unpaid"
        },
        {
            "BillID": 9,
            "Type": "Wifi",
            "TotalAmount": "1999.00",
            "DueDate": "Apr 03",
            "Status": "Overdue"
        },
        {
            "BillID": 10,
            "Type": "Electricity",
            "TotalAmount": "5890.45",
            "DueDate": "Apr 08",
            "Status": "Unpaid"
        },
        {
            "BillID": 11,
            "Type": "Water",
            "TotalAmount": "1185.60",
            "DueDate": "Apr 07",
            "Status": "Paid"
        }
    ]


        billsDashboard = BillsDashboard(billsData)

        # bottomRightWidget = QFrame()
        # bottomRightWidget.setStyleSheet("background-color: #1c1c1c; border-radius: 15px")
        # bottomRightWidget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        # bottomRightWidget.setMinimumHeight(200)

        rightLayout.addWidget(billsDashboard)
        # rightLayout.addSpacing(15)
        # rightLayout.addWidget(bottomRightWidget)