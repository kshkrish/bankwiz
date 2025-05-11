import tkinter as tk
from tkinter import messagebox
import requests
import session

API_URL = "http://127.0.0.1:5000"

def start():
    root = tk.Tk()
    root.title("Apply for Loan")
    root.geometry("500x400")
    root.configure(bg="#E3D6B4")

    tk.Label(root, text="🏦 Apply for Loan", font=("Segoe UI", 22, "bold"), bg="#E3D6B4").pack(pady=20)

    tk.Label(root, text="Loan Type:", bg="#E3D6B4", font=("Segoe UI", 12)).pack()
    type_entry = tk.Entry(root, width=40, font=("Segoe UI", 12))
    type_entry.pack(pady=5)

    tk.Label(root, text="Amount:", bg="#E3D6B4", font=("Segoe UI", 12)).pack()
    amount_entry = tk.Entry(root, width=40, font=("Segoe UI", 12))
    amount_entry.pack(pady=5)

    def apply():
        account = session.get_logged_in_account()
        loan_type = type_entry.get().strip()
        amount = amount_entry.get().strip()

        if not loan_type or not amount:
            return messagebox.showerror("Error", "All fields are required.")

        try:
            res = requests.post(f"{API_URL}/loan/apply", json={
                "account_number": account,
                "loan_type": loan_type,
                "amount": amount
            })
            if res.status_code == 200:
                messagebox.showinfo("Success", res.json().get("message"))
                type_entry.delete(0, tk.END)
                amount_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Error", res.json().get("error", "Failed to apply for loan."))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(root, text="Submit Loan Application", command=apply,
              bg="#000", fg="#C7AE6A", font=("Segoe UI", 12, "bold")).pack(pady=20)

    root.mainloop()
