from datetime import datetime

def diffMonths(d1 : datetime, d2 : datetime) -> int:
    """
    Returns the difference between two datetime objects
    in terms of months.
    """
    return (d1.year - d2.year) * 12 + d1.month - d2.month