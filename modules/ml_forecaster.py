import sqlite3
from .database import setup_database
import numpy as np
from tkinter import Tk, Toplevel, Button, Label, Entry, messagebox, StringVar
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression


class MLForecaster:
    def __init__(self, root, user_id):
        self.root = root
        self.user_id = user_id
        self.conn = sqlite3.connect("finance_manager.db")
        self.create_window()

    def create_window(self):
        forecast_window = Toplevel(self.root)
        forecast_window.title("Expense Forecaster")
        Button(forecast_window, text="Forecast Expenses", command=self.forecast).pack(pady=10)
        forecast_window.geometry("300x200")

    def forecast(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT date, amount FROM expenses WHERE user_id = ?", (self.user_id,))
            data = cursor.fetchall()

            if len(data) < 2:
                messagebox.showerror("Error", "Not enough data to forecast")
                return

            dates = np.array([int(d.replace("-", "")) for d, _ in data]).reshape(-1, 1)
            amounts = np.array([a for _, a in data])

            model = LinearRegression()
            model.fit(dates, amounts)

            future_dates = np.array([dates[-1][0] + i * 100 for i in range(1, 4)]).reshape(-1, 1)
            predictions = model.predict(future_dates)

            cursor.execute("SELECT category, amount FROM budgets WHERE user_id = ?", (self.user_id,))
            budget_data = cursor.fetchall()

            warnings = []
            for category, budget in budget_data:
                if predictions.sum() > budget:
                    warnings.append(f"Forecasted expenses exceed the budget for '{category}'!")

            self.plot_results(dates, amounts, future_dates, predictions, model)

            if warnings:
                messagebox.showwarning("Budget Warning", "\n".join(warnings))

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while forecasting: {e}")

    def plot_results(self, dates, amounts, future_dates, predictions, model):
        plt.figure(figsize=(8, 6))
        plt.scatter(dates, amounts, color='blue', label='Actual Data')
        plt.plot(
            np.vstack((dates, future_dates)),
            np.hstack((model.predict(dates), predictions)),
            color='red',
            linestyle='--',
            label='Forecast',
        )
        plt.xlabel("Date (as YYYYMMDD)")
        plt.ylabel("Amount")
        plt.title("Expense Forecast")
        plt.legend()
        plt.tight_layout()
        plt.show()


class ExpenseTracker:
    def __init__(self, root, user_id):
        self.root = root
        self.user_id = user_id
        self.conn = sqlite3.connect("finance_manager.db")
        self.create_window()

    def create_window(self):
        tracker_window = Toplevel(self.root)
        tracker_window.title("Expense Tracker")
        Label(tracker_window, text="Category:").pack(pady=5)
        self.category_var = StringVar()
        Entry(tracker_window, textvariable=self.category_var).pack(pady=5)

        Label(tracker_window, text="Amount:").pack(pady=5)
        self.amount_var = StringVar()
        Entry(tracker_window, textvariable=self.amount_var).pack(pady=5)

        Label(tracker_window, text="Date (YYYY-MM-DD):").pack(pady=5)
        self.date_var = StringVar()
        Entry(tracker_window, textvariable=self.date_var).pack(pady=5)

        Button(tracker_window, text="Add Expense", command=self.add_expense).pack(pady=10)
        tracker_window.geometry("300x300")

    def add_expense(self):
        category = self.category_var.get()
        amount = self.amount_var.get()
        date = self.date_var.get()

        if validate_inputs(category, amount, date):
            try:
                cursor = self.conn.cursor()
                cursor.execute(
                    "INSERT INTO expenses (user_id, category, amount, date) VALUES (?, ?, ?, ?)",
                    (self.user_id, category, float(amount), date)
                )
                self.conn.commit()
                messagebox.showinfo("Success", "Expense added successfully!")

                forecaster = MLForecaster(self.root, self.user_id)
                forecaster.forecast()

            except sqlite3.Error as e:
                messagebox.showerror("Error", f"Database error: {e}")


def validate_inputs(*inputs):
    for value in inputs:
        if not value or value.strip() == "":
            messagebox.showerror("Error", "All fields must be filled")
            return False

        try:
            float(value)
        except ValueError:
            messagebox.showerror("Error", f"Invalid input: {value}. Must be a valid number.")
            return False

    return True
