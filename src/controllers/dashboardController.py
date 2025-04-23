class DashboardController:
    
    @staticmethod
    def fetchUtilityDashboard(monthRange: int, currPage: int) -> tuple[dict[str, list[dict[str, str]]], int]:
        """
        Fetches all bills per utility within a given range of months as well as the total number of pages needed for the monthRange.
        """
        print(f"Fetching utility cost data for {monthRange} months and page {currPage}")
        return ({}, 1)
    
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
        return []