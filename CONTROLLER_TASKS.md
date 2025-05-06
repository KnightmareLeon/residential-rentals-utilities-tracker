## ✅ `fetchBillsController` – Guide Using 5-Step Workflow

### 🧠 Purpose:

Fetch bills with support for pagination, sorting, and search, including referred fields from `Unit` and `Utility`.

---

### 1. **Input Validation**

Check the types and presence of required parameters:

```python
if not isinstance(currentPage, int) or currentPage < 1:
  raise ValueError("Invalid page number. Must be a positive integer.")

if sortingOrder not in ["ASC", "DESC"]:
  raise ValueError("Invalid sorting order. Must be 'ASC' or 'DESC'.")

if not isinstance(sortingField, str) or not sortingField:
  raise ValueError("Invalid sorting field.")

if not isinstance(searchValue, str):
  raise ValueError("Invalid search value. Must be a string.")
```

---

### 2. **Data Fetching, Handling, and Cleaning**

Clean inputs and prepare parameters for the model:

```python
searchValue = searchValue.strip()
pageSize = 50
```

---

### 3. **Call the Model**

Use the `Bill` model’s `read` and `totalCount` methods. Include referred fields as needed:

```python
referred = {
  Unit: ["Name"],
  Utility: ["Type"]
}

if searchValue == "":
  totalCount = Bill.totalCount()
else:
  totalCount = Bill.totalCount(searchValue=searchValue)

totalPages = (totalCount + pageSize - 1) // pageSize  # avoids off-by-one

bills = Bill.read(
  referred=referred,
  page=currentPage,
  sortBy=sortingField,
  order=sortingOrder,
  searchValue=searchValue if searchValue else None
)
```

---

### 4. **Error Handling**

Wrap logic in `try/except` to ensure stable returns:

```python
try:
  # ... (Steps 1-3)
  return {
    "success": True,
    "data": bills,
    "totalPages": totalPages
  }
except Exception as e:
  return {
    "success": False,
    "error": str(e)
  }
```

---

### 5. **Return Success or Error Message**

Standard format ensures frontend/backend consistency.

---

### ✅ Final Controller Function (Cleaned and Ready)

```python
@staticmethod
def fetchBillsController(currentPage: int, sortingOrder: str, sortingField: str, searchValue: str) -> dict:
  try:
    # Input Validation
    if not isinstance(currentPage, int) or currentPage < 1:
      raise ValueError("Invalid page number. Must be a positive integer.")
    if sortingOrder not in ["ASC", "DESC"]:
      raise ValueError("Invalid sorting order. Must be 'ASC' or 'DESC'.")
    if not isinstance(sortingField, str) or not sortingField:
      raise ValueError("Invalid sorting field.")
    if not isinstance(searchValue, str):
      raise ValueError("Invalid search value. Must be a string.")

    # Data Cleaning
    searchValue = searchValue.strip()
    pageSize = 50
    referred = {Unit: ["Name"], Utility: ["Type"]}

    # Call Model
    totalCount = Bill.totalCount(searchValue=searchValue) if searchValue else Bill.totalCount()
    totalPages = (totalCount + pageSize - 1) // pageSize
    bills = Bill.read(
      referred=referred,
      page=currentPage,
      sortBy=sortingField,
      order=sortingOrder,
      searchValue=searchValue if searchValue else None
    )

    # Return Success
    return {
      "success": True,
      "data": bills,
      "totalPages": totalPages
    }

  except Exception as e:
    # Return Error
    return {
      "success": False,
      "error": str(e)
    }
```

---
