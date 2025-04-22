from models.DatabaseTable import DatabaseTable
from models.DatabaseConnection import DatabaseConnection
from models.UnitDatabaseTable import UnitDatabaseTable
from models.UtilityDatabaseTable import UtilityDatabaseTable

class InstalledUtilityDatabaseTable(DatabaseTable):

    _tableName = "installedutility"
    referredTables = [UnitDatabaseTable, UtilityDatabaseTable]
    
    def _createTable(cls):
        try:
            cursor = DatabaseConnection.getConnection().cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS installedutility ( " +
                "UnitID int NOT NULL, " +
                "UtilityID int NOT NULL, " +
                "InstallationDate date NOT NULL, " +
                "PRIMARY KEY (UnitID,UtilityID), " +
                "KEY UtilityID (UtilityID), " +
                "CONSTRAINT installedutility_ibfk_1 FOREIGN KEY (UnitID) REFERENCES unit (UnitID) ON DELETE CASCADE ON UPDATE CASCADE, " +
                "CONSTRAINT installedutility_ibfk_2 FOREIGN KEY (UtilityID) REFERENCES utility (UtilityID) ON DELETE CASCADE ON UPDATE CASCADE)"
            )
        except Exception as e:
            print(f"Error: {e}")
            raise e
        finally:
            cursor.close()

    @classmethod
    def delete(cls, keys : list[int]):
        """
        Disabled the delete method for this class, to delete data from the table,
        use the delete method of either the Unit or Utility class."""
        pass
