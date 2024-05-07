import sqlite3
import hashlib
import os

def hashPassword(password, salt):
    # Concatenate password and salt
    salted_password = password.encode('utf-8') + salt
    
    # Hash salted password using SHA-256
    hashed_password = hashlib.sha256(salted_password).hexdigest()
    return hashed_password

def authenticate(username, password):
    # Connect to user database
    conn = sqlite3.connect('database/users.db')
    cursor = conn.cursor()

    # Get salt and hashed password for the username
    cursor.execute("SELECT salt, password FROM users WHERE username=?", (username,))
    user_data = cursor.fetchone()

    # Close connection
    conn.close()

    if user_data:
        stored_salt, stored_password = user_data
        hashed_password = hashPassword(password, stored_salt)
        if hashed_password == stored_password:
            if username.lower() == 'admin':
                return 'admin', username, True
            elif username.lower().startswith('tr'):
                return 'teacher', username, True
            elif username.lower().startswith('st'):
                return 'student', username, True
    return None, None, False
