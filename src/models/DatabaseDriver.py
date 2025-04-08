import mysql.connector
from abc import ABC
from dotenv import load_dotenv
import os

class DatabaseConnection:

    def __init__(self):
        load_dotenv()
        self.__db = mysql.connector.connect(
            host = os.getenv("HOST"),
            user = os.getenv("USER"),
            password = os.getenv("PASSWORD"),
            port = 3306,
            database = os.getenv("DATABASE"),
            use_pure = True
        )
        self.__db.autocommit = True
        try:
            __cursorCreate = self.__db.cursor()
            __cursorCreate.execute("CREATE TABLE IF NOT EXISTS unit( " +
                "UnitID int NOT NULL, " +
                "Name varchar(30) NOT NULL, " +
                "Address varchar(255) NOT NULL, " +
                "PRIMARY KEY (UnitID))"
            )
            __cursorCreate.execute("CREATE TABLE IF NOT EXISTS utility (" +
                "UtilityID int NOT NULL, " + 
                "Type varchar(30) NOT NULL, " +
                "Status enum('Active','Inactive') NOT NULL, " +
                "PRIMARY KEY (UtilityID))"
            )
            __cursorCreate.execute("CREATE TABLE IF NOT EXISTS installedutilities ( " +
                "UnitID int NOT NULL, " +
                "UtilityID int NOT NULL, " +
                "InstallationDate date NOT NULL, " +
                "PRIMARY KEY (UnitID,UtilityID), " +
                "KEY UtilityID (UtilityID), " +
                "CONSTRAINT installedutilities_ibfk_1 FOREIGN KEY (UnitID) REFERENCES unit (UnitID) ON DELETE CASCADE ON UPDATE CASCADE, " +
                "CONSTRAINT installedutilities_ibfk_2 FOREIGN KEY (UtilityID) REFERENCES utility (UtilityID) ON DELETE CASCADE ON UPDATE CASCADE)"
            )
            __cursorCreate.execute("CREATE TABLE IF NOT EXISTS utilitybills ( " +
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
            __cursorCreate.close()

    def getConnection(self):
        return self.__db


class TableHandler(ABC):
    
    def __init__(self, table_name : str):
        self.table_name = table_name
        try:
            self.dbConnection = DatabaseConnection()
            cursor = self.dbConnection.getConnection().cursor(dictionary = True)
            cursor.execute("SELECT COLUMN_NAME FROM information_schema.KEY_COLUMN_USAGE " +
                           f"WHERE TABLE_NAME = '{self.table_name}' AND CONSTRAINT_NAME = " +
                           "'PRIMARY'")
            self.primary = cursor.fetchone()['COLUMN_NAME']
        except Exception as e:
            print(f"Error: {e}")
            raise e
        finally:
            cursor.close()
    
    def fetch(self, page : int = 1, limit : int = 50):
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
            cursor = self.dbConnection.getConnection().cursor(dictionary = True)
            offset = (page - 1) * limit
            cursor.execute(f"SELECT * FROM {self.table_name} LIMIT {limit} OFFSET {offset}; ")
            result = cursor.fetchall()
        except Exception as e:
            print(f"Error: {e}")
            raise e
        finally:
            cursor.close()
        return result
    
    def insert(self, data : dict[str, any]):
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
        
            cursor = self.dbConnection.getConnection().cursor()
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
            cursor = self.dbConnection.getConnection().cursor()
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
        
            cursor = self.dbConnection.getConnection().cursor()
            set_clause = ', '.join([f"{k} = '{v}'" for k, v in data.items()])
            sql = f"UPDATE {self.table_name} SET {set_clause} WHERE {self.primary} = {key}"
            cursor.execute(sql)
        except Exception as e:
            print(f"Error: {e}")
            raise e
        finally:
            cursor.close()
class Unit(TableHandler):
    def __init__(self):
        super().__init__("unit")

class Utility(TableHandler):
    def __init__(self):
        super().__init__("utility")

class UtilityBills(TableHandler):
    def __init__(self):
        super().__init__("utilitybills")

class InstalledUtilities(TableHandler):
    def __init__(self):
        self.__init__("installedutilities")

    def delete_data(self, key):
        pass
