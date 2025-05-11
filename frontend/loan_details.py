import tkinter as tk
from tkinter import messagebox
import requests
import session

API_URL = "http://127.0.0.1:5000"

def start():
    root = tk.Tk()
    root.title("Loan Details")
    root.geometry("600x400")
    root.configure(bg="#E3D6B4")

    tk.Label(root, text="📋 Your Loans", font=("Segoe UI", 22, "bold"), bg="#E3D6B4").pack(pady=20)

    text_box = tk.Text(root, height=15, width=70, font=("Segoe UI", 11))
    text_box.pack(pady=10)

    def fetch_loans():
        account = session.get_logged_in_account()
        try:
            res = requests.get(f"{API_URL}/loan/details/{account}")
            if res.status_code == 200:
                loans = res.json().get("loans", [])
                if not loans:
                    text_box.insert(tk.END, "No loans found.\n")
                else:
                    for loan in loans:
                        text_box.insert(tk.END, f"Loan ID: {loan['id']}\n")
                        text_box.insert(tk.END, f"Type: {loan['loan_type']}\n")
                        text_box.insert(tk.END, f"Amount: ₹{loan['amount']}\n")
                        text_box.insert(tk.END, f"Remaining: ₹{loan['remaining']}\n")
                        text_box.insert(tk.END, f"Status: {loan['status']}\n")
                        text_box.insert(tk.END, "-"*40 + "\n")
            else:
                messagebox.showerror("Error", "Unable to fetch loan details.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    fetch_loans()
    root.mainloop()
