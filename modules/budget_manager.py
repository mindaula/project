import sqlite3
from .database import setup_database  
from tkinter import Toplevel, Label, Entry, Button, messagebox

class BudgetManager:
    def __init__(self, root, user_id):
        self.root = root
        self.user_id = user_id
        self.conn = sqlite3.connect("finance_manager.db")
        self.create_window()

    def create_window(self):
        budget_window = Toplevel(self.root)
        budget_window.title("Budget Manager")

        
        def load_existing_categories():
            try:
                cursor = self.conn.cursor()
                cursor.execute("""
                    SELECT DISTINCT name FROM categories
                """)
                categories = cursor.fetchall()
                if categories:
                    print("Vorhandene Kategorien:", [cat[0] for cat in categories]) 
                else:
                    print("Keine Kategorien vorhanden")
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"Database error: {e}")

        load_existing_categories()

        Label(budget_window, text="Category:").grid(row=0, column=0, padx=10, pady=5)
        category_entry = Entry(budget_window)
        category_entry.grid(row=0, column=1, padx=10, pady=5)

        Label(budget_window, text="Amount:").grid(row=1, column=0, padx=10, pady=5)
        amount_entry = Entry(budget_window)
        amount_entry.grid(row=1, column=1, padx=10, pady=5)

        def validate_inputs(category, amount):
            if not category.strip():
                messagebox.showerror("Error", "Category cannot be empty")
                return False
            try:
                float(amount)
                return True
            except ValueError:
                messagebox.showerror("Error", "Amount must be a number")
                return False

        def add_budget():
            category = category_entry.get()
            amount = amount_entry.get()

            if validate_inputs(category, amount):
                try:
                    cursor = self.conn.cursor()
                    cursor.execute("""
                        INSERT INTO budgets (user_id, category, amount)
                        VALUES (?, ?, ?)
                    """, (self.user_id, category, float(amount)))
                    self.conn.commit()
                    messagebox.showinfo("Success", "Budget added successfully!")
                    category_entry.delete(0, 'end')
                    amount_entry.delete(0, 'end')
                    load_existing_categories()
                except sqlite3.Error as e:
                    messagebox.showerror("Error", f"Database error: {e}")

        Button(budget_window, text="Add Budget", command=add_budget).grid(row=2, column=0, columnspan=2, pady=10)

    @staticmethod
    def initialize_database():
        conn = sqlite3.connect("finance_manager.db")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS budgets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                category TEXT NOT NULL,
                amount REAL NOT NULL
            )
        """)
        conn.commit()
        conn.close()
