from enum import Enum

class SortOrder:
    NONE = 0
    ASC = 1
    DESC = 2

class Range(Enum):
    """
    Enum class for storing constant range values. Each constant
    stores a value equivalent to the number of months that they
    are describing when converted.

    The constant values stored are:
    - ONE_MONTH = 1
    - THREE_MONTHS = 3
    - SIX_MONTHS = 6
    - ONE_YEAR = 12
    """
    ONE_MONTH = 1
    THREE_MONTHS = 3
    SIX_MONTHS = 6
    ONE_YEAR = 12

categoryColors = {
            "Electricity": "#FFA500",
            "Water": "#00BFFF",
            "Gas": "#FF1493",
            "Wifi": "#00FF7F",
            "Trash": "#A52A2A",
            "Maintenance": "#9370DB",
            "Miscellaneous": "#CCCCCC"

        }

defaultColor = "#AAAAAA"

billDataHeaders = ["Bill ID", "Unit Name", "Utility ID", "Type",  "Status", "Total Amount", "Billing Period Start", "Billing Period End", "Due Date"]
billDataDatabaseHeaders = ["BillID", "UnitName", "UtilityID", "Type", "Status", "TotalAmount", "BillingPeriodStart", "BillingPeriodEnd", "DueDate"]

utilityDataHeaders = ["Utility ID", "Type", "Unit Name", "Status", "Billing Cycle"]
utilityDataDatabaseHeaders = ["UtilityID", "Type", "UnitName", "Status", "BillingCycle"]