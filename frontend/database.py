import sqlite3

def create_database():
    conn = sqlite3.connect("bankwiz.db")
    cursor = conn.cursor()

    # Enable foreign key constraints
    cursor.execute("PRAGMA foreign_keys = ON;")

    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    phone TEXT UNIQUE NOT NULL,
    account_number TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    pin TEXT NOT NULL,
    branch TEXT NOT NULL,
    account_type TEXT NOT NULL,
    balance REAL DEFAULT 0.0,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

    -- TRANSACTIONS TABLE
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        account_number TEXT NOT NULL,
        type TEXT NOT NULL,
        amount REAL NOT NULL,
        to_account TEXT,
        timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (account_number) REFERENCES users(account_number) ON DELETE CASCADE
    );

    -- LOANS TABLE
    CREATE TABLE IF NOT EXISTS loans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        account_number TEXT NOT NULL,
        loan_type TEXT NOT NULL,
        amount REAL NOT NULL,
        interest_rate REAL NOT NULL,
        duration_months INTEGER NOT NULL,
        status TEXT NOT NULL DEFAULT 'pending',
        approved_on TEXT,
        FOREIGN KEY (account_number) REFERENCES users(account_number) ON DELETE CASCADE
    );

    -- FIXED DEPOSITS TABLE
    CREATE TABLE IF NOT EXISTS fd (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        account_number TEXT NOT NULL,
        amount REAL NOT NULL,
        duration_months INTEGER NOT NULL,
        interest_rate REAL NOT NULL,
        start_date TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (account_number) REFERENCES users(account_number) ON DELETE CASCADE
    );

    -- RECURRING DEPOSITS TABLE
    CREATE TABLE IF NOT EXISTS rd (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        account_number TEXT NOT NULL,
        monthly_amount REAL NOT NULL,
        duration_months INTEGER NOT NULL,
        interest_rate REAL NOT NULL,
        start_date TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (account_number) REFERENCES users(account_number) ON DELETE CASCADE
    );

    -- SYSTEMATIC INVESTMENT PLAN TABLE
    CREATE TABLE IF NOT EXISTS sip (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        account_number TEXT NOT NULL,
        fund_name TEXT NOT NULL,
        monthly_investment REAL NOT NULL,
        start_date TEXT DEFAULT CURRENT_TIMESTAMP,
        duration_months INTEGER NOT NULL,
        FOREIGN KEY (account_number) REFERENCES users(account_number) ON DELETE CASCADE
    );

    -- FEEDBACK TABLE
    CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        account_number TEXT NOT NULL,
        message TEXT NOT NULL,
        submitted_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (account_number) REFERENCES users(account_number) ON DELETE CASCADE
    );
    """)

    conn.commit()
    conn.close()
    print("✅ BankWiz database initialized successfully as 'bankwiz.db'")

def get_all_users():
    import sqlite3
    conn = sqlite3.connect("bankwiz.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, full_name, account_number, branch, balance, created_at FROM users")
    users = cursor.fetchall()
    conn.close()
    return users

def delete_user(account_number):
    import sqlite3
    conn = sqlite3.connect("bankwiz.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE account_number=?", (account_number,))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()


