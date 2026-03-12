"""
view_db.py — A simple script to view all entities and data in the terminal.
Use this to demonstrate the back-end SQLite database!
"""
import sqlite3

def display_database():
    try:
        # Connect to the local database file
        conn = sqlite3.connect('university.db')
        cursor = conn.cursor()
        
        # Get list of all tables (entities)
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [t[0] for t in cursor.fetchall() if t[0] != 'sqlite_sequence']
        
        if not tables:
            print("\n[!] The database is empty. Add some records in the GUI first!")
            return

        print("\n" + "="*50)
        print(" UNIVERSITY DATABASE SYSTEM — SHELL VIEW")
        print("="*50)

        for table_name in tables:
            print(f"\n--- ENTITY: {table_name.upper()} ---")
            
            # Fetch column names
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = [col[1] for col in cursor.fetchall()]
            print(" | ".join(columns))
            print("-" * (len(" | ".join(columns)) + 2))
            
            # Fetch all rows
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            
            if not rows:
                print("  (No records found)")
            else:
                for row in rows:
                    print(" | ".join(str(val) for val in row))
        
        print("\n" + "="*50)
        conn.close()

    except sqlite3.Error as e:
        print(f"\n[!] Error reading university.db: {e}")
    except Exception as e:
        print(f"\n[!] An unexpected error occurred: {e}")

if __name__ == "__main__":
    display_database()
