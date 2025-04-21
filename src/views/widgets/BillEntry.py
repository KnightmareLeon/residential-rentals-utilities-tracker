from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QScrollArea, QPushButton, QFrame, QSizePolicy, QGridLayout
from PyQt6.QtGui import QFont, QColor, QPainter, QBrush
from PyQt6.QtCore import Qt, pyqtSignal

class ColorDot(QLabel):
    def __init__(self, color: QColor, parent=None):
        super().__init__(parent)
        self.color = color
        self.setFixedSize(12, 12)

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
        self.frame.setStyleSheet(f"background-color: #1C1C1C; border-radius: 5px; padding: 5px 0px;") 
        self.frame.setAutoFillBackground(True)
        self.frame.setContentsMargins(0, 0, 0, 0)
    
        layout = QGridLayout(self.frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.setColumnMinimumWidth(0, 90)
        layout.setColumnMinimumWidth(1, 90)
        layout.setColumnMinimumWidth(2, 90)
        layout.setColumnMinimumWidth(3, 90)
        
        # Utility + Icon
        icon = ColorDot(QColor(color))
        labelUtility = QLabel(utility)
        labelUtility.setStyleSheet("color: white;")
        labelUtility.setFont(QFont("Urbanist", 10))
        
        utilityLayout = QHBoxLayout()
        utilityLayout.setSpacing(8)
        utilityLayout.setContentsMargins(0, 0, 0, 0)
        utilityLayout.addWidget(icon)
        utilityLayout.addWidget(labelUtility)
        
        utilityWidget = QWidget()
        utilityWidget.setLayout(utilityLayout)

        # Balance
        labelBalance = QLabel(balance)
        labelBalance.setStyleSheet("color: white;")
        labelBalance.setFont(QFont("Urbanist", 10, QFont.Weight.Bold))

        # Due Date
        labelDue = QLabel(due)
        labelDue.setStyleSheet("color: white;")
        labelDue.setFont(QFont("Urbanist", 10))

        # Status
        labelStatus = QLabel(status)
        if status == "Paid":
            labelStatus.setStyleSheet("color: #00FF6F;")
        elif status == "Unpaid":
            labelStatus.setStyleSheet("color: #FAFA16;")
        elif status == "Overdue":
            labelStatus.setStyleSheet("color: #FA1647;")
        elif status == "Partially Paid":
            labelStatus.setStyleSheet("color: #FF8400;")
        else:
            labelStatus.setStyleSheet("color: white;")

        labelStatus.setFont(QFont("Urbanist", 10))

        # Add widgets to the grid layout
        layout.addWidget(utilityWidget, 0, 0)  
        layout.addWidget(labelBalance, 0, 1)
        layout.addWidget(labelDue, 0, 2)
        layout.addWidget(labelStatus, 0, 3)

        # Adjust column widths (ensure alignment)
        labelBalance.setMinimumWidth(60)
        labelDue.setMinimumWidth(60)
        labelStatus.setMinimumWidth(60)

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.frame)

        # Add the click event
        self.frame.mousePressEvent = self.on_click

    def on_click(self, event):
        self.rowClicked.emit(self.index)

    def enterEvent(self, event):
        self.frame.setStyleSheet(f"background-color: #3b3b3b; border-radius: 5px; padding: 5px 0px;")
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.frame.setStyleSheet(f"background-color: #1c1c1c; border-radius: 5px; padding: 5px 0px;")
        super().leaveEvent(event)
