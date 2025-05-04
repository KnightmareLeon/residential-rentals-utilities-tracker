from src.utils.sampleDataGenerator import generateRandomUtilityData

class UnitsController:
    
    @staticmethod
    def fetchUnits(currentPage: int, sortingOrder: str, sortingField: str, searchValue: str) -> tuple[list[dict[str, str]], int]:
        """
        Fetches all units with pagination, sorting, and searching.
        """
        print(f"Fetching data for page {currentPage} with sorting {sortingField} {sortingOrder} and search '{searchValue}'")
        return ([], 5) 
    
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

        return ({ # UNIT INFO
            "UnitID": id,
            "Name": "B1R001",
            "Address": "Block 2, Room 12, 123 Main St, New York, NY, Block 2, Room 12, 123 Main St, New York, NY",
            "Type": "Individual",
        }, 
        [ # INSTALLED UTILITIES
            {"UtilityID": "U1", "Type": "Electricity", "Status": "Active", "isShared": False},
            {"UtilityID": "U2", "Type": "Water", "Status": "Inactive", "isShared": False},
            {"UtilityID": "U3", "Type": "Gas", "Status": "Active", "isShared": True},
            {"UtilityID": "U4", "Type": "Internet", "Status": "Inactive", "isShared": True},
            {"UtilityID": "U5", "Type": "Trash", "Status": "Active", "isShared": False},
            {"UtilityID": "U6", "Type": "Maintenance", "Status": "Inactive", "isShared": False},
            {"UtilityID": "U7", "Type": "Miscellaneous", "Status": "Active", "isShared": True},
        ], 
        # UNIT UTILITY BILLS 
        generateRandomUtilityData())

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