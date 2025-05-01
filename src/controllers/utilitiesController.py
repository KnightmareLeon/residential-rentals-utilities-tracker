from src.utils.sampleDataGenerator import generateRandomUtilityData, generateRandomeUtilityBills

class UtilitiesController:
    
    @staticmethod
    def fetchUtilities(currentPage: int, sortingOrder: str, sortingField: str, searchValue: str) -> tuple[list[dict[str, str]], int]:
        """
        Fetches all utilitys with pagination, sorting, and searching.
        """
        print(f"Fetching data for page {currentPage} with sorting {sortingField} {sortingOrder} and search '{searchValue}'")
        return ([], 5) 
    
    @staticmethod
    def addUtility(type: str, mainUnit: str, sharedUnits: list[str], status: str, billingCycle: str) -> str:
        """
        Adds a new utility with the given data.
        """
        # get mainUnit ID using mainUnit name and sharedUnits ID using sharedUnits name
        print("Adding utility:", type, mainUnit, sharedUnits, status, billingCycle)    
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
            "InstallationDate": "2023-10-01",
        }, 
        [ # UTILITY UNITS
            {"UnitID": "U001", "Name": "B01R01 (Main)"}, # butngan ug Main ang main unit niya pero controller na bahala
            {"UnitID": "U002", "Name": "B01R02"},
            {"UnitID": "U003", "Name": "B01R03"},
            {"UnitID": "U001", "Name": "B01R01"},
            {"UnitID": "U002", "Name": "B01R02"},
            {"UnitID": "U003", "Name": "B01R03"},
            {"UnitID": "U001", "Name": "B01R01"},
            {"UnitID": "U002", "Name": "B01R02"},
            {"UnitID": "U003", "Name": "B01R03"},
            {"UnitID": "U001", "Name": "B01R01"},
            {"UnitID": "U002", "Name": "B01R02"},
            {"UnitID": "U003", "Name": "B01R03"},
        ],
        # UTILITY BILLS
        generateRandomeUtilityBills("Electricity"))

    @staticmethod
    def editUtility(originalID: str, type: str, unitName: str, status: str, billingCycle: str, installationDate) -> str:
        """
        Edits a utility with the given data.
        """
        print("Editing utility:", originalID, type, unitName, status, billingCycle, installationDate)
        return "Utility edited successfully"
    
    @staticmethod
    def deleteUtility(id: str) -> str:
        """
        Deletes a new utility with the given data.
        """
        print("Deleting utility:", id)
        return "Utility deleted successfully"
    
    @staticmethod
    def getUtilitiesByUnitID(unitName: str) -> list[dict[str, str]]:
        """
        Fetches all utilities with unit ID.
        """
        print("Fetching utilities by unit name:", unitName)
        return [
            {"UtilityID": "E001", "Type": "Electricity"},
            {"UtilityID": "W001", "Type": "Water"},
        ]
