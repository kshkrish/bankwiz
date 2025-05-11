import tkinter as tk
from tkinter import ttk, messagebox
import requests
import session

API_URL = "http://127.0.0.1:5000"

def start():
    root = tk.Tk()
    root.title("Transaction History")
    root.geometry("800x500")
    root.configure(bg="#E3D6B4")

    tk.Label(root, text="📜 Transaction History", font=("Segoe UI", 24, "bold"), bg="#E3D6B4").pack(pady=20)

    tree = ttk.Treeview(root, columns=("Type", "Amount", "Date", "Remark"), show="headings")
    for col in tree["columns"]:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=180)
    tree.pack(pady=10, fill="both", expand=True)

    account = session.get_logged_in_account()
    if account:
        try:
            response = requests.get(f"{API_URL}/transactions/{account}")
            data = response.json()
            for txn in data.get("transactions", []):
                tree.insert("", "end", values=(txn["type"], txn["amount"], txn["date"], txn["remark"]))
        except:
            messagebox.showerror("Error", "Could not fetch transactions.")
    else:
        messagebox.showwarning("Warning", "No user session found.")

    root.mainloop()
