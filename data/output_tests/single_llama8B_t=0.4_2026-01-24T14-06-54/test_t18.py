import pytest
from data.input_code.t18 import str_to_list, lst_to_string, get_char_count_array, remove_dirty_chars

def test_str_to_list_empty_string():
    assert str_to_list("") == []

def test_str_to_list_single_char():
    assert str_to_list("a") == ['a']

def test_str_to_list_multiple_chars():
    assert str_to_list("abc") == ['a', 'b', 'c']

def test_lst_to_string_empty_list():
    assert lst_to_string([]) == ""

def test_lst_to_string_single_char():
    assert lst_to_string(['a']) == "a"

def test_lst_to_string_multiple_chars():
    assert lst_to_string(['a', 'b', 'c']) == "abc"

def test_get_char_count_array_empty_string():
    assert get_char_count_array("") == [0] * 256



def test_remove_dirty_chars_empty_string():
    assert remove_dirty_chars("", "") == ""


def test_remove_dirty_chars_dirty_chars():
    assert remove_dirty_chars("abc", "def") == "abc"

def test_remove_dirty_chars_all_dirty_chars():
    assert remove_dirty_chars("abc", "abcdef") == ""




def test_remove_dirty_chars_second_string_with_all_chars():
    assert remove_dirty_chars("abc", "abcdefghijklmnopqrstuvwxyz") == ""

def test_remove_dirty_chars_invalid_input():
    with pytest.raises(TypeError):
        remove_dirty_chars(123, "abc")
    with pytest.raises(TypeError):
        remove_dirty_chars("abc", 123)