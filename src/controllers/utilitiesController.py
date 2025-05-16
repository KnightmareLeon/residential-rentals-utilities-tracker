import datetime
from PyQt6.QtCore import QDate

from src.models.UtilityDatabaseTable import UtilityDatabaseTable as Utility
from src.models.BillDatabaseTable import BillDatabaseTable as Bill
from src.models.InstalledUtilityDatabaseTable import InstalledUtilityDatabaseTable as InstalledUtility

from src.utils.constants import Range
from src.utils.sampleDataGenerator import generateUtilityData, generateRandomeUtilityBills

class UtilitiesController:
    
    @staticmethod
    def fetchUtilities(currentPage: int, sortingOrder: str, sortingField: str, searchValue: str) -> tuple[list[dict[str, str]], int]:
        """
        Fetches all utilitys with pagination, sorting, and searching.
        """
        print(f"Fetching utilities in page {currentPage} sorted by {sortingField} {sortingOrder} while searching for {searchValue}")
        searchValue = None if searchValue == "" else searchValue
        totalPages =  Utility.totalCount(searchValue=searchValue) // 50 + 1

        fetchedUtils = Utility.read(page=currentPage, sortBy=sortingField, order=sortingOrder, searchValue=searchValue)
        for utility in fetchedUtils:
            mainUnitName = ""
            if InstalledUtility.isUtilityShared(utility["UtilityID"]):
                mainUnitName = InstalledUtility.getMainUnit(utility["UtilityID"], name=True)
            else:
                mainUnitName = InstalledUtility.getUtilityUnits(utility["UtilityID"])[0]["Name"]
            utility["UnitName"] = mainUnitName
        return fetchedUtils, totalPages
    
    @staticmethod
    def addUtility(type: str, mainUnitID: str, sharedUnitIDs: list[str], status: str, billingCycle: str) -> str:
        """
        Adds a new utility with the given data.
        """
        # get mainUnit ID using mainUnit name and sharedUnits ID using sharedUnits name
        print("Adding utility:", type, mainUnitID, sharedUnitIDs, status, billingCycle)    
        return "Utility added successfully"

    @staticmethod
    def viewUtility(id: str) -> tuple[dict[str, str], list[dict[str, str]], list[dict[str, str]]]:
        """
        Fetches all information about a single utility by ID.
        """
        id = int(id)
        
        utilityInfo = Utility.readOne(id)
        installationDates = InstalledUtility.getInstallationDates(id)
        utilityInfo["InstallationDate"] = installationDates[0]["InstallationDate"] if len(installationDates) > 0 else datetime.now()

        utilityUnits = InstalledUtility.getUtilityUnits(id)
        if InstalledUtility.isUtilityShared(id):
            mainUnit = InstalledUtility.getMainUnit(id)
            for unit in utilityUnits:
                if unit["UnitID"] == mainUnit:
                    unit["Name"] = unit["Name"] + " (Main)"
                    break
        return ( 
            # UTILITY INFORMATION
            utilityInfo, 
            # UTILITY UNITS
            utilityUnits,
            # UTILITY BILLS
            Bill.getUtilityBills(id, Range.THREE_MONTHS)
        )
    @staticmethod
    def editUtility(originalID: str, type: str, unitID: str, sharedUnitIDs: list[str], status: str, billingCycle: str, installationDate) -> str:
        """
        Edits a utility with the given data.
        """
        print("Editing utility:", originalID, type, unitID, sharedUnitIDs, status, billingCycle, installationDate)
        return "Utility edited successfully"
    
    @staticmethod
    def deleteUtility(id: str) -> str:
        """
        Deletes a new utility with the given data.
        """
        print("Deleting utility:", id)
        return "Utility deleted successfully"
    
    @staticmethod
    def getUtilitiesByUnitID(unitID: str) -> list[dict[str, str]]:
        """
        Fetches all utilities with unit ID.
        """
        print("Fetching utilities by unit ID:", unitID)
        return [
            {"UtilityID": "E001", "Type": "Electricity"},
            {"UtilityID": "W001", "Type": "Water"},
            {"UtilityID": "WI001", "Type": "Internet"},
        ]
