from PyQt6.QtWidgets import QComboBox, QStyleOptionComboBox, QListView
from PyQt6.QtGui import QStandardItemModel, QStandardItem, QPainter
from PyQt6.QtCore import Qt, QEvent, QModelIndex


class CheckableComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setEditable(False)
        self.setView(QListView())  # Ensure using QListView
        self.view().viewport().installEventFilter(self)

        self.selectedItems = []
        self.staticDisplayText = "Filter:"
        self.onCheckedChangedCallback = None

        self.model().dataChanged.connect(self.handleCheckChange)

        self.setStyleSheet("""
            QComboBox QAbstractItemView {
                background-color: #4e4e4e;
                color: white;
                font-family: "Urbanist";
                font-size: 16px;
                selection-background-color: #44475a;
                selection-color: white;
            }
            QComboBox QAbstractItemView::item:hover {
                background-color: #44475a;
                color: white;
            }
            QListView::item:hover {
                background-color: #44475a;
                color: white;
            }
                           """)

    def addItem(self, text, checked=True):
        item = QStandardItem(text)
        item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsUserCheckable)
        state = Qt.CheckState.Checked if checked else Qt.CheckState.Unchecked
        item.setData(state, Qt.ItemDataRole.CheckStateRole)
        self.model().appendRow(item)
        self.setCurrentIndex(-1)

    def paintEvent(self, event):
        painter = QPainter(self)
        opt = QStyleOptionComboBox()
        self.initStyleOption(opt)
        opt.currentText = self.staticDisplayText
        self.style().drawComplexControl(self.style().ComplexControl.CC_ComboBox, opt, painter, self)
        self.style().drawControl(self.style().ControlElement.CE_ComboBoxLabel, opt, painter, self)

    def handleCheckChange(self):
        self.updateSelectedItems()
        if self.onCheckedChangedCallback:
            self.onCheckedChangedCallback()

    def updateSelectedItems(self):
        self.selectedItems = []
        for index in range(self.model().rowCount()):
            item = self.model().item(index)
            if item.checkState() == Qt.CheckState.Checked:
                self.selectedItems.append(item.text())

    def onItemCheckedChanged(self, callback):
        self.onCheckedChangedCallback = callback

    def checkedItems(self):
        return self.selectedItems

    def eventFilter(self, source, event):
        if source == self.view().viewport() and event.type() == QEvent.Type.MouseButtonPress:
            index: QModelIndex = self.view().indexAt(event.pos())
            if index.isValid():
                item = self.model().itemFromIndex(index)
                currentState = item.checkState()
                newState = Qt.CheckState.Unchecked if currentState == Qt.CheckState.Checked else Qt.CheckState.Checked
                item.setCheckState(newState)
                return True
        return super().eventFilter(source, event)
