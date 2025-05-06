from PyQt6.QtCore import QDate

from src.utils.sampleDataGenerator import generateBillData

from models.BillDatabaseTable import BillDatabaseTable as Bill
from models.UnitDatabaseTable import UnitDatabaseTable as Unit
from models.UtilityDatabaseTable import UtilityDatabaseTable as Utility

class BillsController:
    
    @staticmethod
    def fetchBills(currentPage: int, sortingOrder: str, sortingField: str, searchValue: str) -> tuple[list[dict[str, str]], int]:
        """
        Fetches all units with pagination, sorting, and searching.
        """
        print(f"Fetching data for page {currentPage} with sorting {sortingField} {sortingOrder} and search '{searchValue}'")
        
        if searchValue == "":
            totalPages =  Bill.totalCount() // 50 + 1
            return Bill.read(referred={Unit:["Name"],Utility:["Type"]}, page=currentPage, sortBy=sortingField, order=sortingOrder), totalPages
        totalPages =  Bill.totalCount(searchValue=searchValue) // 50 + 1
        return Bill.read(referred={Unit:["Name"],Utility:["Type"]}, page=currentPage, sortBy=sortingField, order=sortingOrder, searchValue=searchValue), totalPages 
    
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