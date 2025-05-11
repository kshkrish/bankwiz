import tkinter as tk
from tkinter import messagebox
import requests
import session

API_URL = "http://127.0.0.1:5000"

def start():
    root = tk.Tk()
    root.title("Withdraw Money")
    root.geometry("400x300")
    root.configure(bg="#E3D6B4")

    tk.Label(root, text="🏧 Withdraw Money", font=("Segoe UI", 20, "bold"), bg="#E3D6B4").pack(pady=20)

    tk.Label(root, text="Amount (₹):", bg="#E3D6B4").pack()
    amount_entry = tk.Entry(root, font=("Segoe UI", 14))
    amount_entry.pack(pady=10)

    def withdraw():
        amount = amount_entry.get()
        account = session.get_logged_in_account()
        if not account:
            return messagebox.showwarning("Warning", "No user logged in.")
        if not amount.isdigit():
            return messagebox.showerror("Invalid", "Please enter a valid amount.")
        try:
            res = requests.post(f"{API_URL}/withdraw", json={"account_number": account, "amount": float(amount)})
            messagebox.showinfo("Success", res.json().get("message"))
        except:
            messagebox.showerror("Error", "Transaction failed.")

    tk.Button(root, text="Withdraw", command=withdraw, bg="#000", fg="#C7AE6A",
              font=("Segoe UI", 12, "bold")).pack(pady=20)

    root.mainloop()
