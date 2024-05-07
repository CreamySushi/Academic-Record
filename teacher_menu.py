import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from first_menu import firstMenu
from upload_file import browseFile
from PIL import Image, ImageTk
from profile_window import edit_profile_window
import sqlite3

def teacherMenu(username):
    root = tk.Tk()
    root.title("GradeBook Groove")
    root.geometry('1280x720')
    root.configure(bg='#AED6E8')

    # Variables to store the selected values
    selected_subject = tk.StringVar()
    selected_class = tk.StringVar()
    selected_year_level = tk.StringVar()
    selected_term = tk.StringVar()
    selected_semester = tk.StringVar()

    # Store references to class buttons
    class_buttons = []

    def open_edit_profile_window():
        root.lift()  # Lift the main window to the top
        edit_profile_window(root)

    def open_profile_menu(event):
        profile_menu.post(label_profile_icon.winfo_rootx(), label_profile_icon.winfo_rooty() + label_profile_icon.winfo_height())
    
    def change_subject(event, subject_combobox):
        selected_subject.set(subject_combobox.get())

    def select_class(class_num):
        selected_class.set(class_num)
        update_class_buttons()
        displayStudentsGrades()  # Update the table when a class is selected

    def update_class_buttons():
        for button in class_buttons:
            button.config(bg='#AED6E8')  # Reset button color
        if selected_class.get():
            class_buttons[int(selected_class.get()) - 1].config(bg='yellow')  # Highlight selected class

    def exit_application():
        root.destroy()

    def get_name(username):  # Change studentID to username
        # Connect to the user database
        conn = sqlite3.connect('database/users.db')
        cursor = conn.cursor()

        # Retrieve the name associated with the username
        cursor.execute("SELECT name FROM users WHERE username=?", (username,))
        name = cursor.fetchone()[0]  # Fetches the first row, first column which is the name
        conn.close()

        return name
    
    def displayStudentsGrades():
        # Get the selected semester, term, and class
        selected_semester_val = semester_combobox.get()
        selected_term_val = term_combobox.get()
        selected_class_val = selected_class.get()

        if selected_semester_val and selected_term_val and selected_class_val:
            # Connect to grades database
            conn = sqlite3.connect('database/records.db')
            cursor = conn.cursor()

            # Retrieve grades for the selected semester, term, and class
            cursor.execute("SELECT section, studentName, subjectCode, subjectName, grades FROM grades_table WHERE semester=? AND term=? AND section=?", (selected_semester_val, selected_term_val, selected_class_val))
            class_grades = cursor.fetchall()

            conn.close()

            if class_grades:
                # Display class grades
                print(f"\n{selected_semester_val} - {selected_term_val.capitalize()} grades for Class {selected_class_val}:")
                for section, student_name, subject_code, subject_name, grades in class_grades:
                   print(f"{section} | {student_name} | {subject_code} | {subject_name} | {grades}")

                # Update the table with class grades
                update_table(class_grades)

                # Show the table
                table_frame.place(relx=0.5, rely=0.5, anchor="center")
            else:
                print(f"No grades found for Class {selected_class_val} in this semester and term.")

        else:
            print("Please select semester, term, and class.")
    

    def update_table(class_grades):
        # Clear previous data
        for row in table.get_children():
            table.delete(row)

        # Add new data to the table
        for section, student_name, subject_code, subject_name, grades in class_grades:
            table.insert("", "end", values=(section, student_name, subject_code, subject_name, grades))

    # Welcome
    label_welcome = tk.Label(root, text="GradeBook Groove", font=("Arial", 32, "bold"), bg='#AED6E8')
    label_welcome.place(x=20, y=10, anchor='nw')

    # Load the profile icon
    profile_image = Image.open("profile.png")
    profile_image = profile_image.resize((50, 50), Image.LANCZOS)
    profile_icon = ImageTk.PhotoImage(profile_image)

    label_profile_icon = tk.Label(root, image=profile_icon, bg='#AED6E8')
    label_profile_icon.image = profile_icon
    label_profile_icon.place(x=1230, y=10, anchor='ne')
    label_profile_icon.bind("<Button-1>", open_profile_menu)

    # Create the profile menu
    profile_menu = tk.Menu(root, tearoff=0)
    profile_menu.add_command(label="Edit Profile", command=open_edit_profile_window)
    profile_menu.add_command(label="Logout", command=lambda: logout(root))

    def logout(window):
        window.destroy()
        firstMenu()

    name = get_name(username)  # Pass username instead of studentID

    # Profile Icon and UserName
    label_username = tk.Label(root, text=name, font=("Arial", 12, 'bold'), bg='#AED6E8')
    label_username.place(x=1150, y=30, anchor='ne')

    # Separator for Top section
    separator_top = tk.Frame(root, bg='black', height=2, width=1280)
    separator_top.place(x=0, y=80, anchor='nw')

    # Subject Label
    label_subject = tk.Label(root, text="Subject: ", font=("Arial", 14, "bold"), bg='#AED6E8')
    label_subject.place(x=20, y=100, anchor='nw')

    # Subject Combobox
    subjects = [" ", "Math", "Science", "English", "History", "Geography"]
    subject_combobox = ttk.Combobox(root, values=subjects, state="readonly")
    subject_combobox.set(subjects[0])
    subject_combobox.bind("<<ComboboxSelected>>", lambda event: change_subject(event, subject_combobox))
    subject_combobox.place(x=100, y=105, anchor='nw')

    # Year Level
    label_year = tk.Label(root, text="Year:", font=("Arial", 14, "bold"), bg='#AED6E8')
    label_year.place(x=300, y=100, anchor='nw')

    # Year Combobox
    years = [" ", "1", "2", "3", "4"]
    year_combobox = ttk.Combobox(root, values=years, state="readonly")
    year_combobox.set(years[0])
    year_combobox.bind("<<ComboboxSelected>>", lambda event: selected_year_level.set(year_combobox.get()))
    year_combobox.place(x=360, y=105, anchor='nw')

    # Term Label
    label_term = tk.Label(root, text="Term:", font=("Arial", 14, "bold"), bg='#AED6E8')
    label_term.place(x=560, y=100, anchor="nw")

    # Term Combobox
    terms = [" ", "prelim", "midterm", "finals"]
    term_combobox = ttk.Combobox(root, values=terms, state="readonly")
    term_combobox.set(terms[0])
    term_combobox.bind("<<ComboboxSelected>>", lambda event: selected_term.set(term_combobox.get()))
    term_combobox.place(x=625, y=105, anchor="nw")

    # Semester Label
    label_semester = tk.Label(root, text="Semester:", font=("Arial", 14, "bold"), bg='#AED6E8')
    label_semester.place(x=830, y=100, anchor="nw")

    # Semester Combobox
    semester = [" ", "1", "2"]
    semester_combobox = ttk.Combobox(root, values=semester, state="readonly")
    semester_combobox.set(semester[0])
    semester_combobox.bind("<<ComboboxSelected>>", lambda event: selected_semester.set(semester_combobox.get()))
    semester_combobox.place(x=935, y=105, anchor="nw")

    # Separator for Middle section
    separator_middle = tk.Frame(root, bg='black', height=2, width=1280)
    separator_middle.place(x=0, y=150, anchor='nw')

    # Navigation
    label_navigation = tk.Label(root, text="NAVIGATION", font=("Arial", 18, "bold"), bg='#AED6E8')
    label_navigation.place(x=10, y=185, anchor='nw')

    # Separator for Bottom section
    separator_bottom = tk.Frame(root, bg='black', height=2, width=1280)
    separator_bottom.place(x=0, y=250, anchor='nw')

    # Classes as Buttons
    for i in range(1, 5):
        class_button = tk.Button(root, text=f"CLASS {i}", font=("Arial", 14, "bold"), bg='#AED6E8', command=lambda num=i: select_class(num), width=14, relief="flat")
        class_button.place(x=0, y=280 + (i-1)*55, anchor='nw')
        class_buttons.append(class_button)

    # Separator between Navigation and Buttons
    separator_nav_buttons = tk.Frame(root, bg='black', height=1280, width=2)
    separator_nav_buttons.place(x=180, y=150, anchor='nw')

    # Input Grades Button
    button_input_grades = tk.Button(root, text="INPUT GRADES", font=("Arial", 16, "bold"), bg='#AED6E8', relief="flat", command=lambda: browseFile(root, result_label))
    button_input_grades.place(x=250, y=185, anchor='nw')

    # Hidden table to display grades
    table_frame = tk.Frame(root, bg="#FFFFFF", width=800, height=300)
    table_frame.grid_propagate(False)  # Disable auto resizing of frame

    # Create a Treeview widget
    table = ttk.Treeview(table_frame, columns=("Student Name", "Section", "Subject Code", "Subject Name", "Grades"), show="headings", height=10)
    table.heading("Student Name", text="Student Name")
    table.heading("Subject Code", text="Subject Code")
    table.heading("Subject Name", text="Subject Name")
    table.heading("Grades", text="Grades")
    table.pack(pady=20)

    root.protocol("WM_DELETE_WINDOW", exit_application)
    
    result_label = tk.Label(root, text="")
    result_label.pack(pady=10)
    root.mainloop()

firstMenu()
