from PyQt6.QtWidgets import QLabel, QHBoxLayout, QVBoxLayout
from PyQt6.QtCore import Qt

from src.views.widgets.BaseViewWidget import BaseViewWidget
from src.views.widgets.UtilityChartWidget import UtilityChartWidget

class ViewUnit(BaseViewWidget):
    def __init__(self, id: str, unitData: dict, unitUtilities: list, unitBillsData: list, headers: list, databaseHeaders: list, parent=None, mainWindow=None):
        super().__init__("Unit Details", parent=parent, iconPath="assets/icons/units.png", mainWindow=mainWindow)
        self.setMinimumSize(1100, 650)
        self.setMaximumSize(1300, 850)

        contentLayout = QHBoxLayout()
        contentLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        contentLayout.setSpacing(30)

        leftLayout = QVBoxLayout()
        leftLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        leftLayout.setSpacing(25)

        unitInfoCard = self.createCard("Unit Information")
        unitInfoLayout = unitInfoCard.layout()
        unitInfoCard.setMaximumHeight(300)
        for i in range(4):
            self.addDetail(unitInfoLayout, headers[i], unitData[databaseHeaders[i]])
        leftLayout.addWidget(unitInfoCard)

        utilitiesCard = self.createCard("Utilities")
        utilitiesLayout = utilitiesCard.layout()
        self.addUtilityDetails(utilitiesLayout, unitUtilities)
        leftLayout.addWidget(utilitiesCard)

        leftLayout.addStretch()

        contentLayout.addLayout(leftLayout)

        billsCard = self.createCard("Unit Bills")
        billsLayout = billsCard.layout()

        chartWidget = UtilityChartWidget(unitBillsData, f"Total Utilities Cost of Unit {id}", mainWindow=mainWindow, dataType="unit", dataID=id)

        billsLayout.addWidget(chartWidget)

        contentLayout.addWidget(billsCard)

        self.mainLayout.addLayout(contentLayout)
