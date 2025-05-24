from datetime import datetime, date
from dateutil.relativedelta import relativedelta

from PyQt6.QtCore import QDate

from src.models.BillDatabaseTable import BillDatabaseTable as Bill

from src.utils.constants import Range
from src.utils.formatMoney import formatMoney
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
        unitBills = Bill.getAllGroupedBills(range = range, offset=offsetInt)
        for utility in unitBills.keys():
            for bill in unitBills[utility]:
                bill["BillingPeriodEnd"] = bill["BillingPeriodEnd"].strftime("%Y-%m-%d")

        earliestBillDate = Bill.getEarliestBillDate() if Bill.getEarliestBillDate() is not None else date(1900, 1, 1)
        return unitBills,  datetime.now() - relativedelta(dt1=datetime.now(), dt2=datetime.combine(earliestBillDate,datetime.min.time())) + relativedelta(months=monthRange)

    @staticmethod
    def fetchBillsSummary(monthRange: int, currPage: datetime, filters : list[str]) -> tuple[str, str, str]:
        """
        Fetches the Total Balance of Period, Total Cost of Period , and Unpaid Bills.
        """
        range = None
        for r in Range:
            if r.value == monthRange:
                range = r
                break
        offsetInt = diffMonths(datetime.now(), currPage) // range.value + 1
        totalUnpaid, totalCost, unpaidBillCount = (formatMoney(Bill.unpaidBillsTotalSum(range, filters, offset=offsetInt)), 
                                formatMoney(Bill.billsTotalSum(range, filters, offset=offsetInt)),
                                str(Bill.unpaidBillsCount(range, filters, offset=offsetInt)))
        return (totalUnpaid, totalCost, unpaidBillCount)

    @staticmethod
    def fetchUpcomingBills() -> list[dict[str, str]]:
        """
        Fetches 15 upcoming bills.
        """
        print("Fetching upcoming bills")
        urgentBills = Bill.urgentBills()
        for bill in urgentBills:
            bill["BillID"] = str(bill["BillID"])
            bill["DueDate"] = bill["DueDate"].strftime("%B %d, %Y")

        return urgentBills