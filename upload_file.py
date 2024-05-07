import sqlite3
import pandas as pd
from tkinter import filedialog

def browseFile(root, result_label):
    # Search for only excel files
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xls")])
    if file_path:
        uploadFile(file_path, root, result_label)

def uploadFile(file_path, root, result_label):
    try:
        # Load data from file
        df = pd.read_excel(file_path)

        # Clean data
        df.columns = df.columns.str.strip()

        # Connect to database
        connection = sqlite3.connect('database/records.db')

        # Check for duplicates then update existing entries
        for index, row in df.iterrows():  # Skip the first row (header)
            student_id = row.get('studentID', '')
            subject_code = row.get('subjectCode', '')
            term = row.get('term', '')
            grades = row.get('grades', '')
            sem = row.get('semester', '')

            # Check if subjectName and section are available
            subject_name = row.get('subjectName')
            section = row.get('section')

            # Ensure that subjectName and section are not null
            if subject_name is None or section is None:
                raise ValueError("Subject name or section is missing for student: {}".format(student_id))

            # Only insert if required columns are present
            if student_id and subject_code and term and grades and sem:
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM grades_table WHERE studentID=? AND subjectCode=? AND term=? AND semester=?", (student_id, subject_code, term, sem))
                existing_data = cursor.fetchone()

                if existing_data:
                    cursor.execute("UPDATE grades_table SET grades=? WHERE studentID=? AND subjectCode=? AND term=? AND semester=?", (grades, student_id, subject_code, term, sem))
                else:
                    # Append new data to the existing table
                    cursor.execute("INSERT INTO grades_table (studentID, subjectCode, term, grades, subjectName, section, semester) VALUES (?, ?, ?, ?, ?, ?, ?)", (student_id, subject_code, term, grades, subject_name, section, sem))

        # Confirm changes and close connection
        connection.commit()
        result_label.config(text="Excel file processed successfully and data stored in database.")
        root.destroy()
        connection.close()
    except Exception as e:
        result_label.config(text="Error processing Excel file: " + str(e))
        # Check the error in console
        print("Error:", e)
        print("DataFrame:")
        print(df.head()) 





