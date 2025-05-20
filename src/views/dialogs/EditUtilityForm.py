import re

from PyQt6.QtWidgets import QLineEdit, QComboBox, QSpinBox, QDateEdit, QMessageBox
from PyQt6.QtGui import QStandardItem, QStandardItemModel, QBrush, QColor, QFont
from PyQt6.QtCore import Qt
from pyqt6_multiselect_combobox import MultiSelectComboBox

from src.views.widgets.BaseEditWidget import BaseEditWidget
from src.controllers.unitsController import UnitsController
from src.controllers.utilitiesController import UtilitiesController
from src.utils.constants import UTILITIES

class EditUtilityForm(BaseEditWidget):
    def __init__(self, type: str, units: list[dict[str, any]], status: str, billingCycle: str, installationDate: str):
        super().__init__(mainTitle="Edit Utility", iconPath="assets/icons/utilities.png")
        self.setWindowTitle("UtiliTrack - Edit Utility")
        self.setMinimumWidth(400)

        self.originalType = type
        self.originalUnits = units

        self.allUnits = UnitsController.getUnitNames()
        self.unitNameMap = {unit["Name"]: unit["UnitID"] for unit in self.allUnits}
        self.unitIDMap = {unit["UnitID"]: unit for unit in self.allUnits}
        self.indivUnitNames = [f"{unit['Name']} ({unit['Type']})" for unit in self.allUnits if unit["Type"] == "Individual"]
        self.addSection("Utility Information")

        # Determine main unit and its display name
        if len(units) == 1:
            self.mainUnitID = units[0]["UnitID"]
        else:
            mainUnit = next((u for u in units if "(Main)" in u["Name"]), None)
            self.mainUnitID = mainUnit["UnitID"] if mainUnit else None

        self.mainUnitName = self.unitIDMap[self.mainUnitID]["Name"] if self.mainUnitID else None
        mainUnitType = self.unitIDMap[self.mainUnitID]["Type"] if self.mainUnitID else None
        mainUnitDisplay = f"{self.mainUnitName} ({mainUnitType})" if self.mainUnitName else None

        # Prepare dropdown display
        unitDisplay = [f"{unit['Name']} ({unit['Type']})" for unit in self.allUnits]

        self.typeInput = self.addComboBox("Utility", UTILITIES, sectionTitle="Utility Information", defaultValue=type)
        self.unitNameInput = self.addComboBox("Unit", unitDisplay, sectionTitle="Utility Information", defaultValue=mainUnitDisplay)
        self.sharedWithInput = self.addMultiselectComboBox("Shared with Unit(s)", [], sectionTitle="Utility Information", isVisible=False)
        self.installationDateInput = self.addDateInput("Installation Date", sectionTitle="Utility Information", defaultDate=installationDate)
        self.statusInput = self.addComboBox("Status", ['Active','Inactive', 'N/A'], sectionTitle="Utility Information", defaultValue=status)
        self.billingInput = self.addComboBox("Billing Cycle", ['Monthly','Quarterly','Annually','Irregular'], sectionTitle="Utility Information", defaultValue=billingCycle)

        # Connect logic
        self.unitNameInput.currentTextChanged.connect(self.handleUnitNameChange)
        self.sharedWithInput.currentTextChanged.connect(self.updateUtilityTypeOptions)

        self.sharedUnits = [u for u in units if "(Main)" not in u["Name"]]

        # Set selected unit (Main)
        if mainUnitDisplay:
            index = self.unitNameInput.findText(mainUnitDisplay)
            if index >= 0:
                self.unitNameInput.setCurrentIndex(index)
                self.handleUnitNameChange(mainUnitDisplay)
        
        self.handleUnitNameChange(self.unitNameInput.currentText())

        if self.sharedUnits:
            sharedNames = [f"{unit['Name']} ({self.unitIDMap[unit['UnitID']]['Type']})" for unit in self.sharedUnits]
            
            items = [self.sharedWithInput.itemText(i) for i in range(self.sharedWithInput.count())]
            indexesToCheck = [i for i, item in enumerate(items) if item in sharedNames]
            
            self.sharedWithInput.setCurrentIndexes(indexesToCheck)

    def handleUnitNameChange(self, text: str):
        unitType = text.split(' ')[-1][1:-1]
        labelWidget, sharedWidget = self.fields["Shared with Unit(s)"]

        allTypes = ['Electricity','Water','Gas','Internet','Trash','Maintenance','Miscellaneous']

        if unitType == "Shared":
            sharedWidget.clear()
            sharedWidget.addItems(self.indivUnitNames)
            labelWidget.setVisible(True)
            sharedWidget.setVisible(True)

            # Get selected shared unit names, strip "(Type)"
            sharedNames = [re.sub(r'\s*\(.*?\)', '', name).strip() for name in sharedWidget.currentData()]
            sharedUnitIDs = [self.unitNameMap.get(name) for name in sharedNames if self.unitNameMap.get(name)]

            # Get all utility types used by shared units
            existingTypes = set()
            for uid in sharedUnitIDs:
                existingUtilities = UtilitiesController.getUtilitiesByUnitID(uid)
                existingTypes.update(util['Type'] for util in existingUtilities)

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

        self.updateUtilityTypeOptions()
    
    def updateUtilityTypeOptions(self):
        allTypes = ['Electricity','Water','Gas','Internet','Trash','Maintenance','Miscellaneous']
        selectedMain = self.unitNameInput.currentText().strip()
        sharedUnits = self.sharedWithInput.currentData() if self.sharedWithInput.isVisible() else []

        unitIDs = []

        # Get main unit ID
        match = re.match(r'^(.*)\s+\((.*?)\)$', selectedMain)
        if match:
            unitName = match.group(1).strip()
            mainUnitID = self.unitNameMap.get(unitName)
            if mainUnitID:
                unitIDs.append(mainUnitID)

        # Add shared unit IDs (if any)
        strippedSharedNames = [re.sub(r'\s*\(.*?\)', '', name).strip() for name in sharedUnits]
        for name in strippedSharedNames:
            sharedID = self.unitNameMap.get(name)
            if sharedID:
                unitIDs.append(sharedID)

        # Collect all existing utility types from selected units
        existingTypes = set()
        for uid in unitIDs:
            existingUtilities = UtilitiesController.getUtilitiesByUnitID(uid)
            existingTypes.update(util['Type'] for util in existingUtilities)

        existingTypes.discard(self.originalType)

        self.typeInput.clear()
        model = QStandardItemModel()

        hasAvailable = False
        selectedIndex = -1

        for i, t in enumerate(allTypes):
            if t == self.originalType:
                item = QStandardItem(t)
                model.appendRow(item)
                selectedIndex = i
            elif t not in existingTypes:
                hasAvailable = True
                item = QStandardItem(t)
                model.appendRow(item)
            else:
                item = QStandardItem(f"{t} (added)")
                item.setEnabled(False)
                item.setForeground(QBrush(QColor("707070")))
                item.setBackground(QBrush(QColor("#383838")))
                model.appendRow(item)

        self.typeInput.setModel(model)

        if selectedIndex != -1:
            self.typeInput.setCurrentIndex(selectedIndex)
        elif hasAvailable:
            self.typeInput.setCurrentIndex(0)
        else:
            self.typeInput.setCurrentIndex(-1)

    def getFormData(self) -> dict:
        data = {}
        for label, (labelWidget, widget) in self.fields.items():
            print(label)
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
    
    def onEditClicked(self, utilityID):
        updatedData = self.getFormData()

        if not updatedData:
            self.setErrorMessage("Please fill out all required fields.")
            return

        # Show confirmation dialog
        msgBox = QMessageBox(self)
        msgBox.setIcon(QMessageBox.Icon.Warning)
        msgBox.setWindowTitle("Confirm Update")
        msgBox.setText("Are you sure you want to update this utility?")
        msgBox.setStyleSheet("""
        QDialog {
            background-color: #202020;
            font-family: "Urbanist";
            font-size: 16px;
            color: white;
        }
        QLabel {
            color: white;
            font-family: "Urbanist";
            font-size: 16px;
        }
        """)

        yesButton = msgBox.addButton(QMessageBox.StandardButton.Yes)
        noButton = msgBox.addButton(QMessageBox.StandardButton.No)

        yesButton.setCursor(Qt.CursorShape.PointingHandCursor)
        noButton.setCursor(Qt.CursorShape.PointingHandCursor)

        yesButton.setStyleSheet("""
            QPushButton {
                background-color: #541111;
                color: white;
                padding: 6px 12px;
                border-radius: 4px;
                border: none;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #743131;
            }
        """)
        noButton.setStyleSheet("""
            QPushButton {
                background-color: #444444;
                color: white;
                padding: 6px 12px;
                border-radius: 4px;
                border: none;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #666666;
            }
        """)

        msgBox.exec()

        if msgBox.clickedButton() != yesButton:
            return

        # Proceed with update after confirmation
        type = updatedData["Utility"]
        unitID = updatedData["Unit"]
        sharedUnitIDs = updatedData["Shared with Unit(s)"]
        status = updatedData["Status"]
        billing = updatedData["Billing Cycle"]
        installDate = updatedData["Installation Date"]

        response = UtilitiesController.editUtility(
            utilityID, type, unitID, sharedUnitIDs, status, billing, installDate
        )

        if response == "Utility edited successfully":
            self.accept()
        else:
            self.setErrorMessage(response)

    def accept(self):
        super().accept()