import sys
import os
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from PIL import Image, ImageTk
import requests

# === Local Imports ===
from session import set_account_number
import home_page
import create_account_page
import admin_dashboard

# === System Path Configuration ===
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# === Appearance & Theme ===
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# === Color Constants ===
LUX_GOLD = "#C7AE6A"
DEEP_BLACK = "#000000"
SOFT_BEIGE = "#D5C28F"
CLASSIC_GOLD = "#B99A45"
CHARCOAL_BLACK = "#1A1A1A"
PALE_CREAM = "#E3D6B4"

# === Login Window Setup ===
app = ctk.CTk()
app.geometry("800x500")
app.title("Bank Wiz - Login")
app.configure(bg=DEEP_BLACK)

# === Left Panel (Login Frame) ===
login_frame = ctk.CTkFrame(master=app, width=350, height=500, fg_color=CHARCOAL_BLACK, corner_radius=20)
login_frame.pack(side="left", fill="both")

title_label = ctk.CTkLabel(login_frame, text="Login", font=("Segoe UI", 24, "bold"), text_color=LUX_GOLD)
title_label.place(x=130, y=40)

# === Account Number Field ===
acc_label = ctk.CTkLabel(login_frame, text="Account Number", font=("Segoe UI", 14), text_color=PALE_CREAM)
acc_label.place(x=40, y=100)

acc_entry = ctk.CTkEntry(login_frame, width=250, placeholder_text="Enter number...")
acc_entry.place(x=40, y=130)

# === Password Field ===
pass_label = ctk.CTkLabel(login_frame, text="Password", font=("Segoe UI", 14), text_color=PALE_CREAM)
pass_label.place(x=40, y=180)

pass_entry = ctk.CTkEntry(login_frame, width=250, placeholder_text="Enter password...", show="*")
pass_entry.place(x=40, y=210)

# === Button Callbacks ===
def login():
    acc = acc_entry.get().strip()
    pwd = pass_entry.get().strip()

    if not acc or not pwd:
        messagebox.showwarning("Warning", "Please fill in all fields.")
        return

    # Admin Redirect
    if acc == "000000000000" and pwd == "admin":
        app.destroy()
        admin_dashboard.main()
        return

    try:
        response = requests.post("http://127.0.0.1:5000/login", json={
            "account_number": acc,
            "password": pwd
        })

        if response.status_code == 200:
            set_account_number(acc)
            app.destroy()
            home_page.main()
        else:
            messagebox.showerror("Login Failed", "Invalid credentials. Try again.")
    except Exception as e:
        messagebox.showerror("Server Error", f"Could not connect to server:\n{e}")

def open_create_account():
    app.destroy()
    create_account_page.main()

# === Buttons ===
login_button = ctk.CTkButton(login_frame, text="Login", fg_color=LUX_GOLD, text_color=DEEP_BLACK, width=200, command=login)
login_button.place(x=75, y=270)

create_button = ctk.CTkButton(login_frame, text="Create Account", fg_color=SOFT_BEIGE, text_color=DEEP_BLACK, width=200, command=open_create_account)
create_button.place(x=75, y=320)

# === Right Frame (Logo / Branding) ===
right_frame = tk.Frame(app, bg=PALE_CREAM, width=450)
right_frame.pack(side="right", fill="both", expand=True)

try:
    logo_path = os.path.join(os.path.dirname(__file__), "bank.png")
    logo_image = Image.open(logo_path)
    logo_image = logo_image.resize((200, 200), Image.LANCZOS)
    logo_photo = ImageTk.PhotoImage(logo_image)

    logo_label = tk.Label(right_frame, image=logo_photo, bg=PALE_CREAM)
    logo_label.image = logo_photo
    logo_label.place(relx=0.5, rely=0.5, anchor="center")
except:
    tk.Label(right_frame, text="BANK WIZ", font=("Segoe UI", 28, "bold"), fg=CLASSIC_GOLD, bg=PALE_CREAM).place(relx=0.5, rely=0.5, anchor="center")

# === App Launcher ===
def start():
    app.mainloop()

if __name__ == "__main__":
    start()




