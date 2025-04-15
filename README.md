# boarding-house-utilities-tracker

School project for CCC151

Members:
1. Leonard John T. Corpuz
2. Kim Gabriel A. Nasayao
3. Rogelio Angelo C. Bollozos

## 1. First-Time Project Setup After Cloning the Repo

These steps assume you're using **Python 3.10+**, **MySQL Server**, and **pip**.

### Step 1: Clone the Repository

```bash
git clone https://github.com/KnightmareLeon/boarding-house-utilities-tracker.git
cd boarding-house-utilities-tracker
```

### Step 2: Set Up a Python Virtual Environment

```bash
python -m venv venv
source venv/bin/activate       # For Linux/macOS
venv\Scripts\activate          # For Windows
```

### Step 3: Install Python Dependencies

```bash
pip install -r requirements.txt
```

> If anyone installs a new library later, they should run:

```bash
pip freeze > requirements.txt
```

### Step 4: Install and Configure MySQL Server

Make sure MySQL Server is installed **locally** (since you're not using remote DB hosting).

#### On Ubuntu (Linux):

```bash
sudo apt update
sudo apt install mysql-server
sudo systemctl start mysql
sudo mysql_secure_installation
```

#### On Windows:

- Download installer: [https://dev.mysql.com/downloads/installer/](https://dev.mysql.com/downloads/installer/)
    
- Install `MySQL Server`, `Workbench`, and `Command Line Client` (*optional*).
    
- Create an account and take note of your credentials

### Step 5: **Configure DB connection in your project**  

Create a `.env` file in your project root:

```env
HOST=localhost
USER=your_user
PASSWORD=your_password
DATABASE=your_database
```


---

## Project Structure Recommendation

```bash
boarding-house-utilities/
│
├── gui/                    # All PyQt6 views
│   └── mainWindow.py
│
├── controller/             # Logic handling DB ↔ UI
│   └── billController.py
│
├── models/                 # DB queries and data access
│   └── unitModel.py
│
├── assets/                 # Icons, images, etc.
├── requirements.txt        # Python dependencies
├── README.md
├── .env                    # Local credentials (optional)
└── main.py                 # App entry point
```

---

# Workflow for Ongoing Collaboration (Git & GitHub)

---

## For Feature Development

### Step 1: Create and Checkout a Feature Branch

```bash
git checkout dev
git pull origin dev
git checkout -b feature/gui-unit-table
```

> **Always branch off from `dev`**, never from `main`.

---

### Step 2: Make Changes and Commit Locally

```bash
git add .
git commit -m "Added unit table to main UI"
```

---

### Step 3: Push Your Branch to GitHub

```bash
git push -u origin feature/gui-unit-table
```

---

### Step 4: Open a Pull Request (PR) on GitHub

- Merge target: `dev`
    
- Assign a teammate to review your PR.
    
- Add a description: what you added, modified, or fixed.
    

---

### Step 5: After Approval, Merge to `dev`

If you're the one merging:

```bash
git checkout dev
git pull origin dev
git merge feature/gui-unit-table
git push origin dev
```

Then **delete** the feature branch:

```bash
git branch -d feature/gui-unit-table
git push origin --delete feature/gui-unit-table
```

---

## For Pulling New Changes

### Whenever another teammate merges a PR:

1. Fetch and switch to `dev`:
    

```bash
git checkout dev
git pull origin dev
```

2. If new dependencies were added:
    

```bash
pip install -r requirements.txt
```

3. If database changes were made:
    
    - Check if they shared SQL migrations or instructions.
        
    - Run the new SQL manually in MySQL Workbench or CLI.
        

---

## Handling Merge Conflicts

If a conflict arises during merge:

```bash
git status                 # See which files are in conflict
# Open them in your editor, resolve conflict sections marked <<<<<<< >>>>>>.
git add resolved_file.py
git commit
git push
```

---

## Versioning & Releases

When `dev` is stable and tested, merge into `main`:

```bash
git checkout main
git pull origin main
git merge dev
git push origin main
```

Then tag a release:

```bash
git tag -a v1.0 -m "First stable release"
git push origin --tags
```

---

## Testing Changes Before Merge

Each member should run the app locally:

```bash
python main.py
```

- Confirm that the new feature works.
    
- Confirm that nothing else broke.
    
- Confirm that the database is up to date.
    

---

