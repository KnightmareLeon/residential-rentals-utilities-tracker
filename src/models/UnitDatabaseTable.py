from models.DatabaseTable import DatabaseTable
from models.DatabaseConnection import DatabaseConnection

class UnitDatabaseTable(DatabaseTable):

    _tableName = "unit"

    @classmethod  
    def _createTable(cls):
        try:
            cursor = DatabaseConnection.getConnection().cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS unit( " +
                "UnitID int NOT NULL AUTO_INCREMENT, " +
                "Name varchar(30) NOT NULL, " +
                "Address varchar(255) NOT NULL, " +
                "PRIMARY KEY (UnitID), " +
                "UNIQUE KEY Name (Name))"
            )
        except Exception as e:
            print(f"Error: {e}")
            raise e
        finally:
            cursor.close()