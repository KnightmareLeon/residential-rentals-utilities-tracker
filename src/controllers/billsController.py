from PyQt6.QtCore import QDate

from src.utils.sampleDataGenerator import generateBillData

from src.models.BillDatabaseTable import BillDatabaseTable as Bill

class BillsController:
    
    @staticmethod
    def fetchBills(currentPage: int, sortingOrder: str, sortingField: str, searchValue: str) -> tuple[list[dict[str, str]], int]:
        """
        Fetches all units with pagination, sorting, and searching.
        """
        print(f"Fetching bills in page {currentPage} sorted by {sortingField} {sortingOrder} while searching for {searchValue}")
        
        searchValue = None if searchValue == "" else searchValue
        referred = {"unit":["Name"],"utility":["Type"]}
        columns = ["BillID", "TotalAmount", "DueDate", "Status"]
        totalPages =  Bill.totalCount(columns=columns, referred=referred, searchValue=searchValue) // 50 + 1
        return Bill.read(columns=columns, referred=referred, page=currentPage, sortBy=sortingField, order=sortingOrder, searchValue=searchValue), totalPages 
    
    @staticmethod
    def addBill(unitID: str, utilityID: str, totalAmount: str, billingPeriodStart: QDate, billingPeriodEnd: QDate, status: str, dueDate: QDate) -> str:
        """
        Adds a new unit with the given data.
        """
        # Get unit ID using unitName and UtilityID using utilityType
        print("Adding bill:", unitID, utilityID, totalAmount, billingPeriodStart, billingPeriodEnd, status, dueDate)
        return "Bill added successfully"

    @staticmethod
    def viewBill(id: str) -> dict[str, str]:
        """
        Fetches all information about a single bill by ID.
        """
        return {
            "BillID": id,
            "UnitName": "B01R02",
            "UtilityID": "E001",
            "Type": "Electricity",
            "TotalAmount": "100.00",
            "BillingPeriodStart": QDate.currentDate().addMonths(-1),
            "BillingPeriodEnd": QDate.currentDate(),
            "Status": "Paid",
            "DueDate": QDate.currentDate()
        }

    @staticmethod
    def editBill(originalID: str, unitID: str, utilityID: str, totalAmount: str, billingPeriodStart: QDate, billingPeriodEnd: QDate, status: str, dueDate: QDate) -> str:
        """
        Edits a unit with the given data.
        """
        print("Editing bill:", originalID, unitID, utilityID, totalAmount, billingPeriodStart, billingPeriodEnd, status, dueDate)
        return "Bill edited successfully"
    
    @staticmethod
    def deleteBill(id: str) -> str:
        """
        Deletes a new unit with the given data.
        """
        print("Deleting bill:", id)
        return "Bill deleted successfully"