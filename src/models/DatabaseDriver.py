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
    columns = []
    referredTables = []

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
            cls.columns = cls._getColumns(cls)
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
    def getTableName(cls) -> str:
        """
        Returns the name of the table.
        """
        return cls._tableName
    
    @classmethod
    def read(cls, 
             all : bool = True,
             columns : list[str] = None,
             referred : dict['Table' : list[str]] = None,
             searchValue : str = None,
             sortBy : str = None, 
             order : str = "ASC",
             page : int = 1, 
             limit : int = 50
             ) -> list[dict[str, any]]:
        """
        Reads data from the table. The method accepts various parameters to filter,
        sort, and paginate the results. The parameters include:
        - all: A boolean indicating whether to select all columns or not.
        - columns: A list of column names to select.
        - referred: A dictionary of referred tables and their columns.
        - searchValue: A string to search for in the columns.
        - sortBy: A string indicating the column to sort by.
        - order: A string indicating the order of sorting ('ASC' or 'DESC').
        - page: An integer indicating the page number for pagination.
        - limit: An integer indicating the number of records per page.
        The method returns a list of dictionaries where each dictionary represents a row
        """

        result = []
        referred = {} if referred is None else referred
        columns = [] if columns is None else columns
        try:
            if page < 1 or limit < 1:
                raise ValueError("Page and limit must be positive integers.")
            if sortBy is not None and not isinstance(sortBy, str):
                raise ValueError("sortBy must be a string.")
            if not isinstance(order, str):
                raise ValueError("order must be a string.")
            if searchValue is not None and not isinstance(searchValue, str):
                raise ValueError("searchValue must be a string.")
            if not isinstance(all, bool):
                raise ValueError("all must be a boolean.")
            if columns is not None and not isinstance(columns, list):
                raise ValueError("columns must be a list.")
            if referred is not None and not isinstance(referred, dict):
                raise ValueError("referred must be a dictionary.")
            for table in referred.keys():
                if table not in cls.referredTables:
                    raise ValueError(f"Table '{table}' is not a referred table.")
                for column in referred[table]:
                    if column not in table.columns:
                        raise ValueError(f"Column '{column}' does not exist in the table '{table}'.")
                if len(referred[table]) == 0:
                    raise ValueError(f"referredColumns for table '{table}' must not be empty.")
            if not all:
                if len(columns) == 0:
                    raise ValueError("columns must not be empty.")
                for column in columns:
                    if column not in cls.columns:
                        raise ValueError(f"Column '{column}' does not exist in the table.")
            
            searchClause = ""
            if all:
                columns += cls.columns
            columns = [f"{cls._tableName}.{column}" for column in columns]
            if referred:
                for table, tableColumns in referred.items():
                    columns += [f"{table.getTableName()}.{column}" for column in tableColumns]
                if searchClause == "":
                    searchClause = "WHERE "
                searchClause += " AND ".join([f"{cls._tableName}.{table._primary} = {table.getTableName()}.{table._primary}" for table in referred.keys()])

            if searchValue is not None:
                allcolumns = "(" + " OR ".join([column + " REGEXP \'" + searchValue + "\'" for column in columns]) + ")"
                if searchClause == "":
                    searchClause = "WHERE "
                else:
                    searchClause += " AND "
                searchClause += allcolumns
            
            if sortBy is None:
                sortBy = cls._primary
            if sortBy not in cls.columns:
                columnExists = False
                for table in referred.keys():
                    if sortBy in table.columns:
                        sortBy = f"{table.getTableName()}.{sortBy}"
                        columnExists = True
                        break
                if not columnExists:
                    raise ValueError(f"Column '{sortBy}' does not exist in the table.")
            else:
                sortBy = f"{cls._tableName}.{sortBy}"

            if order not in ["ASC", "DESC"]:
                raise ValueError("order must be 'ASC' or 'DESC'.")
            
            selectClause = ', '.join(columns)
            tableNames = ", ".join([table.getTableName() for table in referred.keys()] + [cls._tableName])
            
            cursor = DatabaseConnection.getConnection().cursor(dictionary = True)
            offset = (page - 1) * limit
            sql = f"SELECT {selectClause} FROM {tableNames} {searchClause} ORDER BY {sortBy} {order} LIMIT {limit} OFFSET {offset}; "
            cursor.execute(sql)
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
                if key not in cls.columns:
                    raise ValueError(f"Column '{key}' does not exist in the table.")
            if list(data.keys()) != cls.columns:
                raise ValueError(f"Data keys {data.keys()} do not match table columns {cls.columns}.")
        
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
                if k not in cls.columns:
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
    
    @classmethod
    def totalRows(cls,
                all : bool = True,
                columns : list[str] = None,
                referred : dict['Table' : list[str]] = None,
                searchValue : str = None,
             ) -> int:
        """
        Returns the total number of rows in the table. The method accepts various
        arguments to filter the results. The parameters include:
        - all: A boolean indicating whether to select all columns or not.
        - columns: A list of column names to select.
        - referred: A dictionary of referred tables and their columns.
        - searchValue: A string to search for in the columns.
        """
        total = 0
        referred = {} if referred is None else referred
        columns = [] if columns is None else columns
        try:
            searchClause = ""
            if all:
                columns += cls.columns
            columns = [f"{cls._tableName}.{column}" for column in columns]
            if referred:
                for table, tableColumns in referred.items():
                    columns += [f"{table.getTableName()}.{column}" for column in tableColumns]
                if searchClause == "":
                    searchClause = "WHERE "
                searchClause += " AND ".join([f"{cls._tableName}.{table._primary} = {table.getTableName()}.{table._primary}" for table in referred.keys()])

            if searchValue is not None:
                allcolumns = "(" + " OR ".join([column + " REGEXP \'" + searchValue + "\'" for column in columns]) + ")"
                if searchClause == "":
                    searchClause = "WHERE "
                else:
                    searchClause += " AND "
                searchClause += allcolumns
            
            tableNames = ", ".join([table.getTableName() for table in referred.keys()] + [cls._tableName])

            cursor = DatabaseConnection.getConnection().cursor(dictionary = True)
            sql = f"SELECT COUNT(*) AS total FROM {tableNames} {searchClause};"
            cursor.execute(sql)
            total = cursor.fetchone()['total']
            if total is None:
                total = 0
        except Exception as e:
            print(f"Error: {e}")
            raise e
        finally:
            cursor.close()
        return total
    
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

    referredTables = [Unit, Utility]

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

    referredTables = [Unit, Utility]

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
