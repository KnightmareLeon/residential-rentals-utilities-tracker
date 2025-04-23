from PyQt6.QtWidgets import (
  QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame
)
from PyQt6.QtCore import Qt


class BaseViewWidget(QWidget):
  def __init__(self, mainTitle: str, parent=None):
    super().__init__(parent)
    self.mainTitle = mainTitle
    self.sections = []  # Store section layout references
    self.setupBaseStyle()

    self.layout = QVBoxLayout(self)
    self.layout.setSpacing(15)

    # Main header
    mainHeader = QLabel(mainTitle)
    mainHeader.setObjectName("heading")
    self.layout.addWidget(mainHeader)

  def setupBaseStyle(self):
    self.setStyleSheet("""
      QLabel#heading {
        font-family: "Urbanist";
        font-size: 20px;
        font-weight: bold;
        color: white;
      }
      QLabel#label {
        font-family: "Urbanist";
        font-size: 14px;
        color: white;
      }
      QLabel#value {
        font-family: "Urbanist";
        font-size: 14px;
        color: white;
        font-weight: bold;
      }
      QFrame#card {
        background-color: #1C1C1C;
        border-radius: 15px;
        padding: 15px;
      }
    """)

  def addSection(self, title: str):
    # Section header
    sectionHeader = QLabel(title)
    sectionHeader.setObjectName("heading")
    self.layout.addWidget(sectionHeader)

    # Section card container
    sectionCard = QFrame()
    sectionCard.setObjectName("card")
    sectionLayout = QVBoxLayout(sectionCard)
    sectionLayout.setSpacing(8)

    self.layout.addWidget(sectionCard)
    self.sections.append(sectionLayout)
    return len(self.sections) - 1  # Return index for reference

  def addDetail(self, sectionIndex: int, labelText: str, valueText: str):
    if sectionIndex >= len(self.sections):
      return  # Invalid section index

    row = QHBoxLayout()
    label = QLabel(f"{labelText}:")
    label.setObjectName("label")
    label.setFixedWidth(70)

    value = QLabel(valueText)
    value.setObjectName("value")
    value.setWordWrap(True)

    row.addWidget(label)
    row.addWidget(value, 1)
    self.sections[sectionIndex].addLayout(row)

  def addWidgetToSection(self, sectionIndex: int, widget: QWidget):
    if sectionIndex < len(self.sections):
      self.sections[sectionIndex].addWidget(widget)
