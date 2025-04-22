from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import random

from PyQt6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QButtonGroup, QComboBox
from PyQt6.QtGui import QFont, QPixmap, QIcon
from PyQt6.QtCore import Qt, QSize

import matplotlib.pyplot as plt
from matplotlib import font_manager

urbanistFontPath = "assets/fonts/Urbanist-VariableFont_wght.ttf"
font_manager.fontManager.addfont(urbanistFontPath)

montserratFontPath = "assets/fonts/Montserrat-VariableFont_wght.ttf"
font_manager.fontManager.addfont(montserratFontPath)

urbanistFont = font_manager.FontProperties(fname=urbanistFontPath)
montserratFont = font_manager.FontProperties(fname=montserratFontPath)
plt.rcParams['font.family'] = [urbanistFont.get_name(), montserratFont.get_name()]

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from src.utils.formatMoney import formatMoneyNoDecimal, formatMoney
from src.utils.constants import categoryColors
from src.utils.sampleDataGenerator import generateRandomUtilityData
from src.views.widgets.CheckableComboBox import CheckableComboBox
from src.controllers.dashboardController import DashboardController

class UtilityDashboard(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.dateRange = "1M"
        self.chartDivisions = 10
        self.rangeButtons = []
        self.plottedPoints = []
        self.utilityFilters = ["Electricity", "Water", "Gas", "Wifi", "Trash", "Maintenance"]
        self.data = generateRandomUtilityData(
            startDate=datetime(2023, 4, 1),
            endDate=datetime(2025, 4, 22)
        )

        self.setupUI()

        self.annotation = self.ax.annotate("", xy=(0, 0), xytext=(15, 15),
            textcoords="offset points", bbox=dict(boxstyle="round", fc="black", ec="white", lw=0.5),
            fontsize=8, color="white", arrowprops=dict(arrowstyle="->", color="white"))
        self.annotation.set_visible(False)

        self.canvas.mpl_connect("motion_notify_event", self.onHover)

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
                            color: 'white';
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

        # === Chart Header ===
        chartHeader = QHBoxLayout()
        chartTitle = QLabel("Total Utilities Cost of All Units")
        chartTitle.setFont(QFont("Urbanist", 16, QFont.Weight.Bold))
        chartHeader.addWidget(chartTitle)

        chartHeader.addStretch()

        self.rangeButtons = []
        self.buttonGroup = QButtonGroup(self)
        self.buttonGroup.setExclusive(True)

        self.filterComboBox = CheckableComboBox()
        self.filterComboBox.addItem("Electricity")
        self.filterComboBox.addItem("Water")
        self.filterComboBox.addItem("Gas")
        self.filterComboBox.addItem("Wifi")
        self.filterComboBox.addItem("Trash")
        self.filterComboBox.addItem("Maintenance")
        self.filterComboBox.onItemCheckedChanged(self.handleFilterUpdate)
        self.filterComboBox.setCursor(Qt.CursorShape.PointingHandCursor)

        chartHeader.addWidget(self.filterComboBox)

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
        data = self.data

        canvas = self.createChart(data)
        mainLayout.addWidget(canvas)

        self.handleRangeUpdate()

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

    # CHART
    def generateEvenDateTicks(self, startDate: datetime, endDate: datetime, divisions: int):
        delta = (endDate - startDate) / (divisions - 1)
        return [startDate + i * delta for i in range(divisions)]

    def parseDateRangeToMonths(self, range: str) -> int:
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

    def createChart(self, data: dict[str, list[dict[str, str]]]):
        self.figure = Figure(figsize=(7, 5))
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setMinimumSize(400, 200)
        self.canvas.mpl_connect("button_press_event", self.onChartClick)
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

        self.updateChart(data, self.utilityFilters)
        self.figure.tight_layout()
        return self.canvas
    
    def updateChart(self, data, utilityFilters: list[str]) -> None:
        self.ax.clear()
        self.plottedPoints = []

        self.ax.set_facecolor('#1C1C1C')                
        self.ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.5, color="#333333")
        for spine in self.ax.spines.values():
            spine.set_color('#333333')
        self.ax.tick_params(colors='#CCCCCC')
        self.ax.yaxis.label.set_color('#CCCCCC')
        self.ax.xaxis.label.set_color('#CCCCCC')
        self.ax.title.set_color('#FFFFFF')

        self.ax.margins(x=0.13, y=0.2)

        today = datetime.today()
        months = self.parseDateRangeToMonths(self.dateRange)
        startDate = today - relativedelta(months=months)
        endDate = today

        tickDates = self.generateEvenDateTicks(startDate, endDate, self.chartDivisions)
        tickLabels = [d.strftime("%b %d, %Y") for d in tickDates]
        x = list(range(len(tickDates)))

        # Filter for which utility to display
        filteredCategoryColors = {category: color for category, color in categoryColors.items() if category in utilityFilters}

        for category, color in filteredCategoryColors.items():
            bills = [
                (
                    datetime.strptime(entry["BillingPeriodEnd"], "%Y-%m-%d").date(),
                    int(entry["TotalAmount"]),
                    entry["BillID"]
                )
                for entry in data.get(category, [])
            ]
            bills.sort()

            x_points = []
            y_points = []

            reference_y = None
            for billDate, amount, _ in reversed(bills):
                if billDate < tickDates[0].date():
                    reference_y = amount
                    break

            for billDate, amount, billID in bills:
                for i in range(len(tickDates) - 1):
                    start = tickDates[i].date()
                    end = tickDates[i + 1].date()

                    if start <= billDate < end:
                        totalSpace = (end - start).days
                        offset = (billDate - start).days / totalSpace if totalSpace > 0 else 0
                        x_val = i + offset

                        x_points.append(x_val)
                        y_points.append(amount)

                        label = tickDates[i].strftime("%b %d, %Y")
                        self.plottedPoints.append((x_val, amount, label, category, billID))
                        break

            if x_points:
                if x_points[0] > 0 and reference_y is not None:
                    x_points.insert(0, 0)
                    y_points.insert(0, reference_y)

                self.ax.plot(x_points, y_points, label=category, color=color)

        self.ax.set_xticks(x)
        self.ax.set_xticklabels(tickLabels, rotation=45, fontsize=8, ha="right")
        self.ax.set_ylabel("Cost")
        self.ax.set_title("")

        self.ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: formatMoneyNoDecimal(x)))
        self.ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.35), ncol=4, framealpha=0, labelcolor="white")

        # Adding the annotation for hover effect
        self.annotation = self.ax.annotate("", xy=(0, 0), xytext=(15, 15),
            textcoords="offset points",
            bbox=dict(boxstyle="round", fc="black", ec="white", lw=0.5),
            fontsize=8, color="white",
            arrowprops=dict(arrowstyle="->", color="white"))
        self.annotation.set_visible(False)
        self.annotation.set_clip_on((False))

        self.canvas.draw()

    def onHover(self, event):
        if not event.inaxes:
            self.annotation.set_visible(False)
            self.canvas.draw_idle()
            return

        # Set a small hover threshold in display coords
        displayThreshold = 12  # pixels
        closestPoint = None
        closestDist = float("inf")

        for x, y, label, category, _ in self.plottedPoints:
            dispCoords = self.ax.transData.transform((x, y))
            dist = ((dispCoords[0] - event.x) ** 2 + (dispCoords[1] - event.y) ** 2) ** 0.5
            if dist < displayThreshold and dist < closestDist:
                closestDist = dist
                closestPoint = (x, y, label, category)

        if closestPoint:
            x, y, label, category = closestPoint
            self.annotation.xy = (x, y)
            self.annotation.set_text(f"{category}\n₱{y:,}\n{label}")
            self.annotation.set_visible(True)
            self.canvas.draw_idle()
        else:
            self.annotation.set_visible(False)
            self.canvas.draw_idle()

    def onChartClick(self, event):
        if event.inaxes != self.ax:
            return
        
        displayThreshold = 12  # pixels
        closestPoint = None
        closestDist = float("inf")

        for x, y, label, category, billID in self.plottedPoints:
            dispCoords = self.ax.transData.transform((x, y))
            dist = ((dispCoords[0] - event.x) ** 2 + (dispCoords[1] - event.y) ** 2) ** 0.5
            if dist < displayThreshold and dist < closestDist:
                closestDist = dist
                closestPoint = (x, y, label, category, billID)

        if closestPoint:
            x, y, label, category, billID = closestPoint
            print(f"Clicked on: BillID={billID}, Category='{category}', Amount={y}, Date={label}")

    def handleRangeUpdate(self) -> None:
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
    def updateSummaryCards(self, balance=None, paid=None, unpaid=None) -> None:
        if balance is not None:
            self.summaryLabels["balance"].setText(balance)
        if paid is not None:
            self.summaryLabels["paid"].setText(paid)
        if unpaid is not None:
            self.summaryLabels["unpaid"].setText(unpaid)

    def updateWidget(self) -> None:
        dataRange = self.parseDateRangeToMonths(self.dateRange)
        #self.data = DashboardController.fetchUtilityDashboard(dataRange)
        data = self.data
        self.updateChart(data, self.utilityFilters)

        balance, paid, unpaid = DashboardController.fetchBillsSummary(dataRange)
        balance, paid, unpaid = ("₱ 40,034.12", "₱ 33,342.00", "6")
        self.updateSummaryCards(balance, paid, unpaid)

    def handleFilterUpdate(self):
        self.utilityFilters = self.filterComboBox.checkedItems()
        self.updateWidget()