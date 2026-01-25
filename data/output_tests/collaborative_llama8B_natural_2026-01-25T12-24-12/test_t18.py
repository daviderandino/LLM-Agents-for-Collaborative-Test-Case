import pytest
from data.input_code.t18 import *

@pytest.mark.parametrize('string, expected', [
    ("Hello", ['H', 'e', 'l', 'l', 'o']),
    ("", []),
    ("a", ['a'])
])
def test_str_to_list(string, expected):
    assert str_to_list(string) == expected

@pytest.mark.parametrize('List, expected', [
    (['H', 'e', 'l', 'l', 'o'], "Hello"),
    (['a'], "a"),
    (['b', 'c', 'd'], "bcd")
])
def test_lst_to_string(List, expected):
    assert lst_to_string(List) == expected



def test_remove_dirty_chars_zero_length_second_string():
    assert remove_dirty_chars("Hello", "") == "Hello"


def test_remove_dirty_chars_empty_string():
    assert remove_dirty_chars("", "") == ""

def test_remove_dirty_chars_empty_string_with_second_string():
    assert remove_dirty_chars("", "Hello") == ""

def test_remove_dirty_chars_empty_second_string():
    assert remove_dirty_chars("Hello", "") == "Hello"





