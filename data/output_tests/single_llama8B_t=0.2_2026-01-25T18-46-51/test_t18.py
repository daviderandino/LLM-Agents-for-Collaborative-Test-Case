import pytest
from data.input_code.t18 import str_to_list, lst_to_string, get_char_count_array, remove_dirty_chars





def test_remove_dirty_chars_invalid_input():
    with pytest.raises(TypeError):
        remove_dirty_chars(123, "World")
    with pytest.raises(TypeError):
        remove_dirty_chars("Hello", 123)
    with pytest.raises(TypeError):
        remove_dirty_chars(123, 123)