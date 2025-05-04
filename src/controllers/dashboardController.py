from datetime import datetime
from dateutil.relativedelta import relativedelta

class DashboardController:
    
    @staticmethod
    def fetchUtilityDashboard(monthRange: int, currPage: int) -> tuple[dict[str, list[dict[str, str]]], int]:
        """
        Fetches all bills per utility within a given range of months as well as the total number of pages needed for the monthRange.
        """
        print(f"Fetching utility cost data for {monthRange} months and page {currPage}")
        return ({}, datetime.now() - relativedelta(months=48))
    
    @staticmethod
    def fetchBillsSummary(monthRange: int, currPage: int) -> tuple[float, float, int]:
        """
        Fetches the Total Balance of Period, Total Cost of Period , and Unpaid Bills.
        """
        print(f"Fetching bills summary for {monthRange} months and page {currPage}")
        return (None, None, None)
    
    @staticmethod
    def fetchUpcomingBills() -> list[dict[str, str]]:
        """
        Fetches 15 upcoming bills.
        """
        print("Fetching upcoming bills")
        return [
            {
                "BillID": 1,
                "Type": "Electricity",
                "TotalAmount": "6021.90",
                "DueDate": "Mar 30",
                "Status": "Overdue"
            },
            {
                "BillID": 2,
                "Type": "Water",
                "TotalAmount": "1245.75",
                "DueDate": "Apr 05",
                "Status": "Unpaid"
            },
            {
                "BillID": 3,
                "Type": "Internet",
                "TotalAmount": "1899.00",
                "DueDate": "Apr 02",
                "Status": "Paid"
            },
            {
                "BillID": 4,
                "Type": "Electricity",
                "TotalAmount": "5487.30",
                "DueDate": "Mar 28",
                "Status": "Overdue"
            },
            {
                "BillID": 5,
                "Type": "Water",
                "TotalAmount": "1320.50",
                "DueDate": "Apr 10",
                "Status": "Unpaid"
            },
            {
                "BillID": 6,
                "Type": "Internet",
                "TotalAmount": "1799.00",
                "DueDate": "Apr 01",
                "Status": "Paid"
            },
            {
                "BillID": 7,
                "Type": "Electricity",
                "TotalAmount": "6100.00",
                "DueDate": "Apr 06",
                "Status": "Unpaid"
            },
            {
                "BillID": 8,
                "Type": "Water",
                "TotalAmount": "1100.80",
                "DueDate": "Apr 09",
                "Status": "Unpaid"
            },
            {
                "BillID": 9,
                "Type": "Internet",
                "TotalAmount": "1999.00",
                "DueDate": "Apr 03",
                "Status": "Overdue"
            },
            {
                "BillID": 10,
                "Type": "Electricity",
                "TotalAmount": "5890.45",
                "DueDate": "Apr 08",
                "Status": "Unpaid"
            },
            {
                "BillID": 11,
                "Type": "Water",
                "TotalAmount": "1185.60",
                "DueDate": "Apr 07",
                "Status": "Paid"
            }
        ]

    
    