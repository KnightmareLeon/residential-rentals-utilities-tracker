import re
from PyQt6.QtWidgets import QLineEdit, QComboBox, QSpinBox, QDateEdit
from PyQt6.QtGui import QStandardItem, QStandardItemModel, QBrush, QColor, QFont
from pyqt6_multiselect_combobox import MultiSelectComboBox

from src.views.widgets.BaseCreateWidget import BaseCreateWidget
from src.controllers.unitsController import UnitsController
from src.controllers.utilitiesController import UtilitiesController

class AddUtilityForm(BaseCreateWidget):
    def __init__(self):
        super().__init__(mainTitle="Add Utility", iconPath="assets/icons/utilities.png")
        self.setWindowTitle("UtiliTrack - Add Utility")
        self.setMinimumWidth(400)

        self.unitNames = UnitsController.getUnitNames()
        self.unitNameMap = {unit["UnitName"]: unit["UnitID"] for unit in self.unitNames}
        self.indivUnitNames = [f"{name['UnitName']} ({name['Type']})" for name in self.unitNames if name['Type'] != "Shared"]

        self.addSection("Utility Information")

        self.unitNameInput = self.addComboBox("Unit", [f"{name['UnitName']} ({name['Type']})" for name in self.unitNames], sectionTitle="Utility Information")
        self.unitNameInput.currentTextChanged.connect(self.handleUnitNameChange)

        self.multipleUnitInput = self.addMultiselectComboBox("Shared with Unit(s)", [], sectionTitle="Utility Information", isVisible=False)

        self.typeInput = self.addComboBox("Utility Type", ['Electricity','Water','Gas','Internet','Trash','Maintenance','Miscellaneous'], sectionTitle="Utility Information")
        self.typeInput.currentTextChanged.connect(self.handleUtilityTypeChange)

        self.installationDateInput = self.addDateInput("Installation Date", sectionTitle="Utility Information")
        self.statusInput = self.addComboBox("Status", ['Active','Inactive', 'N/A'], sectionTitle="Utility Information")
        self.billingInput = self.addComboBox("Billing Cycle", ['Monthly','Quarterly','Annually','Irregular'], sectionTitle="Utility Information")

        self.handleUnitNameChange(self.unitNameInput.currentText())

    def handleUnitNameChange(self, text: str):
        unitType = text.split(' ')[-1][1:-1]
        labelWidget, sharedWidget = self.fields["Shared with Unit(s)"]

        if unitType == "Shared":
            sharedWidget.clear()
            sharedWidget.addItems(self.indivUnitNames)
            labelWidget.setVisible(True)
            sharedWidget.setVisible(True)
        else:
            sharedWidget.clear()
            labelWidget.setVisible(False)
            sharedWidget.setVisible(False)

            match = re.match(r'^(.*)\s+\((.*?)\)$', text.strip())
            if not match:
                print(f"Warning: Could not parse unit from '{text}'")
                return

            unitName = match.group(1).strip()
            unitID = self.unitNameMap.get(unitName)
            if unitID is None:
                print(f"Warning: Unit ID not found for '{unitName}'")
                return

            existingUtilities = UtilitiesController.getUtilitiesByUnitID(unitID)
            existingTypes = {util['Type'] for util in existingUtilities}

            allTypes = ['Electricity','Water','Gas','Internet','Trash','Maintenance','Miscellaneous']

            self.typeInput.clear()
            model = QStandardItemModel()

            for t in allTypes:
                if t not in existingTypes:
                    item = QStandardItem(t)
                    model.appendRow(item)

            for t in allTypes:
                if t in existingTypes:
                    item = QStandardItem(f"{t} (added)")
                    item.setEnabled(False)
                    item.setForeground(QBrush(QColor("707070")))
                    item.setBackground(QBrush(QColor("#383838")))
                    model.appendRow(item)

            self.typeInput.setModel(model)
            self.typeInput.setCurrentIndex(0)

    def handleUtilityTypeChange(self, text: str):
        labelWidget, widget = self.fields["Status"]
        
        if text == "Gas" or text == "Maintenance" or text == "Miscellaneous" or text == "Trash":
            widget.setCurrentIndex(2)
        else:
            widget.setCurrentIndex(0)
        # if text == "Gas" or text == "Maintenance" or text == "Miscellaneous" or text == "Trash":
        #     widget.clear()
        #     widget.addItems(['N/A'])
        #     labelWidget.setVisible(False)
        #     widget.setVisible(False)
        # else:
        #     widget.clear()
        #     widget.addItems(['Active','Inactive'])
        #     labelWidget.setVisible(True)
        #     widget.setVisible(True)
    
    def getFormData(self) -> dict:
        data = {}
        for label, (labelWidget, widget) in self.fields.items():
            if isinstance(widget, QLineEdit):
                data[label] = widget.text()
            elif isinstance(widget, QComboBox) and labelWidget.text() == "Unit":
                currentText = widget.currentText().strip()

                match = re.match(r'^(.*)\s+\((.*?)\)$', currentText)
                if match:
                    unitName = match.group(1).strip()
                else:
                    unitName = currentText

                unitID = self.unitNameMap.get(unitName)

                if unitID is None:
                    print(f"Warning: Unit ID not found for '{unitName}'")
                
                data[label] = unitID

            elif isinstance(widget, MultiSelectComboBox) and labelWidget.text().strip() == "Shared with Unit(s)":
                rawUnitNames = widget.currentData()
                strippedUnitNames = [re.sub(r'\s*\(.*?\)', '', name).strip() for name in rawUnitNames]

                unitIDs = []
                for name in strippedUnitNames:
                    unitID = self.unitNameMap.get(name)
                    if unitID is not None:
                        unitIDs.append(unitID)
                    else:
                        print(f"Warning: Unit ID not found for '{name}'")

                data[label] = unitIDs

            elif isinstance(widget, MultiSelectComboBox):
                data[label] = widget.currentData()
            elif isinstance(widget, QComboBox):
                data[label] = widget.currentText()
            elif isinstance(widget, QSpinBox):
                data[label] = widget.value()
            elif isinstance(widget, QDateEdit):
                data[label] = widget.date()
        return data