from src.views.widgets.BaseViewWidget import BaseViewWidget
from src.views.widgets.UtilityChartWidget import UtilityChartWidget

class UtilityView(BaseViewWidget):
    def __init__(self, id: str, unitData: dict, unitBillsData: list, headers: list, databaseHeaders: list, parent=None):
        super().__init__("Utility Details", parent=parent, iconPath="assets/icons/utilities.png")
        self.setMinimumSize(1075, 650)
        self.setMaximumSize(1300, 850)  

        unitInfoSection = self.addSection("Utility Information")
        for i in range(5):
            self.addDetail(unitInfoSection, headers[i], unitData[databaseHeaders[i]])

        billInfoSection = self.addSection("Utility Bills")
        chartWidget = UtilityChartWidget(unitBillsData, f"Total Cost of Utility {id}")
        self.addWidgetToSection(billInfoSection, chartWidget)