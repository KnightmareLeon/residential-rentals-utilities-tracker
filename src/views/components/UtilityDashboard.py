from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import random

from PyQt6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QButtonGroup, QComboBox
from PyQt6.QtGui import QFont, QPixmap, QIcon
from PyQt6.QtCore import Qt, QSize

from src.utils.sampleDataGenerator import generateRandomUtilityData
from src.views.widgets.UtilityChartWidget import UtilityChartWidget

class UtilityDashboard(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.data = generateRandomUtilityData(
            startDate=datetime(2023, 4, 1),
            endDate=datetime(2025, 4, 22)
        )

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
        data = self.data

        self.chartWidget = UtilityChartWidget(self.data, "Total Utilities Cost of All Units")
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
            ("Total balance of period", "₱ 142,034.12", "assets/icons/totalBalance.png", "balance"),
            ("Total paid in period", "₱ 110,342.00", "assets/icons/totalPaid.png", "paid"),
            ("Unpaid Bills", "7", "assets/icons/unpaidBills.png", "unpaid")
        ]

        for title, value, iconPath, key in cards:
            card, label = self.createSummaryCard(title, value, iconPath)
            layout.addWidget(card)
            self.summaryLabels[key] = label

        return container

    # UPDATES
    def updateSummaryCards(self, balance=None, paid=None, unpaid=None) -> None:
        if balance is not None:
            self.summaryLabels["balance"].setText(balance)
        if paid is not None:
            self.summaryLabels["paid"].setText(paid)
        if unpaid is not None:
            self.summaryLabels["unpaid"].setText(unpaid)

    def updateWidgets(self) -> None:
        self.chartWidget.updateWidget()

        # balance, paid, unpaid = DashboardController.fetchBillsSummary(dataRange, currPage)
        balance, paid, unpaid = ("₱ 40,034.12", "₱ 33,342.00", "6")
        self.updateSummaryCards(balance, paid, unpaid)