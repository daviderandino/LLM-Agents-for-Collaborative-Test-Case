import pytest
from data.input_code.t13 import *
from collections import Counter




def test_count_common_single_element():
    assert count_common(["a"]) == [('a', 1)]

def test_count_common_two_elements():
    assert count_common(["a", "b"]) == [('a', 1), ('b', 1)]

def test_count_common_three_elements():
    assert count_common(["a", "b", "c"]) == [('a', 1), ('b', 1), ('c', 1)]

def test_count_common_four_elements():
    assert count_common(["a", "b", "c", "d"]) == [('a', 1), ('b', 1), ('c', 1), ('d', 1)]






