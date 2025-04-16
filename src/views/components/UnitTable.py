from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QPushButton, QWidget, QHBoxLayout, QHeaderView
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QIcon, QColor, QBrush

class SortOrder:
    NONE = 0
    ASC = 1
    DESC = 2

class UnitTable(QTableWidget):
    sortRequested = pyqtSignal(int, int)  # columnIndex, sortOrder
    iconPaths = [
        "assets/icons/view.png",
        "assets/icons/edit.png",
        "assets/icons/delete.png"
    ]
    tableHeaders = [
        "Unit ID",
        "Unit Name",
        "Address",
        "Unit Type",
        "Actions"
    ]
    buttonHoverColors = [
        "#400F98",
        "#B6951E",
        "#541111"
    ]
    buttonHoverHighlightColors = [
        "#501FA8",
        "#C6A52E",
        "#642121"
    ]
    databaseHeaders = [
        "UnitID", 
        "Name", 
        "Address",
        "UnitType"
    ]

    def __init__(self, parent=None, mainWindow=None):
        super().__init__(0, len(self.tableHeaders), parent)
        self.mainWindow = mainWindow
        self.setupTable()

        self.columnSortStates = [SortOrder.NONE] * len(self.tableHeaders)
        self.currentSortIndex = 0
        self.columnSortStates[0] = SortOrder.ASC
        self.updateHeaderLabels()

        self.hoveredRow = -1
        self.setMouseTracking(True)
        self.viewport().setMouseTracking(True)
        self.viewport().installEventFilter(self)

    # DATA UPDATES
    def setupTable(self):
        self.setHorizontalHeaderLabels(self.tableHeaders)
        self.horizontalHeader().setSectionsClickable(True)
        self.horizontalHeader().sectionClicked.connect(self.handleHeaderClicked)
        
        # Style settings
        self.setAlternatingRowColors(False)
        self.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.horizontalHeader().setFixedHeight(50)
        self.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Fixed)
        self.verticalHeader().setDefaultSectionSize(45)
        self.verticalHeader().setVisible(False)
        self.setStyleSheet("""
            QTableWidget {
                font: 12pt "Urbanist";
                border-radius: 12px;
                background-color: #1c1c1c;
                padding: 20px 25px;
                color: white; 
            }
            QHeaderView::section { 
                font: 12pt "Urbanist"; 
                font-weight: bold; 
                font-size: 12pt;
                border-bottom: 2px solid #1c1c1c;
            }
            QHeaderView::section:vertical {
                font: 12pt "Urbanist"; 
                font-weight: normal; 
                font-size: 12pt;
                border: none;
                background-color: #1c1c1c;
            }
            QTableCornerButton::section {
                background-color: #f0f0f0;
                border: none;
                border-bottom: 2px solid #1c1c1c;
            }
            QPushButton { 
                font: 12pt "Urbanist"; 
                font-weight: bold; 
                padding: 0px 15px; 
                border-radius: 3px; 
            }
            QTableWidget {
                gridline-color: transparent;
            }
            QTableWidget::item {
                border-right: 1px solid transparent;
                background-color: transparent;
            }
            QTableWidget::item:hover {
                background-color: #3E3E3E;
            }
            QTableWidget::item:selected {
                background-color: #3c3c3c; ; 
            }
        """)

        header = self.horizontalHeader()
        for i in range(len(self.tableHeaders)-1):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(len(self.tableHeaders)-1, QHeaderView.ResizeMode.ResizeToContents)   

        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)
        self.setColumnWidth(0, 100)
        self.setColumnWidth(5, 220)

    def updateTable(self):
        sortingOrder = self.columnSortStates[self.currentSortIndex]
        sortingField = self.databaseHeaders[self.currentSortIndex]
        searchValue = self.mainWindow.searchInputLineEdit.text().strip()

        if sortingOrder == SortOrder.ASC:
            sortingOrder = "ASC"
        elif sortingOrder == SortOrder.DESC:
            sortingOrder = "DESC"
        else:
            sortingOrder = "ASC"
        
        if searchValue == "":
            print("no search value")
        else:
            print(searchValue, "search value")
            print(sortingField, sortingOrder, "sorting field and order")

        data = None

        #self.populateTable(data)

    # TABLE CREATION
    def populateTable(self, data: list[dict]):
        self.clearContents()
        self.setRowCount(len(data))

        for row_idx, row_data in enumerate(data):
            for col_idx, col_name in enumerate(self.tableHeaders[:-1]):
                value = str(row_data.get(col_name, ""))
                item = QTableWidgetItem(value)
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.setItem(row_idx, col_idx, item)

            self.addActionButtons(row_idx)

    def addActionButtons(self, row_idx, row_count=3):
        button_container = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(5, 2, 5, 2)
        layout.setSpacing(5)

        self.actionButtonsPerRow = getattr(self, "actionButtonsPerRow", {})
        self.actionButtonsPerRow[row_idx] = []
        buttonHandlers = [self.handleViewButton, self.handleEditButton, self.handleDeleteButton]

        for i in range(row_count):
            btn = QPushButton()
            btn.setFixedSize(40, 40)
            btn.setIcon(QIcon(self.iconPaths[i]))
            btn.setIconSize(QSize(40, 40))
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            layout.addWidget(btn)
            self.actionButtonsPerRow[row_idx].append(btn)

            btn.clicked.connect(lambda _, idx=row_idx, handler=buttonHandlers[i]: handler(idx))

        button_container.setLayout(layout)
        self.setCellWidget(row_idx, len(self.tableHeaders) - 1, button_container)

    # BUTTON FUNCTIONS
    def handleEditButton(self, row_idx):
        print("edit", row_idx)

    def handleDeleteButton(self, row_idx):
        print("delete", row_idx)

    def handleViewButton(self, row_idx):
        print("view", row_idx)

    # HEADER FUNCTIONS
    def handleHeaderClicked(self, index):
        if index >= self.columnCount() - 1:
            return
        
        if index == self.currentSortIndex:
            current = self.columnSortStates[index]
            newState = SortOrder.DESC if current == SortOrder.ASC else SortOrder.ASC
        else:
            newState = SortOrder.ASC
            self.currentSortIndex = index

        self.columnSortStates = [SortOrder.NONE] * self.columnCount()
        self.columnSortStates[index] = newState

        self.updateHeaderLabels()
        self.sortRequested.emit(index, newState)

    def updateHeaderLabels(self):
        new_labels = []
        for i, state in enumerate(self.columnSortStates):
            label = self.tableHeaders[i].replace(" ↑", "").replace(" ↓", "").strip()
            if state == SortOrder.ASC:
                label += " ↑"
            elif state == SortOrder.DESC:
                label += " ↓"
            new_labels.append(label)
            
            headerItem = self.horizontalHeaderItem(i)
            headerItem.setBackground(QBrush(QColor(28, 28, 28)))
    
        self.setHorizontalHeaderLabels(new_labels)
        
        if self.currentSortIndex is not None:
            headerItem = self.horizontalHeaderItem(self.currentSortIndex)
            headerItem.setBackground(QBrush(QColor(48, 48, 48))) 
    
    # HOVER FUNCTIONS
    def eventFilter(self, source, event):
        if source == self.viewport():
            if event.type() == QtCore.QEvent.Type.MouseMove:
                index = self.indexAt(event.pos())
                row = index.row()
                if row != self.hoveredRow:
                    self.updateButtonHover(row)
                    self.hoveredRow = row
            elif event.type() == QtCore.QEvent.Type.Leave:
                self.updateButtonHover(-1)
                self.hoveredRow = -1
        return super().eventFilter(source, event)

    def updateButtonHover(self, newRow):
        for row_idx in range(self.rowCount()):
            isHovered = (row_idx == newRow)

            for i, btn in enumerate(self.actionButtonsPerRow.get(row_idx, [])):
                if isHovered:
                    btn.setStyleSheet(f"background-color: {self.buttonHoverColors[i]}; border: none;")
                else:
                    btn.setStyleSheet("background-color: transparent; border: none;")
