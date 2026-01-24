import pytest
from data.input_code.t18 import str_to_list, lst_to_string, get_char_count_array, remove_dirty_chars

def test_str_to_list():
    # Test empty string
    assert str_to_list("") == []
    # Test string with single character
    assert str_to_list("a") == ['a']
    # Test string with multiple characters
    assert str_to_list("abc") == ['a', 'b', 'c']

def test_lst_to_string():
    # Test empty list
    assert lst_to_string([]) == ""
    # Test list with single character
    assert lst_to_string(['a']) == "a"
    # Test list with multiple characters
    assert lst_to_string(['a', 'b', 'c']) == "abc"



def test_remove_dirty_chars_invalid_input():
    # Test None input
    with pytest.raises(TypeError):
        remove_dirty_chars(None, "")
    # Test None second string input
    with pytest.raises(TypeError):
        remove_dirty_chars("a", None)
    # Test non-string input
    with pytest.raises(TypeError):
        remove_dirty_chars(123, "")
    # Test non-string second string input
    with pytest.raises(TypeError):
        remove_dirty_chars("a", 123)