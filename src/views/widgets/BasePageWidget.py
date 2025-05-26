from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt

from abc import abstractmethod

class BasePageWidget(QWidget):
    def __init__(self, tableWidget, buttonText="Add", mainWindow=None):
        super().__init__()
        self.mainWindow = mainWindow
        self.table = tableWidget(mainWindow=self.mainWindow)

        self.currentPage = 1
        self.totalPages = 10000

        self.setupUI(buttonText)
        self.addButton.clicked.connect(self.handleAddButton)
        self.prevButton.clicked.connect(self.prevPage)
        self.nextButton.clicked.connect(self.nextPage)

    def setupUI(self, buttonText):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 30, 0)
        self.layout.setSpacing(10)

        self.setStyleSheet("""
        QPushButton {
            font: 12pt "Urbanist";
            font-weight: bold; 
            padding: 10px 15px; 
            border-radius: 10px;
            background: transparent;
            color: white;
        }
        QPushButton:hover {
            background-color: #3E3E3E;
        }
        #addButton {
            background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0.4 #F72585, stop:1 #3A0CA3);
            font-size: 13pt;
            padding: 15px 45px;
            border-radius: 10px;
        }
        #addButton:hover {
            background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0.4 #FF5FB2, stop:1 #5A30D6);
        }
        #prevButton, #nextButton {
            background-color: #2b2b2b;
        }
        #prevButton:hover, #nextButton:hover {
            background-color: #3E3E3E;
        }
        QLabel {
            font: 12pt "Urbanist";
            color: white;
        }
        """)

        self.bottomBar = QHBoxLayout()

        self.addButton = QPushButton(buttonText)
        self.prevButton = QPushButton("←")
        self.pageLabel = QLabel("Page 1 of 1")
        self.nextButton = QPushButton("→")

        self.addButton.setObjectName("addButton")
        self.prevButton.setObjectName("prevButton")
        self.nextButton.setObjectName("nextButton")

        self.addButton.setToolTip("Add")
        self.prevButton.setToolTip("Previous Page")
        self.nextButton.setToolTip("Next Page")
        self.pageLabel.setToolTip("Current Page")

        self.addButton.setCursor(Qt.CursorShape.PointingHandCursor)
        self.prevButton.setCursor(Qt.CursorShape.PointingHandCursor)
        self.nextButton.setCursor(Qt.CursorShape.PointingHandCursor)

        self.bottomBar.addWidget(self.addButton)
        self.bottomBar.addStretch()
        self.bottomBar.addWidget(self.prevButton)
        self.bottomBar.addWidget(self.pageLabel)
        self.bottomBar.addWidget(self.nextButton)

        self.layout.addLayout(self.bottomBar)
        self.layout.addWidget(self.table)

    def updatePage(self):
        self.table.updateTable()
        self.pageLabel.setText(f"Page {self.currentPage} of {self.totalPages}")

    def nextPage(self):
        if self.currentPage < self.totalPages:
            self.currentPage += 1
            self.updatePage()

    def prevPage(self):
        if self.currentPage > 1:
            self.currentPage -= 1
            self.updatePage()

    def resetPage(self):
        self.currentPage = 1

    @abstractmethod
    def handleAddButton(self):
        pass
    
