from src.models.UnitDatabaseTable import UnitDatabaseTable as Unit
from src.models.UtilityDatabaseTable import UtilityDatabaseTable as Utility
from src.models.InstalledUtilityDatabaseTable import InstalledUtilityDatabaseTable as InstalledUtility
from src.models.BillDatabaseTable import BillDatabaseTable as Bill

from src.utils.sampleDataGenerator import generateRandomUtilityData, generateUnitData
from src.utils.constants import Range

class UnitsController:
    
    @staticmethod
    def fetchUnits(currentPage: int, sortingOrder: str, sortingField: str, searchValue: str) -> tuple[list[dict[str, str]], int]:
        """
        Fetches all units with pagination, sorting, and searching.
        """
        searchValue = None if searchValue == "" else searchValue
        totalPages =  Unit.totalCount(searchValue=searchValue) // 50 + 1
        return Unit.read(page=currentPage, sortBy=sortingField, order=sortingOrder, searchValue=searchValue), totalPages
    
    @staticmethod
    def addUnit(name: str, address: str, type: str) -> str:
        """
        Adds a new unit with the given data.
        """
        print("Adding unit:", name, address, type)
        return "Unit added successfully"

    @staticmethod
    def viewUnit(id: str) -> tuple[dict[str, any], list[dict[str, any]], dict[list[dict[str, str]]]]:
        """
        Fetches all information about a single unit by ID.
        """
        id = int(id)
        unitInfo = Unit.readOne(id)
        installedUtilites = []
        for utilityID in InstalledUtility.getUnitUtilities(id):
            utilityInfo = Utility.readOne(utilityID)
            utilityInfo["isShared"] = InstalledUtility.isUtilityShared(utilityID)
            installedUtilites.append(utilityInfo)
        unitBills = Bill.getUnitBills(id, range = Range.THREE_MONTHS)
        for utility in unitBills.keys():
            for bill in unitBills[utility]:
                bill["BillingPeriodEnd"] = bill["BillingPeriodEnd"].strftime("%Y-%m-%d")
        
        print(unitBills)
        return ( # UNIT INFO
            unitInfo, 
        # INSTALLED UTILITIES
            installedUtilites, 
        # UNIT UTILITY BILLS 
            unitBills)

    @staticmethod
    def editUnit(originalID: str,  name: str, address: str, type: str) -> str:
        """
        Edits a unit with the given data.
        """
        print("Editing unit:", originalID, name, address, type)
        return "Unit edited successfully"
    
    @staticmethod
    def deleteUnit(id: str) -> str:
        """
        Deletes a new unit with the given data.
        """
        print("Deleting unit:", id)
        return "Unit deleted successfully"
    
    @staticmethod
    def getUnitNames() -> list[dict[str, str]]:
        """
        Fetches all unit names with unit ID.
        """
        print("Fetching unit names")
        return [
            {"UnitID": "U002", "UnitName": "B01R02", "Type": "Individual"},
            {"UnitID": "U004", "UnitName": "B01R01", "Type": "Individual"},
            {"UnitID": "U003", "UnitName": "B01R03", "Type": "Individual"},
            {"UnitID": "U001", "UnitName": "B01", "Type": "Shared"},
            {"UnitID": "U005", "UnitName": "B02", "Type": "Shared"},
            {"UnitID": "U006", "UnitName": "B301", "Type": "Individual"},
        ]