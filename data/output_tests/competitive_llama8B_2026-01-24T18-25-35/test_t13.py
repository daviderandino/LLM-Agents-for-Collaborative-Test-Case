import pytest
from data.input_code.t13 import *
from collections import Counter







def test_count_common_list_with_duplicates():
    result = count_common(["a", "a", "a", "b", "b", "c"])
    assert result == [('a', 3), ('b', 2), ('c', 1)]