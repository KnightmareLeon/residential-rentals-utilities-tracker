from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import random

from PyQt6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QButtonGroup
from PyQt6.QtGui import QFont, QPixmap, QIcon
from PyQt6.QtCore import Qt, QSize

import matplotlib.pyplot as plt
plt.rcParams['font.family'] = "Montserrat"
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from src.utils.formatMoney import formatMoneyNoDecimal, formatMoney
from src.utils.sampleDataGenerator import generateRandomUtilityData

class UtilityDashboard(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.dateRange = "1M"
        self.chartDivisions = 10
        self.rangeButtons = []

        self.setupUI()

    def setupUI(self):
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
                            color: 'white';
                           }

                           QPushButton:hover {
                            background-color: #3E3E3E;
                           }
                           """)

        # === Summary Cards ===
        summaryLayout = QHBoxLayout()

        summaryLayout.addWidget(self.createSummaryWidget())

        mainLayout.addLayout(summaryLayout)

        # === Chart Header ===
        chartHeader = QHBoxLayout()
        chartTitle = QLabel("Total Utilities Cost of All Units")
        chartTitle.setFont(QFont("Urbanist", 16, QFont.Weight.Bold))
        chartHeader.addWidget(chartTitle)

        chartHeader.addStretch()

        self.rangeButtons = []
        self.buttonGroup = QButtonGroup(self)
        self.buttonGroup.setExclusive(True)

        for label in ["3M", "6M", "1Y", "2Y"]:
            btn = QPushButton(label)
            btn.setCheckable(True)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            self.rangeButtons.append(btn)
            self.buttonGroup.addButton(btn)
            btn.clicked.connect(self.handleRangeUpdate)
            chartHeader.addWidget(btn)

        self.rangeButtons[0].setChecked(True)

        mainLayout.addLayout(chartHeader)

        # === Matplotlib Chart ===
        data = generateRandomUtilityData(
            startDate=datetime(2024, 4, 1),
            endDate=datetime(2025, 4, 19)
        )

        canvas = self.createChart(data)
        mainLayout.addWidget(canvas)

        self.handleRangeUpdate()

    # SUMMARY CARDS
    def createSummaryCard(self, title, value, iconPath):
        frame = QFrame()
        frame.setFrameShape(QFrame.Shape.StyledPanel)

        mainLayout = QHBoxLayout()
        mainLayout.setContentsMargins(0, 10, 0, 0)
        frame.setLayout(mainLayout)

        iconButton = QPushButton()
        icon = QIcon(iconPath)
        iconButton.setIcon(icon)
        iconButton.setIconSize(QSize(40, 40))  
        iconButton.setFixedSize(40, 40)
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
    
    def createSummaryWidget(self):
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

    # CHART
    def generateEvenDateTicks(self, startDate: datetime, endDate: datetime, divisions: int):
        delta = (endDate - startDate) / (divisions - 1)
        return [startDate + i * delta for i in range(divisions)]

    def praseDateRange(self, range):
        if range == "1M":
            return 1
        elif range == "3M":
            return 3
        elif range == "6M":
            return 6
        elif range == "1Y":
            return 12
        elif range == "2Y":
            return 24

    def createChart(self, data):
        self.figure = Figure(figsize=(7, 5))
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setMinimumSize(400, 300)
        self.ax = self.figure.add_subplot(111)

        self.canvas.setStyleSheet("background-color: #1C1C1C; border: none;")
        self.figure.patch.set_facecolor('#1C1C1C')
        self.ax.set_facecolor('#1C1C1C')                
        self.ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.5, color="#333333")
        for spine in self.ax.spines.values():
            spine.set_color('#333333')
        self.ax.tick_params(colors='#CCCCCC')
        self.ax.yaxis.label.set_color('#CCCCCC')
        self.ax.xaxis.label.set_color('#CCCCCC')
        self.ax.title.set_color('#FFFFFF')

        self.updateChart(data)
        self.figure.tight_layout()
        return self.canvas
    
    def updateChart(self, data):
        self.ax.clear()

        self.ax.set_facecolor('#1C1C1C')                
        self.ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.5, color="#333333")
        for spine in self.ax.spines.values():
            spine.set_color('#333333')
        self.ax.tick_params(colors='#CCCCCC')
        self.ax.yaxis.label.set_color('#CCCCCC')
        self.ax.xaxis.label.set_color('#CCCCCC')
        self.ax.title.set_color('#FFFFFF')

        today = datetime.today()
        months = self.praseDateRange(self.dateRange)
        startDate = today - relativedelta(months=months)
        endDate = today

        tickDates = self.generateEvenDateTicks(startDate, endDate, self.chartDivisions)
        tickLabels = [d.strftime("%b %d, %Y") for d in tickDates]
        x = list(range(len(tickDates)))

        categoryColors = {
            "Electricity": "#FFA500",
            "Water": "#00BFFF",
            "Gas": "#FF1493",
            "Wifi": "#00FF7F",
            "Trash": "#A52A2A",
            "Maintenance": "#9370DB",
            "Miscellaneous": "#CCCCCC"
        }

        for category, color in categoryColors.items():
            bills = [
                (datetime.strptime(entry["BillingPeriodEnd"], "%Y-%m-%d").date(), int(entry["TotalAmount"]))
                for entry in data.get(category, [])
            ]
            bills.sort()

            x_points = []
            y_points = []

            for billDate, amount in bills:
                for i in range(len(tickDates) - 1):
                    start = tickDates[i].date()
                    end = tickDates[i + 1].date()

                    if start <= billDate < end:
                        totalSpace = (end - start).days
                        offset = (billDate - start).days / totalSpace if totalSpace > 0 else 0
                        x_val = i + offset

                        x_points.append(x_val)
                        y_points.append(amount)
                        break

            if x_points:
                self.ax.plot(x_points, y_points, label=category, color=color)

        self.ax.set_xticks(x)
        self.ax.set_xticklabels(tickLabels, rotation=45, fontsize=8, ha="right")
        self.ax.set_ylabel("Cost")
        self.ax.set_title("")

        self.ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: formatMoneyNoDecimal(x)))
        self.ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.35), ncol=4, framealpha=0, labelcolor="white")

        self.canvas.draw()

    def handleRangeUpdate(self):
        for btn in self.rangeButtons:
            if btn.isChecked():
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #EEEEEE;
                        color: #211621;
                        border-radius: 8px;
                        padding: 6px 12px;
                        font-weight: bold;
                        border: none;
                        border-radius: 5px;
                        padding: 10px 15px;
                        margin: 0px 5px;
                        font-family: "Urbanist", sans-serif;
                        font-size: 14px;
                    }
                """)
                self.dateRange = btn.text()
            else:
                btn.setChecked(False)
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #303030;
                        color: #BFBFBF;
                        border: none;
                        padding: 6px 12px;
                        font-weight: normal;
                        border: none;
                        border-radius: 5px;
                        padding: 10px 15px;
                        margin: 0px 5px;
                        font-family: "Urbanist", sans-serif;
                        font-size: 14px;
                    }
                    QPushButton:hover {
                        background-color: #3E3E3E;
                    }
                """)

        self.updateWidget()

    # UPDATES
    def updateSummaryCards(self, balance=None, paid=None, unpaid=None):
        if balance is not None:
            self.summaryLabels["balance"].setText(balance)
        if paid is not None:
            self.summaryLabels["paid"].setText(paid)
        if unpaid is not None:
            self.summaryLabels["unpaid"].setText(unpaid)

    def updateWidget(self):
        dataRange = self.praseDateRange(self.dateRange)
        print(f"Fetching data for {dataRange} months")
        # fetch chart data
        data = generateRandomUtilityData(
            startDate=datetime(2024, 4, 1),
            endDate=datetime(2025, 4, 19)
        )
        self.updateChart(data)

        #fetch summary data
        balance, paid, unpaid = ("₱ 40,034.12", "₱ 33,342.00", "6")
        self.updateSummaryCards(balance, paid, unpaid)

