import pytest
from feedsnooplyze.utils.content_comparer import ContentComparer

def test_get_difference_added_words():
    comparer = ContentComparer("The quick brown fox jumps", "The quick brown fox")
    assert comparer.get_difference() == "jumps"

def test_get_difference_multiple_added_words():
    comparer = ContentComparer("The quick brown fox jumps over the lazy dog", "The quick brown fox")
    assert comparer.get_difference() == "jumps over the lazy dog"

def test_get_difference_no_difference():
    comparer = ContentComparer("Hello world", "Hello world")
    assert comparer.get_difference() == ""

def test_get_difference_all_new():
    comparer = ContentComparer("foo bar baz", "")
    assert comparer.get_difference() == "foo bar baz"

def test_get_difference_removed_words():
    comparer = ContentComparer("Hello", "Hello world")
    assert comparer.get_difference() == ""

def test_get_difference_added_and_removed_words():
    comparer = ContentComparer("Hello there", "Hello world")
    assert comparer.get_difference() == "there"

def test_get_difference_empty_strings():
    comparer = ContentComparer("", "")
    assert comparer.get_difference() == ""