from .DatabaseTable import DatabaseTable
from .DatabaseConnection import DatabaseConnection

class UnitDatabaseTable(DatabaseTable):
    """
    This class represents the unit table in the database.
    It inherits from the DatabaseTable class and provides methods to interact with the table.
    The table stores information about units of the boarding house.
    The table has the following columns:
    - UnitID: int, primary key, auto-incremented
    - Name: varchar(30), unique, not null
    - Address: varchar(255), not null
    - Type: The type of unit (shared or individual).
    - PRIMARY KEY (UnitID)
    - UNIQUE KEY Name (Name)
    """

    _tableName = "unit"

    @classmethod  
    def _createTable(cls):
        try:
            cursor = DatabaseConnection.getConnection().cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS unit( " +
                "UnitID int NOT NULL AUTO_INCREMENT, " +
                "Name varchar(30) NOT NULL, " +
                "Address varchar(255) NOT NULL, "
                "Type enum('Shared','Individual') NOT NULL," +
                "PRIMARY KEY (UnitID), " +
                "UNIQUE KEY Name (Name))"
            )
        except Exception as e:
            print(f"Error: {e}")
            raise e
        finally:
            cursor.close()
    
    @classmethod
    def batchUpdate(cls, 
                    keys : list[int],
                    data : dict[str, str]):
        """
        Batch update the unit table with the given keys and data.
        - keys: list of integers representing the primary keys of the rows to be updated.
        - data: dictionary where the keys are the column names and the values are the new values to be set.
        """
        cls.initialize()
        
        if not isinstance(keys, list):
                raise TypeError("Keys must be a list.")
        if not isinstance(data, dict):
            raise TypeError("Data must be a dict.")
        if not all(isinstance(key, int) for key in keys):
            raise TypeError("Keys must be a list of integers.")
        for column in data.keys():
            if not isinstance(column, str):
                raise TypeError("Data keys must be strings.")
            if not isinstance(data[column], str):
                raise TypeError("Data values must be strings.")
            if column not in cls._columns:
                raise ValueError(f"Column {column} is not a valid column name.")
            if column == cls._primaryKey:
                raise ValueError(f"Cannot update primary key {cls._primaryKey}.")
        try:
            
            cursor = DatabaseConnection.getConnection().cursor()
            sql = f"UPDATE {cls._tableName} SET "
            sql += ", ".join([f"{column} = '{value}'" for column, value in data.items()])
            sql += " WHERE " + " AND ".join([f"{cls._primaryKey} = {key}" for key in keys])
            cursor.execute(sql)
            
        except Exception as e:
            print(f"Error: {e}")
            raise e
        finally:
            cursor.close()
        return
    
    @classmethod
    def doesUnitNameExist(cls, name: str) -> bool:
        """
        Check if a unit name exists in the database.
        - name: string representing the unit name to check.
        """
        cls.initialize()
        if not isinstance(name, str):
            raise TypeError("Name must be a string.")
        result = None
        try:
            cursor = DatabaseConnection.getConnection().cursor()
            sql = f"SELECT * FROM {cls._tableName} WHERE Name = '{name}'"
            cursor.execute(sql)
            result = cursor.fetchone()
        except Exception as e:
            print(f"Error: {e}")
            raise e
        finally:
            cursor.close()

        return result is not None