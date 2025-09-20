import os
import re
import csv


try:
    import docx
except ImportError:
    print("Warning: 'python-docx' is not installed. DOCX file support will be disabled.")
    print("Please run 'pip install python-docx'")
    docx = None

try:
    import PyPDF2
except ImportError:
    print("Warning: 'PyPDF2' is not installed. PDF file support will be disabled.")
    print("Please run 'pip install PyPDF2'")
    PyPDF2 = None

def read_file(file_path):
    """
    Reads the content of a file and returns it as a string.
    Supports .txt, .py, .docx, .pdf, and .csv files.
    """
    # Get the file extension to determine how to read the file
    file_extension = os.path.splitext(file_path)[1].lower()
    content = ""

    if file_extension == '.docx':
        if not docx:
            raise ImportError("python-docx library is required for .docx files.")
        doc = docx.Document(file_path)
        full_text = [para.text for para in doc.paragraphs]
        content = '\n'.join(full_text)

    elif file_extension == '.pdf':
        if not PyPDF2:
            raise ImportError("PyPDF2 library is required for .pdf files.")
        with open(file_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    content += page_text + '\n'

    elif file_extension == '.csv':
        with open(file_path, mode='r', encoding='utf-8', newline='') as csv_file:
            # Read all rows and join them into a single text block
            reader = csv.reader(csv_file)
            for row in reader:
                content += ', '.join(row) + '\n'

    else:  # Assume it's a plain text file (.txt, .py, etc.)
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
    return content

def find_matches(text_content, pattern, ignore_case=False, whole_word=False):
    """
    Finds all matches for a regex pattern within a given text.
    Returns a list of dictionaries, each containing details of a match.
    """
    if not pattern:
        return []

    # If whole word is checked, wrap the pattern in word boundaries
    if whole_word:
        pattern = r'\b' + re.escape(pattern) + r'\b'

    # Set the appropriate regex flag for case-insensitivity
    flags = re.IGNORECASE if ignore_case else 0

    matches = []
    # Iterate through each line to get correct line and character numbers
    for line_number, line in enumerate(text_content.splitlines(), 1):
        for match in re.finditer(pattern, line, flags):
            matches.append({
                'line_number': line_number,
                'start': match.start(),
                'end': match.end(),
                'group': match.group(0)  # The actual matched text
            })
    return matches
