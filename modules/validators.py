from tkinter import messagebox
from datetime import datetime


def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def validate_inputs(category, amount, date=None):
    if not category.strip():
        messagebox.showerror("Error", "Category cannot be empty")
        return False
    if not amount.replace('.', '', 1).isdigit() or float(amount) <= 0:
        messagebox.showerror("Error", "Amount must be a positive number")
        return False
    if date and not is_valid_date(date):
        messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD")
        return False
    return True
