from PyQt6.QtWidgets import (
QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame, QSizePolicy, QPushButton, QSpacerItem
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QSize


class BaseViewWidget(QWidget):
    def __init__(self, mainTitle: str, iconPath: str = None, parent=None,):
        super().__init__(parent)
        self.setObjectName("BaseViewWidget")
        self.setWindowTitle("UtiliTrack - View Details")
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)

        self.mainTitle = mainTitle
        self.iconPath = iconPath
        self.sections = []

        # Setup main layout
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.mainLayout.setContentsMargins(20, 20, 20, 20)
        self.mainLayout.setSpacing(15)

        # Create title bar (icon + title)
        self.setupTitleBar()

        # Create sections container
        self.layout = QHBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout.setSpacing(20)
        self.mainLayout.addLayout(self.layout)

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
        titleLabel.setStyleSheet("font-size: 24px; font-weight: bold;")

        # Add widgets to layout
        titleLayout.addWidget(iconButton)
        titleLayout.addWidget(titleLabel)

        self.mainLayout.addLayout(titleLayout)

    def setupBaseStyle(self):
        self.setStyleSheet("""
            QWidget#BaseViewWidget {
                background-color: #080808;
                padding: 15px;
            }
            QLabel#title {
                font-family: "Urbanist";
                font-size: 28px;
                font-weight: bold;
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
            #iconButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
                border-radius: 6px;
            }
        """)

    def addSection(self, title: str):
        sectionCard = QFrame()
        sectionCard.setObjectName("card")

        sectionLayout = QVBoxLayout(sectionCard)
        sectionLayout.setContentsMargins(10, 10, 10, 10)
        sectionLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        sectionLayout.setSpacing(8)

        sectionHeader = QLabel(title)
        sectionHeader.setObjectName("heading")
        sectionHeader.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        sectionHeader.setFixedHeight(30)
        sectionLayout.addWidget(sectionHeader)

        self.layout.addWidget(sectionCard)
        self.sections.append(sectionLayout)
        return len(self.sections) - 1

    def addDetail(self, sectionIndex: int, labelText: str, valueText: str):
        if sectionIndex >= len(self.sections):
            return

        layout = self.sections[sectionIndex]

        count = layout.count()
        if count > 0:
            lastItem = layout.itemAt(count - 1)
            if isinstance(lastItem.spacerItem(), QSpacerItem):
                layout.takeAt(count - 1)

        row = QHBoxLayout()
        row.setSpacing(10)
        row.setAlignment(Qt.AlignmentFlag.AlignTop)

        label = QLabel(f"{labelText}:")
        label.setObjectName("label")
        label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        label.setFixedWidth(80)
        label.setCursor(Qt.CursorShape.IBeamCursor)

        value = QLabel(valueText)
        value.setObjectName("value")
        value.setWordWrap(True)
        value.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        value.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        value.setCursor(Qt.CursorShape.IBeamCursor)
        value.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        value.setMinimumWidth(150)

        container = QWidget()
        container.setLayout(row)
        container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        row.addWidget(label)
        row.addWidget(value, 1)

        layout.addWidget(container)
        layout.addSpacerItem(QSpacerItem(1, 1, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

    def addWidgetToSection(self, sectionIndex: int, widget: QWidget):
        if sectionIndex < len(self.sections):
            self.sections[sectionIndex].addWidget(widget)
