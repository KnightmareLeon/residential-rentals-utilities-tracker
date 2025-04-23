from models.DatabaseTable import DatabaseTable
from models.DatabaseConnection import DatabaseConnection
from models.UnitDatabaseTable import UnitDatabaseTable
from models.UtilityDatabaseTable import UtilityDatabaseTable
from models.InstalledUtilityDatabaseTable import InstalledUtilityDatabaseTable

class BillDatabaseTable(DatabaseTable):

    _tableName = "bill"
    referredTables = [UnitDatabaseTable, UtilityDatabaseTable]

    @classmethod  
    def _createTable(cls):
        try:
            cursor = DatabaseConnection.getConnection().cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS bill ( " +
                "BillID int NOT NULL, " +
                "UnitID int DEFAULT NULL, " +
                "UtilityID int DEFAULT NULL, " +
                "TotalAmount decimal(10,2) NOT NULL, " +
                "BillingPeriodStart date NOT NULL, " +
                "BillingPeriodEnd date NOT NULL, " +
                "Status enum('Unpaid','Paid','Partially Paid','Overdue') NOT NULL, " +
                "DueDate date NOT NULL, " +
                "PRIMARY KEY (BillID), " +
                "KEY UnitID (UnitID), " +
                "KEY UtilityID (UtilityID), " +
                "CONSTRAINT bill_ibfk_1 FOREIGN KEY (UnitID) REFERENCES unit (UnitID) ON DELETE SET NULL ON UPDATE CASCADE, " +
                "CONSTRAINT bill_ibfk_2 FOREIGN KEY (UtilityID) REFERENCES utility (UtilityID) ON DELETE SET NULL ON UPDATE CASCADE, " +
                "CONSTRAINT bill_chk_1 CHECK ((BillingPeriodEnd > BillingPeriodStart)), " +
                "CONSTRAINT bill_chk_2 CHECK ((DueDate > BillingPeriodEnd)))"
            )
        except Exception as e:
            print(f"Error: {e}")
            raise e
        finally:
            cursor.close()

    @classmethod
    def unitBills(cls,
                  unit : int,
                  range: str) -> dict[str, list[dict[str, any]]]:
        """
        Returns a dictionary of bills for the given unit ID and range.
        The dictionary keys are the utility types, and the values are lists of bills.
        Each bill is represented as a dictionary with keys: BillID, TotalAmount, BillingPeriodEnd.
        
        The range can be one of the following: 1m, 3m, 6m, 1y.
        - 1m: Last month
        - 3m: Last 3 months
        - 6m: Last 6 months
        - 1y: Last year
        """
        if not cls._initialized:
            cls._initialize()
            cls._initialized = True
        result = {}
        try:
            if not isinstance(unit, int):
                raise ValueError("Unit must be an integer.")
            if not isinstance(range, str):
                raise ValueError("Range must be a string.")
            if not range in ["1m", "3m", "6m", "1y"]:
                raise ValueError("Range must be one of the following: 1m, 3m, 6m, 1y.")

            cursor = DatabaseConnection.getConnection().cursor(dictionary = True)
            for utilityID in InstalledUtilityDatabaseTable.getUnitUtilities(unit):
                sql = f"SELECT Type FROM {UtilityDatabaseTable.getTableName()} WHERE UtilityID = {utilityID}"
                cursor.execute(sql)
                utilityType = cursor.fetchone()['Type']

                result[utilityType] = cls.utilityBills(utilityID, range)

        except Exception as e:
            print(f"Error: {e}")
            raise e
        finally:
            cursor.close()
        return result

    @classmethod
    def allUnitsBills(cls,
                      range: str) -> dict[str, list[dict[str, any]]]:
        """
        Returns a dictionary of all bills for the given range.
        The dictionary keys are the utility types, and the values are lists of bills.
        Each bill is represented as a dictionary with keys: BillID, TotalAmount, BillingPeriodEnd.
        """
        if not cls._initialized:
            cls._initialize()
            cls._initialized = True
        result = {}
        try:
            if not isinstance(range, str):
                raise ValueError("Range must be a string.")
            if not range in ["1m", "3m", "6m", "1y"]:
                raise ValueError("Range must be one of the following: 1m, 3m, 6m, 1y.")

            rangeClause = cls.__rangeClause(range)

            cursor = DatabaseConnection.getConnection().cursor(dictionary = True)
            for utility in ["Electricity", "Water", "Gas", "Wifi", "Trash", "Maintenance", "Miscellaneous"]:
                sql = f"SELECT Bill.BillID, Bill.TotalAmount, Bill.BillingPeriodEnd FROM bill " + \
                    f"INNER JOIN utility ON Utility.UtilityID=Bill.UtilityID WHERE Utility.Type='{utility}'" + \
                    f"AND {rangeClause} "             
                cursor.execute(sql)

                result[utility] = cursor.fetchall()

        except Exception as e:
            print(f"Error: {e}")
            raise e
        finally:
            cursor.close()
        return result

    @classmethod
    def utilityBills(cls,
                     utility : int,
                     range: str) -> list[dict[str, any]]:
        """
        Returns a list of bills for the given utility ID and range.
        Each bill is represented as a dictionary with keys: BillID, UnitID, TotalAmount, BillingPeriodEnd.
        """
        if not cls._initialized:
            cls._initialize()
            cls._initialized = True
        result = []
        try:
            if not isinstance(utility, int):
                raise ValueError("Utility must be an integer.")
            if not isinstance(range, str):
                raise ValueError("Range must be a string.")
            if not range in ["1m", "3m", "6m", "1y"]:
                raise ValueError("Range must be one of the following: 1m, 3m, 6m, 1y.")
            
            rangeClause = "AND " + cls.__rangeClause(range)

            cursor = DatabaseConnection.getConnection().cursor(dictionary = True)
            sql = f"SELECT Bill.BillID, Bill.TotalAmount, Bill.BillingPeriodEnd FROM {cls.getTableName()} WHERE Bill.UtilityID = {utility} {rangeClause}"
            cursor.execute(sql)
            result = cursor.fetchall()

        except Exception as e:
            print(f"Error: {e}")
            raise e
        finally:
            cursor.close()
        return result

    @classmethod
    def totalSumBills(cls,
                      range: str,
                      paidOnly: bool = False) -> float:
        """
        Returns the total sum of all bills for the given range.
        The range can be one of the following: 1m, 3m, 6m, 1y.
        """
        if not cls._initialized:
            cls._initialize()
            cls._initialized = True
        result = 0.0
        try:
            if not isinstance(range, str):
                raise ValueError("Range must be a string.")
            if not range in ["1m", "3m", "6m", "1y"]:
                raise ValueError("Range must be one of the following: 1m, 3m, 6m, 1y.")
            if not isinstance(paidOnly, bool):
                raise ValueError("PaidOnly must be a boolean.")
            
            whereClause = cls.__rangeClause(range)

            if paidOnly:
                whereClause += " AND Bill.Status = 'Paid'"
            cursor = DatabaseConnection.getConnection().cursor(dictionary = True)
            sql = f"SELECT SUM(Bill.TotalAmount) AS TotalAmount FROM {cls.getTableName()} WHERE {whereClause}"
            cursor.execute(sql)
            result = cursor.fetchone()['TotalAmount']

        except Exception as e:
            print(f"Error: {e}")
            raise e
        finally:
            cursor.close()
        return result
    
    @classmethod
    def unpaidBillsCount(cls,
                         range: str) -> int:
        """
        Returns the total count of unpaid bills for the given range.
        The range can be one of the following: 1m, 3m, 6m, 1y.
        """
        if not cls._initialized:
            cls._initialize()
            cls._initialized = True
        result = 0
        try:
            if not isinstance(range, str):
                raise ValueError("Range must be a string.")
            if not range in ["1m", "3m", "6m", "1y"]:
                raise ValueError("Range must be one of the following: 1m, 3m, 6m, 1y.")
            
            rangeClause = cls.__rangeClause(range)

            cursor = DatabaseConnection.getConnection().cursor(dictionary = True)
            sql = f"SELECT COUNT(Bill.BillID) AS UnpaidCount FROM {cls.getTableName()} WHERE {rangeClause} AND Bill.Status != 'Paid'"
            cursor.execute(sql)
            result = cursor.fetchone()['UnpaidCount']

        except Exception as e:
            print(f"Error: {e}")
            raise e
        finally:
            cursor.close()
        return result

    @classmethod
    def urgentBills(cls,
                    limit: int = 15) -> list[dict[str, any]]:
        """
        Returns a list of urgent bills.
        An urgent bill is defined as a bill that is not yet paid.
        The list is limited to the specified number of bills.
        """
        if not cls._initialized:
            cls._initialize()
            cls._initialized = True
        result = []
        try:
            if not isinstance(limit, int):
                raise ValueError("Limit must be an integer.")
            if limit <= 0:
                raise ValueError("Limit must be greater than 0.")
            
            cursor = DatabaseConnection.getConnection().cursor(dictionary = True)
            sql = f"SELECT Bill.BillID, Utility.Type, Bill.TotalAmount, Bill.DueDate, Bill.Status, " + \
                f"DATEDIFF(Bill.DueDate, CURDATE()) AS closest FROM {cls.getTableName()} " + \
                f"JOIN {UtilityDatabaseTable.getTableName()} ON Bill.UtilityID = Utility.UtilityID " + \
                f"WHERE Bill.Status != 'Paid'" + \
                f"ORDER BY closest ASC LIMIT {limit}"
            cursor.execute(sql)
            result = cursor.fetchall()

        except Exception as e:
            print(f"Error: {e}")
            raise e
        finally:
            cursor.close()
        return result

    @classmethod
    def __rangeClause(cls,
                      range: str) -> str:
        """
        Returns the range clause for the given range.
        The range can be one of the following: 1m, 3m, 6m, 1y.
        """
        rangeClause = ""
        if range == "1m":
            rangeClause = "Bill.BillingPeriodEnd >= DATE_SUB(CURDATE(), INTERVAL 1 MONTH)"
        elif range == "3m":
            rangeClause = "Bill.BillingPeriodEnd >= DATE_SUB(CURDATE(), INTERVAL 3 MONTH)"
        elif range == "6m":
            rangeClause = "Bill.BillingPeriodEnd >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH)"
        elif range == "1y":
            rangeClause = "Bill.BillingPeriodEnd >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR)"
        return rangeClause