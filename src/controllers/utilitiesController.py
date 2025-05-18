from datetime import date, datetime
from dateutil.relativedelta import relativedelta

from PyQt6.QtCore import QDate

from src.models.UtilityDatabaseTable import UtilityDatabaseTable as Utility
from src.models.UnitDatabaseTable import UnitDatabaseTable as Unit
from src.models.BillDatabaseTable import BillDatabaseTable as Bill
from src.models.InstalledUtilityDatabaseTable import InstalledUtilityDatabaseTable as InstalledUtility

from src.utils.constants import Range
from src.utils.sampleDataGenerator import generateUtilityData, generateRandomeUtilityBills
from src.utils.diffMonths import diffMonths

class UtilitiesController:
    
    @staticmethod
    def fetchUtilities(currentPage: int, sortingOrder: str, sortingField: str, searchValue: str) -> tuple[list[dict[str, str]], int]:
        """
        Fetches all utilitys with pagination, sorting, and searching.
        """
        print(f"Fetching utilities in page {currentPage} sorted by {sortingField} {sortingOrder} while searching for {searchValue}")
        searchValue = None if searchValue == "" else searchValue
        totalPages =  InstalledUtility.uniqueTotalCount(searchValue) // 50 + 1

        fetchedUtils = InstalledUtility.uniqueRead(searchValue,
                                            sortingField,
                                            sortingOrder,
                                            page=currentPage,)
        return fetchedUtils, totalPages
    
    @staticmethod
    def addUtility(type: str, mainUnitID: str, sharedUnitIDs: list[str], status: str, billingCycle: str, installationDate : QDate) -> str:
        """
        Adds a new utility with the given data.
        """
        # get mainUnit ID using mainUnit name and sharedUnits ID using sharedUnits name
        print("Adding utility:", type, mainUnitID, sharedUnitIDs, status, billingCycle, installationDate)
        
        #Conversion of input to proper format
        mainUnitID = int(mainUnitID)
        if len(sharedUnitIDs) > 0:
            sharedUnitIDs = [int(unitID) for unitID in sharedUnitIDs]
        installationDate = installationDate.toString("yyyy-MM-dd")

        #Error Checking
        if InstalledUtility.unitHasUtilityType(mainUnitID, type):
            unitName = Unit.readOne(mainUnitID)["Name"]
            return (f"{type} already exists for {unitName}. Please input another type.")
        if len(sharedUnitIDs) > 0:
            errorMsg = ""
            for sharedUnitID in sharedUnitIDs:
                if InstalledUtility.unitHasUtilityType(sharedUnitID, type):
                    unitName = Unit.readOne(mainUnitID)["Name"]
                    errorMsg += (f"{type} already exists for {unitName}. Please input another type.\n")
            if errorMsg != "":
                return errorMsg
        
        #Adding
        Utility.create({
            "Type": type,
            "Status": status,
            "BillingCycle": billingCycle
        })

        InstalledUtility.create({
            "UtilityID": Utility.getLastID(),
            "UnitID": mainUnitID,
            "InstallationDate": installationDate,
        })

        if len(sharedUnitIDs) > 0:
            for id in sharedUnitIDs:
                InstalledUtility.create({
                    "UtilityID": Utility.getLastID(),
                    "UnitID": id,
                    "InstallationDate": installationDate,
                })

        return "Utility added successfully"

    @staticmethod
    def viewUtility(id: str) -> tuple[dict[str, str], list[dict[str, str]], list[dict[str, str]]]:
        """
        Fetches all information about a single utility by ID.
        """
        id = int(id)
        
        utilityInfo = Utility.readOne(id)
        installationDates = InstalledUtility.getInstallationDates(id)
        utilityInfo["InstallationDate"] = installationDates[0]["InstallationDate"] if len(installationDates) > 0 else datetime.now()

        utilityUnits = InstalledUtility.getUtilityUnits(id)
        if InstalledUtility.isUtilityShared(id):
            mainUnit = InstalledUtility.getMainUnit(id)
            for unit in utilityUnits:
                if unit["UnitID"] == mainUnit:
                    unit["Name"] = unit["Name"] + " (Main)"
                    break
        utilityBills = {utilityInfo["Type"] : Bill.getUtilityBills(id, range=Range.THREE_MONTHS)}
        for bill in utilityBills[utilityInfo["Type"]]:
            bill["BillingPeriodEnd"] = bill["BillingPeriodEnd"].strftime("%Y-%m-%d")
        return ( 
            # UTILITY INFORMATION
            utilityInfo, 
            # UTILITY UNITS
            utilityUnits,
            # UTILITY BILLS
            utilityBills
        )
    
    @staticmethod
    def editUtility(originalID: str, type: str, mainUnitID: str, sharedUnitIDs: list[str], status: str, billingCycle: str, installationDate) -> str:
        """
        Edits a utility with the given data.
        """
        print("Editing utility:", originalID, type, mainUnitID, sharedUnitIDs, status, billingCycle, installationDate)
        
        #Conversion of input to proper format
        originalID = int(originalID)
        mainUnitID = int(mainUnitID)
        if len(sharedUnitIDs) > 0:
            sharedUnitIDs = [int(unitID) for unitID in sharedUnitIDs]
        installationDate = installationDate.toString("yyyy-MM-dd")

        originalData = Utility.readOne(originalID)
        originalUnitID = InstalledUtility.getMainUnit(originalID)
        originalSharedUnitIDs = InstalledUtility.getUtilityUnits(originalID)
        originalSharedUnitIDs = [unit["UnitID"] for unit in originalSharedUnitIDs if unit["UnitID"] != originalUnitID]

        editedColumns = {}

        #Error Checking 
        if type != originalData["Type"] and InstalledUtility.unitHasUtilityType(mainUnitID, type):
            unitName = Unit.readOne(mainUnitID)["Name"]
            return (f"{type} already exists for {unitName}. Please input another type or another unit.")
        if len(sharedUnitIDs) > 0:
            errorMsg = ""
            for sharedUnitID in sharedUnitIDs:
                if InstalledUtility.unitHasUtilityType(sharedUnitID, type):
                    unitName = Unit.readOne(sharedUnitID)["Name"]
                    errorMsg += (f"{type} already exists for {unitName}. Please input another type or another unit.\n")
            if errorMsg != "":
                return errorMsg
        

        if type != originalData["Type"]:
            editedColumns["Type"] = type
        if status != originalData["Status"]:
            editedColumns["Status"] = status
        if billingCycle != originalData["BillingCycle"]:
            editedColumns["BillingCycle"] = billingCycle
        
        Utility.update(originalID, {
            "Type": type,
            "Status": status,
            "BillingCycle": billingCycle
        })

        if mainUnitID != originalUnitID:
            if originalUnitID is not None:
                InstalledUtility.delete([originalUnitID, originalID])
            for id in originalSharedUnitIDs:
                InstalledUtility.delete([id, originalID])
            InstalledUtility.create({
                "UtilityID": originalID,
                "UnitID": mainUnitID,
                "InstallationDate": installationDate,
            })
            if len(sharedUnitIDs) > 0:
                for id in sharedUnitIDs:
                    if id != mainUnitID:
                        InstalledUtility.create({
                            "UtilityID": originalID,
                            "UnitID": id,
                            "InstallationDate": installationDate,
                        })
        else:
            originalInstallationDate = InstalledUtility.getInstallationDates(originalID)[0]["InstallationDate"]

            if installationDate != originalInstallationDate:
                print(installationDate, originalInstallationDate)
                InstalledUtility.update([originalUnitID, originalID], {"InstallationDate": installationDate})
            if sorted(sharedUnitIDs) != sorted(originalSharedUnitIDs):
                for id in originalSharedUnitIDs:
                    if id not in sharedUnitIDs:
                        InstalledUtility.delete([id, originalID])
                for id in sharedUnitIDs:
                    if id not in originalSharedUnitIDs and id != mainUnitID:
                        InstalledUtility.create({
                            "UtilityID": originalID,
                            "UnitID": id,
                            "InstallationDate": installationDate
                        })    

        return "Utility edited successfully"
    
    @staticmethod
    def deleteUtility(id: str) -> str:
        """
        Deletes a new utility with the given data.
        """
        print("Deleting utility:", id)
        Utility.delete([int(id)])
        return "Utility deleted successfully"
    
    @staticmethod
    def getUtilitiesByUnitID(unitID: str) -> list[dict[str, str]]:
        """
        Fetches all utilities with unit ID.
        """
        print("Fetching utilities by unit ID:", unitID)
        unitID = int(unitID)
        utilities = InstalledUtility.getUnitUtilities(unitID, type=True)
        print(utilities)
        return utilities

    @staticmethod
    def fetchUtilityBills(id : str, monthRange : int, offset : datetime) -> tuple[dict[str, list[dict[str, str]]], datetime] :
        id = int(id)
        range = None
        for r in Range:
            if r.value == monthRange:
                range = r
                break
        offsetInt = (diffMonths(datetime.now(), offset)) // range.value + 1
        utilityType = Utility.readOne(id)["Type"] 
        utilityBills = {utilityType : Bill.getUtilityBills(id, range, offset=offsetInt)}
        for bill in utilityBills[utilityType]:
            bill["BillingPeriodEnd"] = bill["BillingPeriodEnd"].strftime("%Y-%m-%d")
        earliestBillDate = Bill.getEarliestUtilityBillDate(id) if Bill.getEarliestUtilityBillDate(id) is not None else date.today() - relativedelta(months=monthRange)
        monthsDiff = diffMonths(datetime.now(), datetime.combine(earliestBillDate, datetime.min.time())) - monthRange
        return utilityBills,  datetime.now() - relativedelta(months=monthsDiff)