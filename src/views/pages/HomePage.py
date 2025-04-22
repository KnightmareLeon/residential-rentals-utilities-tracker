from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QSizePolicy
from PyQt6.QtCore import Qt

from src.utils.sampleDataGenerator import generateBillsDataFromUtility
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
        billsData = generateBillsDataFromUtility()

        billsDashboard = BillsDashboard(billsData)

        # bottomRightWidget = QFrame()
        # bottomRightWidget.setStyleSheet("background-color: #1c1c1c; border-radius: 15px")
        # bottomRightWidget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        # bottomRightWidget.setMinimumHeight(200)

        rightLayout.addWidget(billsDashboard)
        # rightLayout.addSpacing(15)
        # rightLayout.addWidget(bottomRightWidget)