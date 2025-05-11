import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import database as db
import login_page  # Import login_page to redirect after logout

DB_NAME = "bankwiz.db"

# === Color Palette ===
LUX_GOLD = "#C7AE6A"
DEEP_BLACK = "#000000"
SOFT_BEIGE = "#D5C28F"
CLASSIC_GOLD = "#B99A45"
PALE_CREAM = "#E3D6B4"

def start():
    root = tk.Tk()
    root.title("Admin Dashboard - BankWiz")
    root.geometry("800x500")
    root.configure(bg=PALE_CREAM)

    tk.Label(root, text="Admin Dashboard", font=("Segoe UI", 20, "bold"),
             bg=PALE_CREAM, fg=DEEP_BLACK).pack(pady=20)

    table_frame = tk.Frame(root, bg=PALE_CREAM)
    table_frame.pack(pady=10)

 # === Logout Section ===
    def logout():
        root.destroy()  # Close the admin dashboard window
        login_page.start()  # Redirect to the login page

    # Logout Button
    tk.Button(root, text="Logout", bg=DEEP_BLACK, fg=LUX_GOLD,
              font=("Segoe UI", 12), command=logout).pack(pady=20)
    
    # Table Headers
    headers = ["ID", "Name", "Account No", "Branch", "Balance", "Last Login"]
    for i, header in enumerate(headers):
        tk.Label(table_frame, text=header, font=("Segoe UI", 10, "bold"),
                 bg=DEEP_BLACK, fg=LUX_GOLD, width=15, relief="ridge").grid(row=0, column=i)

    # Load Users from database
    users = db.get_all_users()
    for row_num, user in enumerate(users, start=1):
        for col_num, item in enumerate(user):
            tk.Label(table_frame, text=item, bg=PALE_CREAM, fg=DEEP_BLACK,
                     font=("Segoe UI", 10), width=15, relief="groove").grid(row=row_num, column=col_num)

    # === Delete User Section ===
    def delete_user_prompt():
        acc_no = simpledialog.askstring("Delete User", "Enter Account Number to Delete:", parent=root)
        if not acc_no:
            return

        # Admin password verification
        confirm_password = simpledialog.askstring("Confirm", "Enter Admin Password to confirm:", show="*", parent=root)
        if confirm_password == "admin":
            # Delete user from database
            db.delete_user(acc_no)
            messagebox.showinfo("Deleted", f"User {acc_no} deleted successfully.")
            root.destroy()
            start()  # Refresh the dashboard
        else:
            messagebox.showerror("Error", "Incorrect admin password.")

    # Delete Account Button
    tk.Button(root, text="Delete Account", bg=DEEP_BLACK, fg=LUX_GOLD,
              font=("Segoe UI", 12), command=delete_user_prompt).pack(pady=20)

   

    root.mainloop()

# === Main Function ===
def main():
    start()

# For testing directly
if __name__ == "__main__":
    main()



