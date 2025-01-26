import sqlite3

def setup_database():
    try:
        conn = sqlite3.connect("finance_manager.db")
        cursor = conn.cursor()
        
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
        """)

        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS budgets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        """)

        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            date TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        """)

        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
        """)

        
        default_categories = ["Food", "Transport", "Entertainment", "Utilities", "Others"]
        for category in default_categories:
            cursor.execute("""
            INSERT OR IGNORE INTO categories (name) VALUES (?)
            """, (category,))
        
        conn.commit()

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        conn.close()


def get_categories():
    try:
        conn = sqlite3.connect("finance_manager.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM categories")
        categories = [row[0] for row in cursor.fetchall()]
        return categories
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []
    finally:
        conn.close()


def add_category(name):
    try:
        conn = sqlite3.connect("finance_manager.db")
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO categories (name) VALUES (?)
        """, (name,))
        conn.commit()
        print(f"Category '{name}' added successfully!")
    except sqlite3.IntegrityError:
        print(f"Category '{name}' already exists.")
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        conn.close()


def delete_category(name):
    try:
        conn = sqlite3.connect("finance_manager.db")
        cursor = conn.cursor()
        cursor.execute("""
        DELETE FROM categories WHERE name = ?
        """, (name,))
        conn.commit()
        print(f"Category '{name}' deleted successfully!")
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    setup_database()
    print("Database setup complete.")
