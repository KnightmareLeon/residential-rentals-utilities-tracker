from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QScrollArea, QPushButton, QFrame, QSizePolicy, QGridLayout
from PyQt6.QtGui import QFont, QColor, QPainter, QBrush
from PyQt6.QtCore import Qt, QSize, pyqtSignal

from src.utils.constants import categoryColors, defaultColor
from src.views.widgets.BillEntry import BillEntry

class BillsDashboard(QWidget):
    def __init__(self, bills):
        super().__init__()

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

        title = QLabel("Upcoming Bills")
        title.setFont(QFont("Urbanist", 15, QFont.Weight.Bold))
        outerLayout.addWidget(title)

        scrollArea = QScrollArea()
        scrollArea.setWidgetResizable(True)
        scrollArea.setFrameShape(QFrame.Shape.NoFrame)

        contentWidget = QWidget()
        contentWidget.setStyleSheet("background-color: #1C1C1C;")
        contentLayout = QVBoxLayout(contentWidget)
        contentLayout.setSpacing(0)
        contentLayout.setContentsMargins(0, 0, 0, 0)
        contentLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        headerLayout = QGridLayout()
        headerLayout.setContentsMargins(5, 10, 5, 10)
        headerLayout.setSpacing(5)

        headers = ["Type", "Balance", "Due Date", "Status"]
        for i, text in enumerate(headers):
            label = QLabel(text)
            label.setFont(QFont("Urbanist", 10))
            label.setStyleSheet("color: #888888;")
            headerLayout.addWidget(label, 0, i)

        headerWidget = QWidget()
        headerWidget.setLayout(headerLayout)
        contentLayout.addWidget(headerWidget)

        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        line.setStyleSheet("background-color: #444;")
        contentLayout.addWidget(line)

        for index, bill in enumerate(self.bills[:15]):
            utility = bill["Type"]
            color = categoryColors.get(utility, defaultColor)
            balance = f"₱{bill['TotalAmount']}"
            due = bill["DueDate"]
            status = bill["Status"]

            billEntry = BillEntry(index, utility, color, balance, due, status)
            billEntry.rowClicked.connect(self.handleRowClick) 

            contentLayout.addWidget(billEntry)

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
        outerLayout.addWidget(viewAllButton)

        # Final layout for this widget
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(container)

    def handleRowClick(self, index):
        clickedBill = self.bills[index]
        print(f"Bill ID: {clickedBill["BillID"]}")

    def updateDashboard(self):
        #fetch new bills
        newBills = [
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

        self.bills = newBills

        self.clearDashboard()

        for index, bill in enumerate(self.bills[:15]):
            utility = bill["Type"]
            color = categoryColors.get(utility, defaultColor)
            balance = f"₱{bill['TotalAmount']}"
            due = bill["DueDate"]
            status = bill["Status"]

            billEntry = BillEntry(utility, color, balance, due, status, index)
            billEntry.rowClicked.connect(self.handleRowClick)
            self.contentLayout.addWidget(billEntry)

    def clearDashboard(self):
        for i in reversed(range(self.contentLayout.count())):
            widget = self.contentLayout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()