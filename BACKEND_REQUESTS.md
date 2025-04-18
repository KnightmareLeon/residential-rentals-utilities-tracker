# Features and Requests

### 1. Unit Table Update
- Request `UnitID`, `Name`, `Address`, and `UnitType` (add to Unit table)  
- Based on `page`, `sortBy`, `sortOrder`, `searchValue`

---

### 2. Utility Table Update
- Request `UtilityID`, `Type`, `Status`, and `BillingCycle` (from Bills)  
- Based on `page`, `sortBy`, `sortOrder`, `searchValue`

---

### 3. Bill Table Update
- Request `BillID`, `UnitName` (from Units), `Type` (from Utilities), `TotalAmount`, `DueDate`  
- Based on `page`, `sortBy`, `sortOrder`, `searchValue`

---
> Not sure yet how to implement sa GUI pero kani ang goal
### 4. Unit Details  

- Request all Unit fields  
- Request `Bill totalAmount` for a single unit within a given range  
- Based on `range(1m, 3m, 6m, 1y)` and `offset`  
- Naka divide by utility ang data  
- Example:

```json
{
  "Electricity": [
    {
      "TotalAmount": "P10,000",
      "BillingPeriodEnd": "2024-01-01"
    },
    {
      "TotalAmount": "90,000",
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
    "TotalAmount": "P10,000",
    "BillingPeriodEnd": "2024-01-01"
  },
  {
    "TotalAmount": "90,000",
    "BillingPeriodEnd": "2024-02-01"
  }
]
```

---

### 6. Bills Details
- Request all Bills fields + `UnitName` (from Units) + `Type` (from Utilities)
