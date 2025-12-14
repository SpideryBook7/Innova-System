import sqlite3
import hashlib

def init_db():
    connection = sqlite3.connect('database.db')
    
    with open('schema.sql') as f:
        connection.executescript(f.read())

    cur = connection.cursor()

    # Create default admin user
    # Email: admin@innova.com
    # Password: admin
    password = "admin"
    password_hash = hashlib.sha512(password.encode()).hexdigest()

    cur.execute("INSERT INTO usuarios (correo, password) VALUES (?, ?)",
                ('admin@innova.com', password_hash)
                )

    connection.commit()
    connection.close()
    print("Database initialized successfully!")
    print("Default Admin: admin@innova.com / admin")

if __name__ == '__main__':
    init_db()
