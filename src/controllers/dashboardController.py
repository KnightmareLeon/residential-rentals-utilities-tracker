class DashboardController:
    
    @staticmethod
    def fetchUtilityDashboard(monthRange: int) -> dict[str, list[dict[str, str]]]:
        """
        Fetches all bills per utility within a given range of months.
        """
        print(f"Fetching utility cost data for {monthRange} months")
        return {}
    
    @staticmethod
    def fetchBillsSummary(monthRange: int) -> tuple[float, float, int]:
        """
        Fetches the Total Balance of Period, Total Cost of Period , and Unpaid Bills.
        """
        print(f"Fetching bills summary for {monthRange} months")
        return (None, None, None)
    
    @staticmethod
    def fetchUpcomingBills() -> list[dict[str, str]]:
        """
        Fetches 15 upcoming bills.
        """
        print("Fetching upcoming bills")
        return []