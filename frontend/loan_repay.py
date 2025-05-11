import tkinter as tk
from tkinter import messagebox
import requests
import session

API_URL = "http://127.0.0.1:5000"

def start():
    root = tk.Tk()
    root.title("Repay Loan")
    root.geometry("500x350")
    root.configure(bg="#E3D6B4")

    tk.Label(root, text="💸 Repay Loan", font=("Segoe UI", 22, "bold"), bg="#E3D6B4").pack(pady=20)

    tk.Label(root, text="Loan ID:", bg="#E3D6B4", font=("Segoe UI", 12)).pack()
    loan_id_entry = tk.Entry(root, width=40, font=("Segoe UI", 12))
    loan_id_entry.pack(pady=5)

    tk.Label(root, text="Repayment Amount:", bg="#E3D6B4", font=("Segoe UI", 12)).pack()
    amount_entry = tk.Entry(root, width=40, font=("Segoe UI", 12))
    amount_entry.pack(pady=5)

    def repay():
        loan_id = loan_id_entry.get().strip()
        amount = amount_entry.get().strip()
        if not loan_id or not amount:
            return messagebox.showerror("Error", "All fields are required.")

        try:
            res = requests.post(f"{API_URL}/loan/repay", json={
                "loan_id": loan_id,
                "amount": amount
            })
            if res.status_code == 200:
                messagebox.showinfo("Success", res.json().get("message"))
                loan_id_entry.delete(0, tk.END)
                amount_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Error", res.json().get("error", "Repayment failed."))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(root, text="Submit Repayment", command=repay,
              bg="#000", fg="#C7AE6A", font=("Segoe UI", 12, "bold")).pack(pady=20)

    root.mainloop()
