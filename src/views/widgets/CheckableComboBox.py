from PyQt6.QtWidgets import QComboBox
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtCore import Qt

class CheckableComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setModel(QStandardItemModel(self))
        self.view().pressed.connect(self.handleItemPressed)
        self.setEditable(True)
        self.lineEdit().setReadOnly(True)
        self.lineEdit().setPlaceholderText("Filter by:")

        self.selectedItems = []
        self.onCheckedChangedCallback = None

        self.lineEdit().installEventFilter(self)

    def addItem(self, text, checked=False):
        item = QStandardItem(text)
        item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsUserCheckable)
        item.setData(Qt.CheckState.Checked, Qt.ItemDataRole.CheckStateRole)
        self.model().appendRow(item)
        self.setCurrentIndex(-1)
        self.lineEdit().setText("Filter by:")

    def handleItemPressed(self, index):
        item = self.model().itemFromIndex(index)
        newCheckStaate = Qt.CheckState.Checked if item.checkState() == Qt.CheckState.Unchecked else Qt.CheckState.Unchecked
        item.setCheckState(newCheckStaate)
        self.updateText()

        if self.onCheckedChangedCallback:
            self.onCheckedChangedCallback()

    def updateText(self):
        self.selectedItems = []
        for index in range(self.model().rowCount()):
            item = self.model().item(index)
            if item.checkState() == Qt.CheckState.Checked:
                self.selectedItems.append(item.text())
        self.lineEdit().setText("Filter by:")
    
    def eventFilter(self, source, event):
        if source == self.lineEdit() and event.type() == event.Type.MouseButtonPress:
            self.showPopup()
            return True
        return super().eventFilter(source, event)
    
    def onItemCheckedChanged(self, callback):
        self.onCheckedChangedCallback = callback
    
    def checkedItems(self):
        return self.selectedItems