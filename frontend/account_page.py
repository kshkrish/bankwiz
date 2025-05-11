import tkinter as tk
from tkinter import messagebox, Toplevel
from PIL import Image, ImageTk
import home_page
import session

# === Color Palette ===
LUX_GOLD = "#C7AE6A"
DEEP_BLACK = "#000000"
CLASSIC_GOLD = "#B99A45"
PALE_CREAM = "#E3D6B4"

def start():
    root = tk.Tk()
    root.title("Bank Wiz - Account")
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

    # === Title ===
    title_frame = tk.Frame(root, bg=PALE_CREAM)
    title_frame.pack(pady=(10, 20))

    tk.Label(title_frame, text="🧾", font=("Segoe UI Emoji", 28), bg=PALE_CREAM).pack()
    tk.Label(title_frame, text="Account", font=("Segoe UI", 24, "bold"),
             fg=DEEP_BLACK, bg=PALE_CREAM).pack()

    # === Buttons ===
    button_frame = tk.Frame(root, bg=PALE_CREAM)
    button_frame.pack(pady=10)

    btn_style = {
        "bg": DEEP_BLACK,
        "fg": LUX_GOLD,
        "font": ("Segoe UI", 14, "bold"),
        "width": 22,
        "height": 2,
        "bd": 0,
        "activebackground": CLASSIC_GOLD,
        "activeforeground": DEEP_BLACK,
    }

    tk.Button(button_frame, text="Show Details", command=show_details_popup, **btn_style).pack(pady=10)
    tk.Button(button_frame, text="Download Statement", command=download_statement, **btn_style).pack(pady=10)
    tk.Button(button_frame, text="View Charts", command=view_charts, **btn_style).pack(pady=10)
    tk.Button(button_frame, text="Edit Account Info", command=edit_info, **btn_style).pack(pady=10)

    root.mainloop()

def go_home(window):
    window.destroy()
    home_page.start()

def show_details_popup():
    popup = Toplevel()
    popup.title("Account Details")
    popup.geometry("400x350")
    popup.configure(bg=PALE_CREAM)

    canvas = tk.Canvas(popup, bg=PALE_CREAM, highlightthickness=0)
    scrollbar = tk.Scrollbar(popup, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg=PALE_CREAM)

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Dummy data - replace with actual session/db data
    user_data = {
        "Account Holder": session.get("name"),
        "Account Number": session.get("account_number"),
        "Account Type": session.get("account_type"),
        "Branch": session.get("branch"),
        "Balance": "₹50,000",
        "Created On": "2024-01-10",
        "Last Login": "2025-05-01 11:00 AM",
    }

    for key, value in user_data.items():
        tk.Label(scrollable_frame, text=f"{key}:", font=("Segoe UI", 12, "bold"),
                 fg=DEEP_BLACK, bg=PALE_CREAM).pack(anchor="w", padx=20, pady=(5, 0))
        tk.Label(scrollable_frame, text=value, font=("Segoe UI", 12),
                 fg=CLASSIC_GOLD, bg=PALE_CREAM).pack(anchor="w", padx=40)

    tk.Button(popup, text="Close", command=popup.destroy,
              bg=DEEP_BLACK, fg=LUX_GOLD, font=("Segoe UI", 12, "bold"),
              activebackground=CLASSIC_GOLD, activeforeground=DEEP_BLACK).pack(pady=10)

def download_statement():
    messagebox.showinfo("Download", "PDF statement feature coming soon!")

def view_charts():
    messagebox.showinfo("Charts", "Chart visualization coming soon!")

def edit_info():
    messagebox.showinfo("Edit", "Edit account details feature coming soon.")

if __name__ == "__main__":
    start()

