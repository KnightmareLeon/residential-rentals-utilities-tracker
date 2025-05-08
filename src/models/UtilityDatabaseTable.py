from .DatabaseTable import DatabaseTable
from .DatabaseConnection import DatabaseConnection

class UtilityDatabaseTable(DatabaseTable):
    """
    This class represents the utility table in the database.
    It inherits from the DatabaseTable class and provides methods to interact with the table.
    The table stores information about utilities of the boarding house/s.
    The table has the following columns:
    - UtilityID: int, primary key, auto-incremented
    - Type: enum('Electricity','Water','Gas','Internet','Trash','Maintenance','Miscellaneous'), not null
    - Status: enum('Active','Inactive'), not null
    - BillingCycle: enum('Monthly','Quarterly','Annually','Irregular'), not null
    - PRIMARY KEY (UtilityID)
    """
    _tableName = "utility"

    @classmethod  
    def _createTable(cls):
        try:
            cursor = DatabaseConnection.getConnection().cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS utility (" +
                "UtilityID int NOT NULL AUTO_INCREMENT, " + 
                "Type enum('Electricity','Water','Gas','Internet','Trash','Maintenance','Miscellaneous') NOT NULL, " +
                "Status enum('Active','Inactive') NOT NULL, " +
                "BillingCycle enum('Monthly','Quarterly','Annually','Irregular') NOT NULL," +
                "PRIMARY KEY (UtilityID))"
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
        Batch update the utility table with the given keys and data.
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
            if column == "Type":
                if data[column] not in ["Electricity", "Water", "Gas", "Internet", "Trash", "Maintenance", "Miscellaneous"]:
                    raise ValueError(f"Invalid value for column {column}.")
            if column == "Status":
                if data[column] not in ["Active", "Inactive"]:
                    raise ValueError(f"Invalid value for column {column}.")
            if column == "BillingCycle":
                if data[column] not in ["Monthly", "Quarterly", "Annually", "Irregular"]:
                    raise ValueError(f"Invalid value for column {column}.")
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