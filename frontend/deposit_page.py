import tkinter as tk
from tkinter import messagebox, ttk
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
    root.title("Bank Wiz - Deposit")
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

    title_icon = tk.Label(title_frame, text="📈", font=("Segoe UI Emoji", 28), bg=PALE_CREAM)
    title_icon.pack()

    title_label = tk.Label(title_frame, text="Deposits", font=("Segoe UI", 24, "bold"),
                           fg=DEEP_BLACK, bg=PALE_CREAM)
    title_label.pack()

    # === Buttons Frame ===
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

    tk.Button(button_frame, text="Open FD", command=lambda: messagebox.showinfo("FD", "FD form coming soon!"), **btn_style).pack(pady=10)
    tk.Button(button_frame, text="Open RD", command=lambda: messagebox.showinfo("RD", "RD form coming soon!"), **btn_style).pack(pady=10)
    tk.Button(button_frame, text="Open SIP", command=lambda: messagebox.showinfo("SIP", "SIP form coming soon!"), **btn_style).pack(pady=10)
    tk.Button(button_frame, text="View Details", command=show_details_popup, **btn_style).pack(pady=10)

    root.mainloop()

def go_home(current_window):
    current_window.destroy()
    home_page.start()

def show_details_popup():
    popup = tk.Toplevel()
    popup.title("Deposit Details")
    popup.geometry("500x400")
    popup.configure(bg=PALE_CREAM)

    canvas = tk.Canvas(popup, bg=PALE_CREAM, highlightthickness=0)
    scrollbar = ttk.Scrollbar(popup, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg=PALE_CREAM)

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Mock deposit info
    deposit_data = {
        "Active FD": "1",
        "Total FD Amount": "₹50,000",
        "Active RD": "2",
        "Total RD Amount": "₹20,000",
        "Active SIPs": "3",
        "SIP Investment": "₹3,000/month"
    }

    for key, value in deposit_data.items():
        tk.Label(scrollable_frame, text=f"{key}: {value}",
                 font=("Segoe UI", 12), bg=PALE_CREAM, fg=DEEP_BLACK).pack(anchor="w", padx=20, pady=5)

if __name__ == "__main__":
    start()

