import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
from first_menu import firstMenu

def save_profile():
    # Code to save the profile information
    print("Profile information saved")

def change_profile_picture():
    file_path = filedialog.askopenfilename()
    if file_path:
        image = Image.open(file_path)
        image = image.resize((100, 100), Image.LANCZOS)  # Corrected resampling filter
        photo = ImageTk.PhotoImage(image)
        label_profile_picture.config(image=photo)
        label_profile_picture.image = photo
        print("Profile picture changed")

def edit_profile_window(parent):
    window = tk.Toplevel(parent)
    window.title("Edit Profile")
    window.geometry("400x400")

    button_change_picture = ttk.Button(window, text="Change Profile Picture", command=change_profile_picture)
    button_change_picture.grid(row=4, column=0, padx=10, pady=10, sticky='w')

    # Profile Picture Label
    profile_image = Image.open("profile.png")  # Default profile picture
    profile_image = profile_image.resize((100, 100), Image.LANCZOS)  # Corrected resampling filter
    photo = ImageTk.PhotoImage(profile_image)
    global label_profile_picture
    label_profile_picture = tk.Label(window, image=photo)
    label_profile_picture.image = photo
    label_profile_picture.grid(row=4, column=1, padx=10, pady=10)

    button_save = ttk.Button(window, text="Save", command=save_profile)
    button_save.grid(row=5, column=1, padx=10, pady=10, sticky='e')

    window.mainloop()



