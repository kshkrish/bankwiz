import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import home_page
import loan_apply, loan_details, loan_repay

# === Color Palette ===
LUX_GOLD = "#C7AE6A"
DEEP_BLACK = "#000000"
SOFT_BEIGE = "#D5C28F"
CLASSIC_GOLD = "#B99A45"
CHARCOAL_BLACK = "#1A1A1A"
PALE_CREAM = "#E3D6B4"

def show_loan_page():
    root = tk.Tk()
    root.title("Bank Wiz - Loan")
    root.geometry("800x500")
    root.configure(bg=PALE_CREAM)

    # === Top Frame ===
    top_frame = tk.Frame(root, bg=PALE_CREAM)
    top_frame.pack(fill="x", padx=20, pady=(20, 10))

    try:
        logo_img = Image.open("resources/bank_logo.png")
        logo_img = logo_img.resize((100, 40), Image.LANCZOS)
        logo_photo = ImageTk.PhotoImage(logo_img)
        home_btn = tk.Button(top_frame, image=logo_photo, bg=PALE_CREAM, bd=0,
                             activebackground=PALE_CREAM, command=lambda: go_home(root))
        home_btn.image = logo_photo
        home_btn.pack(side="left")
    except:
        home_btn = tk.Button(top_frame, text="🏦 BANK WIZ", font=("Segoe UI", 12, "bold"),
                             fg=CLASSIC_GOLD, bg=PALE_CREAM, bd=0, command=lambda: go_home(root))
        home_btn.pack(side="left")

    # === Title Frame ===
    title_frame = tk.Frame(root, bg=PALE_CREAM)
    title_frame.pack(pady=(10, 20))

    title_icon = tk.Label(title_frame, text="💳", font=("Segoe UI Emoji", 28), bg=PALE_CREAM)
    title_icon.pack()

    title_label = tk.Label(title_frame, text="Loan", font=("Segoe UI", 24, "bold"),
                           fg=DEEP_BLACK, bg=PALE_CREAM)
    title_label.pack()

    # === Center Buttons ===
    button_frame = tk.Frame(root, bg=PALE_CREAM)
    button_frame.pack(pady=10)

    btn_style = {
        "bg": DEEP_BLACK,
        "fg": LUX_GOLD,
        "font": ("Segoe UI", 14, "bold"),
        "width": 20,
        "height": 2,
        "bd": 0,
        "activebackground": CLASSIC_GOLD,
        "activeforeground": DEEP_BLACK,
    }

    tk.Button(button_frame, text="Apply Loan", command=lambda: apply_loan(root), **btn_style).pack(pady=10)
    tk.Button(button_frame, text="Loan Details", command=lambda: loan_details(root), **btn_style).pack(pady=10)
    tk.Button(button_frame, text="Repay Loan", command=lambda: repay_loan(root), **btn_style).pack(pady=10)

    root.mainloop()

# === Navigation Functions ===
# === Navigation Functions ===
def go_home(current_window):
    current_window.destroy()
    home_page.start()  # Call the start function of home_page

def apply_loan(current_window):
    current_window.destroy()
    loan_apply.show_loan_apply_page()

def loan_details(current_window):
    current_window.destroy()
    loan_details.show_loan_details_page()

def repay_loan(current_window):
    current_window.destroy()
    loan_repay.show_loan_repay_page()

# === Start Function ===
def start():
    show_loan_page()

# Only run if directly executed
if __name__ == "__main__":
    start()

