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
        self.dbConnection = None
        try:
            self._createTable()
            cursor = DatabaseConnection.getConnection().cursor(dictionary = True)
            cursor.execute("SELECT COLUMN_NAME FROM information_schema.KEY_COLUMN_USAGE " +
                           f"WHERE TABLE_NAME = '{self.table_name}' AND CONSTRAINT_NAME = " +
                           "'PRIMARY'")
            self.primary = cursor.fetchone()['COLUMN_NAME']
        except Exception as e:
            print(f"Error: {e}")
            raise e
        finally:
            cursor.close()
    
    def read(self, page : int = 1, limit : int = 50):
        """
        Fetches data from the table and returns it as a list of dictionaries.
        Each dictionary represents a row from the table. The default total
        number of rows returned is set to 50. To return other sets of rows,
        pass different integer values to the \'page\' argument, which has a
        default value of 1. Do not give negative integer values or zero
        in any of the arguments, for the method will return an error if it 
        is done.
        """
        result = []
        try:
            if page < 1 or limit < 1:
                raise ValueError("Page and limit must be positive integers.")
            cursor = DatabaseConnection.getConnection().cursor(dictionary = True)
            offset = (page - 1) * limit
            cursor.execute(f"SELECT * FROM {self.table_name} LIMIT {limit} OFFSET {offset}; ")
            result = cursor.fetchall()
        except Exception as e:
            print(f"Error: {e}")
            raise e
        finally:
            cursor.close()
        return result
    
    @abstractmethod
    def _createTable(self):
        pass

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
        
            cursor = DatabaseConnection.getConnection().cursor()
            set_clause = ', '.join([f"{k} = '{v}'" for k, v in data.items()])
            sql = f"UPDATE {self.table_name} SET {set_clause} WHERE {self.primary} = {key}"
            cursor.execute(sql)
        except Exception as e:
            print(f"Error: {e}")
            raise e
        finally:
            cursor.close()
    
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
