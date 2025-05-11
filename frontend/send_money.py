import tkinter as tk
from tkinter import messagebox
import requests
import session

API_URL = "http://127.0.0.1:5000"

def start():
    root = tk.Tk()
    root.title("Send Money")
    root.geometry("450x350")
    root.configure(bg="#E3D6B4")

    tk.Label(root, text="💸 Send Money", font=("Segoe UI", 20, "bold"), bg="#E3D6B4").pack(pady=20)

    fields = ["Recipient Acc No", "Amount (₹)", "Remark"]
    entries = {}

    for field in fields:
        tk.Label(root, text=field + ":", bg="#E3D6B4").pack()
        entry = tk.Entry(root, font=("Segoe UI", 12))
        entry.pack(pady=5)
        entries[field] = entry

    def send():
        from_acc = session.get_logged_in_account()
        to_acc = entries["Recipient Acc No"].get().strip()
        amount = entries["Amount (₹)"].get().strip()
        remark = entries["Remark"].get().strip()

        if not all([from_acc, to_acc, amount]):
            return messagebox.showerror("Error", "Please fill all fields.")
        if not amount.isdigit():
            return messagebox.showerror("Invalid", "Enter a valid amount.")

        try:
            res = requests.post(f"{API_URL}/transfer", json={
                "from_account": from_acc,
                "to_account": to_acc,
                "amount": float(amount),
                "remark": remark
            })
            messagebox.showinfo("Success", res.json().get("message"))
        except:
            messagebox.showerror("Error", "Transfer failed.")

    tk.Button(root, text="Send", command=send, bg="#000", fg="#C7AE6A",
              font=("Segoe UI", 12, "bold")).pack(pady=20)

    root.mainloop()
