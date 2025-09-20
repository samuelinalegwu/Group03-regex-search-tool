import os
import json
import csv
import tempfile
import pytest
from src.core import (
    read_file_content,
    find_matches_in_text,
    RegexSearcher,
    SearchResult,
)


# -------------------------------------------------------------------
# FIXTURES
# -------------------------------------------------------------------
@pytest.fixture
def sample_dir(tmp_path):
    """Create a temporary folder with different file types for testing."""
    folder = tmp_path / "data"
    folder.mkdir()

    # TXT
    (folder / "Data.txt").write_text("Hello World\nRegex Test\nfoo bar baz")

    # CSV
    with open(folder / "Data.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["col1", "col2"])
        writer.writerow(["foo", "bar"])

    # JSON
    (folder / "Data.json").write_text(json.dumps({"key": "value", "foo": "bar"}))

    # DOCX
    try:
        import docx
        doc = docx.Document()
        doc.add_paragraph("This is a docx test with Foo inside.")
        doc.save(folder / "Data.docx")
    except ImportError:
        pass  # Skip if not installed

    # PDF
    try:
        from reportlab.pdfgen import canvas
        pdf_path = folder / "Data.pdf"
        c = canvas.Canvas(str(pdf_path))
        c.drawString(100, 750, "PDF test with foo keyword")
        c.save()
    except ImportError:
        pass  # Skip if not installed

    # XLSX
    try:
        import openpyxl
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.append(["foo", "bar"])
        ws.append(["baz", "qux"])
        wb.save(folder / "Data.xlsx")
    except ImportError:
        pass  # Skip if not installed

    return folder


# -------------------------------------------------------------------
# TESTS
# -------------------------------------------------------------------

def test_read_file_content_handles_all_formats(sample_dir):
    """Ensure all file types can be read without crashing."""
    for file in sample_dir.iterdir():
        content = read_file_content(str(file))
        assert isinstance(content, str)
        assert "Error" not in content  # should not fail silently


def test_find_matches_in_text_basic():
    text = "Hello world\nRegex test\nAnother line"
    pattern = r"\b\w{5}\b"  # words with 5 letters
    matches = find_matches_in_text(text, pattern)
    assert [m.group(0) for m in matches] == ["Hello", "world"]


def test_search_in_folder_finds_matches(sample_dir):
    searcher = RegexSearcher()
    results = list(searcher.search_in_folder(sample_dir, r"foo", flags=0))
    assert any("foo" in res.line_content.lower() for res in results)
    assert all(isinstance(res, SearchResult) for res in results)


def test_export_results_to_csv(sample_dir, tmp_path):
    searcher = RegexSearcher()
    results = list(searcher.search_in_folder(sample_dir, r"foo"))

    out_csv = tmp_path / "out.csv"
    searcher.export_results_to_csv(results, out_csv)

    assert out_csv.exists()
    content = out_csv.read_text()
    assert "File Name" in content
    assert "foo" in content.lower()


def test_query_persistence(tmp_path):
    searcher = RegexSearcher()
    queries = [r"\d+", r"\w+"]
    file_path = tmp_path / "queries.json"

    # Save queries
    searcher.save_queries(queries, file_path=file_path)
    assert file_path.exists()

    # Load queries
    loaded = searcher.load_queries(file_path=file_path)
    assert loaded == queries


def test_invalid_regex_handling():
    text = "some text here"
    with pytest.raises(Exception):
        # compile will fail if pattern is invalid
        find_matches_in_text(text, r"[unclosed")
