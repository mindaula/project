import sqlite3
from .database import setup_database  
from tkinter import Toplevel, Label, Entry, Button, messagebox, ttk

class ExpenseTracker:
    def __init__(self, root, user_id):
        self.root = root
        self.user_id = user_id
        self.conn = sqlite3.connect("finance_manager.db")
        self.create_window()

    def create_window(self):
        expense_window = Toplevel(self.root)
        expense_window.title("Expense Tracker")

        Label(expense_window, text="Category:").grid(row=0, column=0, padx=10, pady=5)
        category_combobox = ttk.Combobox(expense_window)  
        category_combobox.grid(row=0, column=1, padx=10, pady=5)

        Label(expense_window, text="Amount:").grid(row=1, column=0, padx=10, pady=5)
        amount_entry = Entry(expense_window)
        amount_entry.grid(row=1, column=1, padx=10, pady=5)

        Label(expense_window, text="Date (YYYY-MM-DD):").grid(row=2, column=0, padx=10, pady=5)
        date_entry = Entry(expense_window)
        date_entry.grid(row=2, column=1, padx=10, pady=5)

        
        def load_categories():
            try:
                cursor = self.conn.cursor()
                
                cursor.execute("SELECT name FROM categories")
                categories = [cat[0] for cat in cursor.fetchall()]
                if categories:
                    category_combobox['values'] = categories
                    print("Geladene Kategorien:", categories)
                else:
                    print("Keine Kategorien vorhanden")
                    category_combobox['values'] = [] 
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"Database error: {e}")

        load_categories() 

        def validate_inputs(category, amount, date):
            if not category.strip():
                messagebox.showerror("Error", "Category cannot be empty")
                return False
            if not date.strip():
                messagebox.showerror("Error", "Date cannot be empty")
                return False
            try:
                float(amount)
                return True
            except ValueError:
                messagebox.showerror("Error", "Amount must be a number")
                return False

        def add_expense():
            category = category_combobox.get()
            amount = amount_entry.get()
            date = date_entry.get()

            if validate_inputs(category, amount, date):
                try:
                    cursor = self.conn.cursor()
                    cursor.execute("""
                        INSERT INTO expenses (user_id, category, amount, date)
                        VALUES (?, ?, ?, ?)
                    """, (self.user_id, category, float(amount), date))
                    self.conn.commit()
                    messagebox.showinfo("Success", "Expense added successfully!")
                    amount_entry.delete(0, 'end')
                    date_entry.delete(0, 'end')
                    category_combobox.set('')  
                except sqlite3.Error as e:
                    messagebox.showerror("Error", f"Database error: {e}")

        Button(expense_window, text="Add Expense", command=add_expense).grid(row=3, column=0, columnspan=2, pady=10)

    @staticmethod
    def initialize_database():
        conn = sqlite3.connect("finance_manager.db")
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                category TEXT NOT NULL,
                amount REAL NOT NULL,
                date TEXT NOT NULL
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL
            )
        """)
        conn.commit()
        conn.close()
