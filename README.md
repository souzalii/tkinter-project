# My Tkinter App

## Overview

`MyProjects` is a desktop application developed using Python's `tkinter` library for creating graphical user interfaces. The application allows users to manage project-related information, including project details, researchers, co-contributors, and research users. Additionally, it provides functionality for uploading data from Excel files, searching for data in a PostgreSQL database, and exporting query results to Excel.

This project was developed as an experimental venture to explore the integration of Tkinter with PostgreSQL and Excel operations.

### Features

- **Project Information**: Allows users to input and submit project details or upload data from an Excel file.
- **Researcher Information**: Collects details about researchers involved in projects.
- **Project Co-Contributors**: Captures information about co-contributors associated with projects.
- **Research Users**: Manages information about users involved in research projects.
- **Search**: Enables searching of project data in the database and exporting results to Excel.

### Future Improvements

- **Search by Other Fields**: Implement functionality to search by different fields beyond the project ID.
- **Improved Layout**: Update the interface layout to make it more intuitive and visually appealing.

### Dependencies

- `tkinter`: For building the graphical user interface.
- `pandas`: For handling Excel file operations and data manipulation.
- `psycopg2`: For interacting with PostgreSQL databases.
- `openpyxl` or `xlrd`: For reading Excel files (depending on the Excel file format).

### Usage

1. **Running the Application**:
   - Ensure that PostgreSQL is running and a database named `postgres` is available.
   - Modify the database connection parameters in the code.
   - Run the Python script to start the application.

2. **Navigating the Application**:
   - Use the navigation buttons at the top to switch between different pages: Project Information, Researcher Information, Project Co-Contributors, Research Users, and Search.
   - On each page, fill in the required fields or upload an Excel file.
   - Use the search page to query and export data.

3. **Uploading Data**:
   - Data can be uploaded from Excel files that match the required column format for each table.

4. **Searching and Exporting Data**:
   - Enter the Project ID and select a table to search. Export results to an Excel file if needed.

## Code Explanation

### Main Components

- **MyApp Class**: Inherits from `tk.Frame` and encapsulates all the functionality of the application.
  - **Initialization**: Sets up the main frame, buttons, and database connection.
  - **Page Management**: Handles switching between different pages and updating button states.
  - **Database Operations**: Includes methods for submitting data, checking for existing IDs, and handling errors.
  - **Excel Operations**: Provides functionality for uploading and exporting data.

### Methods

- `create_button()`, `create_label_entry()`, `create_text()`, `create_dropdown()`: Helper methods to create and position widgets.
- `submit_project_info()`, `submit_researcher_info()`, `submit_co_contributor_info()`, `submit_research_user_info()`: Methods to submit information to the database.
- `upload_excel()`: Handles uploading data from Excel files.
- `search_data()`, `export_to_excel()`: Methods for searching data and exporting results.

## References

- [@codefirstwithhala](https://www.youtube.com/@codefirstwithhala): For video tutorials and guidance on creating the application.
- [@FabioMusanni](https://www.youtube.com/@FabioMusanni): For various videos that helped in conceptualizing and developing the application.
- **ChatGPT**: For assistance in creating and updating the project documentation.

## Contact

For questions or feedback, please contact [aline.s@outlook.com.br](mailto:aline.s@outlook.com.br).
