from src.views.widgets.BaseViewWidget import BaseViewWidget
from src.views.widgets.UtilityChartWidget import UtilityChartWidget

class BillView(BaseViewWidget):
    def __init__(self, id: str, unitData: dict, unitBillsData: list, headers: list, databaseHeaders: list, parent=None):
        super().__init__("Unit Details", parent=parent, iconPath="assets/icons/units.png")

        unitInfoSection = self.addSection("Unit Information")
        for i in range(4):
            self.addDetail(unitInfoSection, headers[i], unitData[databaseHeaders[i]])
