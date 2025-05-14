from .DatabaseTable import DatabaseTable
from .DatabaseConnection import DatabaseConnection
from .UnitDatabaseTable import UnitDatabaseTable
from .UtilityDatabaseTable import UtilityDatabaseTable

class InstalledUtilityDatabaseTable(DatabaseTable):
    """
    This class represents the installedutility table in the database.
    It inherits from the DatabaseTable class and provides methods to interact with the table.
    The table stores information about the utilities installed in each unit.
    The table has the following columns:
    - UnitID: The ID of the unit (foreign key).
    - UtilityID: The ID of the utility (foreign key).
    - InstallationDate: The date when the utility was installed.
    The table has the following constraints:
    - PRIMARY KEY (UnitID, UtilityID): The combination of UnitID and UtilityID is unique.
    - FOREIGN KEY (UnitID) REFERENCES unit (UnitID): The UnitID must exist in the unit table.
    - FOREIGN KEY (UtilityID) REFERENCES
    utility (UtilityID): The UtilityID must exist in the utility table.
    """
    
    _tableName = "installedutility"
    referredTables = {UnitDatabaseTable.getTableName() : UnitDatabaseTable, 
                      UtilityDatabaseTable.getTableName() : UtilityDatabaseTable}

    @classmethod
    def initialize(cls):
        """
        Initializes the table by creating it if it does not exist and reading the columns.
        This method can be called to ensure that the table is ready for use but it is not
        necessarily required to be called before using the class methods. The class methods
        will automatically call this method if the table is not initialized.

        This class will also initialize the UnitDatabaseTable and UtilityDatabaseTable classes
        to ensure that the foreign key references are valid.
        """
        UnitDatabaseTable.initialize()
        UtilityDatabaseTable.initialize()
        try:
            cursor = DatabaseConnection.getConnection().cursor(dictionary = True)
            if not cls._initialized:
                cls._initialized = True
                cls._createTable()
                cursor.execute("SELECT COLUMN_NAME FROM information_schema.KEY_COLUMN_USAGE " +
                            f"WHERE TABLE_NAME = '{cls._tableName}' AND CONSTRAINT_NAME = " +
                            "'PRIMARY'")
                cls._primary = [row['COLUMN_NAME'] for row in cursor.fetchall()]
                cls._columns = cls._readColumns(cls)
        except Exception as e:
            print(f"Error: {e}")
            raise e
        finally:
            cursor.close()
        
    @classmethod
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
    def getPrimaryKey(cls) -> list[str]:
        """
        Returns the primary keys of the table.
        """
        cls.initialize()
        return cls._primary
    
    @classmethod
    def read(cls, 
             columns : list[str] = None,
             referred : dict['DatabaseTable' : list[str]] = None,
             searchValue : str = None,
             sortBy : str = None, 
             order : str = "ASC",
             page : int = 1, 
             limit : int = 50
             ) -> list[dict[str, any]]:
        """
        Reads data from the table. The method accepts various parameters to filter,
        sort, and paginate the results. The parameters include:
        - columns: A list of column names to select.
        - referred: A dictionary of referred tables and their columns.
        - searchValue: A string to search for in the columns.
        - sortBy: A string indicating the column to sort by.
        - order: A string indicating the order of sorting ('ASC' or 'DESC').
        - page: An integer indicating the page number for pagination.
        - limit: An integer indicating the number of records per page.
        The method returns a list of dictionaries where each dictionary represents a row
        """

        cls.initialize()

        referred = {} if referred is None else referred
        columns = [] if columns is None else columns

        if page < 1 or limit < 1:
                raise ValueError("Page and limit must be positive integers.")
        if sortBy is not None and not isinstance(sortBy, str):
            raise ValueError("sortBy must be a string.")
        if not isinstance(order, str):
            raise ValueError("order must be a string.")
        if searchValue is not None and not isinstance(searchValue, str):
            raise ValueError("searchValue must be a string.")
        if columns is not None and not isinstance(columns, list):
            raise ValueError("columns must be a list.")
        if referred is not None and not isinstance(referred, dict):
            raise ValueError("referred must be a dictionary.")
        for table in referred.keys():
            if not isinstance(table, str):
                raise ValueError("Table names must be strings.")
            if not isinstance(referred[table], list):
                raise ValueError("Referred columns must be a list.")
            if table not in cls.referredTables.keys():
                raise ValueError(f"Table '{table}' is not a referred table.")
            for column in referred[table]:
                if not isinstance(column, str):
                    raise ValueError("Column names must be strings.")
                if column not in cls.referredTables[table].getColumns():
                    raise ValueError(f"Column '{column}' does not exist in the table '{table}'.")
            if len(referred[table]) == 0:
                raise ValueError(f"referredColumns for table '{table}' must not be empty.")

         # Check if columns is empty, if so, use all columns
        if len(columns) == 0:
            columns += cls._columns
        else: # Check if columns are valid
            for column in columns:
                if column not in cls._columns:
                    raise ValueError(f"Column '{column}' does not exist in the table.")
        columns = [f"{cls._tableName}.{column}" for column in columns]
        
        result = []
        
        try:

            searchClause = ""

            if referred: # Check if referred is not empty
                for table, tableColumns in referred.items():
                    columns += [f"{cls.referredTables[table].getTableName()}.{column}" for column in tableColumns]
                if searchClause == "":
                    searchClause = "WHERE "
                searchClause += " AND ".join([f"{cls._tableName}.{cls.referredTables[table].getPrimaryKey()} " + \
                                              f"= {cls.referredTables[table].getTableName()}.{cls.referredTables[table].getPrimaryKey()}" 
                                              for table in referred.keys()])

            if searchValue is not None: # Check if searchValue is not empty
                allcolumns = "(" + " OR ".join([column + " REGEXP \'" + searchValue + "\'" for column in columns]) + ")"
                if searchClause == "":
                    searchClause = "WHERE "
                else:
                    searchClause += " AND "
                searchClause += allcolumns
            
            if sortBy is None: # Check if sortBy is not empty
                sortBy = cls._primary[0]
            if sortBy not in cls._columns: # Check if sortBy is valid
                columnExists = False
                for table in referred.keys():
                    if sortBy in cls.referredTables[table].getColumns():
                        sortBy = f"{cls.referredTables[table].getTableName()}.{sortBy}"
                        columnExists = True
                        break
                if not columnExists:
                    raise ValueError(f"Column '{sortBy}' does not exist in the table.")
            else:
                sortBy = f"{cls._tableName}.{sortBy}"

            if order not in ["ASC", "DESC"]:
                raise ValueError("order must be 'ASC' or 'DESC'.")
            
            selectClause = ', '.join(columns)
            tableNames = ", ".join([cls.referredTables[table].getTableName() for table in referred.keys()] + [cls._tableName])
            
            cursor = DatabaseConnection.getConnection().cursor(dictionary = True)
            offset = (page - 1) * limit
            sql = f"SELECT {selectClause} FROM {tableNames} {searchClause} ORDER BY {sortBy} {order} LIMIT {limit} OFFSET {offset}; "
            print(sql)
            cursor.execute(sql)
            result = cursor.fetchall()
        except Exception as e:
            print(f"Error: {e}")
            raise e
        finally:
            cursor.close()
        return result

    @classmethod
    def create(cls, data : dict[str, str]):
        """
        Inserts data into the table. The data must be a dictionary where the keys
        are the column names and the values are the corresponding values to be inserted.
        The primary key must be included in the data dictionary. The method will
        raise an error if the primary key is not included or if the data is not a
        dictionary.
        - data: A dictionary containing the data to be inserted into the table.
        """
        cls.initialize()

        if not isinstance(data, dict):
                raise ValueError("Data must be a dictionary.")
        for key in data.keys():
            if key not in cls._columns:
                raise ValueError(f"Column '{key}' does not exist in the table.")
        if sorted(list(data.keys())) != sorted(cls._columns):
                raise ValueError(f"Data keys {data.keys()} do not match table columns {cls._columns}.")
        try:
            cursor = DatabaseConnection.getConnection().cursor()
            columnsClause = ', '.join(data.keys())
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
            sql = f"INSERT INTO {cls._tableName} ({columnsClause}) VALUES ({values})"
            cursor.execute(sql)
        except Exception as e:
            print(f"Error: {e}")
            raise e
        finally:
            cursor.close()

    @classmethod
    def delete(cls, keys : list[int]):
        """
        Disabled the delete method for this class, to delete data from the table,
        use the delete method of either the Unit or Utility table."""
        cls.initialize()
        pass

    @classmethod
    def batchUpdate(cls, 
                    keys : list[tuple[int, int]],
                    data : dict[str, str]):
        """
        Batch update the installedutility table with the given keys and data.
        - keys: A list of tuples containing the primary keys (UnitID, UtilityID).
        - data: A dictionary containing the data to be updated in the table.
        """
        cls.initialize()

        if not isinstance(keys, list):
                raise TypeError("Keys must be a list.")
        if not isinstance(data, dict):
            raise TypeError("Data must be a dict.")
        if not all(isinstance(key, tuple) and len(key) == 2 for key in keys):
            raise TypeError("Keys must be a list of tuples with two integers.")
        for column in data.keys():
            if not isinstance(column, str):
                raise TypeError("Data keys must be strings.")
            if not isinstance(data[column], str):
                raise TypeError("Data values must be strings.")
            if column not in cls._columns:
                raise ValueError(f"Column {column} is not a valid column name.")
            if column == cls._primary[0]:
                raise ValueError(f"Cannot update primary key {cls._primary[0]}.")
            if column == cls._primary[1]:
                raise ValueError(f"Cannot update primary key {cls._primary[1]}.")
        try:
            cursor = DatabaseConnection.getConnection().cursor()
            sql = f"UPDATE {cls._tableName} SET "
            sql += ", ".join([f"{column} = '{value}'" for column, value in data.items()])
            sql += " WHERE " + " AND ".join([f"{cls._primary[0]} = {key[0]} AND {cls._primary[1]} = {key[1]}" for key in keys])
            cursor.execute(sql)
        except Exception as e:
            print(f"Error: {e}")
            raise e
        finally:
            cursor.close()
        return 
    
    @classmethod
    def readOne(cls, id : int):
        """
        Method disabled
        """
        pass
    
    #Unique methods for InstalledUtilityDatabaseTable
    #<----------------------------------------->

    @classmethod
    def getUnitUtilities(cls,
                   unit : int,
                   type: bool = False) -> list[int] | dict[int, str]:
        """
        Returns a list of utility IDs for the given unit ID.
        If type is True, returns a dictionary where the keys are utility IDs and the values are the utility types.
        If type is False, returns a list of utility IDs.
        - unit: The ID of the unit.
        - type: A boolean indicating whether to return the utility types or not.
        """
        cls.initialize()

        if not isinstance(unit, int):
            raise ValueError("Unit must be an integer.")
        
        result = None

        try:
            cursor = DatabaseConnection.getConnection().cursor(dictionary = True)
            ifTypeText = f"SELECT UtilityID, Utility.Type FROM {cls.getTableName()} " + \
                         f"JOIN {UtilityDatabaseTable.getTableName()} USING (UtilityID)"
            defaultText = f"SELECT UtilityID FROM {cls.getTableName()}"
            sql = ifTypeText if type else defaultText
            sql += f" WHERE UnitID = {unit}"
            cursor.execute(sql)
            if not type:
                result = [row["UtilityID"] for row in cursor.fetchall()]
            else:
                result = {}
                for row in cursor.fetchall():
                    result[row["UtilityID"]] = row["Type"]

        except Exception as e:
            print(f"Error: {e}")
            raise e
        finally:
            cursor.close()
        return result

    @classmethod
    def getUtilityUnits(cls,
                        utility : int) -> list[dict[str, str]]:
        """
        Returns a list of the unit IDs and names for the given utility ID.
        - utility: The ID of the utility.
        """
        cls.initialize()

        if not isinstance(utility, int):
            raise ValueError("Utility must be an integer.")
        
        result = None

        try:
            cursor = DatabaseConnection.getConnection().cursor(dictionary = True)
            sql = f"SELECT installedutility.UnitID, unit.Name FROM {cls.getTableName()} " + \
                  f"NATURAL JOIN {UnitDatabaseTable.getTableName()} " + \
                  f"WHERE UtilityID = {utility}"
            cursor.execute(sql)
            result = cursor.fetchall()
        except Exception as e:
            print(f"Error: {e}")
            raise e
        finally:
            cursor.close()
        return result
    
    @classmethod
    def isUtilityShared(cls,
                        utility : int) -> bool:
        """
        Returns True if the utility is shared, False otherwise.
        - utility: The ID of the utility.
        """
        cls.initialize()

        if not isinstance(utility, int):
            raise ValueError("Utility must be an integer.")
        
        result = None

        try:
            cursor = DatabaseConnection.getConnection().cursor(dictionary = True)
            sql = f"SELECT Count(*) as UnitCount FROM {cls.getTableName()} NATURAL JOIN {UnitDatabaseTable.getTableName()} " + \
                  f"WHERE UtilityID = {utility} AND {UnitDatabaseTable.getTableName()}.Type='Shared' "
            cursor.execute(sql)
            result = cursor.fetchone()["UnitCount"] > 0
        except Exception as e:
            print(f"Error: {e}")
            raise e
        finally:
            cursor.close()
        return result
    
    @classmethod
    def getMainUnit(cls,
                    utility : int,
                    name : bool = False) -> int | str:
        """
        Returns the main unit ID or Name for the given utility ID.
        - utility: The ID of the utility.
        - name: A boolean indicating whether to return the unit name or not.
        """
        cls.initialize()

        if not isinstance(utility, int):
            raise ValueError("Utility must be an integer.")
        
        result = None

        try:
            cursor = DatabaseConnection.getConnection().cursor(dictionary = True)
            toGet = "Name" if name else "UnitID"
            sql = f"SELECT {toGet} FROM {cls.getTableName()} NATURAL JOIN {UnitDatabaseTable.getTableName()} " + \
                  f"WHERE UtilityID = {utility} AND {UnitDatabaseTable.getTableName()}.Type='Shared' "
            cursor.execute(sql)
            result = cursor.fetchone()[toGet]
        except Exception as e:
            print(f"Error: {e}")
            raise e
        finally:
            cursor.close()
        return result
