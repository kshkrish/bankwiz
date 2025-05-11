import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import transaction_page, account_page, deposit_page, loan_page, feedback_page, login_page
import session

# === Color Palette ===
LUX_GOLD = "#C7AE6A"
DEEP_BLACK = "#000000"
SOFT_BEIGE = "#D5C28F"
CLASSIC_GOLD = "#B99A45"
CHARCOAL_BLACK = "#1A1A1A"
PALE_CREAM = "#E3D6B4"

def start():
    user = session.get_session()
    name = user.get("name", "User")

    root = tk.Tk()
    root.title("Bank Wiz - Home")
    root.geometry("800x500")
    root.configure(bg=PALE_CREAM)

    # === Top Bar ===
    top_frame = tk.Frame(root, bg=PALE_CREAM)
    top_frame.pack(fill="x", padx=20, pady=10)

    try:
        logo_img = Image.open("resources/bank_logo.png")
        logo_img = logo_img.resize((40, 40), Image.LANCZOS)
        logo_photo = ImageTk.PhotoImage(logo_img)
        logo_label = tk.Label(top_frame, image=logo_photo, bg=PALE_CREAM)
        logo_label.image = logo_photo
        logo_label.pack(side="left", padx=(10, 5))
    except:
        logo_label = tk.Label(top_frame, text="🏦", font=("Segoe UI", 18), bg=PALE_CREAM)
        logo_label.pack(side="left")

    bank_name = tk.Label(top_frame, text="BANK WIZ", font=("Segoe UI", 14, "bold"), fg=CLASSIC_GOLD, bg=PALE_CREAM)
    bank_name.pack(side="left")

    greeting = tk.Label(root, text=f"Welcome, {name}!", font=("Segoe UI", 16), bg=PALE_CREAM, fg=DEEP_BLACK)
    greeting.pack(pady=10)

    # === Main Buttons ===
    button_frame = tk.Frame(root, bg=PALE_CREAM)
    button_frame.pack(pady=20)

    btn_style = {
        "bg": DEEP_BLACK,
        "fg": LUX_GOLD,
        "font": ("Segoe UI", 12, "bold"),
        "width": 18,
        "height": 2,
        "bd": 0,
        "activebackground": CLASSIC_GOLD,
        "activeforeground": DEEP_BLACK,
    }

    def open_and_close(current, next_page):
        current.destroy()
        next_page.start()

    tk.Button(button_frame, text="Account", command=lambda: open_and_close(root, account_page), **btn_style).grid(row=0, column=0, padx=20, pady=10)
    tk.Button(button_frame, text="Transaction", command=lambda: open_and_close(root, transaction_page), **btn_style).grid(row=0, column=1, padx=20, pady=10)
    tk.Button(button_frame, text="Deposit", command=lambda: open_and_close(root, deposit_page), **btn_style).grid(row=1, column=0, padx=20, pady=10)
    tk.Button(button_frame, text="Loan", command=lambda: open_and_close(root, loan_page), **btn_style).grid(row=1, column=1, padx=20, pady=10)

    # === Feedback Button ===
    feedback_btn = tk.Button(
        root,
        text="Feedback",
        bg=LUX_GOLD,
        fg=DEEP_BLACK,
        font=("Segoe UI", 10),
        command=lambda: feedback_page.start(),
    )
    feedback_btn.place(relx=1.0, rely=1.0, x=-20, y=-20, anchor="se")

    # === Logout Button ===
    def logout():
        session.clear_session()
        root.destroy()
        login_page.start()

    logout_btn = tk.Button(
        root,
        text="Logout",
        bg=CLASSIC_GOLD,
        fg=DEEP_BLACK,
        font=("Segoe UI", 10),
        command=logout
    )
    logout_btn.place(x=20, y=20)

    root.mainloop()

def main():
    start()

if __name__ == "__main__":
    main()

