from first_menu import firstMenu
import sqlite3
import os
from authentication import hashPassword

def createUser(username, name, password):
    # Check if the username/studentID already exists
    conn = sqlite3.connect('database/users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users WHERE username=?", (username,))
    existing_user = cursor.fetchone()
    conn.close()

    if existing_user:
        print("Error: Username already exists.")
        return

    # Generate salt
    salt = os.urandom(16)
    
    # Hash password with the salt
    hashed_password = hashPassword(password, salt)
    
    conn = sqlite3.connect('database/users.db')
    cursor = conn.cursor()

    cursor.execute("INSERT INTO users (username, name, salt, password) VALUES (?, ?, ?, ?)", (username, name, salt, hashed_password))
    conn.commit()

    # Close connection
    conn.close()
    print("\nUser successfully added")


def deleteUser(username):
    conn = sqlite3.connect('database/users.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM users WHERE username=?", (username,))
    conn.commit()

    conn.close()
    print("\nUser successfully deleted.")


def adminMenu():
    print("\nAdmin Menu:")
    print("Press 1 to create a user")
    print("Press 2 to delete a user")
    print("Press 3 to logout\n")
    option = input("Select an option: ")
    checkOptionAdmin(option)

def checkOptionAdmin(option):
    if option == "1":
        print("Create selected")
        username = input("Enter new username (user ID): ")
        name = input("Enter user's full name: ")
        password = input("Enter password: ")
        createUser(username, name, password)
        adminMenu()
    elif option == "2":
        print("Delete selected")
        username = input("Enter username (user ID) of the user to be deleted: ")
        deleteUser(username)
        adminMenu()
    elif option == "3":
        print("Logout selected")
        firstMenu()
    else:
        print("Invalid option. Please select a valid option.")
        adminMenu()
