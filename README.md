# Group 03 - Regex-Powered Text Search Tool

This project is a desktop application that allows users to run **regex-powered searches** across single files or entire folders with a **modern Tkinter GUI**. It supports multiple file types (TXT, CSV, PDF, DOCX, XLSX, etc.), highlights matches, and allows exporting results.

---

## ✨ Features
- **Single File Search**: Open a file, run regex, and view highlighted matches.  
- **Folder Search**: Run regex across all files in a folder, view results in a table, and preview context.  
- **Regex Options**: Supports `IGNORECASE`, `MULTILINE`, `DOTALL`.  
- **Export**: Save matches to CSV or TXT.  
- **Saved Queries**: Store and reload frequently used regex patterns.  

---

## ⚙️ Setup & Installation

### Prerequisites

-   Python 3.10 or newer
-   `pipenv`


### 1. Clone the Repository

```bash
git clone <https://github.com/samuelinalegwu/Group03-regex-search-tool.git>
cd Group03-regex-search-tool
```


### 2. Create a Virtual Environment & Install Dependencies

This project uses pipenv to manage dependencies. The Pipfile.lock guarantees that you will have the exact same package versions as the developers.

Run the following command to create a virtual environment and install all necessary packages:


``` bash
# Installs both production and development packages
pipenv install --dev
```

### 3. Activate the Virtual Environment
To run the application or tests, you must first activate the virtual environment:

``` bash
pipenv shell
```

------------------------------------------------------------------------

## 🚀 How to Run

### Run the Application
Once the virtual environment is activated, run the main application file:

``` bash
python src/app.py
```

### Run Tests
To ensure everything is set up correctly, you can run the test suite using pytest:


``` bash
pytest
```

You should see all tests pass successfully.

------------------------------------------------------------------------

## 📖 How to Use the Tool

1. **Select a Search Mode:** Choose either the "Single File Search" or "Folder Search" tab.

2. **Enter Regex Pattern:** Type your regular expression in the Regex Pattern input field. You can also save common patterns using the "Save Query" button.

3. **Select Options:** Enable flags like Ignore Case, Multiline, or Dot All to refine your search.

4. **Browse for a File/Folder:** Click the browse button to select your target file or folder.

5. **Perform Search:** Click the "Search" button to find all matches.

6. **View Results:**

    In single file mode, matches are highlighted directly in the text area.

    In folder mode, results appear in the table. Click on a result to see the context preview below.

7. **Export Results:** You can download matches from a single file search or export the entire folder search report to a CSV file.


## 👥 Team & Contributions

- **[Osagie Patrick Osaze]:** [Coordinator / Lead] Responsible for scheduling meetings, ensuring the team meets deadlines, and overseeing the final submission.
- **[Sani Suleiman Haruna]:** [Developer (Core Logic)] Responsible for writing the main application code and implementing the core functionality of the MVP.
- **[Samuel Inalegwu Otu]:** [QA / CI & Tests] Responsible for writing the pytest tests, setting up Continuous Integration (CI), and ensuring code quality.
- **[Obianozie Obinna-Chukwu]:** [Docs / Presenter] Responsible for writing the README, the final report, and creating the demo video and presentation script.
