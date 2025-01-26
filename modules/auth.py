import sqlite3
from .database import setup_database
from tkinter import messagebox
import bcrypt


class Auth:
    def __init__(self, db_path):
        self.db_path = db_path

    def register(self, username, password):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
                existing_user = cursor.fetchone()

                if existing_user:
                    messagebox.showerror("Error", "Username already exists!")
                    return

                hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

                cursor.execute(
                    "INSERT INTO users (username, password) VALUES (?, ?)",
                    (username, hashed_password),
                )
                conn.commit()

                messagebox.showinfo("Success", "Registration successful!")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")

    def login(self, username, password):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT id, password FROM users WHERE username = ?", (username,)
                )
                user = cursor.fetchone()

                if user:
                    stored_password = user[1]
                    if isinstance(stored_password, str):
                        stored_password = stored_password.encode("utf-8")

                    if bcrypt.checkpw(password.encode("utf-8"), stored_password):
                        return user[0]
                    else:
                        messagebox.showerror("Error", "Invalid password")
                else:
                    messagebox.showerror("Error", "Invalid username")

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")

        return None
