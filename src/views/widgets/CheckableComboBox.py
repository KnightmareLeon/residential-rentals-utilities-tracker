from PyQt6.QtWidgets import QComboBox, QStyledItemDelegate
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtCore import Qt, QAbstractItemModel, QModelIndex

class CheckBoxDelegate(QStyledItemDelegate):
    def editorEvent(self, event, model, option, index):
        if index.flags() & Qt.ItemFlag.ItemIsUserCheckable and event.type() == event.Type.MouseButtonRelease:
            current_state = model.data(index, Qt.ItemDataRole.CheckStateRole)
            new_state = Qt.CheckState.Unchecked if current_state == Qt.CheckState.Checked else Qt.CheckState.Checked
            model.setData(index, new_state, Qt.ItemDataRole.CheckStateRole)
            return True
        return super().editorEvent(event, model, option, index)

class CheckableComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setModel(QStandardItemModel(self))
        self.setEditable(True)
        self.lineEdit().setReadOnly(True)
        self.lineEdit().setPlaceholderText("Filter by:")
        self.lineEdit().setCursor(Qt.CursorShape.PointingHandCursor)

        self.selectedItems = []
        self.onCheckedChangedCallback = None

        self.view().setItemDelegate(CheckBoxDelegate(self))
        self.model().dataChanged.connect(self.handleCheckChange)

        self.installEventFilter(self)
        self.lineEdit().installEventFilter(self)
        self.view().viewport().installEventFilter(self) 

    def addItem(self, text, checked=False):
        item = QStandardItem(text)
        item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsUserCheckable)
        item.setData(Qt.CheckState.Checked, Qt.ItemDataRole.CheckStateRole)
        self.model().appendRow(item)
        self.setCurrentIndex(-1)
        self.lineEdit().setText("Filter by:")

    def handleCheckChange(self):
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
        if (source == self or source == self.lineEdit()) and event.type() == event.Type.MouseButtonPress:
            if self.view().isVisible():
                self.hidePopup()
            else:
                self.showPopup()
            return True
        return super().eventFilter(source, event)
    
    def onItemCheckedChanged(self, callback):
        self.onCheckedChangedCallback = callback
    
    def checkedItems(self):
        return self.selectedItems
    
    def handleCheckChange(self):
        self.updateText()
        if self.onCheckedChangedCallback:
            self.onCheckedChangedCallback()