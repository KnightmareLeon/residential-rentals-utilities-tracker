# file: HomePage.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QSizePolicy
from PyQt6.QtCore import Qt
from src.views.components.UtilityDashboard import UtilityDashboard

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
        mainLayout.addLayout(centerLayout, 5)
        mainLayout.addLayout(rightLayout, 2)

        # === Center Column ===
        dashboard = UtilityDashboard()
        centerLayout.addWidget(dashboard)

        # Simulate another widget below the dashboard
        # belowDashboard = QFrame()
        # belowDashboard.setStyleSheet("background-color: #1c1c1c; border-radius: 15px")
        # belowDashboard.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        # belowDashboard.setMinimumHeight(200)
        # centerLayout.addWidget(belowDashboard)

        # === Right Column ===
        topRightWidget = QFrame()
        topRightWidget.setStyleSheet("background-color: #1c1c1c; border-radius: 15px")
        topRightWidget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        topRightWidget.setMinimumHeight(200)

        bottomRightWidget = QFrame()
        bottomRightWidget.setStyleSheet("background-color: #1c1c1c; border-radius: 15px")
        bottomRightWidget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        bottomRightWidget.setMinimumHeight(200)

        rightLayout.addWidget(topRightWidget)
        rightLayout.addSpacing(15)
        rightLayout.addWidget(bottomRightWidget)