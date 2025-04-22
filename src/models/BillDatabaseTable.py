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
                  range: str) -> dict[str, list[dict[str, str]]]:
        """
        Returns a dictionary of bills for the given unit ID and range.
        The dictionary keys are the utility types, and the values are lists of bills.
        Each bill is represented as a dictionary with keys: BillID, TotalAmount, BillingPeriodEnd.
        The range can be one of the following: 1m, 3m, 6m, 1y.
        1m: Last month
        3m: Last 3 months
        6m: Last 6 months
        1y: Last year
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
            
            rangeClause = ""
            if range == "1m":
                rangeClause = "AND Bill.BillingPeriodEnd >= DATE_SUB(CURDATE(), INTERVAL 1 MONTH)"
            elif range == "3m":
                rangeClause = "AND Bill.BillingPeriodEnd >= DATE_SUB(CURDATE(), INTERVAL 3 MONTH)"
            elif range == "6m":
                rangeClause = "AND Bill.BillingPeriodEnd >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH)"
            elif range == "1y":
                rangeClause = "AND Bill.BillingPeriodEnd >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR)"

            cursor = DatabaseConnection.getConnection().cursor(dictionary = True)
            for utilityID in InstalledUtilityDatabaseTable.getUnitUtilities(unit):
                sql1 = f"SELECT Type FROM {UtilityDatabaseTable.getTableName()} WHERE UtilityID = {utilityID}"
                cursor.execute(sql1)
                utilityType = cursor.fetchone()['Type']

                sql2 = f"SELECT Bill.BillID, Bill.TotalAmount, Bill.BillingPeriodEnd FROM {cls.getTableName()} WHERE Bill.UtilityID = {utilityID} AND Bill.UnitID = {unit} {rangeClause}"
                cursor.execute(sql2)
                result[utilityType] = cursor.fetchall()

        except Exception as e:
            print(f"Error: {e}")
            raise e
        finally:
            cursor.close()
        return result
