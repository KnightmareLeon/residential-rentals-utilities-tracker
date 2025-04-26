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
    def viewUnit(id: str) -> tuple[dict[str, str], tuple[list[dict[str, str]], int]]:
        """
        Fetches all information about a single unit by ID.
        """
        print("Viewing unit:", id)

        return ({
            "UnitID": id,
            "Name": "B1R001",
            "Address": "123 Main St, New York, NY",
            "Type": "Individual",
        }, generateRandomUtilityData())

    @staticmethod
    def editUnit(originalID: str, unitID: str, name: str, address: str, type: str) -> str:
        """
        Edits a unit with the given data.
        """
        print("Editing unit:", originalID, unitID, name, address, type)
        return "Unit edited successfully"
    
    @staticmethod
    def deleteUnit(id: str) -> str:
        """
        Deletes a new unit with the given data.
        """
        print("Deleting unit:", id)
        return "Unit deleted successfully"