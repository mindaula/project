import sqlite3
from .database import setup_database
import matplotlib.pyplot as plt
from tkinter import Toplevel, Button, messagebox


class Visualizer:
    def __init__(self, root, user_id):
        self.root = root
        self.user_id = user_id
        self.conn = sqlite3.connect("finance_manager.db")
        self.create_window()

    def create_window(self):
        viz_window = Toplevel(self.root)
        viz_window.title("Expense Visualizer")
        Button(viz_window, text="Show Charts", command=self.plot_data).pack(pady=10)
        viz_window.geometry("300x200")

    def plot_data(self):
        try:
            cursor = self.conn.cursor()

            cursor.execute("""
                SELECT category, SUM(amount) AS total_spent 
                FROM expenses 
                WHERE user_id = ? 
                GROUP BY category
            """, (self.user_id,))
            expense_data = cursor.fetchall()

            cursor.execute("""
                SELECT category, amount AS budget 
                FROM budgets 
                WHERE user_id = ?
            """, (self.user_id,))
            budget_data = cursor.fetchall()

            budget_dict = {row[0]: row[1] for row in budget_data}
            categories = []
            spent = []
            budgets = []

            for category, total_spent in expense_data:
                categories.append(category)
                spent.append(total_spent)
                budgets.append(budget_dict.get(category, 0))

            if not categories:
                messagebox.showerror("Error", "No data to visualize")
                return

            x = range(len(categories))
            plt.figure(figsize=(10, 6))
            plt.bar(x, spent, width=0.4, label="Spent", align="center", color="skyblue")
            plt.bar(x, budgets, width=0.4, label="Budget", align="edge", color="orange")
            plt.xticks(x, categories, rotation=45, ha="right")
            plt.xlabel("Category")
            plt.ylabel("Amount")
            plt.title("Expenses vs Budgets")
            plt.legend()
            plt.tight_layout()
            plt.show()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
