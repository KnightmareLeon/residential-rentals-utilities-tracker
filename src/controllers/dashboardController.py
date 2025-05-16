from datetime import datetime, date
from dateutil.relativedelta import relativedelta

from PyQt6.QtCore import QDate

from src.models.BillDatabaseTable import BillDatabaseTable as Bill

from src.utils.constants import Range
from src.utils.formatMoney import formatMoney
from src.utils.sampleDataGenerator import generateRandomUtilityData
from src.utils.diffMonths import diffMonths

class DashboardController:

    @staticmethod
    def fetchUtilityDashboard(monthRange: int, offset: datetime) -> tuple[dict[str, list[dict[str, str]]], datetime]:
        """
        Fetches all bills per utility within a given range of months as well as the total number of pages needed for the monthRange.
        """
        print(f"Fetching utility cost data for {monthRange} months and page {offset}")
        range = None
        for r in Range:
            if r.value == monthRange:
                range = r
                break
        offsetInt = (diffMonths(datetime.now(), offset)) // range.value + 1
        unitBills = Bill.getAllUnitsBills(range = range, offset=offsetInt)
        for utility in unitBills.keys():
            for bill in unitBills[utility]:
                bill["BillingPeriodEnd"] = bill["BillingPeriodEnd"].strftime("%Y-%m-%d")
        
        earliestBillDates = Bill.getEarliestBillDate() if Bill.getEarliestBillDate() is not None else date(1900, 1, 1)
        monthsDiff = diffMonths(datetime.now(), datetime.combine(earliestBillDates, datetime.min.time()))
        return unitBills,  datetime.now() - relativedelta(months=monthsDiff)
    
    @staticmethod
    def fetchBillsSummary(monthRange: int, currPage: QDate) -> tuple[str, str, int]:
        """
        Fetches the Total Balance of Period, Total Cost of Period , and Unpaid Bills.
        """
        range = None
        for r in Range:
            if r.value == monthRange:
                range = r
                break
        offsetInt = diffMonths(datetime.now(), currPage) + 1
        balance, paid, unpaid = (formatMoney(Bill.billsTotalSum(range=range, offset=offsetInt)), 
                                 formatMoney(Bill.billsTotalSum(range=range, offset=offsetInt, paidOnly=True)),
                                 str(Bill.unpaidBillsCount(range=range, offset=offsetInt)))
        return (balance, paid, unpaid)
    
    @staticmethod
    def fetchUpcomingBills() -> list[dict[str, str]]:
        """
        Fetches 15 upcoming bills.
        """
        print("Fetching upcoming bills")
        urgentBills = Bill.urgentBills()
        for bill in urgentBills:
            bill["BillID"] = str(bill["BillID"])
            bill["DueDate"] = bill["DueDate"].strftime("%Y-%m-%d")

        return urgentBills
    
    