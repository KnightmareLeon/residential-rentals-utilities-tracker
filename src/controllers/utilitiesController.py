class UtilitiesController:
    
    @staticmethod
    def fetchUtilities(currentPage: int, sortingOrder: str, sortingField: str, searchValue: str) -> tuple[list[dict[str, str]], int]:
        """
        Fetches all utilitys with pagination, sorting, and searching.
        """
        print(f"Fetching data for page {currentPage} with sorting {sortingField} {sortingOrder} and search '{searchValue}'")
        return ([], 5) 
    
    @staticmethod
    def addUtility(type: str, status: str, billingCycle: str) -> str:
        """
        Adds a new utility with the given data.
        """
        print("Adding utility:", type, status, billingCycle)    
        return "Utility added successfully"

    @staticmethod
    def viewUtility(id: str) -> dict[str, str]:
        """
        Fetches all information about a single utility by ID.
        """
        print("Viewing utility:", id)

    @staticmethod
    def editUtility(originalID: str, type: str, status: str, billingCycle: str) -> str:
        """
        Edits a utility with the given data.
        """
        print("Editing utility:", originalID, type, status, billingCycle)
        return "Utility edited successfully"
    
    @staticmethod
    def deleteUtility(id: str) -> str:
        """
        Deletes a new utility with the given data.
        """
        print("Deleting utility:", id)
        return "Utility deleted successfully"