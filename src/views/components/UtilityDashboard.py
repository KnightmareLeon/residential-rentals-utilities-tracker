from PyQt6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QButtonGroup, QComboBox
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import Qt, QSize, QDate
from datetime import datetime

from src.views.widgets.UtilitySumChartWidget import UtilitySumChartWidget
from src.controllers.dashboardController import DashboardController

class UtilityDashboard(QFrame):
    def __init__(self, parent=None, mainWindow=None):
        super().__init__(parent)
        self.mainWindow = mainWindow

        self.setupUI()

    def setupUI(self) -> None:
        mainLayout = QVBoxLayout()
        self.setLayout(mainLayout)
        self.setObjectName("UtilityDashboard")

        self.setStyleSheet("""
                           #UtilityDashboard {
                            background-color: #1C1C1C;
                            border-radius: 15px;
                            padding: 5px 20px 0px 20px;
                           }
                           QLabel {
                            font-family: "Urbanist", sans-serif;
                           }

                           QPushButton {
                            background-color: #303030;
                            border: none;
                            color: 'white';
                            border-radius: 5px;
                           }

                           QPushButton:hover {
                            background-color: #3E3E3E;
                           }

                           QComboBox {
                            background-color: #1C1C1C;
                            color: white;
                            border: 2px solid #3E3E3E;
                            padding: 10px 15px;
                            border-radius: 10px;
                            font-family: "Urbanist", sans-serif;
                            font-size: 14px;
                           }
                           """)

        # === Summary Cards ===
        summaryLayout = QHBoxLayout()
        summaryLayout.addWidget(self.createSummaryWidget())
        mainLayout.addLayout(summaryLayout)

        # === Utility Chart ===
        data, _ = DashboardController.fetchUtilityDashboard(3, datetime.now())
        self.chartWidget = UtilitySumChartWidget(data, "Total Utilities Cost of All Units", utilityDashboard=self, mainWindow=self.mainWindow)
        mainLayout.addWidget(self.chartWidget)

        self.chartWidget.handleRangeUpdate()

    # SUMMARY CARDS
    def createSummaryCard(self, title: str, value: str, iconPath: str) -> tuple[QFrame, QLabel]:
        frame = QFrame()
        frame.setFrameShape(QFrame.Shape.StyledPanel)

        mainLayout = QHBoxLayout()
        mainLayout.setContentsMargins(0, 10, 0, 0)
        frame.setLayout(mainLayout)

        iconButton = QPushButton()
        icon = QIcon(iconPath)
        iconButton.setIcon(icon)
        iconButton.setIconSize(QSize(35, 35))  
        iconButton.setFixedSize(35, 35)
        iconButton.setStyleSheet("""
            QPushButton {
                border: none;
                background: transparent;
            }
            QPushButton:focus {
                outline: none;
            }
        """)

        textLayout = QVBoxLayout()
        labelTitle = QLabel(title)
        labelTitle.setStyleSheet("color: gray;")
        labelTitle.setFont(QFont("Urbanist", 10, QFont.Weight.Medium))

        labelValue = QLabel(value)
        labelValue.setStyleSheet("color: white;")
        labelValue.setFont(QFont("Urbanist", 15, QFont.Weight.Bold))

        textLayout.addWidget(labelTitle)
        textLayout.addWidget(labelValue)

        mainLayout.addWidget(iconButton)
        mainLayout.addLayout(textLayout)

        return frame, labelValue
    
    def createSummaryWidget(self)-> None:
        container = QFrame()
        layout = QHBoxLayout()
        container.setLayout(layout)

        self.summaryLabels = {}  # Store value labels here

        cards = [
            ("Total Cost of period", "", "assets/icons/totalBalance.png", "balance"),
            ("Total Unpaid in period", "", "assets/icons/totalPaid.png", "paid"),
            ("Unpaid Bills", "", "assets/icons/unpaidBills.png", "unpaid")
        ]

        for title, value, iconPath, key in cards:
            card, label = self.createSummaryCard(title, value, iconPath)
            layout.addWidget(card)
            self.summaryLabels[key] = label

        return container

    # UPDATES
    def updateSummaryCards(self, totalCost=None, totalUnpaid=None, unpaidBills=None) -> None:
        if totalCost is not None:
            self.summaryLabels["balance"].setText(totalCost)
        if totalUnpaid is not None:
            self.summaryLabels["paid"].setText(totalUnpaid)
        if unpaidBills is not None:
            self.summaryLabels["unpaid"].setText(unpaidBills)

    def updateWidgets(self) -> None:
        self.chartWidget.updateWidget()

        monthRange = self.chartWidget.parseDateRangeToMonths(self.chartWidget.dateRange)
        offset = self.chartWidget.currDateOffset

        totalUnpaid, totalCost, unpaidBills = DashboardController.fetchBillsSummary(monthRange, offset)
        self.updateSummaryCards(totalCost, totalUnpaid, unpaidBills)
