from PyQt6.QtCore import QDate

from src.models.UtilityDatabaseTable import UtilityDatabaseTable as Utility

from src.utils.sampleDataGenerator import generateUtilityData, generateRandomeUtilityBills

class UtilitiesController:
    
    @staticmethod
    def fetchUtilities(currentPage: int, sortingOrder: str, sortingField: str, searchValue: str) -> tuple[list[dict[str, str]], int]:
        """
        Fetches all utilitys with pagination, sorting, and searching.
        """
        searchValue = None if searchValue == "" else searchValue
        totalPages =  Utility.totalCount(searchValue=searchValue) // 50 + 1
        return Utility.read(page=currentPage, sortBy=sortingField, order=sortingOrder, searchValue=searchValue), totalPages
    
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
        return ({ # UTILITY INFORMATION
            "UtilityID": id,
            "Type": "Electricity",
            "Status": "Active",
            "BillingCycle": "Monthly",
            "InstallationDate": QDate.currentDate(),
        }, 
        [ # UTILITY UNITS
            {"UnitID": "U001", "Name": "B01 (Main)"}, # butngan ug Main ang main unit niya pero controller na bahala haha
            {"UnitID": "U002", "Name": "B01R02"},
            {"UnitID": "U003", "Name": "B01R03"},

        ],
        # UTILITY BILLS
        generateRandomeUtilityBills("Electricity"))

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
