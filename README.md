# Group 3 - Regex-Powered Text Search Tool

This project is a **desktop application** that provides a user-friendly
graphical interface for finding and extracting text patterns from
various file types using **regular expressions (regex)**.

It is designed to be a simple yet powerful tool for tasks like searching
through log files, analyzing data, or filtering content.

------------------------------------------------------------------------

## ✨ Features

-   **Modern & Clean UI**\
    Minimalist, light-blue themed interface that is easy to navigate.

-   **Multi-File Support**\
    Load and search through a variety of file formats:

    -   Microsoft Word (`.docx`)\
    -   PDF (`.pdf`)\
    -   CSV (`.csv`)\
    -   Plain Text (`.txt`, `.py`, etc.)

-   **Powerful Regex Engine**\
    Utilizes Python's built-in `re` module for reliable pattern
    matching.

-   **Flexible Search Options**

    -   Case Insensitive Search: find matches regardless of case.\
    -   Whole Word Search: match only complete words, not substrings.

-   **Clear & Interactive Results**

    -   Matches are highlighted directly in the text view.\
    -   A results panel displays a detailed list of all matches,
        including line and character positions.

------------------------------------------------------------------------

## 📂 Project Structure

    .
    ├── app.py              # Main application file (Tkinter GUI)
    ├── main.py             # Core logic for reading files and finding matches
    ├── test_main.py        # Unit tests for the core logic (pytest)
    └── requirements.txt    # Project dependencies

------------------------------------------------------------------------

## ⚙️ Setup & Installation

### Prerequisites

-   Python 3.6 or newer

### 1. Create a Virtual Environment (Recommended)

**Windows**

``` bash
python -m venv venv
venv\Scriptsctivate
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
