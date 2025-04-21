from PyQt6.QtCore import QDate

class BillsController:
    
    @staticmethod
    def fetchBills(currentPage: int, sortingOrder: str, sortingField: str, searchValue: str) -> tuple[list[dict[str, str]], int]:
        """
        Fetches all units with pagination, sorting, and searching.
        """
        print(f"Fetching data for page {currentPage} with sorting {sortingField} {sortingOrder} and search '{searchValue}'")
        return ([], 5) 
    
    @staticmethod
    def addBill(unitID: str, utilityID: str, totalAmount: str, billingPeriodStart: QDate, billingPeriodEnd: QDate, status: str, dueDate: QDate) -> str:
        """
        Adds a new unit with the given data.
        """
        print("Adding bill:", unitID, utilityID, totalAmount, billingPeriodStart, billingPeriodEnd, status, dueDate)
        return "Bill added successfully"

    @staticmethod
    def viewBill(id: str) -> dict[str, str]:
        """
        Fetches all information about a single unit by ID.
        """
        print("Viewing bill:", id)

    @staticmethod
    def editBill(originalID: str, unitID: str, utilityID: str, totalAmount: str, billingPeriodStart: QDate, billingPeriodEnd: QDate, status: str, dueDate: QDate) -> str:
        """
        Edits a unit with the given data.
        """
        print("Editing utility:", originalID, unitID, utilityID, totalAmount, billingPeriodStart, billingPeriodEnd, status, dueDate)
        return "Bill edited successfully"
    
    @staticmethod
    def deleteBill(id: str) -> str:
        """
        Deletes a new unit with the given data.
        """
        print("Deleting bill:", id)
        return "Bill deleted successfully"