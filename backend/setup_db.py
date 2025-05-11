import sqlite3

def create_tables():
    conn = sqlite3.connect("bankwiz.db")
    cursor = conn.cursor()

    # USERS table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT,
            phone TEXT,
            account_number TEXT UNIQUE,
            password TEXT,
            pin TEXT,
            branch TEXT,
            balance REAL DEFAULT 0,
            last_login TEXT
        )
    """)

    # TRANSACTIONS table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_number TEXT,
            type TEXT,
            amount REAL,
            date TEXT,
            details TEXT
        )
    """)

    # FIXED DEPOSIT (FD)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fd (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_number TEXT,
            amount REAL,
            rate REAL,
            duration INTEGER,
            created_on TEXT
        )
    """)

    # RECURRING DEPOSIT (RD)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rd (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_number TEXT,
            monthly_amount REAL,
            rate REAL,
            duration INTEGER,
            created_on TEXT
        )
    """)

    # SYSTEMATIC INVESTMENT PLAN (SIP)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sip (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_number TEXT,
            monthly_amount REAL,
            fund_name TEXT,
            start_date TEXT
        )
    """)

    # LOANS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS loans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_number TEXT,
            loan_type TEXT,
            amount REAL,
            interest REAL,
            duration INTEGER,
            start_date TEXT,
            status TEXT
        )
    """)

    # FEEDBACK (Optional)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_number TEXT,
            message TEXT,
            date TEXT
        )
    """)

    conn.commit()
    conn.close()
    print("✅ Database and all tables created successfully!")

if __name__ == "__main__":
    create_tables()
