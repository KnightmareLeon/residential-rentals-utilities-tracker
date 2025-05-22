import sys
import os
import random
from datetime import date, timedelta, datetime
from PyQt6.QtCore import QDate

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.controllers.unitsController import UnitsController
from src.controllers.utilitiesController import UtilitiesController
from src.controllers.billsController import BillsController

# Simulated controllers
# class UnitsController:
#     @staticmethod
#     def addUnit(name: str, address: str, type: str) -> str:
#         print(f"[Unit] {name}, {address}, {type}")
#         return "Unit added successfully"
# class UtilitiesController:
#     @staticmethod
#     def addUtility(type: str, mainUnitID: str, sharedUnitIDs: list[str], status: str, billingCycle: str, installationDate: QDate) -> str:
#         print(f"[Utility] {type}, Main: {mainUnitID}, Shared: {sharedUnitIDs}, Status: {status}, Cycle: {billingCycle}, Installed: {installationDate.toString('yyyy-MM-dd')}")
#         return "Utility added successfully"
# class BillsController:
#     @staticmethod
#     def addBill(unitID: str, utilityID: str, totalAmount: str, billingPeriodStart: QDate, billingPeriodEnd: QDate, status: str, dueDate: QDate) -> str:
#         print(f"[Bill] Unit {unitID}, Utility {utilityID}, Amount: ₱{totalAmount}, Period: {billingPeriodStart.toString('yyyy-MM-dd')} to {billingPeriodEnd.toString('yyyy-MM-dd')}, Status: {status}, Due: {dueDate.toString('yyyy-MM-dd')}")
#         return "Bill added successfully"

# Constants
SHARED_UTILITIES = ['Internet', 'Trash', 'Maintenance', 'Miscellaneous']
INDIVIDUAL_UTILITIES = ['Electricity', 'Water', 'Gas']
STATUSES = ['Unpaid', 'Paid', 'Partially Paid', 'Overdue']
START_DATE = date(2024, 1, 1)

def create_units():
    units = []
    shared_count = 3
    individual_per_shared = 4

    unit_id = 1
    for s in range(shared_count):
        shared_name = f"Shared Unit {s+1}"
        shared_address = f"123 Shared Street {s+1}"
        UnitsController.addUnit(shared_name, shared_address, "Shared")
        shared_unit = {"id": unit_id, "name": shared_name, "type": "Shared", "address": shared_address}
        unit_id += 1

        individuals = []
        for i in range(individual_per_shared):
            indiv_name = f"Unit {s+1}-{i+1}"
            UnitsController.addUnit(indiv_name, shared_address, "Individual")
            individuals.append({"id": unit_id, "name": indiv_name, "type": "Individual", "address": shared_address})
            unit_id += 1

        units.append({"shared": shared_unit, "individuals": individuals})

    return units

def add_utilities(units, install_date):
    utility_id_counter = 1
    utility_records = []

    for group in units:
        shared = group["shared"]
        individuals = group["individuals"]

        # Add shared utilities to shared unit
        for utility in SHARED_UTILITIES:
            UtilitiesController.addUtility(
                type=utility,
                mainUnitID=str(shared["id"]),
                sharedUnitIDs=[str(ind["id"]) for ind in individuals],
                status="Active",
                billingCycle="Monthly" if utility in ['Internet', 'Trash'] else "Irregular",
                installationDate=QDate(install_date.year, install_date.month, install_date.day)
            )
            utility_records.append({"utility": utility, "unit_id": shared["id"], "id": utility_id_counter, "shared": True})
            utility_id_counter += 1

        # Add individual utilities to individual units
        for ind in individuals:
            for utility in INDIVIDUAL_UTILITIES:
                UtilitiesController.addUtility(
                    type=utility,
                    mainUnitID=str(ind["id"]),
                    sharedUnitIDs=[],
                    status="Active",
                    billingCycle="Monthly" if utility != "Gas" else "Irregular",
                    installationDate=QDate(install_date.year, install_date.month, install_date.day)
                )
                utility_records.append({"utility": utility, "unit_id": ind["id"], "id": utility_id_counter, "shared": False})
                utility_id_counter += 1

    return utility_records

def generate_bills(utility_records, from_date):
    today = date.today()
    first_of_this_month = date(today.year, today.month, 1)
    month_cursor = date(from_date.year, from_date.month, 1)

    while month_cursor < today:
        next_month = (month_cursor.replace(day=28) + timedelta(days=4)).replace(day=1)
        for record in utility_records:
            utility_type = record["utility"]
            is_irregular = utility_type in ['Gas', 'Maintenance', 'Miscellaneous']
            is_monthly = not is_irregular

            should_add = is_monthly or (is_irregular and random.random() < 0.25)
            if not should_add:
                continue

            # Determine billing period
            if is_monthly:
                billing_start = QDate(month_cursor.year, month_cursor.month, 1)
                billing_end = QDate(next_month.year, next_month.month, 1).addDays(-1)
            else:
                rand_day = random.randint(1, 28)
                start_date = date(month_cursor.year, month_cursor.month, rand_day)
                end_date = start_date + timedelta(days=random.randint(3, 10))
                billing_start = QDate(start_date.year, start_date.month, start_date.day)
                billing_end = QDate(end_date.year, end_date.month, end_date.day)

            due_date = billing_end.addDays(15)

            # Determine status based on age
            if month_cursor < first_of_this_month - timedelta(days=90):
                status = 'Paid'
            elif first_of_this_month - timedelta(days=90) <= month_cursor < first_of_this_month - timedelta(days=30):
                # Bills 2–3 months ago → mostly paid, some overdue
                status = random.choices(
                    ['Paid', 'Overdue'],
                    weights=[80, 20],
                    k=1
                )[0]
            elif month_cursor >= first_of_this_month:
                # Current month → no overdue bills
                status = random.choices(
                    ['Paid', 'Unpaid', 'Partially Paid'],
                    weights=[40, 30, 30],
                    k=1
                )[0]
            else:
                # 1 month ago
                status = random.choices(
                    ['Paid', 'Unpaid', 'Partially Paid', 'Overdue'],
                    weights=[60, 15, 15, 10],
                    k=1
                )[0]

            amount = {
                'Electricity': random.uniform(1500, 4000),
                'Water': random.uniform(100, 800),
                'Gas': random.uniform(800, 1100),
                'Internet': random.uniform(1000, 3500),
                'Trash': random.uniform(50, 300),
                'Maintenance': random.uniform(50, 3500),
                'Miscellaneous': random.uniform(50, 3500),
            }[utility_type]

            BillsController.addBill(
                unitID=str(record["unit_id"]),
                utilityID=str(record["id"]),
                totalAmount=f"{amount:.2f}",
                billingPeriodStart=billing_start,
                billingPeriodEnd=billing_end,
                status=status,
                dueDate=due_date
            )
        month_cursor = next_month

# Run everything
unit_groups = create_units()
utility_data = add_utilities(unit_groups, START_DATE)
generate_bills(utility_data, START_DATE)
