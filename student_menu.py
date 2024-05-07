import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from PIL import Image, ImageTk
from first_menu import firstMenu
from profile_window import edit_profile_window

def studentMenu(username):
    def exit_application():
        root.destroy()

    def open_edit_profile_window():
        root.lift()  # Lift the main window to the top
        edit_profile_window(root)

    def open_profile_menu(event):
        profile_menu.post(label_profile_icon.winfo_rootx(), label_profile_icon.winfo_rooty() + label_profile_icon.winfo_height())

    def logout(window):
        window.destroy()
        firstMenu()

    def displayStudentGrades():
    # Get the selected semester and term
        selected_semester = semester_combobox.get()
        selected_term = term_combobox.get()

        if selected_semester and selected_term:
            # Connect to grades database
            conn = sqlite3.connect('database/records.db')
            cursor = conn.cursor()

            # Retrieve grades for the selected semester, term, and studentID
            cursor.execute("SELECT subjectCode, subjectName, grades FROM grades_table WHERE studentID=? AND semester=? AND term=?", (username, selected_semester, selected_term))
            student_grades = cursor.fetchall()

            conn.close()

            if student_grades:
            # Display student's grades
                print(f"\n{selected_semester} - {selected_term.capitalize()} grades:")
                for subject_code, subject_name, grades in student_grades:
                    print(f"{subject_code} | {subject_name} | {grades}")

                # Update the table with student grades
                update_table(student_grades)

                # Show the table
                table_frame.place(relx=0.5, rely=0.5, anchor="center")
            else:
                print("No grades found for this semester and term.")

        else:
            print("Please select both semester and term.")


    def update_table(student_grades):
        # Clear previous data
        for row in table.get_children():
            table.delete(row)

        # Add new data to the table
        for subject_code, subject_name, grades in student_grades:
            table.insert("", "end", values=(subject_code, subject_name, grades))

    root = tk.Tk()
    root.title("GradeBook Groove")
    root.geometry('1280x720')
    root.configure(bg='#AED6E8')

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

    # Get name from the database
    def get_name(username):
        conn = sqlite3.connect('database/users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM users WHERE username=?", (username,))
        row = cursor.fetchone()  # Fetch the row once
        name = row[0] if row else ""  # Use row to get name if it exists, else set to ""
        conn.close()
        return name

    # Profile Icon and UserName
    name = get_name(username)
    label_username = tk.Label(root, text=name, font=("Arial", 12, 'bold'), bg='#AED6E8')
    label_username.place(x=1150, y=30, anchor='ne')

    # Separator for Top section
    separator_top = tk.Frame(root, bg='black', height=2, width=1280)
    separator_top.place(x=0, y=80, anchor='nw')

    # Term Label
    label_term = tk.Label(root, text="Term:", font=("Arial", 14, "bold"), bg='#AED6E8')
    label_term.place(x=20, y=100, anchor='nw')

    # Term Combobox
    terms = [" ", "prelim", "midterm", "finals"]
    term_combobox = ttk.Combobox(root, values=terms, state="readonly")
    term_combobox.set(terms[0])
    term_combobox.bind("<<ComboboxSelected>>")
    term_combobox.place(x=90, y=105, anchor='nw')

    # Semester Label
    label_semester = tk.Label(root, text="Semester:", font=("Arial", 14, "bold"), bg='#AED6E8')
    label_semester.place(x=250, y=100, anchor='nw')

    # Semester Combobox
    semester = [" ", "1", "2"]
    semester_combobox = ttk.Combobox(root, values=semester, state="readonly")
    semester_combobox.set(semester[0])
    semester_combobox.bind("<<ComboboxSelected>>")
    semester_combobox.place(x=360, y=105, anchor='nw')

    # View Grades Button
    button_input_grades = tk.Button(root, text="VIEW GRADES", font=("Arial", 14, "bold"), bg='#AED6E8', relief="flat", command=displayStudentGrades)
    button_input_grades.place(x=560, y=98, anchor="nw")

    # Separator for Middle section
    separator_middle = tk.Frame(root, bg='black', height=2, width=1280)
    separator_middle.place(x=0, y=150, anchor='nw')

    # Hidden table to display grades
    table_frame = tk.Frame(root, bg="#FFFFFF", width=800, height=300)
    table_frame.grid_propagate(False)  # Disable auto resizing of frame

    # Create a Treeview widget
    table = ttk.Treeview(table_frame, columns=("Subject Code", "Subject Name", "Grades"), show="headings", height=10)
    table.heading("Subject Code", text="Subject Code")
    table.heading("Subject Name", text="Subject Name")
    table.heading("Grades", text="Grades")
    table.pack(pady=20)

    root.mainloop()

