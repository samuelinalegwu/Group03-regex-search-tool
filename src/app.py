import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext, font
import re
from core import RegexSearcher, read_file_content, find_matches_in_text


class RegexSearchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Group 3 - Advanced Regex Search Tool")
        self.root.geometry("650x500")   # Changed from 1100x800
        self.root.minsize(650, 500)     # Adjusted minimum size

        self.searcher = RegexSearcher()
        self.folder_search_results = []
        self.file_search_matches = []
        self.saved_queries = self.searcher.load_queries()

        self._setup_styles()
        self._setup_ui()

    # -------------------------------------------------------------------------
    # STYLE SETUP
    # -------------------------------------------------------------------------
    def _setup_styles(self):
        self.style = ttk.Style(self.root)
        self.style.theme_use("clam")
        self.root.geometry("600x630")

        self.BG_COLOR = "#f0f8ff"
        self.PRIMARY_COLOR = "#ffffff"
        self.ACCENT_COLOR = "#5889EC"
        self.ACCENT_HOVER = "#2156B8"
        self.TEXT_COLOR = "#000000"
        self.BORDER_COLOR = "#b1b1d7"
        self.MATCH_HIGHLIGHT = "#0325d2"

        self.default_font = font.Font(family="Segoe UI", size=10)
        self.header_font = font.Font(family="Segoe UI", size=10, weight="bold")
        self.text_font = font.Font(family="Consolas", size=10)

        self.root.configure(bg=self.BG_COLOR)

        self.style.configure(".", background=self.BG_COLOR,
                             font=self.default_font)
        self.style.configure("TFrame", background="#ffffff")
        self.style.configure("TLabel", background=self.BG_COLOR)
        self.style.configure("TCheckbutton", background=self.BG_COLOR)
        self.style.configure("TLabelframe", background=self.BG_COLOR,
                             bordercolor=self.BORDER_COLOR, padding=5,)
        self.style.configure("TLabelframe.Label", background=self.BG_COLOR,
                             foreground=self.TEXT_COLOR, font=self.header_font)
        self.style.configure("TButton", padding=5, relief="flat", background=self.ACCENT_COLOR,
                             foreground=self.PRIMARY_COLOR, font=font.Font(family="Segoe UI", size=5, weight="bold"))
        self.style.map("TButton", background=[
                       ("active", self.ACCENT_HOVER), ("pressed", self.ACCENT_HOVER)])
        self.style.configure(
            "TNotebook", background=self.BG_COLOR, borderwidth=0)
        self.style.configure("TNotebook.Tab", background=self.BG_COLOR, padding=[
                             5, 2], font=self.default_font)
        self.style.map("TNotebook.Tab", background=[
                       ("selected", self.PRIMARY_COLOR)])
        self.style.configure("Treeview", rowheight=25, fieldbackground=self.PRIMARY_COLOR, background=self.PRIMARY_COLOR,
                             font=self.default_font)
        self.style.configure("Treeview.Heading", font=self.header_font,
                             background=self.BG_COLOR, relief="flat")
        self.style.map("Treeview.Heading", background=[
                       ("active", self.BG_COLOR)])

    # -------------------------------------------------------------------------
    # UI SETUP
    # -------------------------------------------------------------------------
    def _setup_ui(self):
        top_frame = ttk.Frame(self.root, padding=5)
        top_frame.pack(fill=tk.X, side=tk.TOP)
        self._create_regex_controls(top_frame)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        self._create_file_search_tab()
        self._create_folder_search_tab()

    def _create_regex_controls(self, parent):
        regex_frame = ttk.Labelframe(parent, text="Regex Pattern")
        regex_frame.pack(fill=tk.X, pady=5)
        self.pattern_var = tk.StringVar()
        self.pattern_combo = ttk.Combobox(regex_frame, textvariable=self.pattern_var,
                                          values=self.saved_queries, font=self.default_font)
        self.pattern_combo.pack(side=tk.LEFT, fill=tk.X,
                                expand=True, padx=(0, 10))
        ttk.Button(regex_frame, text="Save Query",
                   command=self._save_query).pack(side=tk.LEFT)

        flags_frame = ttk.Labelframe(parent, text="Regex Options (Flags)")
        flags_frame.pack(fill=tk.X, pady=5)
        self.ignore_case_var = tk.BooleanVar()
        self.multiline_var = tk.BooleanVar()
        self.dotall_var = tk.BooleanVar()
        ttk.Checkbutton(flags_frame, text="Ignore Case",
                        variable=self.ignore_case_var).pack(side=tk.LEFT, padx=15)
        ttk.Checkbutton(flags_frame, text="Multiline",
                        variable=self.multiline_var).pack(side=tk.LEFT, padx=15)
        ttk.Checkbutton(flags_frame, text="Dot All",
                        variable=self.dotall_var).pack(side=tk.LEFT, padx=15)

    # -------------------------------------------------------------------------
    # FILE SEARCH TAB
    # -------------------------------------------------------------------------
    def _create_file_search_tab(self):
        file_tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(file_tab, text="Single File Search")

        file_controls = ttk.Frame(file_tab)
        file_controls.pack(fill=tk.X, pady=5)
        self.file_path_var = tk.StringVar()
        ttk.Entry(file_controls, textvariable=self.file_path_var, state="readonly", font=self.default_font).pack(
            side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        ttk.Button(file_controls, text="Browse File...",
                   command=self._browse_file).pack(side=tk.LEFT)
        ttk.Button(file_controls, text="Search in File",
                   command=self._perform_file_search).pack(side=tk.LEFT, padx=5)

        text_frame = ttk.Frame(file_tab)
        text_frame.pack(fill=tk.BOTH, expand=True)
        self.file_text_area = scrolledtext.ScrolledText(text_frame, wrap=tk.WORD, font=self.text_font,
                                                        bg=self.PRIMARY_COLOR, bd=1, relief="solid",
                                                        highlightthickness=2, highlightbackground=self.BORDER_COLOR, height=15)
        self.file_text_area.pack(fill=tk.BOTH, expand=True)
        self.file_text_area.tag_configure(
            "match", background=self.MATCH_HIGHLIGHT, foreground="White")

        bottom_frame = ttk.Frame(file_tab)
        bottom_frame.pack(fill=tk.X, pady=5)
        self.file_match_label = ttk.Label(
            bottom_frame, text="Matches Found: 0")
        self.file_match_label.pack(side=tk.LEFT)
        ttk.Button(bottom_frame, text="Download Matches",
                   command=self._download_file_matches).pack(side=tk.RIGHT)

    # -------------------------------------------------------------------------
    # FOLDER SEARCH TAB
    # -------------------------------------------------------------------------
    def _create_folder_search_tab(self):
        folder_tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(folder_tab, text="Folder Search")

        folder_controls = ttk.Frame(folder_tab)
        folder_controls.pack(fill=tk.X, pady=5)
        self.folder_path_var = tk.StringVar()
        ttk.Entry(folder_controls, textvariable=self.folder_path_var, state="readonly",
                  font=self.default_font).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        ttk.Button(folder_controls, text="Browse Folder...",
                   command=self._browse_folder).pack(side=tk.LEFT)
        ttk.Button(folder_controls, text="Search in Folder",
                   command=self._perform_folder_search).pack(side=tk.LEFT, padx=5)

        results_frame = ttk.Labelframe(
            folder_tab, text="Search Results", height=5)
        results_frame.pack(fill=tk.BOTH, expand=False, pady=0)

        columns = ("file", "line", "match")
        self.results_tree = ttk.Treeview(
            results_frame, columns=columns, show="headings", height=5)
        self.results_tree.heading("file", text="File Name")
        self.results_tree.heading("line", text="Line No.")
        self.results_tree.heading("match", text="Matched Text")
        self.results_tree.column("line", width=80, anchor=tk.CENTER)

        vsb = ttk.Scrollbar(results_frame, orient="vertical",
                            command=self.results_tree.yview)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        self.results_tree.configure(yscrollcommand=vsb.set)
        self.results_tree.pack(fill=tk.BOTH, expand=True)
        self.results_tree.bind("<<TreeviewSelect>>", self._on_result_select)

        context_frame = ttk.Labelframe(folder_tab, text="Context Preview")
        context_frame.pack(fill=tk.X, pady=2)
        self.context_text = tk.Text(context_frame, height=5, wrap=tk.WORD, state="disabled", font=self.text_font,
                                    bg=self.PRIMARY_COLOR, bd=1, relief="solid",
                                    highlightthickness=1, highlightbackground=self.BORDER_COLOR)
        self.context_text.pack(fill=tk.X, expand=True)
        self.context_text.tag_configure(
            "match", background=self.MATCH_HIGHLIGHT, foreground="White")

        ttk.Button(folder_tab, text="Export Results to CSV",
                   command=self._export_results).pack(pady=5)

    # -------------------------------------------------------------------------
    # EVENT HANDLERS
    # -------------------------------------------------------------------------
    def _get_regex_flags(self):
        flags = 0
        if self.ignore_case_var.get():
            flags |= re.IGNORECASE
        if self.multiline_var.get():
            flags |= re.MULTILINE
        if self.dotall_var.get():
            flags |= re.DOTALL
        return flags

    def _browse_file(self):
        filetypes = [
            ("All Supported Files",
             "*.txt *.py *.log *.md *.csv *.json *.pdf *.docx *.xlsx"),
            ("Text Files", "*.txt *.py *.log *.md"),
            ("PDF Files", "*.pdf"),
            ("Word Documents", "*.docx"),
            ("Excel Spreadsheets", "*.xlsx"),
            ("CSV Files", "*.csv"),
            ("All Files", "*.*"),
        ]
        path = filedialog.askopenfilename(filetypes=filetypes)
        if path:
            self.file_path_var.set(path)
            content = read_file_content(path)
            self.file_text_area.delete("1.0", tk.END)
            self.file_text_area.insert("1.0", content)

    def _browse_folder(self):
        path = filedialog.askdirectory()
        if path:
            self.folder_path_var.set(path)

    def _perform_file_search(self):
        pattern = self.pattern_var.get()
        content = self.file_text_area.get("1.0", tk.END)
        if not pattern:
            messagebox.showwarning(
                "Input Required", "Please enter a regex pattern.")
            return

        self.file_text_area.tag_remove("match", "1.0", tk.END)

        try:
            flags = self._get_regex_flags()
            self.file_search_matches = find_matches_in_text(
                content, pattern, flags)
            self.file_match_label.config(
                text=f"Matches Found: {len(self.file_search_matches)}")

            for match in self.file_search_matches:
                start_index = f"1.0 + {match.start()} chars"
                end_index = f"1.0 + {match.end()} chars"
                self.file_text_area.tag_add("match", start_index, end_index)
        except re.error as e:
            messagebox.showerror(
                "Invalid Regex", f"The regex pattern is invalid.\n\nDetails: {e}")

    def _download_file_matches(self):
        if not self.file_search_matches:
            messagebox.showwarning(
                "No Matches", "There are no matches to download.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.csv"), ("All files", "*.*")],
            title="Download Matches As...",
            initialfile="matched_text.txt",
        )

        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(
                        f"--- Found {len(self.file_search_matches)} matches ---\n\n")
                    for match in self.file_search_matches:
                        f.write(match.group(0) + "\n")
                messagebox.showinfo("Download Complete",
                                    f"Matches saved to:\n{file_path}")
            except Exception as e:
                messagebox.showerror(
                    "Download Failed", f"Could not save the file.\n\nError: {e}")

    def _perform_folder_search(self):
        folder = self.folder_path_var.get()
        pattern = self.pattern_var.get()
        if not folder or not pattern:
            messagebox.showwarning(
                "Input Required", "Please select a folder and enter a regex pattern.")
            return

        self._clear_folder_results()

        try:
            flags = self._get_regex_flags()
            self.folder_search_results = list(
                self.searcher.search_in_folder(folder, pattern, flags))

            if not self.folder_search_results:
                messagebox.showinfo("Search Complete", "No matches found.")
                return

            for i, res in enumerate(self.folder_search_results):
                self.results_tree.insert("", tk.END, iid=i,
                                         values=(res.file_name, res.line_number, res.match_group))

        except re.error as e:
            messagebox.showerror(
                "Invalid Regex", f"The regex pattern is invalid.\n\nDetails: {e}")

    def _on_result_select(self, event):
        selected_items = self.results_tree.selection()
        if not selected_items:
            return

        selected_iid = int(selected_items[0])
        result = self.folder_search_results[selected_iid]

        self.context_text.config(state="normal")
        self.context_text.delete("1.0", tk.END)
        self.context_text.insert("1.0", result.line_content)

        try:
            start_index = result.line_content.find(result.match_group)
            if start_index != -1:
                end_index = start_index + len(result.match_group)
                self.context_text.tag_add(
                    "match", f"1.{start_index}", f"1.{end_index}")
        except tk.TclError:
            pass
        self.context_text.config(state="disabled")

    def _export_results(self):
        if not self.folder_search_results:
            messagebox.showwarning(
                "No Results", "There are no search results to export.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Save Results As...",
            initialfile="MatchReport.csv",
        )
        if file_path:
            self.searcher.export_results_to_csv(
                self.folder_search_results, file_path)
            messagebox.showinfo("Export Successful",
                                f"Results saved to:\n{file_path}")

    def _save_query(self):
        query = self.pattern_var.get()
        if query and query not in self.saved_queries:
            self.saved_queries.append(query)
            self.searcher.save_queries(self.saved_queries)
            self.pattern_combo["values"] = self.saved_queries
            messagebox.showinfo(
                "Query Saved", f"The pattern '{query}' has been saved.")

    def _clear_folder_results(self):
        self.results_tree.delete(*self.results_tree.get_children())
        self.context_text.config(state="normal")
        self.context_text.delete("1.0", tk.END)
        self.context_text.config(state="disabled")


if __name__ == "__main__":
    root = tk.Tk()
    app = RegexSearchApp(root)
    root.mainloop()
