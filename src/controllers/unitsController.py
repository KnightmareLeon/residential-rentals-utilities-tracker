from datetime import date, datetime
from dateutil.relativedelta import relativedelta

from src.models.UnitDatabaseTable import UnitDatabaseTable as Unit
from src.models.UtilityDatabaseTable import UtilityDatabaseTable as Utility
from src.models.InstalledUtilityDatabaseTable import InstalledUtilityDatabaseTable as InstalledUtility
from src.models.BillDatabaseTable import BillDatabaseTable as Bill

from src.utils.sampleDataGenerator import generateRandomUtilityData, generateUnitData
from src.utils.constants import Range
from src.utils.diffMonths import diffMonths

class UnitsController:
    
    @staticmethod
    def fetchUnits(currentPage: int, sortingOrder: str, sortingField: str, searchValue: str) -> tuple[list[dict[str, str]], int]:
        """
        Fetches all units with pagination, sorting, and searching.
        """
        print(f"Fetching units in page {currentPage} sorted by {sortingField} {sortingOrder} while searching for {searchValue}")
        searchValue = None if searchValue == "" else searchValue
        totalPages =  Unit.totalCount(searchValue=searchValue) // 50 + 1
        return Unit.read(page=currentPage, sortBy=sortingField, order=sortingOrder, searchValue=searchValue), totalPages
    
    @staticmethod
    def addUnit(name: str, address: str, type: str) -> str:
        """
        Adds a new unit with the given data.
        """
        if Unit.doesUnitNameExist(name):
            return (f"{name} already exists. Please input another name.")
        print("Adding unit:", name, address, type)
        Unit.create({"Name" : name, "Address" : address, "Type" : type})
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
        
        return ( # UNIT INFO
            unitInfo, 
        # INSTALLED UTILITIES
            installedUtilites, 
        # UNIT UTILITY BILLS 
            unitBills)

    @staticmethod
    def editUnit(originalID: str, name: str, address: str, type: str) -> str:
        """
        Edits a unit with the given data.
        """
        print("Editing unit:", originalID, name, address, type)
        originalID = int(originalID)
        originalData = Unit.readOne(originalID)
        editedColumns = {}
        
        if name != originalData["Name"] and Unit.doesUnitNameExist(name):
            return f"{name} already exists. Please input another name."
        if name != originalData["Name"]:
            editedColumns["Name"] = name
        if address != originalData["Address"]:
            editedColumns["Address"] = address
        if type != originalData["Type"]:
            editedColumns["Type"] = type
        if editedColumns == {}:
            return "No changes made."
        
        Unit.update(originalID, editedColumns)

        return "Unit edited successfully"
    
    @staticmethod
    def deleteUnit(id: str) -> str:
        """
        Deletes a new unit with the given data.
        """
        Unit.delete([int(id)])
        return "Unit deleted successfully"
    
    @staticmethod
    def getUnitNames() -> list[dict[str, str]]:
        """
        Fetches all unit names with unit ID.
        """
        print("Fetching unit names")
        
        return Unit.read(columns=["UnitID", "Name", "Type"], limit=Unit.totalCount(), sortBy="Name", order="ASC")
    
    @staticmethod
    def fetchUnitBills(id : str, monthRange : int, offset : datetime) -> tuple[dict[str, list[dict[str, str]]], datetime] :
        id = int(id)
        range = None
        for r in Range:
            if r.value == monthRange:
                range = r
                break
        offsetInt = (diffMonths(datetime.now(), offset)) // range.value + 1
        unitBills = Bill.getUnitBills(id, range, offset=offsetInt)
        for utility in unitBills.keys():
            for bill in unitBills[utility]:
                bill["BillingPeriodEnd"] = bill["BillingPeriodEnd"].strftime("%Y-%m-%d")
        
        earliestBillDates = Bill.getEarliestUnitBillDates(id) if Bill.getEarliestUnitBillDates(id) is not None else None
        if earliestBillDates is not None:
            for utility in earliestBillDates.keys():
                earliestBillDates[utility] = earliestBillDates[utility] if earliestBillDates[utility] is not None else date.today()
        print(earliestBillDates)
        earliestBillDate = min(earliestBillDates.values()) if len(earliestBillDates.values()) > 0 else date.today() - relativedelta(months=monthRange)
        monthsDiff = diffMonths(datetime.now(), datetime.combine(earliestBillDate, datetime.min.time())) - monthRange
        return unitBills,  datetime.now() - relativedelta(months=monthsDiff)
        