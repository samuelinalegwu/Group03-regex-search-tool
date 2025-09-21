import os
import re
import csv
import json

# --- Optional Imports for Advanced File Processing ---
try:
    import docx
    from PyPDF2 import PdfReader
    import openpyxl
except ImportError: 
    print("Warning: Libraries for DOCX, PDF, and Excel not found.")
    print("Please run: pip install python-docx PyPDF2 openpyxl")
    docx = None
    PdfReader = None
    openpyxl = None


def read_file_content(file_path):
    """
    Reads file content into a string. Supports PDF, DOCX, XLSX, CSV, and text files.
    """
    content = ""
    try:
        ext = os.path.splitext(file_path)[1].lower()

        if ext == ".docx" and docx:
            doc = docx.Document(file_path)
            content = "\n".join([p.text for p in doc.paragraphs])

        elif ext == ".pdf" and PdfReader:
            reader = PdfReader(file_path)
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    content += text + "\n"

        elif ext == ".xlsx" and openpyxl:
            workbook = openpyxl.load_workbook(file_path)
            sheet = workbook.active
            for row in sheet.iter_rows(values_only=True):
                content += "\t".join([str(cell) for cell in row if cell is not None]) + "\n"

        elif ext == ".csv":
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                reader = csv.reader(f)
                for row in reader:
                    content += ", ".join(row) + "\n"

        else:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

    except Exception as e:
        content = f"Error reading file '{os.path.basename(file_path)}':\n\n{e}"

    return content


def find_matches_in_text(text_content, pattern, flags=0):
    """Finds regex matches in text."""
    compiled_pattern = re.compile(pattern, flags)
    return list(compiled_pattern.finditer(text_content))


class SearchResult:
    """Container for a regex match."""
    def __init__(self, file_path, line_number, line_content, match_group):
        self.file_path = file_path
        self.file_name = os.path.basename(file_path)
        self.line_number = line_number
        self.line_content = line_content.strip()
        self.match_group = match_group


class RegexSearcher:
    """Handles searching, exporting, and query persistence."""

    def search_in_folder(self, folder_path, pattern, flags=0):
        compiled_pattern = re.compile(pattern, flags)
        for root, _, files in os.walk(folder_path):
            for filename in files:
                file_path = os.path.join(root, filename)
                content = read_file_content(file_path)
                if content.startswith("Error reading file"):
                    continue
                for line_num, line in enumerate(content.splitlines(), 1):
                    for match in compiled_pattern.finditer(line):
                        yield SearchResult(
                            file_path=file_path,
                            line_number=line_num,
                            line_content=line,
                            match_group=match.group(0),
                        )

    def export_results_to_csv(self, results, output_path):
        with open(output_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["File Name", "Line Number", "Matched Text", "Full Line"])
            for res in results:
                writer.writerow([res.file_name, res.line_number, res.match_group, res.line_content])

    def save_queries(self, queries, file_path="saved_queries.json"):
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(queries, f, indent=2)

    def load_queries(self, file_path="saved_queries.json"):
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return []
