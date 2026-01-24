import pytest
from data.input_code.t19 import test_duplicate

class TestTestDuplicate:
    def test_empty_array(self):
        assert test_duplicate([]) is False

    def test_no_duplicates(self):
        assert test_duplicate([1, 2, 3, 4, 5]) is False

    def test_duplicates(self):
        assert test_duplicate([1, 2, 2, 3, 3]) is True



    def test_empty_list_with_none(self):
        with pytest.raises(TypeError):
            test_duplicate(None)


    def test_empty_list_with_float(self):
        with pytest.raises(TypeError):
            test_duplicate(3.5)