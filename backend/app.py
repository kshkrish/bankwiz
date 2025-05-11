from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime
from flask_cors import CORS
import random

DB_NAME = "bankwiz.db"
app = Flask(__name__)
CORS(app)

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    account_number = data.get("account_number")
    password = data.get("password")

    if not account_number or not password:
        return jsonify({"error": "Missing account number or password"}), 400

    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE account_number=? AND password=?", (account_number, password)).fetchone()
    conn.close()

    if user:
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401

# === Utility ===
def generate_account_number():
    return str(random.randint(100000000000, 999999999999))  # 12-digit

# === USER AUTH ===

@app.route('/register', methods=['POST'])
@app.route('/register', methods=['POST'])
@app.route("/register", methods=["POST"])

def register():
    data = request.get_json()

    name = data.get("name")
    phone = data.get("phone")
    password = data.get("password")
    pin = data.get("pin")
    branch = data.get("branch")
    account_type = data.get("account_type")

    # Basic validation
    if not all([name, phone, password, pin, branch, account_type]):
        return jsonify({'message': 'All fields are required'}), 400

    if len(pin) != 4 or not pin.isdigit():
        return jsonify({'message': 'PIN must be exactly 4 digits'}), 400

    # Check if phone number is already in use
    conn = sqlite3.connect("bankwiz.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE phone = ?", (phone,))
    existing_user = cursor.fetchone()

    if existing_user:
        conn.close()
        return jsonify({'message': 'Phone number already registered'}), 400

    # Generate account number
    account_number = generate_account_number()

    # Insert the new user into the database
    try:
        cursor.execute("""
        INSERT INTO users (full_name, phone, account_number, password, pin, branch, account_type)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (name, phone, account_number, password, pin, branch, account_type))

        conn.commit()
        conn.close()

        return jsonify({
            'message': 'Registration successful',
            'account_number': account_number
        }), 200
    except sqlite3.IntegrityError as e:
        if "users.phone" in str(e):
            return jsonify({'message': 'Phone number already registered'}), 400
        elif "users.account_number" in str(e):
            return jsonify({'message': 'Account number conflict, please try again'}), 400
        else:
            return jsonify({'message': f"Registration failed: {str(e)}"}), 400
    except Exception as e:
        conn.close()
        return jsonify({'message': f"Error: {str(e)}"}), 500


# === ADMIN DASHBOARD ===

@app.route('/admin/users', methods=['GET'])
def get_all_users():
    conn = get_db_connection()
    users = conn.execute("SELECT full_name, phone, account_number, pin, branch, balance FROM users").fetchall()
    conn.close()
    return jsonify([dict(user) for user in users])

@app.route('/admin/delete', methods=['POST'])
def admin_delete_user():
    data = request.json
    account_number = data.get("account_number")
    password = data.get("password")
    pin = data.get("pin")

    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE account_number=? AND password=? AND pin=?", 
                        (account_number, password, pin)).fetchone()
    if user:
        conn.execute("DELETE FROM users WHERE account_number=?", (account_number,))
        conn.commit()
        conn.close()
        return jsonify({"message": "User deleted successfully"})
    else:
        conn.close()
        return jsonify({"error": "Invalid password or PIN"}), 403

# === ACCOUNT ===

@app.route('/account/<account_number>', methods=['GET'])
def get_account(account_number):
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE account_number=?", (account_number,)).fetchone()
    conn.close()
    if user:
        user_dict = dict(user)
        user_dict.pop("password", None)  # Don't return the password in the response
        return jsonify(user_dict)
    return jsonify({"error": "Account not found"}), 404

@app.route('/account/<account_number>', methods=['PUT'])
def update_account(account_number):
    data = request.json
    allowed_fields = ['full_name', 'phone', 'password', 'pin']
    updates = ", ".join(f"{field}=?" for field in allowed_fields if field in data)
    values = [data[field] for field in allowed_fields if field in data]
    
    if not updates:
        return jsonify({"error": "No valid fields provided"}), 400

    values.append(account_number)
    conn = get_db_connection()
    conn.execute(f"UPDATE users SET {updates} WHERE account_number = ?", values)
    conn.commit()
    conn.close()
    return jsonify({"message": "Account updated successfully"})

# === DELETE USER ===

@app.route('/account/<account_number>', methods=['DELETE'])
def delete_account(account_number):
    data = request.json
    password = data.get("password")
    pin = data.get("pin")

    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE account_number=? AND password=? AND pin=?", 
                        (account_number, password, pin)).fetchone()
    if user:
        conn.execute("DELETE FROM users WHERE account_number=?", (account_number,))
        conn.commit()
        conn.close()
        return jsonify({"message": "Account deleted"})
    else:
        conn.close()
        return jsonify({"error": "Invalid credentials"}), 403

# === TRANSACTIONS ===

@app.route('/transactions/<account_number>', methods=['GET'])
def get_transactions(account_number):
    conn = get_db_connection()
    txns = conn.execute("SELECT * FROM transactions WHERE account_number=? ORDER BY timestamp DESC", 
                        (account_number,)).fetchall()
    conn.close()
    return jsonify([dict(txn) for txn in txns])

@app.route('/transaction', methods=['POST'])
def add_transaction():
    data = request.json
    account_number = data['account_number']
    txn_type = data['type']
    amount = float(data['amount'])
    to_account = data.get("to_account")

    conn = get_db_connection()

    # Withdraw or Transfer
    if txn_type in ['withdraw', 'transfer']:
        balance = conn.execute("SELECT balance FROM users WHERE account_number=?", 
                               (account_number,)).fetchone()
        if not balance or balance['balance'] < amount:
            conn.close()
            return jsonify({"error": "Insufficient balance"}), 400
        conn.execute("UPDATE users SET balance = balance - ? WHERE account_number=?", 
                     (amount, account_number))

    # Deposit or Receiver
    if txn_type == "deposit":
        conn.execute("UPDATE users SET balance = balance + ? WHERE account_number=?", 
                     (amount, account_number))

    if txn_type == "transfer" and to_account:
        conn.execute("UPDATE users SET balance = balance + ? WHERE account_number=?", 
                     (amount, to_account))

    conn.execute("INSERT INTO transactions (account_number, type, amount, to_account) VALUES (?, ?, ?, ?)",
                 (account_number, txn_type, amount, to_account))
    conn.commit()
    conn.close()
    return jsonify({"message": "Transaction successful"})

# === LOANS ===

@app.route("/loan/apply", methods=["POST"])
def loan_apply():
    data = request.get_json()
    acc = data.get("account_number")
    loan_type = data.get("loan_type")
    amount = float(data.get("amount"))

    conn = get_db_connection()
    conn.execute("INSERT INTO loans (account_number, loan_type, amount, remaining, status) VALUES (?, ?, ?, ?, ?)",
                 (acc, loan_type, amount, amount, "active"))
    conn.commit()
    conn.close()
    return jsonify({"message": "Loan application submitted."}), 200

@app.route("/loan/details/<account_number>")
def loan_details(account_number):
    conn = get_db_connection()
    loans = conn.execute("SELECT id, loan_type, amount, remaining, status FROM loans WHERE account_number=?", 
                         (account_number,)).fetchall()
    conn.close()
    return jsonify({"loans": [dict(l) for l in loans]})

@app.route("/loan/repay", methods=["POST"])
def loan_repay():
    data = request.get_json()
    loan_id = data.get("loan_id")
    repay_amt = float(data.get("amount"))

    conn = get_db_connection()
    loan = conn.execute("SELECT remaining FROM loans WHERE id=?", (loan_id,)).fetchone()
    if not loan:
        conn.close()
        return jsonify({"error": "Loan not found"}), 404

    new_amt = max(loan["remaining"] - repay_amt, 0)
    status = "closed" if new_amt == 0 else "active"
    conn.execute("UPDATE loans SET remaining=?, status=? WHERE id=?", (new_amt, status, loan_id))
    conn.commit()
    conn.close()
    return jsonify({"message": "Repayment successful"}), 200

# === FEEDBACK ===

@app.route("/feedback", methods=["POST"])
def submit_feedback():
    data = request.get_json()
    acc_no = data.get("account_number")
    subject = data.get("subject")
    message = data.get("message")

    if not acc_no or not subject or not message:
        return jsonify({"error": "Missing fields"}), 400

    conn = get_db_connection()
    conn.execute("INSERT INTO feedback (account_number, subject, message) VALUES (?, ?, ?)", 
                 (acc_no, subject, message))
    conn.commit()
    conn.close()
    return jsonify({"message": "Feedback submitted"}), 200

# === RUN SERVER ===

if __name__ == '__main__':
    app.run(debug=True)


