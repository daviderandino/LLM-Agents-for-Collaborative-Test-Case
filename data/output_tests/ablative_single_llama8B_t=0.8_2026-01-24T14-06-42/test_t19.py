import pytest
from data.input_code.t19 import is_duplicate

class TestTestDuplicate:
    def test_empty_array(self):
        assert is_duplicate([]) is False

    def test_no_duplicates(self):
        assert is_duplicate([1, 2, 3, 4, 5]) is False

    def test_duplicates(self):
        assert is_duplicate([1, 2, 2, 3, 3]) is True



    def test_empty_list_with_none(self):
        with pytest.raises(TypeError):
            is_duplicate(None)


    def test_empty_list_with_float(self):
        with pytest.raises(TypeError):
            is_duplicate(3.5)