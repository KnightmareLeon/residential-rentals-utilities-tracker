class UtilitiesController:
    
    @staticmethod
    def fetchData(currentPage: int, sortingOrder: str, sortingField: str, searchValue: str) -> tuple[list[dict[str, str]], int]:
        print(f"Fetching data for page {currentPage} with sorting {sortingField} {sortingOrder} and search '{searchValue}'")
        return ([], 5) 
    
    @staticmethod
    def addRecord(data: dict[str, str]) -> str:
        print("Adding utility:", data)
        return "Utility added successfully"

    @staticmethod
    def viewRecord(id: str) -> dict[str, str]:
        print("Viewing utility:", id)

    @staticmethod
    def editRecord(id: str, data: dict[str, str]) -> str:
        print("Editing utility:", id, data)
        return "Utility edited successfully"
    
    @staticmethod
    def deleteRecord(id: str) -> str:
        print("Deleting utility:", id)
        return "Utility deleted successfully"