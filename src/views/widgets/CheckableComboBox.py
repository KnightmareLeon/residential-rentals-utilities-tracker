from PyQt6.QtWidgets import QComboBox, QStyledItemDelegate, QStyleOptionComboBox

from PyQt6.QtGui import QStandardItemModel, QStandardItem, QPainter
from PyQt6.QtCore import Qt

class CheckBoxDelegate(QStyledItemDelegate):
    def editorEvent(self, event, model, option, index):
        if (index.flags() & Qt.ItemFlag.ItemIsUserCheckable) and event.type() == event.Type.MouseButtonRelease:
            # Check if the event is inside the item's rectangle
            if event.button() == event.Button.LeftButton:
                current_state = model.data(index, Qt.ItemDataRole.CheckStateRole)
                new_state = Qt.CheckState.Unchecked if current_state == Qt.CheckState.Checked else Qt.CheckState.Checked
                model.setData(index, new_state, Qt.ItemDataRole.CheckStateRole)
                return True
        return super().editorEvent(event, model, option, index)

class CheckableComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setModel(QStandardItemModel(self))
        self.setEditable(False)

        self.selectedItems = []
        self.staticDisplayText = "Filter:"
        self.onCheckedChangedCallback = None

        self.view().setItemDelegate(CheckBoxDelegate(self))
        self.model().dataChanged.connect(self.handleCheckChange)

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
        self.initStyleOption(opt)  # Proper usage: pass the QStyleOptionComboBox instance
        opt.currentText = self.staticDisplayText  # Override displayed text
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
