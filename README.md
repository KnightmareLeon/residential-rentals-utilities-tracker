# UtiliTrack

UtiliTrack is a desktop application designed for rental property owners to track, manage, and analyze utility expenses across their units. Users can link units to utilities (like electricity, water, internet, etc.), log bills over time, and view cost trends through charts and visualizations. This helps identify inefficiencies, detect cost spikes, compare usage across units, and make data-driven decisions—such as whether to bundle shared utilities into rent. Ideal for managing anything from multi-room homes to large apartment complexes, UtiliTrack empowers owners to optimize expenses and improve financial performance.



## About
This application was made for a school project for the course **CCC151 - Information Management**

Here is the our [Google Docs link](https://docs.google.com/document/d/14NUibsdk8e9LtcCpfhOJAlk9soUE7Fkw1tqVVz8lVOI/edit?usp=sharing) that has our **Entity-Relationship Diagram** (ERD), **Entity-Relationship** (ERM), **Data Dictionary**, and **SQL Data Definition Language** (SQL DDL) for this project.

Members:
1. Leonard John T. Corpuz
2. Kim Gabriel A. Nasayao
3. Rogelio Angelo C. Bollozos



## Setup

### 1. Clone the Repository

First, clone the repository to your local system:

```bash
git clone https://github.com/KnightmareLeon/residential-rentals-utilities-tracker.git
cd utilitrack
```

### 2. Install Dependencies

Make sure you have Python 3.10+ installed. Then, create and activate a virtual environment:

#### Create a virtual environment
```bash
python -m venv venv
```

#### Activate the Virtual Environment
- On Windows:

    ```bash
    ./venv/Scripts/activate
    ```

- On Linux/macOS:

    ```bash
    source venv/bin/activate
    ```

#### Install Required Packages
```bash
pip install -r requirements.txt
```

### 3. Set Up the MySQL Database
Create a new MySQL database schema using your MySQL client or any GUI like MySQL Workbench:

```sql
CREATE DATABASE your_schema_name;
```

Create a .env file in the project root and add your MySQL configuration:

```ini
HOST=localhost
USER=your_mysql_username
PASSWORD=your_mysql_password
DATABASE=your_schema_name
```
Make sure the user has permission to access and modify the selected database.

### 4. Start the Application
You can now run the application!

```python
python main.py
```

## Features

### 1. **Dashboard**
   - **Utility Cost Visualization**: Displays a chart of utility costs over a selected time range (e.g., 1 month, 3 months, 6 months, 1 year).
   - **Summary Cards**:
     - Total balance of the selected period.
     - Total paid amount in the selected period.
     - Count of unpaid bills.
   - **Pagination**: Navigate through historical data using next/previous buttons.

### 2. **Bills Management**
   - **Upcoming Bills**: View a list of the top 15 most urgent bills, including details like:
     - Bill ID
     - Type (e.g., Electricity, Water, Internet)
     - Total Amount
     - Due Date
     - Status (e.g., Paid, Unpaid, Overdue)
   - **Add Bill**:
     - Assign bills to specific utilities (individual or shared).
     - Specify bill details such as type, amount, due date, and status.
   - **Edit Bill**:
     - Modify existing bill details, including amount, due date, and status.
   - **Delete Bill**:
     - Remove bills that are no longer needed or were added by mistake.

### 3. **Utilities Management**
   - **Add Utility**:
     - Assign utilities to specific units or share them across multiple units.
     - Specify utility type (e.g., Electricity, Water, Gas, Internet).
     - Set utility status (Active/Inactive) and billing cycle (Monthly, Quarterly, Annually).
   - **Edit Utility**:
     - Modify utility details, including type, associated units, status, and billing cycle.
   - **View Utility**:
     - View detailed information about a utility, including:
       - Utility ID, Type, Status, Billing Cycle, Installation Date.
       - Associated units and their details.
       - Historical bills for the utility.
   - **Delete Utility**: Remove utilities no longer in use.

### 4. **Units Management**
   - **View Unit Details**:
     - Display unit information, including:
       - Unit ID, Name, Address, and Unit Type.
       - Associated utilities and their statuses.
       - Historical bills for the unit.
   - **Shared Utilities**: Manage utilities shared across multiple units.

### 5. **Data Visualization**
   - **Interactive Charts**:
     - Hover over data points to view detailed information.
     - Filter utilities by type (e.g., Electricity, Water).
   - **Date Range Selection**:
     - Choose from predefined ranges (e.g., 1 month, 3 months, 6 months, 1 year).

### 6. **Database Integration**
   - **Utility Table**:
     - Stores information about utilities, including type, status, and billing cycle.
   - **Unit Table**:
     - Stores unit details, including name, address, and type.
   - **Bills Table**:
     - Tracks all bills, including their amounts, due dates, and statuses.
