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

## 🚀 Setup & Run Instructions

### Requirements
- Python **3.10+**
- `pipenv` for dependency management

### Installation
```bash
git clone https://github.com/your-org/group03-regex-search-tool.git
cd group03-regex-search-tool
pipenv install
