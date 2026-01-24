import pytest
from data.input_code.t13 import *
from collections import Counter





def test_count_common_long_string_list():
    assert count_common(["a"] * 10000) == [('a', 10000)]

def test_count_common_multiple_words():
    assert count_common(["a", "b", "c"]) == [('a', 1), ('b', 1), ('c', 1)]