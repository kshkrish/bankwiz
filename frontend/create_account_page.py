import customtkinter as ctk
from tkinter import messagebox
import requests
import login_page  # Assumes you have login_page.start()

def main():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    app = ctk.CTk()
    app.title("Create New Account")
    app.geometry("400x650")

    # === Colors ===
    LUX_GOLD = "#C7AE6A"
    DEEP_BLACK = "#000000"
    BEIGE_GOLD = "#D5C28F"
    CLASSIC_GOLD = "#B99A45"
    CHARCOAL_BLACK = "#1A1A1A"
    PALE_CREAM = "#E3D6B4"

    app.configure(bg=CHARCOAL_BLACK)

    frame = ctk.CTkFrame(app, fg_color=CHARCOAL_BLACK, corner_radius=20)
    frame.pack(expand=True, fill="both", padx=20, pady=20)

    ctk.CTkLabel(frame, text="Let's Get Started!", font=("Segoe UI", 20, "bold"), text_color=LUX_GOLD).pack(pady=(20, 0))
    ctk.CTkLabel(frame, text="Fill the form to open a new account", font=("Segoe UI", 12), text_color=PALE_CREAM).pack(pady=(0, 10))

    def add_entry(label_text, placeholder, is_password=False):
        ctk.CTkLabel(frame, text=label_text, font=("Segoe UI", 12), text_color=PALE_CREAM).pack(pady=(10, 0))
        entry = ctk.CTkEntry(
            frame, placeholder_text=placeholder, width=300,
            fg_color=DEEP_BLACK, text_color=PALE_CREAM,
            border_color=CLASSIC_GOLD, border_width=1,
            placeholder_text_color=BEIGE_GOLD,
            show="*" if is_password else ""
        )
        entry.pack()
        return entry

    name_entry = add_entry("Full Name", "Enter name")
    phone_entry = add_entry("Phone Number", "Enter phone number")
    password_entry = add_entry("Password", "Enter password", is_password=True)
    confirm_password_entry = add_entry("Confirm Password", "Re-enter password", is_password=True)
    pin_entry = add_entry("4-digit PIN", "Enter 4-digit PIN", is_password=True)

    # === Dropdowns ===
    dropdown_frame = ctk.CTkFrame(frame, fg_color=CHARCOAL_BLACK)
    dropdown_frame.pack(pady=(10, 0))

    branch_option = ctk.CTkOptionMenu(dropdown_frame, values=[
        "Delhi", "Mumbai", "Chennai", "Kolkata", "Bangalore"
    ], width=140, fg_color=BEIGE_GOLD, button_color=CLASSIC_GOLD, text_color=DEEP_BLACK)
    branch_option.grid(row=0, column=0, padx=5)

    acc_type_option = ctk.CTkOptionMenu(dropdown_frame, values=[
        "Savings", "Current", "Business"
    ], width=140, fg_color=BEIGE_GOLD, button_color=CLASSIC_GOLD, text_color=DEEP_BLACK)
    acc_type_option.grid(row=0, column=1, padx=5)

    # === Register Logic ===
    def register_user():
        name = name_entry.get().strip()
        phone = phone_entry.get().strip()
        password = password_entry.get()
        confirm_password = confirm_password_entry.get()
        pin = pin_entry.get().strip()
        branch = branch_option.get()
        acc_type = acc_type_option.get()

        if not all([name, phone, password, confirm_password, pin, branch, acc_type]):
            messagebox.showerror("Error", "Please fill all fields.")
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match.")
            return

        if not (pin.isdigit() and len(pin) == 4):
            messagebox.showerror("Error", "PIN must be exactly 4 digits.")
            return

        try:
            payload = {
                "name": name,
                "phone": phone,
                "password": password,
                "pin": pin,
                "branch": branch,
                "account_type": acc_type
            }

            response = requests.post("http://127.0.0.1:5000/register", json=payload)

            if response.status_code == 200:
                acc_no = response.json().get("account_number", "N/A")
                messagebox.showinfo("Success", f"Account created successfully!\nAccount Number: {acc_no}")
                app.destroy()
                login_page.start()
            else:
                error_msg = response.json().get("message", "Registration failed.")
                messagebox.showerror("Failed", f"Status {response.status_code}: {error_msg}")

        except Exception as e:
            messagebox.showerror("Server Error", f"Could not connect to server.\n{str(e)}")

    # === Buttons ===
    ctk.CTkButton(
        frame, text="Register", width=200,
        fg_color=BEIGE_GOLD, text_color=DEEP_BLACK,
        hover_color=LUX_GOLD, command=register_user
    ).pack(pady=(20, 10))

    ctk.CTkButton(
        frame, text="Back to Login", width=200,
        fg_color=BEIGE_GOLD, text_color=DEEP_BLACK,
        hover_color=LUX_GOLD, command=lambda: [app.destroy(), login_page.start()]
    ).pack(pady=(0, 20))

    app.mainloop()


if __name__ == "__main__":
    main()




