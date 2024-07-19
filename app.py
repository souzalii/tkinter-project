import tkinter as tk
from tkinter import ttk
import pandas as pd
import psycopg2
from psycopg2 import sql
from datetime import datetime

class MyApp(tk.Frame):
    def __init__(self, root):
        self.current_page_index = 4
        self.pages = [self.page1, self.page2, self.page3, self.page4, self.page5]

        self.colourTitle = '#666666'
        self.colourGreen1 = '#00A685'
        self.colourGreen2 = '#009977'
        self.colourBackGrey = '#eeeeee'
        self.colourBackWhite = '#fff'

        super().__init__(root, bg=self.colourBackWhite)
        self.main_frame = self
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(0, weight=0)
        self.main_frame.rowconfigure(1, weight=0)
        self.main_frame.rowconfigure(2, weight=0)
        self.main_frame.rowconfigure(3, weight=1)

        self.button_dict = {}
        self.load_main_widgets()
        self.update_button_state()

        self.db_connection = psycopg2.connect(
            host="localhost",
            database="postgres",
            user="postgres",
            password="UWA2024"
        )
        self.db_cursor = self.db_connection.cursor()

    def create_button(self, text, column, row, command_arg, local=None):
        if local is None:
            local = self.pager
        button = tk.Button(
            local,
            background=self.colourGreen1,
            foreground=self.colourBackWhite,
            activebackground=self.colourGreen2,
            activeforeground=self.colourBackWhite,
            disabledforeground='#52bfa9',
            highlightthickness=0,
            relief=tk.FLAT,
            font=('Ariel', 12),
            text=text,
            command=lambda: self.change_page(command_arg)
        )
        button.grid(column=column, row=row, padx=5, pady=10)
        
        return button

    def clear_frame(self, frame):
        for child in frame.winfo_children():
            child.destroy()

    def clear_entries(self):
        for child in self.page_content.winfo_children():
            if isinstance(child, tk.Entry):
                child.delete(0, tk.END)

    def show_message(self, message, success=True):
        color = self.colourGreen1 if success else 'red'
        if hasattr(self, 'message_label'):
            self.message_label.destroy()
        self.message_label = tk.Label(self.page_content, text=message, background=self.colourBackWhite, foreground=color, font=('Ariel', 12))
        self.message_label.grid(row=5, column=0, columnspan=4, pady=10)

    def change_page(self, button):
        page_map = {
            'Project-Info': 0,
            'Researcher-Info': 1,
            'Researcher-Contributer': 2,
            'Researcher-User': 3,
            'Search': 4
        }
        self.current_page_index = page_map[button]
        self.clear_frame(self.page_content)
        self.pages[self.current_page_index]()
        self.update_button_state()

    def update_button_state(self):
        for index, button in self.button_dict.items():
            if index == self.current_page_index:
                button.config(state=tk.DISABLED)
            else:
                button.config(state=tk.ACTIVE)

    def load_main_widgets(self):
        self.create_header()
        self.create_page_title()
        self.create_page_content()
        self.pages[self.current_page_index]()

    def create_header(self):
        self.pager = tk.Frame(self.main_frame, background=self.colourBackGrey)
        self.pager.grid(column=0, row=0, sticky=tk.NSEW)

        self.app_title = tk.Label(self.pager, background=self.colourBackGrey, foreground=self.colourGreen2, font=('Ariel', 18), text='Nesp Projects')
        self.app_title.grid(column=0, row=0, sticky=tk.NSEW, padx=30, pady=10)

        self.bt_project = self.create_button('Project Information', 2, 0, 'Project-Info')
        self.bt_researcher = self.create_button('Project Researchers', 3, 0, 'Researcher-Info')
        self.bt_cocontributer = self.create_button('Project Co-Contributer', 4, 0, 'Researcher-Contributer')
        self.bt_users = self.create_button('Project User', 5, 0, 'Researcher-User')
        self.bt_search = self.create_button('Search', 0, 1, 'Search')

        self.button_dict = {
            0: self.bt_project,
            1: self.bt_researcher,
            2: self.bt_cocontributer,
            3: self.bt_users,
            4: self.bt_search
        }

        self.bt_project.config(state=tk.DISABLED)

    def create_page_title(self):
        self.page_container = tk.Frame(self.main_frame, background=self.colourGreen1, height=2)
        self.page_container.columnconfigure(0, weight=1)
        self.page_container.rowconfigure(0, weight=0)
        self.page_container.grid(column=0, row=1, sticky=tk.NSEW)
        self.title = tk.Label(self.page_container, foreground=self.colourBackWhite, background=self.colourGreen1, height=2, font=('Ariel', 18))
        self.title.grid(column=0, row=0)

    def create_page_content(self):
        self.page_content = tk.Frame(self.main_frame, background=self.colourBackWhite)
        self.page_content.columnconfigure(0, weight=0)
        self.page_content.rowconfigure(0, weight=0)
        self.page_content.grid(column=0, row=2, sticky=tk.NSEW, padx=20, pady=30)

    def create_label_entry(self, text, column, row):
        label = tk.Label(self.page_content, text=text, background=self.colourBackWhite, font=('Ariel', 12))
        label.grid(row=row, column=column, sticky=tk.W, padx=5, pady=5)
        entry = tk.Entry(self.page_content, font=('Ariel', 12))
        entry.grid(row=row, column=column + 1, padx=5, pady=5, sticky=tk.W)
        return entry

    def create_dropdown(self, text, options, column, row):
        label = tk.Label(self.page_content, text=text, background=self.colourBackWhite, font=('Ariel', 12))
        label.grid(row=row, column=column, sticky=tk.W, padx=5, pady=5)
        dropdown = ttk.Combobox(self.page_content, values=options, state='readonly')
        dropdown.grid(row=row, column=column + 1, padx=5, pady=5,sticky=tk.W) 
        dropdown.current(0)  # Set the default selection
        return dropdown

    def validate_entries(self, entries):
        for entry in entries:
            if not entry.get().strip():
                return False
        return True

    def validate_date_format(self, date_text):
        try:
            datetime.strptime(date_text, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    def check_project_id_exists(self, project_id):
        try:
            self.db_cursor.execute("SELECT 1 FROM projects WHERE project_id = %s", (project_id,))
            result = self.db_cursor.fetchone()
            return result is not None
        except Exception as e:
            print(f"Error checking project ID: {e}")  # Log para erros
            return False

    def submit_project_info(self):
        entries = [
            self.entry_project_id,
            self.entry_project_title,
            self.entry_start_date,
            self.entry_end_date,
            self.entry_project_leader,
            self.entry_organisation
        ]

        if not self.validate_entries(entries):
            self.show_message("Please fill in all fields.", success=False)
            return

        project_id = self.entry_project_id.get()
        project_title = self.entry_project_title.get()
        start_date = self.entry_start_date.get()
        end_date = self.entry_end_date.get()
        project_leader = self.entry_project_leader.get()
        organisation = self.entry_organisation.get()

        if not self.validate_date_format(start_date) or not self.validate_date_format(end_date):
            self.show_message("Invalid date format. Use YYYY-MM-DD.", success=False)
            return

        if self.check_project_id_exists(project_id):
            self.show_message("Project ID already exists.", success=False)
            return

        insert_query = """
        INSERT INTO projects (project_id, project_title, project_start_date, project_end_date, project_leader, organisation)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        try:
            self.db_cursor.execute(insert_query, (project_id, project_title, start_date, end_date, project_leader, organisation))
            self.db_connection.commit()
            self.clear_entries()
            self.show_message("Project information submitted successfully!")
        except Exception as e:
            self.show_message(f"Error: {e}", success=False)

    def page1(self):
        self.title.config(text='Project Information')
        self.entry_project_id = self.create_label_entry('Project ID: ', 0, 0)
        self.entry_project_title = self.create_label_entry('Project Title: ', 2, 0)
        self.entry_start_date = self.create_label_entry('Start Date: ', 0, 1)
        self.entry_end_date = self.create_label_entry('End Date: ', 2, 1)
        self.entry_project_leader = self.create_label_entry('Project Leader: ', 0, 2)
        self.entry_organisation = self.create_label_entry('Organisation: ', 2, 2)
        self.bt_submit = tk.Button(
            self.page_content,
            background=self.colourGreen1,
            foreground=self.colourBackWhite,
            activebackground=self.colourGreen2,
            activeforeground=self.colourBackWhite,
            font=('Ariel', 12),
            text='Submit',
            command=self.submit_project_info
        )
        self.bt_submit.grid(column=3, row=3, padx=5, pady=10)

    def page2(self):
        self.title.config(text='Project Researchers')
        self.entry_project_id = self.create_label_entry('Project ID: ', 0, 0)
        self.entry_name = self.create_label_entry('Name: ', 2, 0)
        self.entry_organisation = self.create_label_entry('Organisation: ', 0, 1)
        self.entry_project_role = self.create_label_entry('Project Role: ', 2, 1)
        self.bt_submit = tk.Button(
            self.page_content,
            background=self.colourGreen1,
            foreground=self.colourBackWhite,
            activebackground=self.colourGreen2,
            activeforeground=self.colourBackWhite,
            font=('Ariel', 12),
            text='Submit',
            command=self.submit_researcher_info
        )
        self.bt_submit.grid(column=3, row=3, padx=5, pady=10)

    def submit_researcher_info(self):
        entries = [
            self.entry_project_id,
            self.entry_name,
            self.entry_organisation,
            self.entry_project_role
        ]

        if not self.validate_entries(entries):
            self.show_message("Please fill in all fields.", success=False)
            return

        project_id = self.entry_project_id.get()
        name = self.entry_name.get()
        organisation = self.entry_organisation.get()
        project_role = self.entry_project_role.get()

        if not self.check_project_id_exists(project_id):
            self.show_message("Project ID does not exist.", success=False)
            return
            
        insert_query = """
        INSERT INTO researchers (project_id, name, organisation, project_role)
        VALUES (%s, %s, %s, %s)
        """
        try:
            self.db_cursor.execute(insert_query, (project_id, name, organisation, project_role))
            self.db_connection.commit()
            self.clear_entries()
            self.show_message("Researcher information submitted successfully!")
        except Exception as e:
            self.show_message(f"Error: {e}", success=False)

    def page3(self):
        self.title.config(text='Project Co-Contributer')
        self.entry_project_id = self.create_label_entry('Project ID: ', 0, 0)
        self.entry_name = self.create_label_entry('Name: ', 2, 0)
        self.entry_organisation = self.create_label_entry('Organisation: ', 0, 1)
        self.entry_contribution = self.create_label_entry('Contribution: ', 2, 1)
        self.entry_project_role = self.create_label_entry('Project Role: ', 0, 2)
        self.bt_submit = tk.Button(
            self.page_content,
            background=self.colourGreen1,
            foreground=self.colourBackWhite,
            activebackground=self.colourGreen2,
            activeforeground=self.colourBackWhite,
            font=('Ariel', 12),
            text='Submit',
            command=self.submit_co_contributor_info
        )
        self.bt_submit.grid(column=3, row=3, padx=5, pady=10)

    def submit_co_contributor_info(self):
        entries = [
            self.entry_project_id,
            self.entry_name,
            self.entry_organisation,
            self.entry_contribution,
            self.entry_project_role
        ]

        if not self.validate_entries(entries):
            self.show_message("Please fill in all fields.", success=False)
            return

        project_id = self.entry_project_id.get().strip()
        name = self.entry_name.get().strip()
        organisation = self.entry_organisation.get().strip()
        contribution = self.entry_contribution.get().strip()
        project_role = self.entry_project_role.get().strip()

        if not self.check_project_id_exists(project_id):
            self.show_message("Project ID does not exist.", success=False)
            return

        insert_query = """
        INSERT INTO co_contributors (project_id, name, organisation, contribution, project_role)
        VALUES (%s, %s, %s, %s, %s)
        """
        try:
            self.db_cursor.execute(insert_query, (project_id, name, organisation, contribution, project_role))
            self.db_connection.commit()
            self.clear_entries()
            self.show_message("Co-contributor information submitted successfully!")
        except Exception as e:
            self.show_message(f"Error: {e}", success=False)

    def page4(self):
        self.title.config(text='Project User')
        self.entry_project_id = self.create_label_entry('Project ID: ', 0, 0)
        self.entry_type = self.create_label_entry('Type: ', 2, 0)
        self.entry_organisation = self.create_label_entry('Organisation: ', 0, 1)
        self.entry_name = self.create_label_entry('Name: ', 2, 1)
        self.entry_email = self.create_label_entry('Email: ', 0, 2)
        self.bt_submit = tk.Button(
            self.page_content,
            background=self.colourGreen1,
            foreground=self.colourBackWhite,
            activebackground=self.colourGreen2,
            activeforeground=self.colourBackWhite,
            font=('Ariel', 12),
            text='Submit',
            command=self.submit_research_user_info
        )
        self.bt_submit.grid(column=3, row=3, padx=5, pady=10)

    def submit_research_user_info(self):
        entries = [
            self.entry_project_id,
            self.entry_type,
            self.entry_organisation,
            self.entry_name,
            self.entry_email
        ]

        if not self.validate_entries(entries):
            self.show_message("Please fill in all fields.", success=False)
            return

        project_id = self.entry_project_id.get()
        type_ = self.entry_type.get()
        organisation = self.entry_organisation.get()
        name = self.entry_name.get()
        email = self.entry_email.get()
        
        if not self.check_project_id_exists(project_id):
            self.show_message("Project ID does not exist.", success=False)
            return

        insert_query = """
        INSERT INTO research_users (project_id, type, organisation, name, email)
        VALUES (%s, %s, %s, %s, %s)
        """
        try:
            self.db_cursor.execute(insert_query, (project_id, type_, organisation, name, email))
            self.db_connection.commit()
            self.clear_entries()
            self.show_message("Research user information submitted successfully!")
        except Exception as e:
            self.show_message(f"Error: {e}", success=False)

    def page5(self):
        self.title.config(text='Search')

        self.entry_project_id = self.create_label_entry('Project ID: ', 0, 0)
        self.dropdown_table = self.create_dropdown('Select table',['projects', 'researchers', 'co_contributors', 'research_users'], 0, 1)

        self.bt_search = tk.Button(
            self.page_content,
            background=self.colourGreen1,
            foreground=self.colourBackWhite,
            activebackground=self.colourGreen2,
            activeforeground=self.colourBackWhite,
            font=('Ariel', 12),
            text='Search',
            command=self.search_data
        )
        self.bt_search.grid(column=0, row=2, padx=5, pady=10)
        
        self.export_button = tk.Button(self.page_content, text='Export to Excel', state=tk.DISABLED, command=self.export_to_excel)
        self.export_button.grid(row=2, column=1, pady=10)

        self.output_text = tk.Text(self.page_content, height=10, width=100)
        self.output_text.grid(row=3, column=0, columnspan=3, padx=5, pady=10)

    def search_data(self):
        project_id = self.entry_project_id.get().strip()
        selected_table = self.dropdown_table.get()

        if not project_id or not selected_table:
            self.show_message("Please fill in all fields.", success=False)
            return

        if not self.check_project_id_exists(project_id):
            self.show_message("Project ID does not exist.", success=False)
            return

        query = sql.SQL("SELECT * FROM {} WHERE project_id = %s").format(sql.Identifier(selected_table))
        try:
            self.db_cursor.execute(query, (project_id,))
            rows = self.db_cursor.fetchall()

            if not rows:
                self.output_text.delete(1.0, tk.END)
                self.show_message("No results found.", success=False)
                self.export_button.config(state=tk.DISABLED)
                return

            columns = [desc[0] for desc in self.db_cursor.description]
            df = pd.DataFrame(rows, columns=columns)

            # Clear previous output
            self.output_text.delete(1.0, tk.END)

            # Display output on the screen
            self.output_text.insert(tk.END, df.to_string(index=False))

            self.export_button.config(state=tk.NORMAL)

        except Exception as e:
            self.show_message(f"Error: {e}", success=False)




    def export_to_excel(self):
        project_id = self.entry_project_id.get().strip()
        selected_table = self.dropdown_table.get()

        query = sql.SQL("SELECT * FROM {} WHERE project_id = %s").format(sql.Identifier(selected_table))

        try:
            self.db_cursor.execute(query, (project_id,))
            rows = self.db_cursor.fetchall()

            columns = [desc[0] for desc in self.db_cursor.description]
            df = pd.DataFrame(rows, columns=columns)

            file_name = f"{project_id}_{selected_table}.xlsx"
            df.to_excel(file_name, index=False)
            self.show_message(f"Data exported to {file_name} successfully!")


        except Exception as e:
            self.show_message(f"Error: {e}", success=False)


if __name__ == "__main__":
    root = tk.Tk()
    #root.geometry("800x600")
    app = MyApp(root)
    app.mainloop()

