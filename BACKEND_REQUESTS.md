# Features and Requests

### 1. Unit Table Update
- Request `UnitID`, `Name`, `Address`, and `UnitType` (add to Unit table)
- Based on `page`, `sortBy`, `sortOrder`, `searchValue`
- Request total number of records that satisfy the filters

---

### 2. Utility Table Update
- Request `UtilityID`, `Type`, `Status`, and `BillingCycle` (from Bills)  
- Based on `page`, `sortBy`, `sortOrder`, `searchValue`
- Request total number of records that satisfy the filters

---

### 3. Bill Table Update
- Request `BillID`, `UnitName` (from Units), `Type` (from Utilities), `TotalAmount`, `DueDate`  
- Based on `page`, `sortBy`, `sortOrder`, `searchValue`
- Request total number of records that satisfy the filters

---
> Not sure yet how to implement sa GUI pero kani ang goal
### 4. Unit Details  

- Request all Unit fields  
- Request `Bill totalAmount` and `BillID`for a single unit within a given range  
- Based on `range(1m, 3m, 6m, 1y)` and `offset` (kaning offset is like a page)
- Naka divide by utility ang data  
- Example:

```json
{
  "Electricity": [
    {
        "BillID": 1,
        "TotalAmount": 10000,
        "BillingPeriodEnd": "2024-01-01"
    },
    {
        "BillID": 2,
        "TotalAmount": 90000,
        "BillingPeriodEnd": "2024-02-01"
    }
  ],
  "Water": [
    // same for water
  ]
}
```

---

### 5. Utility Details
- Request all Utility fields + Billing Cycle (from Bills)  
- Same sa Unit Details but for one utility only  
- Example:

```json
[
    {
        "BillID": 1,
        "TotalAmount": 10000,
        "BillingPeriodEnd": "2024-01-01"
    },
    {
        "BillID": 2,
        "TotalAmount": 90000,
        "BillingPeriodEnd": "2024-02-01"
    }
]
```

---

### 6. Bills Details
- Request all Bills fields + `UnitName` (from Units) + `Type` (from Utilities)


### 7. Fetch Utility Dashboard data

- This is very similar to Unit Details
- Request Bill `totalAmount` and `BillID` for **ALL** units within a given range  
- Based on `range(1m, 3m, 6m, 1y)` and `offset` (kaning offset is like a page)
- Also fetches the most recent request that is before the range (ex: range is Jun 4 - Sep 4, we request for the most recent bill before Jun 4)
- Example:

```json
{
  "Electricity": [
    {
        "BillID": 1,
        "TotalAmount": 10000,
        "BillingPeriodEnd": "2024-01-01"
    },
    {
        "BillID": 2,
        "TotalAmount": 90000,
        "BillingPeriodEnd": "2024-02-01"
    }
  ],
  "Water": [
    // same for water
  ]
}
```

### 8. Fetch Bills Summary data

- This is interelated to the previous request
- Request the SUM of all Bills within a given range (excluding the most recent bill that is outside of the range)
- Request the SUM of all Bills within a given range that has a `Status` of `Paid`
- Request the COUNT of all Bills within a given range that has a `Status` of `Unpaid`, `Partially Paid`, or `Overdue`


### 9. Fetch Upcoming Bills data

- Request `BillID`, `Type`, `TotalAmount`, `DueDate`, `Status` of the top 15 Bills sorted by closest `Due Date`