import sqlite3
import os

def setup_database():
    # Remove existing database if it exists
    if os.path.exists('passwords.db'):
        os.remove('passwords.db')
        print("Removed existing database")
    
    # Create new database
    conn = sqlite3.connect('passwords.db')
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT,
            master_password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create passwords table
    cursor.execute('''
        CREATE TABLE passwords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            website TEXT NOT NULL,
            username TEXT,
            encrypted_password TEXT NOT NULL,
            url TEXT,
            category TEXT DEFAULT 'General',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
    ''')
    
    conn.commit()
    conn.close()
    print("SQLite database setup completed successfully!")
    print("Database file: passwords.db")

if __name__ == '__main__':
    setup_database()