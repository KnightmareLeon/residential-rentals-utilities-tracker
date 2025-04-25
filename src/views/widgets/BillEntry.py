from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QScrollArea, QPushButton, QFrame, QSizePolicy, QGridLayout
from PyQt6.QtGui import QFont, QColor, QPainter, QBrush
from PyQt6.QtCore import Qt, pyqtSignal

from src.utils.formatMoney import formatMoneyNoDecimal
from src.utils.formatText import insertSoftBreaks

class ColorDot(QLabel):
    def __init__(self, color: QColor, parent=None):
        super().__init__(parent)
        self.color = color
        self.setFixedSize(15, 15)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QBrush(self.color))
        painter.setPen(Qt.PenStyle.NoPen)
        radius = min(self.width(), self.height()) // 2
        painter.drawEllipse(self.rect().center(), radius, radius)

class BillEntry(QWidget):
    rowClicked = pyqtSignal(int)

    def __init__(self, index, utility, color, balance, due, status):
        super().__init__()

        self.index = index
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setAutoFillBackground(True)
        self.setContentsMargins(0, 0, 0, 0)

        self.frame = QFrame(self)
        self.frame.setStyleSheet("background-color: #1C1C1C; border-radius: 5px; padding: 8px;")
        self.frame.setContentsMargins(0, 0, 0, 0)
        self.frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.frame.setFixedHeight(45)

        layout = QGridLayout(self.frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        layout.setColumnStretch(0, 3)
        layout.setColumnStretch(1, 2)
        layout.setColumnStretch(2, 2)
        layout.setColumnStretch(3, 2)

        # Utility + Icon
        icon = ColorDot(QColor(color))

        if utility == "Miscellaneous":
            utility = "Misc"
        labelUtility = QLabel(utility)
        labelUtility.setStyleSheet("color: white;")
        labelUtility.setFont(QFont("Urbanist", 10))
        labelUtility.setWordWrap(True)
        labelUtility.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        utilityLayout = QHBoxLayout()
        utilityLayout.setSpacing(0)
        utilityLayout.setContentsMargins(0, 0, 0, 0)
        utilityLayout.addWidget(icon, 0, Qt.AlignmentFlag.AlignCenter)
        utilityLayout.addWidget(labelUtility)

        utilityWidget = QWidget()
        utilityWidget.setLayout(utilityLayout)
        utilityWidget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        utilityWidget.setFixedWidth(100)

        # Balance
        labelBalance = QLabel(formatMoneyNoDecimal(balance))
        labelBalance.setStyleSheet("color: white;")
        labelBalance.setFont(QFont("Urbanist", 10))
        labelBalance.setWordWrap(True)
        labelBalance.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        labelBalance.setFixedWidth(70)

        # Due Date
        labelDue = QLabel(due)
        labelDue.setStyleSheet("color: white;")
        labelDue.setFont(QFont("Urbanist", 10))
        labelDue.setWordWrap(True)
        labelDue.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        labelDue.setFixedWidth(70)

        # Status
        labelStatus = QLabel(status)
        labelStatus.setFont(QFont("Urbanist", 10))
        labelStatus.setWordWrap(True)
        labelStatus.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        statusColor = {
            "Paid": "#00FF6F",
            "Unpaid": "#FFE921",
            "Overdue": "#FA1647",
            "Partially Paid": "#FF8400"
        }
        labelStatus.setStyleSheet(f"color: {statusColor.get(status, 'white')};")

        # Add widgets to the grid layout
        layout.addWidget(utilityWidget, 0, 0)
        layout.addWidget(labelBalance, 0, 1)
        layout.addWidget(labelDue, 0, 2)
        layout.addWidget(labelStatus, 0, 3)

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.frame)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.frame.mousePressEvent = self.on_click

    def on_click(self, event):
        self.rowClicked.emit(self.index)

    def enterEvent(self, event):
        self.frame.setStyleSheet("background-color: #3b3b3b; border-radius: 5px; padding: 8px;")
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.frame.setStyleSheet("background-color: #1c1c1c; border-radius: 5px; padding: 8px;")
        super().leaveEvent(event)
