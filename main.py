import tkinter as tk
from tkinter import messagebox
from authentication import authenticate
from admin_menu import adminMenu
from teacher_menu import teacherMenu
from student_menu import studentMenu
from first_menu import firstMenu
from PIL import Image, ImageTk

def login():
    # Create a login window
    login_window = tk.Tk()
    login_window.title("Login")
    login_window.configure(bg="lightblue")

    # Text above entry fields
    text_above_entry = tk.Label(login_window, text=" GRADEBOOK GROOVE", font=("Arial", 14), bg="lightblue")
    text_above_entry.place(relx=0.5, rely=0.283, anchor=tk.CENTER)

    # Set login window size
    login_window.geometry("400x250")

    # Load the logo image
    original_logo = Image.open('logo.png').resize((60,60)) 
    logo_image = ImageTk.PhotoImage(original_logo) 

    # Logo
    logo_label = tk.Label(login_window, image=logo_image, bg="lightblue")
    logo_label.place(relx=0.08, rely=0.15,)

    # Username and password entry fields
    username_label = tk.Label(login_window, text="Username:", fg="black", bg="lightblue")
    username_label.place(relx=0.3, rely=0.4, anchor=tk.CENTER)
    username_entry = tk.Entry(login_window)
    username_entry.place(relx=0.55, rely=0.4, anchor=tk.CENTER)
    
    password_label = tk.Label(login_window, text="Password:", fg="black", bg="lightblue")
    password_label.place(relx=0.3, rely=0.5, anchor=tk.CENTER)
    password_entry = tk.Entry(login_window, show="*")
    password_entry.place(relx=0.55, rely=0.5, anchor=tk.CENTER)

    # Check if user is legit
    def authenticateUser():
        username = username_entry.get()
        password = password_entry.get()
        user_type, authenticated_username, authenticated = authenticate(username, password)
        if authenticated:
            if user_type == 'admin':
                login_window.destroy()
                adminMenu()
            elif user_type == 'teacher':
                login_window.destroy()
                teacherMenu(authenticated_username)
            elif user_type == 'student':
                login_window.destroy()
                studentMenu(authenticated_username)
        else:
            messagebox.showerror("Error", "Invalid username or password")

    login_button = tk.Button(login_window, text="Login", command=authenticateUser)
    login_button.place(relx=0.55, rely=0.65, anchor=tk.CENTER)

    # Run tkinter event loop for login window
    login_window.mainloop()
    
if __name__ == "__main__":
    firstMenu() 
