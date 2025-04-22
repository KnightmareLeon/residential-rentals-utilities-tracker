from models.DatabaseTable import DatabaseTable
from models.DatabaseConnection import DatabaseConnection

class UtilityDatabaseTable(DatabaseTable):

    _tableName = "utility"

    @classmethod  
    def _createTable(cls):
        try:
            cursor = DatabaseConnection.getConnection().cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS utility (" +
                "UtilityID int NOT NULL, " + 
                "Type enum('Electricity','Water','Gas','Wifi','Trash','Maintenance','Miscellaneous') NOT NULL, " +
                "Status enum('Active','Inactive') NOT NULL, " +
                "BillingCycle enum('Monthly','Quarterly','Annually','Irregular') NOT NULL," +
                "PRIMARY KEY (UtilityID))"
            )
        except Exception as e:
            print(f"Error: {e}")
            raise e
        finally:
            cursor.close()