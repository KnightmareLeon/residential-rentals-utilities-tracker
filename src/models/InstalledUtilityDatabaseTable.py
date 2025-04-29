from models.DatabaseTable import DatabaseTable
from models.DatabaseConnection import DatabaseConnection
from models.UnitDatabaseTable import UnitDatabaseTable
from models.UtilityDatabaseTable import UtilityDatabaseTable

class InstalledUtilityDatabaseTable(DatabaseTable):

    _tableName = "installedutility"
    referredTables = [UnitDatabaseTable, UtilityDatabaseTable]

    @classmethod
    def _initialize(cls):
        try:
            cls._createTable()
            cursor = DatabaseConnection.getConnection().cursor(dictionary = True)
            cursor.execute("SELECT COLUMN_NAME FROM information_schema.KEY_COLUMN_USAGE " +
                           f"WHERE TABLE_NAME = '{cls._tableName}' AND CONSTRAINT_NAME = " +
                           "'PRIMARY'")
            cls._primary = [row['COLUMN_NAME'] for row in cursor.fetchall()]
            cls.columns = cls._getColumns(cls)
        except Exception as e:
            print(f"Error: {e}")
            raise e
        finally:
            cursor.close()
    
    @classmethod
    def getPrimaryKey(cls) -> list[str]:
        """
        Returns the primary key of the table.
        """
        if not cls._initialized:
            cls._initialize()
            cls._initialized = True
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
        if not cls._initialized:
            cls._initialize()
            cls._initialized = True
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
                
            
            # Check if columns is empty, if so, use all columns
            if len(columns) == 0:
                columns += cls.columns
            else: # Check if columns are valid
                for column in columns:
                    if column not in cls.columns:
                        raise ValueError(f"Column '{column}' does not exist in the table.")
            columns = [f"{cls._tableName}.{column}" for column in columns]

            searchClause = ""

            if referred: # Check if referred is not empty
                for table, tableColumns in referred.items():
                    columns += [f"{table.getTableName()}.{column}" for column in tableColumns]
                if searchClause == "":
                    searchClause = "WHERE "
                searchClause += " AND ".join([f"{cls._tableName}.{table._primary} = {table.getTableName()}.{table._primary}" for table in referred.keys()])

            if searchValue is not None: # Check if searchValue is not empty
                allcolumns = "(" + " OR ".join([column + " REGEXP \'" + searchValue + "\'" for column in columns]) + ")"
                if searchClause == "":
                    searchClause = "WHERE "
                else:
                    searchClause += " AND "
                searchClause += allcolumns
            
            if sortBy is None: # Check if sortBy is not empty
                sortBy = cls._primary[0]
            if sortBy not in cls.columns: # Check if sortBy is valid
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
    def getUnitUtilities(cls,
                   unit : int,
                   type: bool = False) -> list[int] | dict[int, str]:
        """
        Returns a list of utility IDs for the given unit ID.
        """
        if not cls._initialized:
            cls._initialize()
            cls._initialized = True
        result = None
        try:
            if not isinstance(unit, int):
                raise ValueError("Unit must be an integer.")
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
        if not cls._initialized:
            cls._initialize()
            cls._initialized = True
        pass
