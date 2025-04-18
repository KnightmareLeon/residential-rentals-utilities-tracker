import mysql.connector
from abc import ABC, abstractmethod
from dotenv import load_dotenv
import os

class DatabaseConnection:

    __db = None

    @staticmethod
    def startConnection():
        """
        Initializes the database connection using the credentials stored in the .env file.
        """
        if DatabaseConnection.__db is not None:
            return
        
        load_dotenv()
        DatabaseConnection.__db = mysql.connector.connect(
            host = os.getenv("HOST"),
            user = os.getenv("USER"),
            password = os.getenv("PASSWORD"),
            port = 3306,
            database = os.getenv("DATABASE"),
            use_pure = True
        )
        DatabaseConnection.__db.autocommit = True

    @staticmethod
    def getConnection():
        """
        Returns the database connection object. If the connection is not established,
        it initializes the connection first.
        """
        if DatabaseConnection.__db is None:
            DatabaseConnection.startConnection()
        return DatabaseConnection.__db

    @staticmethod
    def closeConnection():
        """
        Closes the database connection if it is open.
        """
        if DatabaseConnection.__db is None:
            return
        if DatabaseConnection.__db.is_connected():
            DatabaseConnection.__db.close()

class Table(ABC):
    
    _tableName = None
    _primary = None
    _columns = []

    @classmethod
    def initialize(cls):
        try:
            cls._tableName = cls.__name__.lower()
            cls._createTable(cls)
            cursor = DatabaseConnection.getConnection().cursor(dictionary = True)
            cursor.execute("SELECT COLUMN_NAME FROM information_schema.KEY_COLUMN_USAGE " +
                           f"WHERE TABLE_NAME = '{cls._tableName}' AND CONSTRAINT_NAME = " +
                           "'PRIMARY'")
            cls._primary = cursor.fetchone()['COLUMN_NAME']
            cls._columns = cls._getColumns(cls)
        except Exception as e:
            print(f"Error: {e}")
            raise e
        finally:
            cursor.close()
    
    @classmethod  
    @abstractmethod
    def _createTable(cls):
        pass

    @classmethod
    def read(cls, 
             page : int = 1, 
             limit : int = 50, 
             sortBy : str = None, 
             order : str = "ASC",
             searchValue : str = None
             ) -> list[dict[str, any]]:
        """
        Fetches data from the table and returns it as a list of dictionaries.
        Each dictionary represents a row from the table. 
        The keys of the dictionary are the column names and the values are the
        corresponding values from the row. 
        
        The method takes the following arguments:

        The default total number of rows returned is set to 50 by the \'limit'\
        argument. Simply pass the \'limit\' argument to change the number of rows
        returned. 
        
        The \'page\' argument is used to paginate the data. The default
        page is set to 1. The \'page\' argument is used to specify the page number.
        
        The \'sortBy\' argument is used to sort the data based on a specific column. 
        The default sort column is set to the primary key of the table. The \'sortBy\'
        argument can be set to any column name in the table.

        The \'order\' argument is used to specify the order. The default order is set to \'ASC\'.
        The \'order\' argument can be set to either \'ASC\' or \'DESC\'.

        The \'searchValue\' argument is used to search for a specific value in the table.
        The \'searchValue\' argument can be set to any string value. The search is done using a regular expression.
        The search is done on all columns in the table. The \'searchValue\' argument is optional.
        """

        result = []
        try:
            if page < 1 or limit < 1:
                raise ValueError("Page and limit must be positive integers.")
            if sortBy is not None and not isinstance(sortBy, str):
                raise ValueError("sortBy must be a string.")
            if sortBy is not None and sortBy not in cls._columns:
                raise ValueError(f"sortBy must be one of the following columns: {cls._columns}")
            if not isinstance(order, str):
                raise ValueError("order must be a string.")
            if order not in ["ASC", "DESC"]:
                raise ValueError("order must be 'ASC' or 'DESC'.")
            if searchValue is not None and not isinstance(searchValue, str):
                raise ValueError("searchValue must be a string.")
            
            if sortBy is None:
                sortBy = cls._primary

            searchClause = ""
            if searchValue is not None:
                allcolumns = " OR ".join([column + " REGEXP \'" + searchValue + "\'" for column in cls._columns])
                searchClause = f"WHERE {allcolumns} "
            cursor = DatabaseConnection.getConnection().cursor(dictionary = True)
            offset = (page - 1) * limit
            cursor.execute(f"SELECT * FROM {cls._tableName} {searchClause}ORDER BY {sortBy} {order} LIMIT {limit} OFFSET {offset}; ")
            result = cursor.fetchall()
        except Exception as e:
            print(f"Error: {e}")
            raise e
        finally:
            cursor.close()
        return result

    @classmethod
    def create(cls, data : dict[str, any]):
        """
        Inserts data into the table. The data must be a dictionary where the keys
        are the column names and the values are the corresponding values to be inserted.
        The primary key must be included in the data dictionary. The method will
        raise an error if the primary key is not included or if the data is not a
        dictionary.
        """
        try:
            if not isinstance(data, dict):
                raise ValueError("Data must be a dictionary.")
            if cls._primary not in data:
                raise ValueError(f"Primary key '{cls._primary}' is required in the data.")
            if not isinstance(data[cls._primary], int):
                raise ValueError(f"Primary key '{cls._primary}' must be an integer.")
            for key in data.keys():
                if key not in cls._columns:
                    raise ValueError(f"Column '{key}' does not exist in the table.")
            if list(data.keys()) != cls._columns:
                raise ValueError(f"Data keys {data.keys()} do not match table columns {cls._columns}.")
        
            cursor = DatabaseConnection.getConnection().cursor()
            columns = ', '.join(data.keys())
            values = []
            for data in data.values():
                if isinstance(data, str):
                    data = f"'{data}'"
                elif isinstance(data, int):
                    data = str(data)
                else:
                    raise ValueError(f"Unsupported data type: {type(data)}")
                values.append(data)
            values = ', '.join(values)
            sql = f"INSERT INTO {cls._tableName} ({columns}) VALUES ({values})"
            cursor.execute(sql)
        except Exception as e:
            print(f"Error: {e}")
            raise e
        finally:
            cursor.close()
    
    @classmethod
    def delete(cls, keys : list[int]):
        """
        Deletes data from the table based on the primary key. The key must be an integer
        and must exist in the table. The method will raise an error if the key is not
        an integer or if the key does not exist in the table.
        """
        try:
            if not isinstance(keys, list):
                raise ValueError("Keys must be a list of integers.")
            for key in keys:
                if not isinstance(key, int):
                    raise ValueError("Keys must be a list of integers.")
            cursor = DatabaseConnection.getConnection().cursor()
            keysClause = ', '.join([str(key) for key in keys])
            sql = f"DELETE FROM {cls._tableName} WHERE {cls._primary} IN ({keysClause})"
            cursor.execute(sql)
        except Exception as e:
            print(f"Error: {e}")
            raise e
        finally:
            cursor.close()

    @classmethod
    def update(cls, key : int, data : dict[str, any]):
        """
        Updates data in the table based on the primary key. The key must be an integer
        and must exist in the table. The data must be a dictionary where the keys are
        the column names and the values are the corresponding values to be updated.
        The method will raise an error if the key is not an integer or if the key does
        not exist in the table.
        """
        try:
            if not isinstance(key, int):
                raise ValueError("Key must be an integer.")
            if not isinstance(data, dict):
                raise ValueError("Data must be a dictionary.")
            for k in data.keys():
                if k not in cls._columns:
                    raise ValueError(f"Column '{k}' does not exist in the table.")    
        
            cursor = DatabaseConnection.getConnection().cursor()
            set_clause = ', '.join([f"{k} = '{v}'" for k, v in data.items()])
            sql = f"UPDATE {cls._tableName} SET {set_clause} WHERE {cls._primary} = {key}"
            cursor.execute(sql)
        except Exception as e:
            print(f"Error: {e}")
            raise e
        finally:
            cursor.close()
    
    def _getColumns(cls) -> list[str]:
        """
        Returns a list of column names in the table.
        """
        columns = []
        try:
            cursor = DatabaseConnection.getConnection().cursor(dictionary = True)
            cursor.execute(f"SELECT COLUMN_NAME FROM information_schema.COLUMNS WHERE TABLE_NAME = '{cls._tableName}'")
            columns = [row['COLUMN_NAME'] for row in cursor.fetchall()]
        except Exception as e:
            print(f"Error: {e}")
            raise e
        finally:
            cursor.close()
        return columns
    
class Unit(Table):

    def _createTable(cls):
        try:
            cursor = DatabaseConnection.getConnection().cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS unit( " +
                "UnitID int NOT NULL, " +
                "Name varchar(30) NOT NULL, " +
                "Address varchar(255) NOT NULL, " +
                "Type varchar(30) NOT NULL, " +
                "PRIMARY KEY (UnitID))"
            )
        except Exception as e:
            print(f"Error: {e}")
            raise e
        finally:
            cursor.close()

class Utility(Table):

    def _createTable(cls):
        try:
            cursor = DatabaseConnection.getConnection().cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS utility (" +
                "UtilityID int NOT NULL, " + 
                "Type varchar(30) NOT NULL, " +
                "Status enum('Active','Inactive') NOT NULL, " +
                "BillingCycle enum('Monthly','Quarterly','Annually','Irregular') NOT NULL," +
                "PRIMARY KEY (UtilityID))"
            )
        except Exception as e:
            print(f"Error: {e}")
            raise e
        finally:
            cursor.close()

class Bill(Table):

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

class InstalledUtility(Table):

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
