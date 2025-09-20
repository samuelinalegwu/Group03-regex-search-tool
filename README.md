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

-   Python 3.6 or newer

### 1. Create a Virtual Environment (Recommended)

**Windows**

``` bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux**

``` bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

``` bash
pip install -r requirements.txt
```

------------------------------------------------------------------------

## 🚀 How to Run

### Run the Application

``` bash
python app.py
```

### Run Tests

``` bash
pytest
```

You should see all tests pass successfully.

------------------------------------------------------------------------

## 📖 How to Use the Tool

1.  **Load a File**
    -   Click **"Load File"** to open a file dialog and select a
        supported document.\
    -   Content will appear in the *Text to Search* area.
2.  **Enter Regex Pattern**
    -   Type your regular expression in the *Regex Pattern* input field.
3.  **Select Options**
    -   Enable **Case Insensitive** or **Whole Word** to refine your
        search.
4.  **Perform Search**
    -   Click **"Search"** to find matches.
5.  **View Results**
    -   Matches are highlighted in the text area.\
    -   A detailed list of matches (with line & character positions)
        appears in the *Results* panel.
