from datetime import datetime
from dateutil.relativedelta import relativedelta

from PyQt6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QButtonGroup, QSizePolicy, QListView
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, pyqtSignal

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
from src.utils.constants import categoryColors, billDataHeaders, billDataDatabaseHeaders
from src.views.widgets.CheckableComboBox import CheckableComboBox
from src.views.dialogs.ViewBill import ViewBill
from src.controllers.dashboardController import DashboardController
from src.controllers.billsController import BillsController

class UtilityChartWidget(QFrame):

    def __init__(self, data, title, parent=None, mainWindow=None):
        super().__init__(parent)
        self.mainWindow = mainWindow

        self.currDateOffset = datetime.now()
        self.lastDateOffset = datetime.now() - relativedelta(months=48)
        self.dateRange = "1M"
        self.chartDivisions = 10
        self.rangeButtons = []
        self.plottedPoints = []
        self.utilityFilters = data.keys()
        self.data = data
        self.title = title

        self.setupUI()

        self.annotation = self.ax.annotate("", xy=(0, 0), xytext=(15, 15),
            textcoords="offset points", bbox=dict(boxstyle="round", fc="black", ec="white", lw=0.5),
            fontsize=8, color="white", arrowprops=dict(arrowstyle="->", color="white"))
        self.annotation.set_visible(False)

        self.canvas.mpl_connect("motion_notify_event", self.onHover)

    def setupUI(self):
        layout = QVBoxLayout(self)
        self.setObjectName("UtilityChartWidget")
        self.setStyleSheet("""
                           #UtilityChartWidget {
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
                            border: none;
                            border-radius: 8px;
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

        headerLayout = QHBoxLayout()
        headerLayout.setContentsMargins(0, 0, 0, 15)

        chartTitle = QLabel(self.title)
        chartTitle.setFont(QFont("Urbanist", 14, QFont.Weight.Bold))
        chartTitle.setStyleSheet("color: white;")
        chartTitle.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        chartTitle.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        chartTitle.setWordWrap(True)
        headerLayout.addWidget(chartTitle)
        headerLayout.addStretch()

        self.filterComboBox = CheckableComboBox()
        for label in self.utilityFilters:
            self.filterComboBox.addItem(label)
        self.filterComboBox.onItemCheckedChanged(self.handleFilterUpdate)
        self.filterComboBox.setStyleSheet("""
            QComboBox QAbstractItemView {
                background-color: #4e4e4e;
                color: white;
                font-family: "Urbanist";
                font-size: 16px;
                selection-background-color: #44475a;
                selection-color: white;
                border: none;
                outline: 0;
            }
            QListView::item {
                padding: 5px;
            }
            QListView::item:hover {
                background-color: #44475a;
            }
            QListView::item:selected {
                background-color: #6272a4;
            }
        """)
        self.filterComboBox.setCursor(Qt.CursorShape.PointingHandCursor)
        headerLayout.addWidget(self.filterComboBox)

        self.buttonGroup = QButtonGroup(self)
        self.buttonGroup.setExclusive(True)
        for label in ["3M", "6M", "1Y", "2Y"]:
            btn = QPushButton(label)
            btn.setCheckable(True)
            btn.clicked.connect(self.handleRangeUpdate)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            self.rangeButtons.append(btn)
            self.buttonGroup.addButton(btn)
            headerLayout.addWidget(btn)
        self.rangeButtons[0].setChecked(True)

        layout.addLayout(headerLayout)
        layout.addWidget(self.createChart(self.data))

        # Pagination Controls
        paginationLayout = QHBoxLayout()
        paginationLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        paginationLayout.setSpacing(20)

        self.prevButton = QPushButton("←")
        self.prevButton.setFont(QFont("Urbanist", 12, QFont.Weight.Bold))
        self.prevButton.setFixedSize(32, 32)
        self.prevButton.setCursor(Qt.CursorShape.PointingHandCursor)
        self.prevButton.clicked.connect(self.handlePrevPage)

        self.pageLabel = QLabel(f"{datetime.now().strftime('%B %d, %Y')}")
        self.pageLabel.setFont(QFont("Urbanist", 12, QFont.Weight.Normal))
        self.pageLabel.setStyleSheet("color: white;")
        self.pageLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pageLabel.setFixedWidth(150)

        self.nextButton = QPushButton("→")
        self.nextButton.setFont(QFont("Urbanist", 12, QFont.Weight.Bold))
        self.nextButton.setFixedSize(32, 32)
        self.nextButton.setCursor(Qt.CursorShape.PointingHandCursor)
        self.nextButton.clicked.connect(self.handleNextPage)

        paginationLayout.addWidget(self.prevButton)
        paginationLayout.addWidget(self.pageLabel)
        paginationLayout.addWidget(self.nextButton)
        layout.addLayout(paginationLayout)

        self.handleRangeUpdate()

    def createChart(self, data):
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

        self.updateChart(data)
        self.figure.tight_layout()
        return self.canvas

    def updateChart(self, data):
        self.ax.clear()
        self.plottedPoints = []

        self.ax.margins(x=0.13, y=0.2)

        today = datetime.today()
        months = self.parseDateRangeToMonths(self.dateRange)
        startDate = today - relativedelta(months=months)
        endDate = today

        tickDates = self.generateEvenDateTicks(startDate, endDate, self.chartDivisions)
        tickLabels = [d.strftime("%b %d, %Y") for d in tickDates]
        x = list(range(len(tickDates)))

        # Filter for which utility to display
        filteredCategoryColors = {category: color for category, color in categoryColors.items() if category in self.utilityFilters}

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

                        self.plottedPoints.append((x_val, amount, billDate, category, billID))
                        break

            if x_points:
                if x_points[0] > 0 and reference_y is not None:
                    x_points.insert(0, 0)
                    y_points.insert(0, reference_y)

                self.ax.plot(x_points, y_points, label=category, color=color, marker='o', markersize=4, linewidth=1)

        self.ax.set_xticks(x)
        self.ax.set_xticklabels(tickLabels, rotation=45, fontsize=8, ha="right")
        self.ax.set_ylabel("Cost", color="#FFFFFF")
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

        for x, y, billDate, category, _ in self.plottedPoints:
            dispCoords = self.ax.transData.transform((x, y))
            dist = ((dispCoords[0] - event.x) ** 2 + (dispCoords[1] - event.y) ** 2) ** 0.5
            if dist < displayThreshold and dist < closestDist:
                closestDist = dist
                closestPoint = (x, y, billDate, category)

        if closestPoint:
            x, y, billDate, category = closestPoint
            dateStr = billDate.strftime("%b %d, %Y")

            self.annotation.xy = (x, y)
            self.annotation.set_text(f"{category}\n₱{y:,}\n{dateStr}")
            self.annotation.set_fontsize(8)
            self.annotation.set_visible(True)
            self.annotation.set_position((5, 5))
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

        for x, y, billDate, category, billID in self.plottedPoints:
            dispCoords = self.ax.transData.transform((x, y))
            dist = ((dispCoords[0] - event.x) ** 2 + (dispCoords[1] - event.y) ** 2) ** 0.5
            if dist < displayThreshold and dist < closestDist:
                closestDist = dist
                closestPoint = (x, y, billDate, category, billID)

        if closestPoint:
            x, y, billDate, category, billID = closestPoint

            billData = BillsController.viewBill(billID)
            if billData:
                self.viewWindow = ViewBill(billID, billData, billDataHeaders, billDataDatabaseHeaders, mainWindow=self.mainWindow)
                self.viewWindow.show()

    def generateEvenDateTicks(self, startDate: datetime, endDate: datetime, divisions: int):
        delta = (endDate - startDate) / (divisions - 1)
        return [startDate + i * delta for i in range(divisions)]
    
    def parseDateRangeToMonths(self, range):
        return {"1M": 1, "3M": 3, "6M": 6, "1Y": 12, "2Y": 24}.get(range, 1)

    def handleFilterUpdate(self):
        self.utilityFilters = self.filterComboBox.checkedItems()
        self.updateChart(self.data)

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
        self.currDateOffset = datetime.now()
        self.updatePageLabel()
        self.updateChart(self.data)

    def handlePrevPage(self):
        curr = self.currDateOffset.replace(hour=0, minute=0, second=0, microsecond=0)
        last = self.lastDateOffset.replace(hour=0, minute=0, second=0, microsecond=0)

        if curr > last:
            self.currDateOffset -= relativedelta(months=self.parseDateRangeToMonths(self.dateRange))
            self.updatePageLabel()
            self.updateWidget()

    def handleNextPage(self):
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        current = self.currDateOffset.replace(hour=0, minute=0, second=0, microsecond=0)

        if current < today:
            months = self.parseDateRangeToMonths(self.dateRange)
            self.currDateOffset += relativedelta(months=months)
            self.updatePageLabel()
            self.updateWidget()

    def updatePageLabel(self):
        self.pageLabel.setText(f"{self.currDateOffset.strftime('%B %d, %Y')}")
    
    # Controllers
    def updateWidget(self) -> None:
        months = self.parseDateRangeToMonths(self.dateRange)
        data, lastDateOffset = DashboardController.fetchUtilityDashboard(months, self.currDateOffset)
        self.data = data
        self.lastDateOffset = lastDateOffset
        self.updatePageLabel()
        
        self.updateChart(data)