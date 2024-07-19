import tkinter
from tkinter import ttk
from tkinter import messagebox 
import psycopg2
import pandas as pd
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
import customtkinter as ctk

# Connect to PostgreSQL
connection = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="USER",
    password="PASSWORD"
)

def insert_into_inventory():
    try:
        # Establish a connection and create a cursor
        cursor = connection.cursor()

        # Get data from the form
        project_id = project_id_entry.get()
        project_title = project_title_entry.get()
        project_start = project_start_entry.get()
        project_end = project_end_entry.get()
        title_user = title_combobox.get()
        first_name = first_name_entry.get()
        last_name = last_name_entry.get()
        project_role_value = project_role.get("1.0", "end").strip()  # Get and strip whitespace
        org_name = org_name_entry.get()
        user_type = user_type_var.get()

        # Validate the data (you can add more validation logic here as needed)
        if not (first_name and last_name and project_id and project_title):
            messagebox.showwarning(title="Warning", message="Please complete all required fields.")
            return

        # Convert dates to proper format if needed
        # Assuming project_start and project_end are in 'YYYY-MM-DD' format already

        # Insert data into the inventory table
        insert_query = """
            INSERT INTO inventory (project_id, project_title, project_start_date, project_end_date, user_title, first_name, last_name, project_role, org_name, user_type)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        # Execute the SQL query with parameters
        cursor.execute(insert_query, (project_id, project_title, project_start, project_end, title_user, first_name, last_name, project_role_value, org_name, user_type))
        
        # Commit the transaction to make the change persistent
        connection.commit()

        # Close cursor
        cursor.close()

        # Display success message to the user
        messagebox.showinfo(title="Completed!", message="Information saved successfully.")

    except (Exception, psycopg2.Error) as error:
        # Display error message if there's an issue with the database insertion
        messagebox.showerror(title="Error", message=f"Error inserting data into PostgreSQL: {error}")

def search_inventory():
    try:
        # Establish a connection and create a cursor
        cursor = connection.cursor()

        # Clear any previous search results in the listbox
        search_results.delete(0, tkinter.END)

        # Get the project_id to search for
        search_project_id = search_entry.get()

        # Search query
        search_query = """
            SELECT * FROM inventory
            WHERE project_id = %s
        """
        cursor.execute(search_query, (search_project_id,))
        rows = cursor.fetchall()

        # Display search results in the listbox
        for row in rows:
            search_results.insert(tkinter.END, row)

        # Close cursor
        cursor.close()

    except (Exception, psycopg2.Error) as error:
        # Display error message if there's an issue with the database search
        messagebox.showerror(title="Error", message=f"Error searching data in PostgreSQL: {error}")

def save_to_excel():
    try:
        # Get the project_id to search for
        search_project_id = search_entry.get()

        # Establish a connection and create a cursor
        cursor = connection.cursor()

        # Search query
        search_query = """
            SELECT * FROM inventory
            WHERE project_id = %s
        """
        cursor.execute(search_query, (search_project_id,))
        rows = cursor.fetchall()

        # Create a pandas DataFrame from the SQL results
        df = pd.DataFrame(rows, columns=["project_id", "project_title", "project_start_date", "project_end_date", 
                                         "user_title", "first_name", "last_name", "project_role", "org_name", "user_type"])

        # Export to Excel
        excel_filename = f"search_results_{search_project_id}.xlsx"
        df.to_excel(excel_filename, index=False)

        # Close cursor
        cursor.close()

        messagebox.showinfo(title="Exported to Excel", message=f"Search results exported to {excel_filename}")

    except (Exception, psycopg2.Error) as error:
        # Display error message if there's an issue with the database search or exporting to Excel
        messagebox.showerror(title="Error", message=f"Error exporting data to Excel: {error}")

def enter_data():
    # Validate and insert data into the inventory table
    insert_into_inventory()

# Start application window
window = tkinter.Tk()
window.title("Data Entry Form")

frame = tkinter.Frame(window)
frame.pack()

# Project information frame
project_frame = tkinter.LabelFrame(frame, text=" Project Information ")
project_frame.grid(row=0, column=0, sticky="news", padx=20, pady=20)

project_id_label = tkinter.Label(project_frame, text='Project ID: ')
project_id_label.grid(row=0, column=0)
project_id_entry = tkinter.Entry(project_frame)
project_id_entry.grid(row=0, column=1)

project_title_label = tkinter.Label(project_frame, text='Project Title: ')
project_title_label.grid(row=1, column=0)
project_title_entry = tkinter.Entry(project_frame)
project_title_entry.grid(row=1, column=1)

project_start_label = tkinter.Label(project_frame, text='Start Date: ')
project_start_label.grid(row=2, column=0)
project_start_entry = tkinter.Entry(project_frame)
project_start_entry.grid(row=2, column=1)

project_end_label = tkinter.Label(project_frame, text='End Date:')
project_end_label.grid(row=3, column=0)
project_end_entry = tkinter.Entry(project_frame)
project_end_entry.grid(row=3, column=1)

# User information frame
user_info_frame = tkinter.LabelFrame(frame, text=" User Information ")
user_info_frame.grid(row=1, column=0, sticky="news", padx=20, pady=20)

first_name_label = tkinter.Label(user_info_frame, text='First Name')
first_name_label.grid(row=0, column=0)
first_name_entry = tkinter.Entry(user_info_frame)
first_name_entry.grid(row=0, column=1)

last_name_label = tkinter.Label(user_info_frame, text='Last Name')
last_name_label.grid(row=0, column=2)
last_name_entry = tkinter.Entry(user_info_frame)
last_name_entry.grid(row=0, column=3)

title_label = tkinter.Label(user_info_frame, text="Title")
title_label.grid(row=1, column=0)
title_combobox = ttk.Combobox(user_info_frame, values=["", "Mr.", "Ms.", "Dr."])
title_combobox.grid(row=1, column=1)

project_role_label = tkinter.Label(user_info_frame, text="Project Role")
project_role_label.grid(row=2, column=0)
project_role = tkinter.Text(user_info_frame, width=15, height=4, font=("Arial", 12))
project_role.grid(row=2, column=1, columnspan=3)

# Organisation information frame
org_info_frame = tkinter.LabelFrame(frame, text=" Organisation ")
org_info_frame.grid(row=2, column=0, sticky="news", padx=20, pady=20)

org_name_label = tkinter.Label(org_info_frame, text='Organisation Name')
org_name_label.grid(row=0, column=0)
org_name_entry = tkinter.Entry(org_info_frame)
org_name_entry.grid(row=0, column=1)

user_type_label = tkinter.Label(org_info_frame, text='User Type: ')
user_type_label.grid(row=1, column=0)

user_type_var = tkinter.StringVar(value="Not registered")
user_type_check = tkinter.Checkbutton(org_info_frame, text="Primary user", variable=user_type_var, onvalue="Primary", offvalue="Not primary")
user_type_check2 = tkinter.Checkbutton(org_info_frame, text="Secondary user", variable=user_type_var, onvalue="Secondary", offvalue="Not secondary")
user_type_check3 = tkinter.Checkbutton(org_info_frame, text="Other user", variable=user_type_var, onvalue="Other", offvalue="Not other")
user_type_check.grid(row=1, column=1)
user_type_check2.grid(row=2, column=1)
user_type_check3.grid(row=3, column=1)

# Search frame
search_frame = tkinter.LabelFrame(frame, text=" Search by Project ID ")
search_frame.grid(row=3, column=0, sticky="news", padx=20, pady=20)

search_label = tkinter.Label(search_frame, text="Enter Project ID:")
search_label.grid(row=0, column=0, padx=10, pady=10)

search_entry = tkinter.Entry(search_frame)
search_entry.grid(row=0, column=1, padx=10, pady=10)

search_button = tkinter.Button(search_frame, text="Search", command=search_inventory)
search_button.grid(row=0, column=2, padx=10, pady=10)

# Export to Excel button
export_excel_button = tkinter.Button(search_frame, text="Export to Excel", command=save_to_excel)
export_excel_button.grid(row=0, column=3, padx=10, pady=10)

# Results listbox
search_results = tkinter.Listbox(frame, width=80, height=10)
search_results.grid(row=4, column=0, padx=20, pady=20, sticky="news")

# Configure grid layout
for widget in frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

# Start GUI main loop
window.mainloop()
