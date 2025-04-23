from BaseViewWidget import BaseViewWidget
from PyQt6.QtWidgets import QLabel


class UnitViewWidget(BaseViewWidget):
  def __init__(self, unitData: dict, chartWidget=None, parent=None):
    super().__init__("Unit View", parent)

    # Section 1: Unit Details
    infoSection = self.addSection("Unit Details")
    self.addDetail(infoSection, "Unit ID", str(unitData.get("id", "")))
    self.addDetail(infoSection, "Name", unitData.get("name", ""))
    self.addDetail(infoSection, "Type", unitData.get("type", ""))
    self.addDetail(infoSection, "Address", unitData.get("address", ""))

    # Section 2: Unit Costs (chart)
    if chartWidget:
      costSection = self.addSection("Unit Costs")
      self.addWidgetToSection(costSection, chartWidget)
