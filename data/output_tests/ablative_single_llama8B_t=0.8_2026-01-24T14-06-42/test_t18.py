import pytest
from data.input_code.t18 import (
    NO_OF_CHARS,
    str_to_list,
    lst_to_string,
    get_char_count_array,
    remove_dirty_chars,
)

class TestStringOperations:
    def test_str_to_list_empty_string(self):
        """Test str_to_list with an empty string."""
        assert str_to_list("") == []

    def test_str_to_list_single_character(self):
        """Test str_to_list with a single character."""
        assert str_to_list("a") == ["a"]

    def test_str_to_list_multiple_characters(self):
        """Test str_to_list with multiple characters."""
        assert str_to_list("abc") == ["a", "b", "c"]

    def test_lst_to_string_empty_list(self):
        """Test lst_to_string with an empty list."""
        assert lst_to_string([]) == ""

    def test_lst_to_string_single_character(self):
        """Test lst_to_string with a single character."""
        assert lst_to_string(["a"]) == "a"

    def test_lst_to_string_multiple_characters(self):
        """Test lst_to_string with multiple characters."""
        assert lst_to_string(["a", "b", "c"]) == "abc"

    def test_get_char_count_array_string(self):
        """Test get_char_count_array with a string."""
        count = get_char_count_array("abc")
        assert count[ord("a")] == 1
        assert count[ord("b")] == 1
        assert count[ord("c")] == 1
        assert count[ord("x")] == 0

    def test_get_char_count_array_empty_string(self):
        """Test get_char_count_array with an empty string."""
        count = get_char_count_array("")
        for i in range(NO_OF_CHARS):
            assert count[i] == 0


    def test_remove_dirty_chars_no_match(self):
        """Test remove_dirty_chars with a non-matching string."""
        assert remove_dirty_chars("abc", "def") == "abc"

    def test_remove_dirty_chars_empty_string(self):
        """Test remove_dirty_chars with an empty string."""
        assert remove_dirty_chars("", "abc") == ""


    def test_remove_dirty_chars_invalid_input_type(self):
        """Test remove_dirty_chars with invalid input types."""
        with pytest.raises(TypeError):
            remove_dirty_chars("abc", 123)
        with pytest.raises(TypeError):
            remove_dirty_chars(123, "abc")