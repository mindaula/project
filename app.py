import os
import tkinter as tk
from tkinter import messagebox, simpledialog
from modules.database import setup_database, add_category, get_categories, delete_category
from modules.auth import Auth
from modules.validators import validate_inputs, is_valid_date
from modules.expense_tracker import ExpenseTracker
from modules.ml_forecaster import MLForecaster



class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Finance Manager")
        self.db_path = "finance_manager.db"
        setup_database()
        self.auth = Auth(self.db_path)
        self.user_id = None
        self.create_login_window()

    def create_login_window(self):
        self.login_window = tk.Toplevel(self.root)
        self.login_window.title("Login")
        tk.Label(self.login_window, text="Username:").pack(pady=5)
        self.username_entry = tk.Entry(self.login_window)
        self.username_entry.pack(pady=5)

        tk.Label(self.login_window, text="Password:").pack(pady=5)
        self.password_entry = tk.Entry(self.login_window, show="*")
        self.password_entry.pack(pady=5)

        tk.Button(self.login_window, text="Login", command=self.login).pack(pady=5)
        tk.Button(self.login_window, text="Register", command=self.register).pack(pady=5)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        self.user_id = self.auth.login(username, password)

        if self.user_id:
            messagebox.showinfo("Success", "Login successful!")
            self.login_window.destroy()
            self.create_main_window()
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        self.auth.register(username, password)

    def create_main_window(self):
        tk.Label(self.root, text="Welcome to Finance Manager").pack(pady=10)
        tk.Button(self.root, text="Set Up Budgets", command=self.setup_budgets).pack(pady=5)
        tk.Button(self.root, text="Track Expenses", command=self.track_expenses).pack(pady=5)
        tk.Button(self.root, text="Forecast Expenses", command=self.forecast_expenses).pack(pady=5)
        tk.Button(self.root, text="Manage Categories", command=self.manage_categories).pack(pady=5)

    def setup_budgets(self):
        ExpenseTracker(self.root, self.user_id).setup_budgets()

    def track_expenses(self):
        ExpenseTracker(self.root, self.user_id).track_expenses()

    def forecast_expenses(self):
        MLForecaster(self.root, self.user_id)

    def manage_categories(self):
        categories_window = tk.Toplevel(self.root)
        categories_window.title("Manage Categories")

        tk.Label(categories_window, text="Available Categories:").pack(pady=5)

        categories_listbox = tk.Listbox(categories_window)
        categories_listbox.pack(pady=5)

        categories = get_categories()
        for category in categories:
            categories_listbox.insert(tk.END, category)

        def add_new_category():
            new_category = simpledialog.askstring("New Category", "Enter the category name:")
            if new_category:
                add_category(new_category)
                categories_listbox.insert(tk.END, new_category)
                messagebox.showinfo("Success", f"Category '{new_category}' added!")

        def delete_selected_category():
            selected_category = categories_listbox.get(tk.ACTIVE)
            if selected_category:
                confirm = messagebox.askyesno("Confirm", f"Are you sure you want to delete '{selected_category}'?")
                if confirm:
                    delete_category(selected_category)
                    categories_listbox.delete(tk.ACTIVE)
                    messagebox.showinfo("Success", f"Category '{selected_category}' deleted!")

        tk.Button(categories_window, text="Add Category", command=add_new_category).pack(pady=5)
        tk.Button(categories_window, text="Delete Selected", command=delete_selected_category).pack(pady=5)


if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
