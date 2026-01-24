import pytest
from data.input_code.t18 import str_to_list, lst_to_string, get_char_count_array, remove_dirty_chars




def test_remove_dirty_chars_empty_string():
    assert remove_dirty_chars('', '') == ''



def test_remove_dirty_chars_no_chars_in_second_string():
    assert remove_dirty_chars('hello world', 'abc') == 'hello world'




