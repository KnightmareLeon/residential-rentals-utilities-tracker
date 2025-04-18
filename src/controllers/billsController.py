class BillsController:
    
    @staticmethod
    def fetchData(currentPage: int, sortingOrder: str, sortingField: str, searchValue: str) -> tuple[list[dict[str, str]], int]:
        print(f"Fetching data for page {currentPage} with sorting {sortingField} {sortingOrder} and search '{searchValue}'")
        return ([], 5) 
    
    @staticmethod
    def addRecord(data: dict[str, str]) -> str:
        print("Adding bill:", data)
        return "Bill added successfully"

    @staticmethod
    def viewRecord(id: str) -> dict[str, str]:
        print("Viewing bill:", id)

    @staticmethod
    def editRecord(id: str, data: dict[str, str]) -> str:
        print("Editing utility:", id, data)
        return "Bill edited successfully"
    
    @staticmethod
    def deleteRecord(id: str) -> str:
        print("Deleting bill:", id)
        return "Bill deleted successfully"