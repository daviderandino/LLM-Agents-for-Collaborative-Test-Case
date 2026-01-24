import pytest
from data.input_code.t18 import str_to_list, lst_to_string, get_char_count_array, remove_dirty_chars

def test_str_to_list():
    # Check normal string
    assert str_to_list('hello') == ['h', 'e', 'l', 'l', 'o']
    # Check empty string
    assert str_to_list('') == []

def test_lst_to_string():
    # Check normal list
    assert lst_to_string(['h', 'e', 'l', 'l', 'o']) == 'hello'
    # Check empty list
    assert lst_to_string([]) == ''
    # Check single-character list
    assert lst_to_string(['a']) == 'a'
    # Check None input
    with pytest.raises(TypeError):
        lst_to_string(None)


def test_remove_dirty_chars_empty_string():
    # Check if input string is empty
    assert remove_dirty_chars('','') == ''





def test_remove_dirty_chars_second_string_none():
    # Check if second string is None
    with pytest.raises(TypeError):
        remove_dirty_chars('hello', None)

def test_remove_dirty_chars_input_string_none():
    # Check if input string is None
    with pytest.raises(TypeError):
        remove_dirty_chars(None, 'hello')

def test_remove_dirty_chars_invalid_input_types():
    # Check if inputs have incorrect types
    with pytest.raises(TypeError):
        remove_dirty_chars(123, '')