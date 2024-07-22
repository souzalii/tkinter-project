import tkinter as tk
from tkinter import ttk, filedialog
import pandas as pd
import psycopg2
from psycopg2 import sql
from datetime import datetime

class MyApp(tk.Frame):
    def __init__(self, root):
        super().__init__(root, bg='#fff')
        
        self.current_page_index = 4 # Index of the current page
        self.pages = [self.page1, self.page2, self.page3, self.page4, self.page5]

        #Color settings for the UI
        self.colourTitle = '#666666'
        self.colourGreen1 = '#00A685'
        self.colourGreen2 = '#009977'
        self.colourBackGrey = '#eeeeee'
        self.colourBackWhite = '#fff'

        # Main frame configuration
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

        # Database connection setup
        self.db_connection = psycopg2.connect(
            host="localhost",
            database="postgres",
            user="postgres",
            password="UWA2024"
        )
        self.db_cursor = self.db_connection.cursor()

    #function to create buttons
    def create_button(self, text, column, row, command, local=None):
        if local is None:
            local = self.pager
        elif local == "page_content":
            local = self.page_content
        
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
            command=command
        )
        button.grid(column=column, row=row, padx=5, pady=10)
        
        return button

    #Clear all widgets in a frame
    def clear_frame(self, frame):
        for child in frame.winfo_children():
            child.destroy()

    #Clear all entry fields
    def clear_entries(self):
        for child in self.page_content.winfo_children():
            if isinstance(child, tk.Entry):
                child.delete(0, tk.END)

    #Messages display
    def show_message(self, message, success=True):
        color = self.colourGreen1 if success else 'red'
        if hasattr(self, 'message_label'):
            self.message_label.destroy()
        self.message_label = tk.Label(self.page_content, text=message, background=self.colourBackWhite, foreground=color, font=('Ariel', 12))
        self.message_label.grid(row=0, column=0, columnspan=4, pady=10)

    #Func to change pages
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
        self.canvas.yview_moveto(0) # Reset scroll position to the top

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

    #Create the header frame and navigation buttons
    def create_header(self):
        self.pager = tk.Frame(self.main_frame, background=self.colourBackGrey)
        self.pager.grid(column=0, row=0, sticky=tk.NSEW,columnspan=2)

        self.app_title = tk.Label(self.pager, background=self.colourBackGrey, foreground=self.colourGreen2, font=('Ariel', 18), text='Nesp Projects')
        self.app_title.grid(column=0, row=0, sticky=tk.NSEW, padx=30, pady=10)

        self.bt_project = self.create_button('Project Information', 2, 0, lambda: self.change_page('Project-Info'))
        self.bt_researcher = self.create_button('Project Researchers', 3, 0, lambda: self.change_page('Researcher-Info'))
        self.bt_cocontributer = self.create_button('Project Co-Contributer', 4, 0, lambda: self.change_page('Researcher-Contributer'))
        self.bt_users = self.create_button('Project User', 5, 0, lambda: self.change_page('Researcher-User'))
        self.bt_search = self.create_button('Search', 0, 1, lambda: self.change_page('Search'))

        self.button_dict = {
            0: self.bt_project,
            1: self.bt_researcher,
            2: self.bt_cocontributer,
            3: self.bt_users,
            4: self.bt_search
        }

        self.bt_project.config(state=tk.DISABLED)

    #Create struct and elements of the pages
    def create_page_title(self):
        self.page_container = tk.Frame(self.main_frame, background=self.colourGreen1, height=2)
        self.page_container.columnconfigure(0, weight=1)
        self.page_container.rowconfigure(0, weight=0)
        self.page_container.grid(column=0, row=1, sticky=tk.NSEW, columnspan=2)
        self.title = tk.Label(self.page_container, foreground=self.colourBackWhite, background=self.colourGreen1, height=2, font=('Ariel', 18))
        self.title.grid(column=0, row=0)

    def create_page_content(self):
        self.canvas = tk.Canvas(self.main_frame, background=self.colourBackWhite)
        self.scroll_y = tk.Scrollbar(self.main_frame, orient="vertical", command=self.canvas.yview)
        
        self.page_content = tk.Frame(self.canvas, background=self.colourBackWhite)
        self.page_content.bind("<Configure>", self.on_frame_configure)

        self.canvas.create_window((0, 0), window=self.page_content, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scroll_y.set)

        self.canvas.grid(row=2, column=0, sticky="nsew")
        self.scroll_y.grid(row=2, column=1, sticky="ns")

        self.main_frame.grid_rowconfigure(0, weight=0)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(2, weight=1)

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.canvas.update_idletasks()
        self.canvas.config(width=self.page_content.winfo_width())

    def create_label_entry(self, text, column, row):
        label = tk.Label(self.page_content, text=text, background=self.colourBackWhite, font=('Ariel', 12))
        label.grid(row=row, column=column, sticky=tk.W, padx=5, pady=5)
        entry = tk.Entry(self.page_content, font=('Ariel', 12))
        entry.grid(row=row, column=column + 1, padx=5, pady=5, sticky=tk.W)
        return entry

    def create_text(self, text, column, row, columnspan=None): 
        if columnspan is None:
            columnspan = 2
        label = tk.Label(self.page_content, text=text, background=self.colourBackWhite, font=('Ariel', 12))
        label.grid(row=row, column=column, padx=5, pady=5,columnspan=columnspan,sticky=tk.EW)

    def create_dropdown(self, text, options, column, row):
        label = tk.Label(self.page_content, text=text, background=self.colourBackWhite, font=('Ariel', 12))
        label.grid(row=row, column=column, sticky=tk.W, padx=5, pady=5)
        dropdown = ttk.Combobox(self.page_content, values=options, state='readonly')
        dropdown.grid(row=row, column=column + 1, padx=5, pady=5, sticky=tk.W)
        dropdown.current(0)  # Set the default selection
        return dropdown

    #Validate information 
    def validate_entries(self, entries):
        return all(entry.get().strip() for entry in entries)

    def validate_date_format(self, date_text):
        try:
            datetime.strptime(date_text, '%d/%m/%Y')
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

        project_id = self.entry_project_id.get().strip()
        project_title = self.entry_project_title.get().strip()
        start_date = self.entry_start_date.get().strip()
        end_date = self.entry_end_date.get().strip()
        project_leader = self.entry_project_leader.get().strip()
        organisation = self.entry_organisation.get().strip()

        if not self.validate_date_format(start_date) or not self.validate_date_format(end_date):
            self.show_message("Invalid date format. Use DD/MM/YYYY.", success=False)
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

    #Submit information
    def submit_researcher_info(self):
        entries = [
            self.entry_project_id,
            self.entry_name,
            self.entry_organisation
        ]

        if not self.validate_entries(entries):
            self.show_message("Please fill in all fields.", success=False)
            return

        project_id = self.entry_project_id.get().strip()
        name = self.entry_name.get().strip()
        organisation = self.entry_organisation.get().strip()
        project_role = self.entry_project_role.get().strip() or None

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

    def submit_co_contributor_info(self):
        entries = [
            self.entry_project_id,
            self.entry_name,
            self.entry_organisation
        ]

        if not self.validate_entries(entries):
            self.show_message("Please fill in all fields.", success=False)
            return

        project_id = self.entry_project_id.get().strip()
        name = self.entry_name.get().strip()
        organisation = self.entry_organisation.get().strip()
        contribution = self.entry_contribution.get().strip() or None

        if not self.check_project_id_exists(project_id):
            self.show_message("Project ID does not exist.", success=False)
            return

        insert_query = """
        INSERT INTO co_contributors (project_id, name, organisation, contribution)
        VALUES (%s, %s, %s, %s)
        """
        try:
            self.db_cursor.execute(insert_query, (project_id, name, organisation, contribution))
            self.db_connection.commit()
            self.clear_entries()
            self.show_message("Co-contributor information submitted successfully!")
        except Exception as e:
            self.show_message(f"Error: {e}", success=False)

    def submit_research_user_info(self):
        entries = [
            self.entry_project_id,
            self.entry_organisation
        ]

        if not self.validate_entries(entries):
            self.show_message("Please fill in all fields.", success=False)
            return

        project_id = self.entry_project_id.get().strip()
        type_ = self.entry_type.get().strip() or None
        organisation = self.entry_organisation.get().strip()
        name = self.entry_name.get().strip() or None
        email = self.entry_email.get().strip() or None

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


    def upload_excel(self, table_name):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xls")])
        if not file_path:
            return

        try:
            df = pd.read_excel(file_path)
        except Exception as e:
            self.show_message(f"Error reading file: {e}", success=False)
            return

        # Define and check number of columns
        column_counts = {
            'projects': 6,
            'researchers': 4,
            'co_contributors': 4,
            'research_users': 5
        }
        if len(df.columns) != column_counts.get(table_name, 0):
            self.show_message(f"Error: The file does not have the correct number of columns for {table_name}.", success=False)
            return

        for column in df.columns:
            df[column] = df[column].astype(str).str.strip()

        errors = []

        for index, row in df.iterrows():
            columns = ', '.join(row.index)
            values = ', '.join(['%s'] * len(row))
            insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
            
            try:
                self.db_cursor.execute(insert_query, tuple(row))
            except Exception as e:
                errors.append((index + 1, str(e)))  # +1 for 1-based line numbers
            finally:
                self.db_connection.commit()

        if errors:
            error_messages = '\n'.join([f"Line {line}: {error}" for line, error in errors])
            self.show_message(f"Errors encountered:\n{error_messages}", success=False)
        else:
            self.show_message(f"{table_name.capitalize()} information submitted successfully!")

    
    #Search and export functionality 
    def search_data(self):
        if hasattr(self, 'message_label'):
            self.message_label.destroy()
        
        project_id = self.entry_project_id.get().strip()
        selected_table = self.dropdown_table.get()
        
        if not selected_table:
            self.show_message("Please select a table.", success=False)
            return

        if project_id.lower() == "all" or project_id == "*":
            query = sql.SQL("SELECT * FROM {}").format(sql.Identifier(selected_table))
            params = ()
        else:
            if not project_id:
                self.show_message("Please fill in the Project ID.", success=False)
                return
            
            if not self.check_project_id_exists(project_id):
                self.show_message("Project ID does not exist.", success=False)
                return
            
            query = sql.SQL("SELECT * FROM {} WHERE project_id = %s").format(sql.Identifier(selected_table))
            params = (project_id,)

        try:
            self.db_cursor.execute(query, params)
            rows = self.db_cursor.fetchall()

            if not rows:
                self.output_text.delete(1.0, tk.END)
                self.show_message("No results found.", success=False)
                self.export_button.config(state=tk.DISABLED)
                return

            columns = [desc[0] for desc in self.db_cursor.description]
            df = pd.DataFrame(rows, columns=columns)

            self.output_text.delete(1.0, tk.END)
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

    #Content of pages
    def page1(self):
        self.title.config(text='Project Information')

        self.app_text_2 = self.create_text('Fill in the fields to include the information or provide a file. The file must have 6 columns in the same order as the form.', 0, 5)       

        self.entry_project_id = self.create_label_entry('Project ID: ', 0, 20)
        self.entry_project_title = self.create_label_entry('Project Title: ', 0, 21)
        self.entry_start_date = self.create_label_entry('Start Date (DD/MM/YYYY): ', 0, 22)
        self.entry_end_date = self.create_label_entry('End Date (DD/MM/YYYY): ', 0, 23)
        self.entry_project_leader = self.create_label_entry('Project Leader: ', 0, 24)
        self.entry_organisation = self.create_label_entry('Organisation: ', 0, 25)
        
        self.bt_submit =self.create_button('Submit', 0,30,self.submit_project_info,'page_content')
        self.upload_button =self.create_button('Upload Excel', 1,30,lambda: self.upload_excel('projects'),'page_content')

    def page2(self):
        self.title.config(text='Researcher Information')        
        
        self.app_text_2 = self.create_text('Fill in the fields to include the information or provide a file. The file must have 4 columns in the same order as the form.', 0, 5)      

        self.entry_project_id = self.create_label_entry('Project ID: ', 0, 20)
        self.entry_name = self.create_label_entry('Name: ', 0, 21)
        self.entry_organisation = self.create_label_entry('Organisation: ', 0, 22)
        self.entry_project_role = self.create_label_entry('Project Role: ', 0, 23)

        self.bt_submit =self.create_button('Submit', 0,30,self.submit_researcher_info,'page_content')
        self.upload_button =self.create_button('Upload Excel', 1,30,lambda: self.upload_excel('researchers'),'page_content')

    def page3(self):
        self.title.config(text='Project Co-Contributer')        
        
        self.app_text_2 = self.create_text('Fill in the fields to include the information or provide a file. The file must have 4 columns in the same order as the form.', 0, 5)    

        self.entry_project_id = self.create_label_entry('Project ID: ', 0, 20)
        self.entry_name = self.create_label_entry('Name: ', 0, 21)
        self.entry_organisation = self.create_label_entry('Organisation: ', 0, 22)
        self.entry_contribution = self.create_label_entry('Contribution: ', 0, 23)

        self.bt_submit =self.create_button('Submit', 0,30,self.submit_co_contributor_info,'page_content')
        self.upload_button =self.create_button('Upload Excel', 1,30,lambda: self.upload_excel('co_contributors'),'page_content')

    def page4(self):
        self.title.config(text='Project User')        
        
        self.app_text_2 = self.create_text('Fill in the fields to include the information or provide a file. The file must have 5 columns in the same order as the form.', 0, 5)     

        self.entry_project_id = self.create_label_entry('Project ID: ', 0, 20)
        self.entry_type = self.create_label_entry('Type: ', 0, 21)
        self.entry_organisation = self.create_label_entry('Organisation: ', 0, 22)
        self.entry_name = self.create_label_entry('Name: ', 0, 23)
        self.entry_email = self.create_label_entry('Email: ', 0, 24)

        self.bt_submit =self.create_button('Submit', 0,30,self.submit_research_user_info,'page_content')
        self.upload_button =self.create_button('Upload Excel', 1,30,lambda: self.upload_excel('research_users'),'page_content')

    def page5(self):
        self.title.config(text='Search')
      
        self.app_text_2 = self.create_text('Enter the project ID and select the table you want to query. If you want all the values ​​in the table, type "all" and select the table.', 0, 4) 

        self.entry_project_id = self.create_label_entry('Project ID: ', 0, 5)
        self.dropdown_table = self.create_dropdown('Select table',['projects', 'researchers', 'co_contributors', 'research_users'], 0, 10)

        self.bt_search = self.create_button('Search', 0,15,self.search_data,'page_content')
        self.export_button = self.create_button('Export to Excel', 1,15,self.export_to_excel,'page_content')
        self.export_button.config(state=tk.DISABLED)

        scrollbar = tk.Scrollbar(self.page_content)
        scrollbar.grid(row=20, column=3, sticky='ns', padx=(0, 10), pady=10)

        self.output_text = tk.Text(self.page_content, height=10, width=100, yscrollcommand=scrollbar.set)
        self.output_text.grid(row=20, column=0, columnspan=3, padx=5, pady=10)

        scrollbar.config(command=self.output_text.yview)

if __name__ == "__main__":
    root = tk.Tk()
    app = MyApp(root)    
    root.geometry("960x600")
    app.mainloop()