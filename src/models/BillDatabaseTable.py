import datetime
import math

from .DatabaseTable import DatabaseTable
from .DatabaseConnection import DatabaseConnection
from .UnitDatabaseTable import UnitDatabaseTable
from .UtilityDatabaseTable import UtilityDatabaseTable
from .InstalledUtilityDatabaseTable import InstalledUtilityDatabaseTable

from src.utils.constants import Range
from src.utils.constants import UTILITIES

class BillDatabaseTable(DatabaseTable):
    """
    This class represents the bill table in the database.
    It inherits from the DatabaseTable class and provides methods to interact with the table.
    The table stores information about bills of the boarding house/s.
    The table has the following columns:
    - BillID: int, primary key, auto-incremented
    - UnitID: int, foreign key, references UnitDatabaseTable
    - UtilityID: int, foreign key, references UtilityDatabaseTable
    - TotalAmount: decimal(10,2), not null
    - BillingPeriodStart: date, not null
    - BillingPeriodEnd: date, not null
    - Status: enum('Unpaid','Paid','Partially Paid','Overdue'), not null
    - DueDate: date, not null
    - PRIMARY KEY (BillID)
    - KEY UnitID (UnitID)
    - KEY UtilityID (UtilityID)
    - CONSTRAINT bill_ibfk_1 FOREIGN KEY (UnitID) REFERENCES unit (UnitID) ON DELETE SET NULL ON UPDATE CASCADE
    - CONSTRAINT bill_ibfk_2 FOREIGN KEY (UtilityID) REFERENCES utility (UtilityID) ON DELETE SET NULL ON UPDATE CASCADE
    - CONSTRAINT bill_chk_1 CHECK ((BillingPeriodEnd > BillingPeriodStart))
    - CONSTRAINT bill_chk_2 CHECK ((DueDate > BillingPeriodEnd))
    """
    
    _tableName = "bill"
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
        super().initialize()

    @classmethod  
    def _createTable(cls):
        try:
            cursor = DatabaseConnection.getConnection().cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS bill ( " +
                "BillID int NOT NULL AUTO_INCREMENT, " +
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

    @classmethod
    def batchUpdate(cls, 
                    keys : list[int],
                    data : dict[str, str | float | datetime.date]):
        """
        Batch update the bill table with the given keys and data.
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
            if not isinstance(data[column], str) and not isinstance(data[column], float) and not isinstance(data[column], datetime.date):
                raise TypeError("Data values must be strings, floats, or datetime.date.")
            if column not in cls._columns:
                raise ValueError(f"Column {column} is not a valid column name.")
            if column == cls._primaryKey or column == UnitDatabaseTable._primaryKey or column == UtilityDatabaseTable._primaryKey:
                raise ValueError(f"Cannot update primary key or foreign keys.")
            if column == "TotalAmount":
                if data[column] < 0:
                    raise ValueError(f"Invalid value for column {column}.")
            if column == "Status":
                if data[column] not in ["Unpaid", "Paid", "Partially Paid", "Overdue"]:
                    raise ValueError(f"Invalid value for column {column}.")
            if column == "BillingPeriodStart":
                if not isinstance(data[column], datetime.date):
                    raise ValueError(f"Invalid value for column {column}.")
            if column == "BillingPeriodEnd":
                if not isinstance(data[column], datetime.date):
                    raise ValueError(f"Invalid value for column {column}.")
                if data[column] < data["BillingPeriodStart"]:
                    raise ValueError(f"BillingPeriodEnd must be greater than BillingPeriodStart.")
            if column == "DueDate":
                if not isinstance(data[column], datetime.date):
                    raise ValueError(f"Invalid value for column {column}.")
                if data[column] < data["BillingPeriodEnd"]:
                    raise ValueError(f"DueDate must be greater than BillingPeriodEnd.")
            if column == "Status":
                if data[column] not in ["Unpaid", "Paid", "Partially Paid", "Overdue"]:
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
    
    #Unique methods for BillDatabaseTable
    #<----------------------------------------->

    @classmethod
    def uniqueRead(cls,
            searchValue : str,
            sortBy : str, 
            order : str,
            page : int = 1, 
            limit : int = 50
            ) -> list[dict[str, any]]:
        """
        The unique method for reading data from the installedutility table with records
        from unit and utility table.
        The method accepts various parameters to filter,
        sort, and paginate the results. The parameters include:
        - searchValue: A string to search for in the columns.
        - sortBy: A string indicating the column to sort by.
        - order: A string indicating the order of sorting ('ASC' or 'DESC').
        - page: An integer indicating the page number for pagination.
        - limit: An integer indicating the number of records per page.
        """
        cls.initialize()

        if page < 1 or limit < 1:
            raise ValueError("Page and limit must be positive integers.")
        if not isinstance(sortBy, str):
            raise ValueError("sortBy must be a string.")
        if not isinstance(order, str):
            raise ValueError("order must be a string.")
        
        result = None

        try:
            cursor = DatabaseConnection.getConnection().cursor(dictionary = True)
            offset = (page - 1) * limit
            sql = """
                SELECT b.BillID, u.Name, ut.Type, b.TotalAmount, b.DueDate, b.Status FROM bill b
                LEFT JOIN utility ut ON b.UtilityID = ut.UtilityID LEFT JOIN unit u ON b.UnitID = u.UnitID 
                """
            if searchValue is not None:
                sql += f"WHERE (BillID REGEXP \'{searchValue}\' OR ut.Type REGEXP \'{searchValue}\' OR Name REGEXP \'{searchValue}\' "
                sql += f"OR TotalAmount REGEXP \'{searchValue}\' OR DueDate REGEXP \'{searchValue}\' "
                sql += f"OR b.Status REGEXP \'{searchValue}\') "
            sql += """   
                UNION SELECT b.billID, u.Name, ut.Type, b.TotalAmount, b.DueDate, b.Status FROM bill b
                RIGHT JOIN utility ut ON b.UtilityID = ut.UtilityID JOIN unit u ON b.UnitID = u.UnitID 
                """
            if searchValue is not None:
                sql += f"WHERE (BillID REGEXP \'{searchValue}\' OR ut.Type REGEXP \'{searchValue}\' OR Name REGEXP \'{searchValue}\' "
                sql += f"OR TotalAmount REGEXP \'{searchValue}\' OR DueDate REGEXP \'{searchValue}\' "
                sql += f"OR b.Status REGEXP \'{searchValue}\') "
            sql += f"ORDER BY {sortBy} {order} LIMIT {limit} OFFSET {offset};"
            cursor.execute(sql)
            result = cursor.fetchall()
        
        except Exception as e:
            print(f"Error: {e}")
            raise e
        finally:
            cursor.close()
        return result

    @classmethod
    def uniqueTotalCount(cls,
        searchValue : str) -> int:
        """
        Unique method to get the total count of records in the bills table with records
        from unit and utility table.
        """
        cls.initialize()

        result = 0
        
        try:
            cursor = DatabaseConnection.getConnection().cursor(dictionary = True)
            sql = """
            SELECT COUNT(*) FROM bill b 
            LEFT JOIN utility ut ON b.UtilityID = ut.UtilityID LEFT JOIN unit u ON b.UnitID = u.UnitID 
            """
            if searchValue is not None:
                sql += f"WHERE (BillID REGEXP \'{searchValue}\' OR ut.Type REGEXP \'{searchValue}\' OR Name REGEXP \'{searchValue}\' "
                sql += f"OR TotalAmount REGEXP \'{searchValue}\' OR DueDate REGEXP \'{searchValue}\' "
                sql += f"OR b.Status REGEXP \'{searchValue}\') "
            cursor.execute(sql)
            res1 = cursor.fetchone()["COUNT(*)"]
            sql = """
            SELECT COUNT(*) FROM bill b 
            RIGHT JOIN utility ut ON b.UtilityID = ut.UtilityID JOIN unit u ON b.UnitID = u.UnitID 
            """
            if searchValue is not None:
                sql += f"WHERE (BillID REGEXP \'{searchValue}\' OR ut.Type REGEXP \'{searchValue}\' OR Name REGEXP \'{searchValue}\' "
                sql += f"OR TotalAmount REGEXP \'{searchValue}\' OR DueDate REGEXP \'{searchValue}\' "
                sql += f"OR b.Status REGEXP \'{searchValue}\') "
            print(sql)
            cursor.execute(sql)
            res2 = cursor.fetchone()["COUNT(*)"]

            result = max(res1, res2)
        except Exception as e:
            print(f"Error: {e}")
            raise e
        finally:
            cursor.close()
        return result
    
    @classmethod
    def getUnitBills(cls,
                unit : int,
                range: Range,
                offset: int = 1) -> dict[str, list[dict[str, any]]]:
        """
        Returns a dictionary of bills for the given unit ID and range.
        The dictionary keys are the utility types, and the values are lists of bills.
        Each bill is represented as a dictionary with keys: BillID, TotalAmount, BillingPeriodEnd.
        
        The range can be one of the following: 3m, 6m, 1y, 2y.
        The offset is the number of months to go back from the current date.
        For example, if the range is 3m and the offset is 2, it will return bills from 6 months ago to 3 months ago.
        
        - unit: int, the ID of the unit to get bills for.
        - range: Range, the range of months to get bills for.
        - offset: int, the number of months to go back from the current date.
        """
        cls.initialize()
        
        if not isinstance(unit, int):
            raise ValueError("Unit must be an integer.")
        
        result = {}

        try:
            cursor = DatabaseConnection.getConnection().cursor(dictionary = True)
            for utilityID in InstalledUtilityDatabaseTable.getUnitUtilities(unit):
                sql = f"SELECT Type FROM {UtilityDatabaseTable.getTableName()} WHERE UtilityID = {utilityID}"
                cursor.execute(sql)
                utilityType = cursor.fetchone()['Type']
                unitType = UnitDatabaseTable.readOne(unit)['Type']
                utilityIsShared = InstalledUtilityDatabaseTable.isUtilityShared(utilityID)
                if(unitType == 'Shared' and utilityIsShared or unitType == 'Individual' and not utilityIsShared):
                    result[utilityType] = cls.getUtilityBills(utilityID, range, offset)

        except Exception as e:
            print(f"Error: {e}")
            raise e
        finally:
            cursor.close()
        return result

    @classmethod
    def getAllUnitsBills(cls,
                    range: Range,
                    offset: int = 1) -> dict[str, list[dict[str, any]]]:
        """
        Returns a dictionary of all bills for the given range.
        The range can be one of the following: 3m, 6m, 1y, 2y.
        The dictionary keys are the utility types, and the values are lists of bills.
        Each bill is represented as a dictionary with keys: BillID, TotalAmount, BillingPeriodEnd.

        = range: Range, the range of months to get bills for.
        - offset: int, the number of months to go back from the current date.
        """
        cls.initialize()

        result = {}

        try:

            rangeClause = cls.__rangeClause(range, offset)

            cursor = DatabaseConnection.getConnection().cursor(dictionary = True)
            for utility in UTILITIES:
                sql = f"SELECT Bill.BillID, Bill.TotalAmount, Bill.BillingPeriodEnd FROM bill " + \
                    f"INNER JOIN utility ON Utility.UtilityID=Bill.UtilityID WHERE Utility.Type='{utility}'" + \
                    f"AND {rangeClause} "             
                cursor.execute(sql)

                result[utility] = cursor.fetchall()

        except Exception as e:
            print(f"Error: {e}")
            raise e
        finally:
            cursor.close()
        return result

    @classmethod
    def getUtilityBills(cls,
                    utility : int,
                    range: Range,
                    offset: int = 1) -> list[dict[str, int | float | datetime.date]]:
        """
        Returns a list of bills for the given utility ID and range.
        Each bill is represented as a dictionary with keys: BillID, UnitID, TotalAmount, BillingPeriodEnd.

        - utility: int, the ID of the utility to get bills for.
        - range: Range, the range of months to get bills for.
        - offset: int, the number of months to go back from the current date.
        """
        cls.initialize()
        
        result = []

        try:
            
            rangeClause = "AND " + cls.__rangeClause(range, offset)

            cursor = DatabaseConnection.getConnection().cursor(dictionary = True)
            sql = f"SELECT Bill.BillID, Bill.TotalAmount, Bill.BillingPeriodEnd FROM {cls.getTableName()} WHERE Bill.UtilityID = {utility} {rangeClause}"
            cursor.execute(sql)
            result = cursor.fetchall()

        except Exception as e:
            print(f"Error: {e}")
            raise e
        finally:
            cursor.close()
        return result

    @classmethod
    def getAllGroupedBills(cls,
                        range : Range,
                        offset : int = 1) -> dict[str, list[dict[str, float | datetime.date]]]:
        """
        Returns a dictionary where each utility type is a key. Each utility type
        will have a list of bills grouped by billing period end date and their
        total amount is summed up. Bills are limited to the given range and offset.
        """
        cls.initialize()
        result = {}
        try:
            cursor = DatabaseConnection.getConnection().cursor(dictionary = True)
            rangeClause = cls.__rangeClause(range, offset)
            for utility in UTILITIES:
                sql = f"SELECT Bill.BillingPeriodEnd, SUM(Bill.TotalAmount) AS TotalAmount FROM {cls.getTableName()}, " + \
                    f"{UtilityDatabaseTable.getTableName()} " + \
                    f"WHERE bill.UtilityID = utility.UtilityID AND utility.Type='{utility}' AND {rangeClause} " + \
                    f"GROUP BY Bill.BillingPeriodEnd"
                cursor.execute(sql)
                result[utility] = cursor.fetchall()
        except Exception as e:
            print(f"Error: {e}")
            raise e
        finally:
            cursor.close()
        return result
    
    @classmethod
    def billsTotalSum(cls,
                    range: Range,
                    offset: int = 1,
                    paidOnly: bool = False) -> float:
        """
        Returns the total sum of all bills for the given range.
        The range can be one of the following: 3m, 6m, 1y, 2y.

        - range: Range, the range of months to get bills for.
        - offset: int, the number of months to go back from the current date.
        - paidOnly: bool, if True, only paid bills will be included in the sum.
        """
        cls.initialize()

        result = 0.0

        try:
            
            whereClause = cls.__rangeClause(range, offset)

            if paidOnly:
                whereClause += " AND Bill.Status = 'Paid'"
            cursor = DatabaseConnection.getConnection().cursor(dictionary = True)
            sql = f"SELECT SUM(Bill.TotalAmount) AS TotalAmount FROM {cls.getTableName()} WHERE {whereClause}"
            cursor.execute(sql)
            result = cursor.fetchone()['TotalAmount']

        except Exception as e:
            print(f"Error: {e}")
            raise e
        finally:
            cursor.close()
        return result
    
    @classmethod
    def unpaidBillsCount(cls,
                        range: Range,
                        offset: int = 1) -> int:
        """
        Returns the total count of unpaid bills for the given range.
        The range can be one of the following: 3m, 6m, 1y, 2y.

        - range: Range, the range of months to get bills for.
        - offset: int, the number of months to go back from the current date.
        """
        cls.initialize()

        result = 0

        try:
            
            rangeClause = cls.__rangeClause(range, offset)

            cursor = DatabaseConnection.getConnection().cursor(dictionary = True)
            sql = f"SELECT COUNT(Bill.BillID) AS UnpaidCount FROM {cls.getTableName()} WHERE {rangeClause} AND Bill.Status != 'Paid'"
            cursor.execute(sql)
            result = cursor.fetchone()['UnpaidCount']

        except Exception as e:
            print(f"Error: {e}")
            raise e
        finally:
            cursor.close()
        return result

    @classmethod
    def urgentBills(cls,
                    limit: int = 15) -> list[dict[str, int | str | float | datetime.date]]:
        """
        Returns a list of urgent bills.
        An urgent bill is defined as a bill that is not yet paid.
        The list is limited to the specified number of bills.

        - limit: int, the maximum number of bills to return.
        """
        cls.initialize()

        result = []

        try:
            if not isinstance(limit, int):
                raise ValueError("Limit must be an integer.")
            if limit <= 0:
                raise ValueError("Limit must be greater than 0.")
            
            cursor = DatabaseConnection.getConnection().cursor(dictionary = True)
            sql = f"SELECT Bill.BillID, Utility.Type, Bill.TotalAmount, Bill.DueDate, Bill.Status, " + \
                f"DATEDIFF(Bill.DueDate, CURDATE()) AS closest FROM {cls.getTableName()} " + \
                f"JOIN {UtilityDatabaseTable.getTableName()} ON Bill.UtilityID = Utility.UtilityID " + \
                f"WHERE Bill.Status != 'Paid'" + \
                f"ORDER BY closest ASC LIMIT {limit}"
            cursor.execute(sql)
            result = cursor.fetchall()

        except Exception as e:
            print(f"Error: {e}")
            raise e
        finally:
            cursor.close()
        return result

    @classmethod
    def getUnitBillsMaxOffset(cls,
                             unit: int,
                             range: Range) -> dict[str, int]:
        """
        Returns the maximum offset for the given unit ID and range.
        The range can be one of the following: 3m, 6m, 1y, 2y.

        - unit: int, the ID of the unit to get bills for.
        - range: Range, the range of months to get bills for.
        """
        cls.initialize()
        result = {}
        try:
            if not isinstance(unit, int):
                raise ValueError("Unit must be an integer.")
            
            for utilityID, utilityDate in cls.getEarliestUnitBillDates(unit).items():
                sql = f"SELECT Type FROM {UtilityDatabaseTable.getTableName()} WHERE UtilityID = {utilityID}"
                cursor = DatabaseConnection.getConnection().cursor(dictionary = True)
                cursor.execute(sql)
                utilityType = cursor.fetchone()['Type']
                result[utilityType] = cls.__getMaxOffset(utilityDate, range)
        except Exception as e:
            print(f"Error: {e}")
            raise e
        return result

    @classmethod
    def getUtilityBillsMaxOffset(cls,
                                utility: int,
                                range: Range) -> int:
        """
        Returns the maximum offset for the given utility ID and range.
        The range can be one of the following: 3m, 6m, 1y, 2y.

        - utility: int, the ID of the utility to get bills for.
        - range: Range, the range of months to get bills for.
        """
        cls.initialize()

        result = 0
        try:
            if not isinstance(utility, int):
                raise ValueError("Utility must be an integer.")
            
            result = cls.__getMaxOffset(cls.getEarliestUtilityBillDates(utility), range)

        except Exception as e:
            print(f"Error: {e}")
            raise e
        return result
    
    @classmethod
    def getAllUnitBillsMaxOffset(cls,
                                range: Range) -> int:
        """
        Returns the maximum offset for the given range.
        The range can be one of the following: 3m, 6m, 1y, 2y.

        - range: Range, the range of months to get bills for.
        """
        cls.initialize()

        result = 0
        try:
            cursor = DatabaseConnection.getConnection().cursor(dictionary = True)
            sql = f"SELECT Bill.BillingPeriodEnd FROM bill LIMIT 1"
            cursor.execute(sql)
            result = cls.__getMaxOffset(cursor.fetchone()['BillingPeriodEnd'], range)
        except Exception as e:
            print(f"Error: {e}")
            raise e
        return result
    
    @classmethod
    def getEarliestUnitBillDates(cls,
                                unit: int) -> dict[int, 'datetime.date']:
        """
        Returns the earliest billing period end dates for the given unit ID
        per utility installed in the unit.

        - unit: int, the ID of the unit to get bills for.
        """
        cls.initialize()

        result = {}
        try:
            if not isinstance(unit, int):
                raise ValueError("Unit must be an integer.")
            
            cursor = DatabaseConnection.getConnection().cursor(dictionary = True)
            for utilityID in InstalledUtilityDatabaseTable.getUnitUtilities(unit):
                sql = f"SELECT Bill.BillingPeriodEnd FROM {cls.getTableName()} " + \
                    f"WHERE Bill.UtilityID = {utilityID} AND Bill.UnitID = {unit}" + \
                    f" LIMIT 1"
                cursor.execute(sql)
                sqlRes = cursor.fetchone()
                result[utilityID] = sqlRes['BillingPeriodEnd'] if cursor.rowcount > 0 else None

        except Exception as e:
            print(f"Error: {e}")
            raise e
        finally:
            cursor.close()
        return result

    @classmethod
    def getEarliestUtilityBillDate(cls,
                                    utility: int) -> datetime.date:
        """
        Returns the earliest billing period end dates for the given utility ID.

        - utility: int, the ID of the utility to get bills for.
        """
        cls.initialize()

        result = None

        try:
            if not isinstance(utility, int):
                raise ValueError("Utility must be an integer.")
            
            cursor = DatabaseConnection.getConnection().cursor(dictionary = True)
            sql = f"SELECT Bill.BillingPeriodEnd FROM {cls.getTableName()} " + \
                f"WHERE Bill.UtilityID = {utility} " + \
                f"ORDER BY Bill.BillingPeriodEnd ASC LIMIT 1"
            cursor.execute(sql)
            sqlRes = cursor.fetchone()
            result = sqlRes['BillingPeriodEnd'] if cursor.rowcount > 0 else None

        except Exception as e:
            print(f"Error: {e}")
            raise e
        finally:
            cursor.close()
        return result

    @classmethod
    def getEarliestBillDate(cls) -> datetime.date:
        """
        Returns the earliest billing period end dates for all bills.

        """
        cls.initialize()

        result = None

        try:
            cursor = DatabaseConnection.getConnection().cursor(dictionary = True)
            sql = f"SELECT Bill.BillingPeriodEnd FROM {cls.getTableName()} " + \
                f"LIMIT 1"
            cursor.execute(sql)
            sqlRes = cursor.fetchone()
            result = sqlRes['BillingPeriodEnd'] if cursor.rowcount > 0 else None

        except Exception as e:
            print(f"Error: {e}")
            raise e
        finally:
            cursor.close()
        return result

    #Helper methods

    @classmethod
    def __rangeClause(cls,
                      range: Range,
                      offset: int) -> str:
        """
        Helper method that returns the range clause for the given range.
        The range can be one of the following: 3m, 6m, 1y, 2y.

        - range: Range, the range of months to get bills for.
        - offset: int, the number of months to go back from the current date.
        """
        cls.initialize()

        if not isinstance(range, Range):
            raise ValueError("Range must be an instance of Range enum.")
        if not range in [Range.THREE_MONTHS, Range.SIX_MONTHS, Range.ONE_YEAR, Range.TWO_YEARS]:
            raise ValueError("Range must be one of the following: 3m, 6m, 1y, 2y.")
        if offset <= 0:
            raise ValueError("Offset must be greater than 0.")
        if not isinstance(offset, int):
            raise ValueError("Offset must be an integer.")
        
        rangeClause = f"Bill.BillingPeriodEnd >= DATE_SUB(CURDATE(), INTERVAL {range.value * offset} MONTH) AND" + \
            f" Bill.BillingPeriodEnd <= DATE_SUB(CURDATE(), INTERVAL {range.value * (offset - 1)} MONTH)"
        return rangeClause

    @classmethod
    def __getMaxOffset(cls,
                       date: datetime.date,
                       range: Range) -> int:
        """
        Helper method that returns the maximum offset for the given date and range.
        The range can be one of the following: 3m, 6m, 1y, 2y.

        - date: datetime.date, the date to get the maximum offset for.
        - range: Range, the range of months to get the maximum offset for.
        """
        cls.initialize()

        if not isinstance(date, datetime.date):
            raise ValueError("Date must be a datetime.date object.")
        if not isinstance(range, Range):
            raise ValueError("Range must be an instance of Range enum.")
        if not range in [Range.THREE_MONTHS, Range.SIX_MONTHS, Range.ONE_YEAR, Range.TWO_YEARS]:
            raise ValueError("Range must be one of the following: 3m, 6m, 1y, 2y.")
        try:
            date = "'" + date.strftime("%Y-%m-%d") + "'"
            
            cursor = DatabaseConnection.getConnection().cursor(dictionary = True)
            sql = f"SELECT " + \
                f"TIMESTAMPDIFF(MONTH, {date}, CURDATE()) +" + \
                f"DATEDIFF( " + \
                f"    CURDATE(), " + \
                f"    {date} + INTERVAL " + \
                f"    TIMESTAMPDIFF(MONTH, {date}, CURDATE()) " + \
                f"    MONTH " + \
                f") / " + \
                f"DATEDIFF(" + \
                f"    {date} + INTERVAL " + \
                f"    TIMESTAMPDIFF(MONTH, {date}, CURDATE()) + 1 " + \
                f"    MONTH, " + \
                f"    {date} + INTERVAL " + \
                f"    TIMESTAMPDIFF(MONTH, {date}, CURDATE()) " + \
                f"    MONTH " + \
                f") AS MaxOffset " + \
                f"FROM {cls.getTableName()} " + \
                f"WHERE Bill.BillingPeriodEnd = {date} " + \
                f"ORDER BY Bill.BillingPeriodEnd DESC LIMIT 1"
            cursor.execute(sql)
            result = math.ceil(cursor.fetchone()['MaxOffset'] / range.value)
        except Exception as e:
            print(f"Error: {e}")
            raise e
        finally:
            cursor.close()
        return result