import datetime
import math

from models.DatabaseTable import DatabaseTable
from models.DatabaseConnection import DatabaseConnection
from models.UnitDatabaseTable import UnitDatabaseTable
from models.UtilityDatabaseTable import UtilityDatabaseTable
from models.InstalledUtilityDatabaseTable import InstalledUtilityDatabaseTable

from utils.constants import Range

class BillDatabaseTable(DatabaseTable):

    _tableName = "bill"
    referredTables = [UnitDatabaseTable, UtilityDatabaseTable]

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
    def getUnitBills(cls,
                  unit : int,
                  range: Range,
                  offset: int = 1) -> dict[str, list[dict[str, any]]]:
        """
        Returns a dictionary of bills for the given unit ID and range.
        The dictionary keys are the utility types, and the values are lists of bills.
        Each bill is represented as a dictionary with keys: BillID, TotalAmount, BillingPeriodEnd.
        
        The range can be one of the following: 3m, 6m, 1y, 2y.
        """
        if not cls._initialized:
            cls._initialize()
            cls._initialized = True
        result = {}
        try:
            if not isinstance(unit, int):
                raise ValueError("Unit must be an integer.")
            
            cursor = DatabaseConnection.getConnection().cursor(dictionary = True)
            for utilityID in InstalledUtilityDatabaseTable.getUnitUtilities(unit):
                sql = f"SELECT Type FROM {UtilityDatabaseTable.getTableName()} WHERE UtilityID = {utilityID}"
                cursor.execute(sql)
                utilityType = cursor.fetchone()['Type']

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
        """
        if not cls._initialized:
            cls._initialize()
            cls._initialized = True
        result = {}
        try:

            rangeClause = cls.__rangeClause(range, offset)

            cursor = DatabaseConnection.getConnection().cursor(dictionary = True)
            for utility in ["Electricity", "Water", "Gas", "Wifi", "Trash", "Maintenance", "Miscellaneous"]:
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
                     offset: int = 1) -> list[dict[str, any]]:
        """
        Returns a list of bills for the given utility ID and range.
        Each bill is represented as a dictionary with keys: BillID, UnitID, TotalAmount, BillingPeriodEnd.
        """
        if not cls._initialized:
            cls._initialize()
            cls._initialized = True
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
    def billsTotalSum(cls,
                      range: Range,
                      offset: int = 1,
                      paidOnly: bool = False) -> float:
        """
        Returns the total sum of all bills for the given range.
        The range can be one of the following: 3m, 6m, 1y, 2y.
        """
        if not cls._initialized:
            cls._initialize()
            cls._initialized = True
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
        """
        if not cls._initialized:
            cls._initialize()
            cls._initialized = True
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
                    limit: int = 15) -> list[dict[str, any]]:
        """
        Returns a list of urgent bills.
        An urgent bill is defined as a bill that is not yet paid.
        The list is limited to the specified number of bills.
        """
        if not cls._initialized:
            cls._initialize()
            cls._initialized = True
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
        """
        if not cls._initialized:
            cls._initialize()
            cls._initialized = True
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
            """
            if not cls._initialized:
                cls._initialize()
                cls._initialized = True
            result = {}
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
            """
            if not cls._initialized:
                cls._initialize()
                cls._initialized = True
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
    def __rangeClause(cls,
                      range: Range,
                      offset: int) -> str:
        """
        Returns the range clause for the given range.
        The range can be one of the following: 3m, 6m, 1y, 2y.
        """
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
    def getEarliestUnitBillDates(cls,
                                    unit: int
                                    ) -> dict[int, 'datetime.date']:
        """
        Returns the earliest billing period end dates for the given unit ID
        per utility installed in the unit.
        """
        if not cls._initialized:
            cls._initialize()
            cls._initialized = True
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
                result[utilityID] = cursor.fetchone()['BillingPeriodEnd']

        except Exception as e:
            print(f"Error: {e}")
            raise e
        finally:
            cursor.close()
        return result

    @classmethod
    def getEarliestUtilityBillDates(cls,
                                       utility: int
                                       ) -> 'datetime.date':
        """
        Returns the earliest billing period end dates for the given utility ID.
        """
        if not cls._initialized:
            cls._initialize()
            cls._initialized = True
        result = {}
        try:
            if not isinstance(utility, int):
                raise ValueError("Utility must be an integer.")
            
            cursor = DatabaseConnection.getConnection().cursor(dictionary = True)
            sql = f"SELECT Bill.BillingPeriodEnd FROM {cls.getTableName()} " + \
                f"WHERE Bill.UtilityID = {utility} " + \
                f"ORDER BY Bill.BillingPeriodEnd ASC LIMIT 1"
            cursor.execute(sql)
            result = cursor.fetchone()['BillingPeriodEnd']

        except Exception as e:
            print(f"Error: {e}")
            raise e
        finally:
            cursor.close()
        return result

    @classmethod
    def __getMaxOffset(cls,
                       date: 'datetime.date',
                       range: Range) -> int:
        """
        Returns the maximum offset for the given date and range.
        The range can be one of the following: 3m, 6m, 1y, 2y.
        """
        if not cls._initialized:
            cls._initialize()
            cls._initialized = True
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