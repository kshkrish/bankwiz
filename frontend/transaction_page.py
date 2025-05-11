import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import home_page
import transaction_history, deposit_money, withdraw_money, send_money
import session

# === Color Palette ===
LUX_GOLD = "#C7AE6A"
DEEP_BLACK = "#000000"
CLASSIC_GOLD = "#B99A45"
PALE_CREAM = "#E3D6B4"

def start():
    root = tk.Tk()
    root.title("Bank Wiz - Transaction")
    root.geometry("800x500")
    root.configure(bg=PALE_CREAM)

    # === Top Bar ===
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

    # === Title Section ===
    title_frame = tk.Frame(root, bg=PALE_CREAM)
    title_frame.pack(pady=(10, 20))

    title_icon = tk.Label(title_frame, text="💰", font=("Segoe UI Emoji", 28), bg=PALE_CREAM)
    title_icon.pack()

    title_label = tk.Label(title_frame, text="Transactions", font=("Segoe UI", 24, "bold"),
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

    # Buttons
    tk.Button(button_frame, text="Deposit Money", command=deposit_money.start, **btn_style).pack(pady=10)
    tk.Button(button_frame, text="Withdraw Money", command=withdraw_money.start, **btn_style).pack(pady=10)
    tk.Button(button_frame, text="Send Money", command=send_money.start, **btn_style).pack(pady=10)
    tk.Button(button_frame, text="Transaction History", command=transaction_history.start, **btn_style).pack(pady=10)

    root.mainloop()

def go_home(current_window):
    current_window.destroy()
    home_page.start()

if __name__ == "__main__":
    start()

