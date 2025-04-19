import random
from datetime import date, timedelta, datetime

unit_types = ["Residential", "Commercial", "Industrial", "Mixed-Use", "Office", "Retail"]
statuses = ["Active", "Inactive"]
payment_statuses = ["Paid", "Unpaid", "Overdue", "Partially Paid"]
street_names = ["Main", "Side", "Back", "Central", "Elm", "Pine", "Maple", "Oak", "Hill", "River"]

utility_types = ["Water", "Electricity", "Internet", "Gas", "Cable", "Waste"]
unit_names = [f"Unit {name}" for name in ["Alpha", "Beta", "Gamma", "Delta", "Epsilon", "Zeta", "Eta", "Theta", "Iota", "Kappa"]]
utility_statuses = ["Active", "Inactive"]
billing_cycles = ["Monthly", "Quarterly", "Yearly"]

bill_types = ["Electricity", "Water", "Internet", "Gas", "Cable", "Waste", "Miscellaneous"]
unit_names = [f"Unit {name}" for name in ["Alpha", "Beta", "Gamma", "Delta", "Epsilon", "Zeta", "Eta", "Theta", "Iota", "Kappa"]]
bill_statuses = ["Unpaid", "Paid", "Overdue", "Partially Paid"]

def generateUnitData():
    sampleData1 = []

    for i in range(1, 51):
        unit_id = f"U{i:03}"
        name = f"Unit {chr(64 + ((i - 1) % 26 + 1))}{i}"
        address = f"{100 + i * 3} {random.choice(street_names)} St"
        unit_type = random.choice(unit_types)
        status = random.choice(statuses)
        payment_status = random.choice(payment_statuses)

        sampleData1.append({
            "UnitID": unit_id,
            "Name": name,
            "Address": address,
            "UnitType": unit_type,
            "Status": status,
            "PaymentStatus": payment_status
        })

    return sampleData1

def generateUtilityData():
    sampleData2 = []

    for i in range(1, 51):
        utility_id = f"UT{i:03}"
        utility_type = random.choice(utility_types)
        unit_name = random.choice(unit_names)
        status = random.choice(utility_statuses)
        billing_cycle = random.choice(billing_cycles)

        sampleData2.append({
            "UtilityID": utility_id,
            "Type": utility_type,
            "UnitName": unit_name,
            "Status": status,
            "BillingCycle": billing_cycle
        })
    
    return sampleData2

def generateBillData():
    sampleData3 = []

    for i in range(1, 51):
        bill_id = f"BILL{i:03}"
        unit_name = random.choice(unit_names)
        bill_type = random.choice(bill_types)
        amount = f"₱{random.uniform(500, 10000):,.2f}"  
        days_offset = random.randint(-10, 30)
        due_date = (date.today() + timedelta(days=days_offset)).isoformat()
        status = random.choice(bill_statuses)

        sampleData3.append({
            "BillID": bill_id,
            "UnitName": unit_name,
            "Type": bill_type,
            "TotalAmount": amount,
            "DueDate": due_date,
            "Status": status
        })
    
    return sampleData3

def generateRandomUtilityData(startDate=None, endDate=None):
    if startDate is None:
        startDate = datetime.today() - timedelta(days=365)
    if endDate is None:
        endDate = datetime.today()

    def random_date(start, end):
        delta = end - start
        return start + timedelta(days=random.randint(0, delta.days))

    categories = {
        "Electricity": (1000, 10000),
        "Water": (50, 250),
        "Gas": (1000, 2000),
        "Wifi": (1000, 3500),
        "Trash": (500, 500),
        "Maintenance": (100, 5000),
        "Miscellaneous": (0, 5000)
    }

    data = {}
    for category, (min_amt, max_amt) in categories.items():
        num_entries = random.randint(20, 50)
        bills = []
        for _ in range(num_entries):
            bill_date = random_date(startDate, endDate)
            amount = random.randint(min_amt, max_amt)
            bills.append({
                "TotalAmount": str(amount),
                "BillingPeriodEnd": bill_date.strftime("%Y-%m-%d")
            })
        bills.sort(key=lambda b: b["BillingPeriodEnd"])
        data[category] = bills

    return data