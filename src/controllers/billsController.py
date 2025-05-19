from PyQt6.QtCore import QDate

from src.utils.sampleDataGenerator import generateBillData

from src.models.BillDatabaseTable import BillDatabaseTable as Bill
from src.models.UnitDatabaseTable import UnitDatabaseTable as Unit
from src.models.UtilityDatabaseTable import UtilityDatabaseTable as Utility
from src.controllers.utilitiesController import UtilitiesController

class BillsController:
    
    @staticmethod
    def fetchBills(currentPage: int, sortingOrder: str, sortingField: str, searchValue: str) -> tuple[list[dict[str, str]], int]:
        """
        Fetches all units with pagination, sorting, and searching.
        """
        print(f"Fetching bills in page {currentPage} sorted by {sortingField} {sortingOrder} while searching for {searchValue}")
        
        searchValue = None if searchValue == "" else searchValue

        totalPages =  Bill.uniqueTotalCount(searchValue) // 50 + 1
        return Bill.uniqueRead(searchValue, sortingField, sortingOrder, page=currentPage), totalPages 
    
    @staticmethod
    def addBill(unitID: str, utilityID: str, totalAmount: str, billingPeriodStart: QDate, billingPeriodEnd: QDate, status: str, dueDate: QDate) -> str:
        """
        Adds a new unit with the given data.
        """
        
        if billingPeriodEnd <= billingPeriodStart:
            return "Billing Period End must be later than Billing Period Start"

        if dueDate <= billingPeriodStart:
            return "Due Date must be later than Billing Period Start"

        if totalAmount.strip() == "":
            return "Total Amount is required"
        
        amountValue = float(totalAmount)
        if amountValue >= 100000000:
            return "Total Amount must be less than 100,000,000"
        elif amountValue < 0:
            return "Total Amount cannot be negative"
        
        # Get unit ID using unitName and UtilityID using utilityType
        Bill.create({
            "UnitID": unitID,
            "UtilityID": utilityID,
            "TotalAmount": str(totalAmount),
            "BillingPeriodStart": billingPeriodStart.toString("yyyy-MM-dd"),
            "BillingPeriodEnd": billingPeriodEnd.toString("yyyy-MM-dd"),
            "Status": status,
            "DueDate": dueDate.toString("yyyy-MM-dd")
        })
        return "Bill added successfully"

    @staticmethod
    def viewBill(id: str) -> dict[str, str]:
        """
        Fetches all information about a single bill by ID.
        """
        id = int(id)
        billInfo = Bill.readOne(id)
        billInfo["Type"] = Utility.readOne(billInfo["UtilityID"])["Type"] if billInfo["UtilityID"] is not None else None
        billInfo["UnitName"] = Unit.readOne(billInfo["UnitID"])["Name"] if billInfo["UnitID"] is not None else None
        return billInfo

    @staticmethod
    def editBill(originalID: str, unitID: str, utilityID: str, status: str, totalAmount, dueDate, billingPeriodStart, billingPeriodEnd) -> str:
        """
        Edits a bill with the given data.
        Validates values and applies update to the database.
        """

        if str(utilityID).isdigit():
            utilityID = int(utilityID)
        else:
            utilities = UtilitiesController.getUtilitiesByUnitID(unitID)
            for utility in utilities:
                if utility["Type"] == utilityID:
                    utilityID = utility["UtilityID"]
                    break
            else:
                return f"No Utilities found for this unit"

        amountText = str(totalAmount).strip()
        if amountText == "":
            return "Total Amount is required"

        amountValue = float(amountText)
        if amountValue >= 100000000:
            return "Total Amount must be less than 100,000,000"
        if amountValue < 0:
            return "Total Amount cannot be negative"

        if billingPeriodEnd <= billingPeriodStart:
            return "Billing Period End must be later than Billing Period Start"

        if dueDate <= billingPeriodStart:
            return "Due Date must be later than Billing Period Start"

        print("Editing bill:", originalID, unitID, utilityID, amountValue, billingPeriodStart, billingPeriodEnd, status, dueDate)
        editedColumns = {
            "UnitID": unitID,
            "UtilityID": utilityID,
            "TotalAmount": str(amountValue),
            "BillingPeriodStart": billingPeriodStart,
            "BillingPeriodEnd": billingPeriodEnd,
            "Status": status,
            "DueDate": dueDate
        }

        Bill.update(int(originalID), editedColumns)
        return "Bill edited successfully"
        
    @staticmethod
    def deleteBill(id: str) -> str:
        """
        Deletes a new unit with the given data.
        """
        print("Deleting bill:", id)
        Bill.delete([int(id)])
        return "Bill deleted successfully"