from PyQt6.QtWidgets import QLabel, QHBoxLayout, QVBoxLayout, QSizePolicy, QScrollArea, QFrame
from PyQt6.QtCore import Qt

from src.views.widgets.BaseViewWidget import BaseViewWidget
from src.views.widgets.UtilityChartWidget import UtilityChartWidget

class ViewUtility(BaseViewWidget):
    def __init__(self, id: str, utilityData: dict, utilityUnits: list, utilityBillsData: list, headers: list, databaseHeaders: list, parent=None, mainWindow=None):
        super().__init__("Utility Details", parent=parent, iconPath="assets/icons/utilities.png", mainWindow=mainWindow)
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
        
        utilitiesCard = QFrame()
        utilitiesCard.setObjectName("card")

        utilitiesCardLayout = QVBoxLayout(utilitiesCard)
        utilitiesCardLayout.setContentsMargins(0, 0, 0, 0)
        utilitiesCardLayout.setSpacing(0)
        utilitiesCardLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        header = QLabel("Units")
        header.setObjectName("heading")
        header.setContentsMargins(0, 0, 0, 10)
        header.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        utilitiesCardLayout.addWidget(header)
        self.addDetailHeader(utilitiesCardLayout, "ID", "Name")

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setContentsMargins(0, 0, 0, 0)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
 
        utilityUnitsCard = self.createCard("")
        utilityUnitLayout = utilityUnitsCard.layout()
        #utilityUnitLayout.setContentsMargins(0, 0, 0, 0)
        #utilityUnitLayout.setSpacing(0)
        
        for i in range(len(utilityUnits)):
            self.addDetail_bold(utilityUnitLayout, utilityUnits[i]["UnitID"], utilityUnits[i]["Name"])

        scroll.setWidget(utilityUnitsCard)
        utilitiesCardLayout.addWidget(scroll)
        utilitiesCardLayout.addStretch()

        leftLayout.addWidget(utilitiesCard)
        contentLayout.addLayout(leftLayout)

        billInfoSection = self.createCard("Utility Bills")
        billInfoLayout = billInfoSection.layout()
        chartWidget = UtilityChartWidget(utilityBillsData, f"Total Cost of Utility {id}", mainWindow=mainWindow, dataType="utility", dataID=id)
        billInfoLayout.addWidget(chartWidget)

        contentLayout.addWidget(billInfoSection)

        self.mainLayout.addLayout(contentLayout)
        