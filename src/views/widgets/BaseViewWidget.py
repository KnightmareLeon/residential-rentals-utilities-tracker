from PyQt6.QtWidgets import (
QWidget, QDialog, QLabel, QVBoxLayout, QHBoxLayout, QFrame, QSizePolicy, QPushButton, QSpacerItem, QGridLayout, QLayout, QScrollArea
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QSize, QDate


class BaseViewWidget(QDialog):
    def __init__(self, mainTitle: str, iconPath: str = None, parent=None,):
        super().__init__(parent)
        self.setWindowIcon(QIcon("assets/logos/logoIcon.png"))
        self.setObjectName("BaseViewWidget")
        self.setWindowTitle(f"UtiliTrack - View {mainTitle}")
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        self.setModal(True)

        self.mainTitle = mainTitle
        self.iconPath = iconPath
        self.sections = []

        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.mainLayout.setContentsMargins(20, 20, 20, 20)
        self.mainLayout.setSpacing(15)

        self.setupTitleBar()

        self.gridLayout = QGridLayout()
        self.gridLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.gridLayout.setSpacing(20)
        self.mainLayout.addLayout(self.gridLayout)

        self.setupBaseStyle()

    def setupTitleBar(self):
        titleLayout = QHBoxLayout()
        titleLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        titleLayout.setSpacing(10)

        iconButton = QPushButton()
        iconButton.setFixedSize(30, 30)
        iconButton.setObjectName("iconButton")
        iconButton.setCursor(Qt.CursorShape.PointingHandCursor)

        if self.iconPath:
            icon = QIcon(self.iconPath)
            iconButton.setIcon(icon)
            iconButton.setIconSize(QSize(24, 24))
        else:
            iconButton.setText("")

        # Title label
        titleLabel = QLabel(self.mainTitle)
        titleLabel.setObjectName("mainTitle")
        titleLabel.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        exitButton = QPushButton(icon=QIcon("assets/icons/exit.png"))
        exitButton.setFixedSize(45, 45)
        exitButton.setObjectName("exitButton")
        exitButton.setCursor(Qt.CursorShape.PointingHandCursor)
        exitButton.clicked.connect(self.handleExitClicked)

        # Add widgets to layout
        titleLayout.addWidget(iconButton)
        titleLayout.addWidget(titleLabel)
        titleLayout.addStretch()
        titleLayout.addWidget(exitButton)

        self.mainLayout.addLayout(titleLayout)

    def setupBaseStyle(self):
        self.setStyleSheet("""
            QWidget#BaseViewWidget {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #131313, 
                    stop: 1 #040404
                );
                padding: 15px;
            }
            QLabel#mainTitle {
                font-family: "Urbanist";
                font-size: 28px;
                font-weight: bold;
                color: white;
            }
            QLabel#sectionTitle {
                font-family: "Urbanist";
                font-size: 20px;
                font-weight: bold;
                color: white;
            }
            QLabel#sectionContent {
                font-family: "Urbanist";
                font-size: 15px;
                color: white;
            }
            QLabel#heading {
                font-family: "Urbanist";
                font-size: 20px;
                font-weight: bold;
                color: white;
            }
            QLabel#label {
                font-family: "Urbanist";
                font-size: 15px;
                color: white;
            }
            QLabel#value {
                font-family: "Urbanist";
                font-size: 15px;
                color: white;
                font-weight: bold;
            }
            QFrame#card {
                background-color: #1C1C1C;
                border-radius: 15px;
                padding: 15px;
            }
            #iconButton {
                border: none;
                background-color: transparent;
            }
            QPushButton#exitButton {
                background-color: #2b2b2b;
                border: none;
                color: white;
                font-size: 30px;
                font-weight: bold;
                border-radius: 6px;
                padding: 5px;
            }
            QPushButton#exitButton:hover {
                background-color: #3b3b3b;
            }
            QLabel#detailHeader {
                font-family: "Urbanist";
                font-size: 14px;
                font-weight: bold;
                color: #777777;
            }
            QScrollBar:vertical {
                background: #2e2e2e;
                width: 12px;
                margin: 0px 0px 0px 0px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background: #888;
                min-height: 20px;
                border-radius: 6px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                background: none;
                height: 0px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
            QScrollBar:horizontal { 
                background: #2e2e2e;
                height: 12px;
                margin: 0px 0px 0px 0px;
                border-radius: 6px;
            }
            QScrollBar::handle:horizontal {
                background: #888;
                min-width: 20px;
                border-radius: 6px;
            }
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                background: none;
                width: 0px;
            }
            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
                background: none;
            }
        """)

    def addWidgetToGrid(self, row: int, column: int, widget: QWidget, rowSpan: int = 1, colSpan: int = 1):
        self.gridLayout.addWidget(widget, row, column, rowSpan, colSpan)

    def createCard(self, title: str = "") -> QFrame:
        card = QFrame()
        card.setObjectName("card")

        layout = QVBoxLayout(card)
        layout.setContentsMargins(10, 10, 10, 10) 
        layout.setSpacing(5)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        if title != "":
            header = QLabel(title)
            header.setObjectName("heading")
            header.setContentsMargins(0, 0, 0, 10)
            header.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

            layout.addWidget(header)

        return card

    def createScrollCard(self, title: str = "") -> QScrollArea:
        card = QFrame()
        card.setObjectName("card")

        layout = QVBoxLayout(card)
        layout.setContentsMargins(10, 10, 10, 10) 
        layout.setSpacing(15)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        if title != "":
            header = QLabel(title)
            header.setObjectName("heading")
            header.setContentsMargins(0, 0, 0, 10)
            header.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

            layout.addWidget(header)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setWidget(card)

        return scroll

    def addDetail(self, layout: QVBoxLayout, label: str, value: str):
        container = QWidget()
        container.setContentsMargins(0, 0, 0, 0)

        hLayout = QHBoxLayout(container)
        hLayout.setContentsMargins(0, 0, 0, 0)
        hLayout.setSpacing(10)

        labelWidget = QLabel(f"{label}:")
        labelWidget.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        labelWidget.setWordWrap(True)
        #labelWidget.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        labelWidget.setContentsMargins(0, 0, 0, 0)
        labelWidget.setObjectName("label")
        labelWidget.setFixedWidth(100)

        if isinstance(value, QDate):
            value = value.toString()

        valueWidget = QLabel(str(value))
        valueWidget.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        valueWidget.setWordWrap(True)
        valueWidget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        valueWidget.setMinimumWidth(120)
        valueWidget.setContentsMargins(0, 0, 0, 0)
        valueWidget.setObjectName("value")
        valueWidget.setCursor(Qt.CursorShape.IBeamCursor)
        valueWidget.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

        if value == "Active":
            valueWidget.setStyleSheet("color: #00FF6F;")
        elif value == "Inactive":
            valueWidget.setStyleSheet("color: #FA1647;")

        hLayout.addWidget(labelWidget)
        hLayout.addWidget(valueWidget)
        layout.addWidget(container)
    
    def addDetail_bold(self, layout: QVBoxLayout, label: str, value: str):
        container = QWidget()
        container.setContentsMargins(0, 0, 0, 0)

        hLayout = QHBoxLayout(container)
        hLayout.setContentsMargins(0, 0, 0, 0)
        hLayout.setSpacing(10)

        labelWidget = QLabel(f"{label}:")
        labelWidget.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        labelWidget.setWordWrap(True)
        labelWidget.setContentsMargins(0, 0, 0, 0)
        labelWidget.setObjectName("value")
        labelWidget.setFixedWidth(100)

        valueWidget = QLabel(str(value))
        valueWidget.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        valueWidget.setWordWrap(True)
        valueWidget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        valueWidget.setContentsMargins(0, 0, 0, 0)
        valueWidget.setObjectName("value")
        valueWidget.setCursor(Qt.CursorShape.IBeamCursor)
        valueWidget.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

        hLayout.addWidget(labelWidget)
        hLayout.addWidget(valueWidget)
        layout.addWidget(container)
    
    def addDetailHeader(self, layout: QVBoxLayout, label1: str, label2: str):
        container = QWidget()
        container.setContentsMargins(0, 0, 0, 0)

        hLayout = QHBoxLayout(container)
        hLayout.setContentsMargins(25, 0, 0, 0)
        hLayout.setSpacing(10)

        label1Widget = QLabel(f"{label1}:")
        label1Widget.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        label1Widget.setWordWrap(True)
        label1Widget.setContentsMargins(0, 0, 0, 0)
        label1Widget.setObjectName("detailHeader")
        label1Widget.setFixedWidth(100)

        label2Widget = QLabel(str(label2))
        label2Widget.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        label2Widget.setWordWrap(True)
        label2Widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        label2Widget.setContentsMargins(0, 0, 0, 0)
        label2Widget.setObjectName("detailHeader")
        label2Widget.setCursor(Qt.CursorShape.IBeamCursor)
        label2Widget.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

        hLayout.addWidget(label1Widget)
        hLayout.addWidget(label2Widget)
        layout.addWidget(container)
 
    def addUtilityDetails(self, layout: QVBoxLayout, utilities: list[dict]):
        headers = ["ID", "Type", "Status", "Shared"]
        headerRow = QHBoxLayout()
        headerRow.setContentsMargins(0, 0, 0, 10)
        headerRow.setSpacing(20)
        headerRow.setAlignment(Qt.AlignmentFlag.AlignTop)

        for index, header in enumerate(headers):
            headerLabel = QLabel(header)
            headerLabel.setObjectName("header")
            headerLabel.setAlignment(Qt.AlignmentFlag.AlignLeft)
            headerLabel.setStyleSheet("font-family: 'Urbanist'; font-size: 14px; font-weight: bold; color: #777777;")
            
            if header == "ID":
                headerLabel.setMinimumWidth(50)
                headerLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            elif header == "Type":
                headerLabel.setMinimumWidth(100)
            elif header == "Status":
                headerLabel.setMinimumWidth(70)
            elif header == "Shared":
                headerLabel.setMinimumWidth(70)

            headerRow.addWidget(headerLabel)
        
        layout.addLayout(headerRow)

        for utility in utilities:
            row = QHBoxLayout()
            row.setSpacing(20)
            row.setAlignment(Qt.AlignmentFlag.AlignTop)

            def addUtilityDetails(label: str, valueText: str):
                container = QWidget()
                pairLayout = QHBoxLayout(container)
                pairLayout.setContentsMargins(0, 0, 0, 0)
                pairLayout.setSpacing(5)

                value = QLabel(str(valueText))
                value.setObjectName("value")
                value.setWordWrap(True)
                value.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
                value.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
                value.setCursor(Qt.CursorShape.IBeamCursor)
                value.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
                value.setMinimumWidth(70)

                if label == "Utility ID":
                    value.setMinimumWidth(50)
                    value.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
                if label == "Type":
                    value.setMinimumWidth(100)
                    value.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
                if value.text() == "Active":
                    value.setStyleSheet("color: #00FF6F;")
                elif value.text() == "Inactive":
                    value.setStyleSheet("color: #FA1647;")
                elif value.text() == "Shared" or value.text() == "Individual":
                    value.setStyleSheet("color: #AAAAAA;")

                pairLayout.addWidget(value)
                row.addWidget(container)

            addUtilityDetails("Utility ID", utility["UtilityID"])
            addUtilityDetails("Type", utility["Type"])
            addUtilityDetails("Status", utility["Status"])
            addUtilityDetails("Shared", "Shared" if utility["isShared"] else "Individual")

            layout.addLayout(row)

    def handleExitClicked(self):
        self.close()