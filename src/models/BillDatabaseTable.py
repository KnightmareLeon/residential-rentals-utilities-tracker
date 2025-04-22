from models.DatabaseTable import DatabaseTable
from models.DatabaseConnection import DatabaseConnection
from models.UnitDatabaseTable import UnitDatabaseTable
from models.UtilityDatabaseTable import UtilityDatabaseTable
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
                  unit : int) -> list[dict[str, any]]:
        """
        Returns a list of dictionaries containing the unit costs for each utility.
        The list contains dictionaries with the following keys:
        """
        result = []
        try:
            if not isinstance(unit, int):
                raise ValueError("Unit must be an integer.")
            cursor = DatabaseConnection.getConnection().cursor(dictionary = True)
            sql = f"SELECT Utility.Type, Bill.TotalAmount, Bill.DueDate, Bill.Status FROM {cls.getTableName()} INNER JOIN utility ON Bill.UtilityID=Utility.UtilityID WHERE Bill.UnitID = {unit}"
            cursor.execute(sql)
            result = cursor.fetchall()
        except Exception as e:
            print(f"Error: {e}")
            raise e
        finally:
            cursor.close()
        return result
