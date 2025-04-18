from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QPushButton, QWidget, QHBoxLayout, QHeaderView, QStyledItemDelegate
from PyQt6.QtCore import Qt, QSize, pyqtSignal
from PyQt6.QtGui import QIcon, QColor, QBrush, QPalette

from abc import ABC, abstractmethod

from src.utils.constants import SortOrder

class TableItemDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        viewOption = option
        itemForeground = index.data(Qt.ItemDataRole.ForegroundRole)

        if itemForeground:
            itemColor = itemForeground.color() if hasattr(itemForeground, 'color') else itemForeground
            if itemColor != option.palette.color(QPalette.ColorRole.Text):
                viewOption.palette.setColor(QPalette.ColorRole.HighlightedText, itemColor)

        super().paint(painter, viewOption, index)

class BaseTableWidget(QTableWidget):
    sortRequested = pyqtSignal(int, int)  # columnIndex, sortOrder

    ICON_PATHS = [
        "assets/icons/view.png",
        "assets/icons/edit.png",
        "assets/icons/delete.png"
    ]
    BUTTON_HOVER_COLORS = [
        "#400F98",
        "#B6951E",
        "#541111"
    ]
    BUTTON_HOVER_HIGHLIGHT_COLORS = [
        "#602FB8",
        "#D6B53E",
        "#743131"
    ]
    BUTTON_COUNT = 3
    TABLE_TEXT_COLOR_MAP = {
        (3, "Active"): "#00FF6F",
        (3, "Inactive"): "#FA1647",
        (5, "Paid"): "#00FF6F",
        (5, "Unpaid"): "#FAFA16",
        (5, "Overdue"): "#FA1647",
        (5, "Partially Paid"): "#FF8400",
    }

    def __init__(self, columnHeaders: list[str], databaseHeaders: list[str], parent=None, mainWindow=None):
        super().__init__(0, len(columnHeaders), parent)
        self.mainWindow = mainWindow
        self.columnHeaders = columnHeaders
        self.databaseHeaders = databaseHeaders
        self.columnSortStates = [SortOrder.NONE] * len(columnHeaders)
        self.currentSortIndex = 0
        self.columnSortStates[0] = SortOrder.ASC

        self.hoveredRow = -1
        self.actionButtonsPerRow = {}
        self.itemColors = {}

        self.setupTable()
        self.updateHeaderLabels()

        self.setItemDelegate(TableItemDelegate(self))
        self.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.setMouseTracking(True)
        self.viewport().setMouseTracking(True)
        self.viewport().installEventFilter(self)

    def setupTable(self):
        self.setHorizontalHeaderLabels(self.columnHeaders)
        self.horizontalHeader().setSectionsClickable(True)
        self.horizontalHeader().sectionClicked.connect(self.handleHeaderClicked)

        self.setAlternatingRowColors(False)
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.horizontalHeader().setFixedHeight(60)
        self.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        self.verticalHeader().setDefaultSectionSize(45)
        self.verticalHeader().setVisible(False)

        self.setStyleSheet(""" 
            QTableWidget {
                font: 12pt "Urbanist";
                border-radius: 12px;
                background-color: #1c1c1c;
                padding: 20px 25px;
                color: white;
                gridline-color: transparent;
            }
            QHeaderView::section { 
                font: 12pt "Urbanist"; 
                font-weight: bold;
                color: white;
                padding: 6px;
            }
            QTableCornerButton::section {
                background-color: #f0f0f0;
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
                background-color: #3c3c3c;
            }
        """)

        header = self.horizontalHeader()
        for i in range(self.columnCount() - 1):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)

        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        self.setColumnWidth(0, 90)

        header.setSectionResizeMode(self.columnCount() - 1, QHeaderView.ResizeMode.ResizeToContents)

    def populateTable(self, data: list[dict]):
        self.clearContents()
        self.setRowCount(len(data))

        for row_idx, row_data in enumerate(data):
            for col_idx, col_name in enumerate(self.databaseHeaders):
                value = str(row_data.get(col_name, ""))
                item = QTableWidgetItem(value)
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)

                key = (col_idx, value)
                if key in self.TABLE_TEXT_COLOR_MAP:
                    color = QColor(self.TABLE_TEXT_COLOR_MAP[key])
                    item.setForeground(QBrush(color))
                    self.itemColors[(row_idx, col_idx)] = color
                
                self.setItem(row_idx, col_idx, item)

            self.addActionButtons(row_idx)

    def addActionButtons(self, row_idx):
        button_container = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(5, 2, 5, 2)
        layout.setSpacing(5)

        self.actionButtonsPerRow[row_idx] = []
        buttonHandlers = [self.handleViewButton, self.handleEditButton, self.handleDeleteButton]

        for i in range(self.BUTTON_COUNT):
            btn = QPushButton()
            btn.setFixedSize(40, 40)
            btn.setIcon(QIcon(self.ICON_PATHS[i]))
            btn.setIconSize(QSize(40, 40))
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            layout.addWidget(btn)
            self.actionButtonsPerRow[row_idx].append(btn)

            if i < len(buttonHandlers):
                btn.clicked.connect(lambda _, idx=row_idx, handler=buttonHandlers[i]: handler(idx))

        button_container.setLayout(layout)
        self.setCellWidget(row_idx, self.columnCount() - 1, button_container)

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
            label = self.columnHeaders[i].replace(" ↑", "").replace(" ↓", "").strip()
            if state == SortOrder.ASC:
                label += " ↑"
            elif state == SortOrder.DESC:
                label += " ↓"
            new_labels.append(label)

            headerItem = self.horizontalHeaderItem(i)
            if headerItem:
                headerItem.setBackground(QBrush(QColor(28, 28, 28)))

        self.setHorizontalHeaderLabels(new_labels)

        if self.currentSortIndex is not None:
            headerItem = self.horizontalHeaderItem(self.currentSortIndex)
            if headerItem:
                headerItem.setBackground(QBrush(QColor(48, 48, 48)))
    
    def selectionChanged(self, selected, deselected):
        super().selectionChanged(selected, deselected)

        for index in selected.indexes():
            row = index.row()
            col = index.column()
            originalColor = self.itemColors.get((row, col), QColor("white"))
            item = self.item(row, col)
            if item:
                item.setForeground(QBrush(originalColor))

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
                    btn.setStyleSheet(f"""
                        QPushButton {{
                            background-color: {self.BUTTON_HOVER_COLORS[i]};
                            border: none;
                        }}
                        QPushButton:hover {{
                            background-color: {self.BUTTON_HOVER_HIGHLIGHT_COLORS[i]};
                        }}
                    """)
                else:
                    btn.setStyleSheet("background-color: transparent; border: none;")

    @abstractmethod
    def handleViewButton(self, row_idx):
        pass

    @abstractmethod
    def handleEditButton(self, row_idx):
        pass

    @abstractmethod
    def handleDeleteButton(self, row_idx):
        pass
