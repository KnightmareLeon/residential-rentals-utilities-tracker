from PyQt6.QtWidgets import QLabel, QHBoxLayout, QVBoxLayout, QSizePolicy
from PyQt6.QtCore import Qt

from src.views.widgets.BaseViewWidget import BaseViewWidget
from src.views.widgets.UtilityChartWidget import UtilityChartWidget

class UtilityView(BaseViewWidget):
    def __init__(self, id: str, utilityData: dict, utilityUnits: list, utilityBillsData: list, headers: list, databaseHeaders: list, parent=None):
        super().__init__("Utility Details", parent=parent, iconPath="assets/icons/utilities.png")
        self.setMinimumSize(1075, 600)
        self.setMaximumSize(1300, 850)

        contentLayout = QHBoxLayout()
        contentLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        contentLayout.setSpacing(30)

        leftLayout = QVBoxLayout()
        leftLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        leftLayout.setSpacing(25) 

        utilityInfoCard = self.createCard("Utility Information")
        utilityInfoLayout = utilityInfoCard.layout()
        for i in range(5):
            self.addDetail(utilityInfoLayout, headers[i], utilityData[databaseHeaders[i]])
        leftLayout.addWidget(utilityInfoCard)

        utilityUnitsCard = self.createScrollCard("Units")
        utilityUnitLayout = utilityUnitsCard.widget().layout()
        self.addDetailHeader(utilityUnitLayout, "ID", "Name")
        for i in range(len(utilityUnits)):
            self.addDetail_bold(utilityUnitLayout, utilityUnits[i]["UnitID"], utilityUnits[i]["Name"])
        leftLayout.addWidget(utilityUnitsCard)

        contentLayout.addLayout(leftLayout)

        billInfoSection = self.createCard("Utility Bills")
        billInfoLayout = billInfoSection.layout()
        chartWidget = UtilityChartWidget(utilityBillsData, f"Total Cost of Utility {id}")
        billInfoLayout.addWidget(chartWidget)

        contentLayout.addWidget(billInfoSection)

        self.mainLayout.addLayout(contentLayout)