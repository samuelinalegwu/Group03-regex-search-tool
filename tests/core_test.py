import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
import os
import sys
import re

# Ensure the src directory is in sys.path to find core.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core import read_file_content, find_matches_in_text, SearchResult, RegexSearcher

# Sample test content
TEST_TXT_CONTENT = """Hello world
This is a test
Another TEST line
hello WORLD"""

@pytest.fixture
def temp_text_file(tmp_path):
    """Create a temporary text file for testing."""
    txt_file = tmp_path / "test.txt"
    txt_file.write_text(TEST_TXT_CONTENT, encoding="utf-8")
    return str(txt_file)

@pytest.fixture
def temp_folder(tmp_path):
    """Create a temporary folder with a test file."""
    txt_file = tmp_path / "test.txt"
    txt_file.write_text(TEST_TXT_CONTENT, encoding="utf-8")
    return str(tmp_path)

def test_read_file_content(temp_text_file):
    """Test reading a text file."""
    content = read_file_content(temp_text_file)
    assert content == TEST_TXT_CONTENT
    assert "Hello world" in content
    assert isinstance(content, str)

def test_read_file_content_non_existent():
    """Test reading a non-existent file."""
    content = read_file_content("non_existent.txt")
    assert content.startswith("Error reading file")
    assert "non_existent.txt" in content

def test_find_matches_in_text():
    """Test regex matching in text."""
    pattern = r"[hH]ello"
    matches = find_matches_in_text(TEST_TXT_CONTENT, pattern, flags=re.IGNORECASE)
    assert len(matches) == 2
    assert matches[0].group(0) == "Hello"
    assert matches[1].group(0) == "hello"

def test_find_matches_in_text_invalid_regex():
    """Test handling of invalid regex pattern."""
    pattern = r"[a-z"  # Invalid regex
    with pytest.raises(re.error):
        find_matches_in_text(TEST_TXT_CONTENT, pattern)

def test_search_result():
    """Test SearchResult object creation."""
    result = SearchResult(
        file_path="test.txt",
        line_number=1,
        line_content="Hello world",
        match_group="Hello"
    )
    assert result.file_name == "test.txt"
    assert result.line_number == 1
    assert result.line_content == "Hello world"
    assert result.match_group == "Hello"

def test_regex_searcher_search_in_folder(temp_folder):
    """Test searching for matches in a folder."""
    searcher = RegexSearcher()
    pattern = r"test"
    results = list(searcher.search_in_folder(temp_folder, pattern, flags=re.IGNORECASE))
    assert len(results) >= 2  # Should find 'test' in test.txt
    found = any(
        result.file_name == "test.txt" and result.match_group.lower() == "test"
        for result in results
    )
    assert found

def test_regex_searcher_save_load_queries(tmp_path):
    """Test saving and loading regex queries."""
    searcher = RegexSearcher()
    queries = [r"\d+", r"[a-zA-Z]+"]
    query_file = str(tmp_path / "saved_queries.json")
    
    searcher.save_queries(queries, query_file)
    assert os.path.exists(query_file)
    
    loaded_queries = searcher.load_queries(query_file)
    assert loaded_queries == queries

def test_regex_searcher_export_results(tmp_path):
    """Test exporting search results to CSV."""
    searcher = RegexSearcher()
    results = [
        SearchResult("test.txt", 1, "Hello world", "Hello"),
        SearchResult("test.txt", 2, "This is a test", "test")
    ]
    output_file = str(tmp_path / "output.csv")
    
    searcher.export_results_to_csv(results, output_file)
    assert os.path.exists(output_file)
    
    with open(output_file, "r", encoding="utf-8") as f:
        content = f.read()
        assert "test.txt,1,Hello,Hello world" in content
        assert "test.txt,2,test,This is a test" in content

if __name__ == "__main__":
    pytest.main(["-v", __file__])