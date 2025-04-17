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
    
    def __init__(self, table_name : str):
        self.table_name = table_name
        self.primary = None
        self.columns = []
        try:
            self._createTable()
            cursor = DatabaseConnection.getConnection().cursor(dictionary = True)
            cursor.execute("SELECT COLUMN_NAME FROM information_schema.KEY_COLUMN_USAGE " +
                           f"WHERE TABLE_NAME = '{self.table_name}' AND CONSTRAINT_NAME = " +
                           "'PRIMARY'")
            self.primary = cursor.fetchone()['COLUMN_NAME']
            self.columns = self._getColumns()
        except Exception as e:
            print(f"Error: {e}")
            raise e
        finally:
            cursor.close()
        
    @abstractmethod
    def _createTable(self):
        pass

    def read(self, 
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
        """

        result = []
        try:
            if page < 1 or limit < 1:
                raise ValueError("Page and limit must be positive integers.")
            if sortBy is not None and not isinstance(sortBy, str):
                raise ValueError("sortBy must be a string.")
            if sortBy is not None and sortBy not in self.columns:
                raise ValueError(f"sortBy must be one of the following columns: {self.columns}")
            if not isinstance(order, str):
                raise ValueError("order must be a string.")
            if order not in ["ASC", "DESC"]:
                raise ValueError("order must be 'ASC' or 'DESC'.")
            if searchValue is not None and not isinstance(searchValue, str):
                raise ValueError("searchValue must be a string.")
            
            if sortBy is None:
                sortBy = self.primary

            searchClause = ""
            if searchValue is not None:
                allcolumns = " OR ".join([column + " REGEXP \'" + searchValue + "\'" for column in self.columns])
                searchClause = f"WHERE {allcolumns} "
            cursor = DatabaseConnection.getConnection().cursor(dictionary = True)
            offset = (page - 1) * limit
            cursor.execute(f"SELECT * FROM {self.table_name} {searchClause}ORDER BY {sortBy} {order} LIMIT {limit} OFFSET {offset}; ")
            result = cursor.fetchall()
        except Exception as e:
            print(f"Error: {e}")
            raise e
        finally:
            cursor.close()
        return result

    def create(self, data : dict[str, any]):
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
            if self.primary not in data:
                raise ValueError(f"Primary key '{self.primary}' is required in the data.")
            if not isinstance(data[self.primary], int):
                raise ValueError(f"Primary key '{self.primary}' must be an integer.")
            for key in data.keys():
                if key not in self.columns:
                    raise ValueError(f"Column '{key}' does not exist in the table.")
            if list(data.keys()) != self.columns:
                raise ValueError(f"Data keys {data.keys()} do not match table columns {self.columns}.")
        
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
            sql = f"INSERT INTO {self.table_name} ({columns}) VALUES ({values})"
            cursor.execute(sql)
        except Exception as e:
            print(f"Error: {e}")
            raise e
        finally:
            cursor.close()
    
    def delete(self, key : int):
        """
        Deletes data from the table based on the primary key. The key must be an integer
        and must exist in the table. The method will raise an error if the key is not
        an integer or if the key does not exist in the table.
        """
        try:
            if not isinstance(key, int):
                raise ValueError("Key must be an integer.")
            cursor = DatabaseConnection.getConnection().cursor()
            sql = f"DELETE FROM {self.table_name} WHERE {self.primary} = {key}"
            cursor.execute(sql)
        except Exception as e:
            print(f"Error: {e}")
            raise e
        finally:
            cursor.close()

    def update(self, key : int, data : dict[str, any]):
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
                if k not in self.columns:
                    raise ValueError(f"Column '{k}' does not exist in the table.")    
        
            cursor = DatabaseConnection.getConnection().cursor()
            set_clause = ', '.join([f"{k} = '{v}'" for k, v in data.items()])
            sql = f"UPDATE {self.table_name} SET {set_clause} WHERE {self.primary} = {key}"
            cursor.execute(sql)
        except Exception as e:
            print(f"Error: {e}")
            raise e
        finally:
            cursor.close()
    
    def _getColumns(self) -> list[str]:
        """
        Returns a list of column names in the table.
        """
        columns = []
        try:
            cursor = DatabaseConnection.getConnection().cursor(dictionary = True)
            cursor.execute(f"SELECT COLUMN_NAME FROM information_schema.COLUMNS WHERE TABLE_NAME = '{self.table_name}'")
            columns = [row['COLUMN_NAME'] for row in cursor.fetchall()]
        except Exception as e:
            print(f"Error: {e}")
            raise e
        finally:
            cursor.close()
        return columns
    
class Unit(Table):
    def __init__(self):
        super().__init__("unit")

    def _createTable(self):
        try:
            cursor = DatabaseConnection.getConnection().cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS unit( " +
                "UnitID int NOT NULL, " +
                "Name varchar(30) NOT NULL, " +
                "Address varchar(255) NOT NULL, " +
                "PRIMARY KEY (UnitID))"
            )
        except Exception as e:
            print(f"Error: {e}")
            raise e
        finally:
            cursor.close()

class Utility(Table):
    def __init__(self):
        super().__init__("utility")

    def _createTable(self):
        try:
            cursor = DatabaseConnection.getConnection().cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS utility (" +
                "UtilityID int NOT NULL, " + 
                "Type varchar(30) NOT NULL, " +
                "Status enum('Active','Inactive') NOT NULL, " +
                "PRIMARY KEY (UtilityID))"
            )
        except Exception as e:
            print(f"Error: {e}")
            raise e
        finally:
            cursor.close()

class UtilityBills(Table):
    def __init__(self):
        super().__init__("utilitybills")

    def _createTable(self):
        try:
            cursor = DatabaseConnection.getConnection().cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS utilitybills ( " +
                "BillID int NOT NULL, " +
                "UnitID int DEFAULT NULL, " +
                "UtilityID int DEFAULT NULL, " +
                "TotalAmount decimal(10,2) NOT NULL, " +
                "BillingPeriodStart date NOT NULL, " +
                "BillingPeriodEnd date NOT NULL, " +
                "Status enum('Unpaid','Paid','Partially Paid','Overdue') NOT NULL, " +
                "DueDate date NOT NULL, " +
                "BillingCycle enum('Monthly','Quarterly','Annually','Irregular') NOT NULL, " +
                "PRIMARY KEY (BillID), " +
                "KEY UnitID (UnitID), " +
                "KEY UtilityID (UtilityID), " +
                "CONSTRAINT utilitybills_ibfk_1 FOREIGN KEY (UnitID) REFERENCES unit (UnitID) ON DELETE SET NULL ON UPDATE CASCADE, " +
                "CONSTRAINT utilitybills_ibfk_2 FOREIGN KEY (UtilityID) REFERENCES utility (UtilityID) ON DELETE SET NULL ON UPDATE CASCADE, " +
                "CONSTRAINT utilitybills_chk_1 CHECK ((BillingPeriodEnd > BillingPeriodStart)), " +
                "CONSTRAINT utilitybills_chk_2 CHECK ((DueDate > BillingPeriodEnd)))"
            )
        except Exception as e:
            print(f"Error: {e}")
            raise e
        finally:
            cursor.close()

class InstalledUtilities(Table):
    def __init__(self):
        self.__init__("installedutilities")

    def _createTable(self):
        try:
            cursor = DatabaseConnection.getConnection().cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS installedutilities ( " +
                "UnitID int NOT NULL, " +
                "UtilityID int NOT NULL, " +
                "InstallationDate date NOT NULL, " +
                "PRIMARY KEY (UnitID,UtilityID), " +
                "KEY UtilityID (UtilityID), " +
                "CONSTRAINT installedutilities_ibfk_1 FOREIGN KEY (UnitID) REFERENCES unit (UnitID) ON DELETE CASCADE ON UPDATE CASCADE, " +
                "CONSTRAINT installedutilities_ibfk_2 FOREIGN KEY (UtilityID) REFERENCES utility (UtilityID) ON DELETE CASCADE ON UPDATE CASCADE)"
            )
        except Exception as e:
            print(f"Error: {e}")
            raise e
        finally:
            cursor.close()

    def delete_data(self, key):
        """
        Disabled the delete method for this class, to delete data from the table,
        use the delete method of either the Unit or Utility class."""
        pass
