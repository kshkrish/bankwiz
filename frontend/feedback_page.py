import tkinter as tk
from tkinter import messagebox
import requests
import session

API_URL = "http://127.0.0.1:5000"

def start():
    root = tk.Tk()
    root.title("Feedback")
    root.geometry("500x450")
    root.configure(bg="#E3D6B4")

    tk.Label(root, text="📝 Feedback", font=("Segoe UI", 22, "bold"), bg="#E3D6B4").pack(pady=20)

    tk.Label(root, text="Subject:", bg="#E3D6B4", font=("Segoe UI", 12)).pack(anchor="w", padx=30)
    subject_entry = tk.Entry(root, width=50, font=("Segoe UI", 12))
    subject_entry.pack(pady=5)

    tk.Label(root, text="Message:", bg="#E3D6B4", font=("Segoe UI", 12)).pack(anchor="w", padx=30)
    message_text = tk.Text(root, height=10, width=50, font=("Segoe UI", 12))
    message_text.pack(pady=5)

    def submit_feedback():
        subject = subject_entry.get().strip()
        message_body = message_text.get("1.0", tk.END).strip()
        account = session.get_logged_in_account()

        if not account:
            return messagebox.showerror("Error", "You must be logged in to submit feedback.")
        if not subject or not message_body:
            return messagebox.showerror("Error", "All fields are required.")

        try:
            res = requests.post(f"{API_URL}/feedback", json={
                "account_number": account,
                "subject": subject,
                "message": message_body
            })
            if res.status_code == 200:
                messagebox.showinfo("Success", res.json().get("message"))
                subject_entry.delete(0, tk.END)
                message_text.delete("1.0", tk.END)
            else:
                messagebox.showerror("Error", res.json().get("error", "Failed to submit feedback."))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to connect to server.\n{e}")

    tk.Button(root, text="Submit Feedback", command=submit_feedback,
              bg="#000", fg="#C7AE6A", font=("Segoe UI", 12, "bold")).pack(pady=20)

    root.mainloop()
