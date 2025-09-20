import pytest
from main import find_matches # Import the function you want to test

def test_simple_match():
    """Tests a basic, single match."""
    text = "Hello world, this is a test."
    pattern = "world"
    matches = find_matches(text, pattern)
    assert len(matches) == 1
    assert matches[0]['group'] == "world"
    assert matches[0]['line_number'] == 1

def test_no_match_found():
    """Tests that an empty list is returned when no match is found."""
    text = "Hello world, this is a test."
    pattern = "python"
    matches = find_matches(text, pattern)
    assert len(matches) == 0

def test_case_insensitive_match():
    """Tests the case-insensitive search option."""
    text = "Python is great, and python is easy."
    pattern = "python"
    # Test without ignore_case
    matches_sensitive = find_matches(text, pattern, ignore_case=False)
    assert len(matches_sensitive) == 1
    
    # Test with ignore_case=True
    matches_insensitive = find_matches(text, pattern, ignore_case=True)
    assert len(matches_insensitive) == 2
    assert matches_insensitive[0]['group'] == "Python"
    assert matches_insensitive[1]['group'] == "python"

def test_whole_word_match():
    """Tests the whole word search option."""
    text = "This is a programmer's program."
    pattern = "program"
    # Test without whole_word
    matches_partial = find_matches(text, pattern, whole_word=False)
    assert len(matches_partial) == 2 # Finds "programmer" and "program"
    
    # Test with whole_word=True
    matches_whole = find_matches(text, pattern, whole_word=True)
    assert len(matches_whole) == 1 # Should only find "program"
    assert matches_whole[0]['group'] == "program"

def test_multiple_lines():
    """Tests that matches are found on different lines with correct line numbers."""
    text = "first line has a word\nsecond line has the same word"
    pattern = "word"
    matches = find_matches(text, pattern)
    assert len(matches) == 2
    assert matches[0]['line_number'] == 1
    assert matches[1]['line_number'] == 2