import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox, font
import os
import re

# Import the core logic functions from main.py
from main import read_file, find_matches

class RegexSearchApp:
    def __init__(self, root):
        """Initializes the application GUI with a modern, self-contained style."""
        self.root = root
        self.root.title("Group 3 - Regex Search Tool")
        self.root.geometry("850x700")
        self.root.minsize(600, 500)

        # --- Style Configuration (No external file needed) ---
        self.style = ttk.Style(self.root)
        
        # --- Color & Font Definitions ---
        BG_COLOR = "#f0f8ff"       # AliceBlue - A very light blue
        PRIMARY_COLOR = "#ffffff"  # White for frames
        TEXT_COLOR = "#1f1f1f"
        BUTTON_COLOR = "#e1f0ff"   # Lighter button blue
        BUTTON_HOVER = "#d1e9ff"
        BUTTON_ACTIVE = "#b4d9ff"
        ENTRY_BG = "#ffffff"
        BORDER_COLOR = "#b0c4de"   # LightSteelBlue for borders
        MATCH_HIGHLIGHT = "#aeeeee" # A pleasant turquoise for highlights
        
        # --- Font Definitions ---
        self.default_font = font.nametofont("TkDefaultFont")
        self.default_font.configure(family="Segoe UI", size=10)
        self.title_font = font.Font(family="Segoe UI", size=11, weight="bold")
        
        # --- Apply Base Styles ---
        self.root.configure(bg=BG_COLOR)
        self.style.theme_use('clam') # Using a theme that allows more customization
        
        self.style.configure('.', background=BG_COLOR, foreground=TEXT_COLOR, font=self.default_font)
        self.style.configure('TFrame', background=PRIMARY_COLOR, borderwidth=1, relief='solid', bordercolor=BORDER_COLOR)
        self.style.configure('NoBorder.TFrame', background=BG_COLOR, borderwidth=0) # Frame with no border
        self.style.configure('TLabel', background=PRIMARY_COLOR)
        self.style.configure('Header.TLabel', background=BG_COLOR, font=self.title_font)
        self.style.configure('TCheckbutton', background=PRIMARY_COLOR)
        
        # Custom Button Style
        self.style.configure('TButton', padding=6, relief="flat", background=BUTTON_COLOR,
                             borderwidth=1, bordercolor=BORDER_COLOR)
        self.style.map('TButton',
            background=[('active', BUTTON_HOVER), ('pressed', BUTTON_ACTIVE)],
            relief=[('pressed', 'sunken')])
        
        # --- Main Layout ---
        main_frame = ttk.Frame(self.root, padding=(20, 10), style='NoBorder.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # --- Search Options Frame ---
        options_frame = ttk.Frame(main_frame, padding=15)
        options_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Regex Pattern Input
        ttk.Label(options_frame, text="Regex Pattern:", font=self.default_font).pack(side=tk.LEFT, padx=(0, 5))
        self.pattern_var = tk.StringVar()
        self.pattern_entry = ttk.Entry(options_frame, textvariable=self.pattern_var, width=30, font=self.default_font)
        self.pattern_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

        # Checkboxes
        self.ignore_case_var = tk.BooleanVar()
        self.case_check = ttk.Checkbutton(options_frame, text="Case Insensitive", variable=self.ignore_case_var)
        self.case_check.pack(side=tk.LEFT, padx=5)

        self.whole_word_var = tk.BooleanVar()
        self.word_check = ttk.Checkbutton(options_frame, text="Whole Word", variable=self.whole_word_var)
        self.word_check.pack(side=tk.LEFT, padx=5)

        # --- Control Buttons Frame ---
        button_frame = ttk.Frame(main_frame, padding=(0, 10), style='NoBorder.TFrame')
        button_frame.pack(fill=tk.X)
        
        self.load_button = ttk.Button(button_frame, text="Load File", command=self.load_file)
        self.load_button.pack(side=tk.LEFT, padx=(0, 10))

        self.search_button = ttk.Button(button_frame, text="Search", command=self.perform_search)
        self.search_button.pack(side=tk.LEFT)

        self.file_label = ttk.Label(main_frame, text="No file loaded.", style='TLabel', background=BG_COLOR)
        self.file_label.pack(fill=tk.X, pady=5)

        # --- Text Input Frame ---
        input_frame = ttk.Frame(main_frame, style='NoBorder.TFrame')
        input_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        ttk.Label(input_frame, text="Text to Search", style='Header.TLabel').pack(anchor="w", pady=(0, 5))
        
        self.text_area = scrolledtext.ScrolledText(input_frame, wrap=tk.WORD,
            font=self.default_font, bg=ENTRY_BG, fg=TEXT_COLOR, relief="solid", bd=1,
            highlightthickness=1, highlightcolor=BORDER_COLOR)
        self.text_area.pack(fill=tk.BOTH, expand=True)
        self.text_area.tag_configure("match", background=MATCH_HIGHLIGHT, foreground=TEXT_COLOR)

        # --- Results Frame ---
        results_frame = ttk.Frame(main_frame, style='NoBorder.TFrame')
        results_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        ttk.Label(results_frame, text="Results", style='Header.TLabel').pack(anchor="w", pady=(0, 5))

        self.results_area = scrolledtext.ScrolledText(results_frame, wrap=tk.WORD,
            font=self.default_font, bg=ENTRY_BG, fg=TEXT_COLOR, relief="solid", bd=1,
            highlightthickness=1, highlightcolor=BORDER_COLOR)
        self.results_area.pack(fill=tk.BOTH, expand=True)
        self.results_area.config(state=tk.DISABLED)

    def load_file(self):
        """Opens a file dialog and loads the content of the selected file."""
        file_path = filedialog.askopenfilename(
            title="Select a file to load",
            filetypes=(
                ("Supported Files", "*.docx *.pdf *.csv *.txt *.py"),
                ("Word Documents", "*.docx"),
                ("PDF Files", "*.pdf"),
                ("CSV Files", "*.csv"),
                ("Text Files", "*.txt"),
                ("All Files", "*.*")
            )
        )
        if not file_path:
            return

        try:
            content = read_file(file_path)
            
            self.text_area.delete("1.0", tk.END)
            self.results_area.config(state=tk.NORMAL)
            self.results_area.delete("1.0", tk.END)
            self.results_area.config(state=tk.DISABLED)
            
            self.text_area.insert("1.0", content)
            self.file_label.config(text=f"Currently loaded: {os.path.basename(file_path)}")

        except Exception as e:
            messagebox.showerror("Error Reading File", f"Failed to read file: {file_path}\n\nError: {e}")
            self.file_label.config(text="Failed to load file.")

    def perform_search(self):
        """Executes the regex search and updates the GUI."""
        self.text_area.tag_remove("match", "1.0", tk.END)
        self.results_area.config(state=tk.NORMAL)
        self.results_area.delete("1.0", tk.END)

        pattern = self.pattern_var.get()
        text_content = self.text_area.get("1.0", tk.END)
        ignore_case = self.ignore_case_var.get()
        whole_word = self.whole_word_var.get()
        
        try:
            matches = find_matches(text_content, pattern, ignore_case, whole_word)

            if not matches:
                self.results_area.insert(tk.END, "No matches found.")
            else:
                for i, match_info in enumerate(matches, 1):
                    start_pos = f"{match_info['line_number']}.{match_info['start']}"
                    end_pos = f"{match_info['line_number']}.{match_info['end']}"
                    self.text_area.tag_add("match", start_pos, end_pos)
                    
                    result_info = (f"Match {i}: Line {match_info['line_number']}, "
                                   f"Ch {match_info['start']} -> '{match_info['group']}'\n")
                    self.results_area.insert(tk.END, result_info)
        
        except re.error as e:
            self.results_area.insert(tk.END, f"Regex Error: {e}")
        except Exception as e:
            self.results_area.insert(tk.END, f"An unexpected error occurred: {e}")

        self.results_area.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = RegexSearchApp(root)
    root.mainloop()

