import pytest
from data.input_code.t9 import *

@pytest.mark.parametrize('input_str, expected', [
    ('abcabc', 3),
    ('abcd', 4),
    ('', 0),
    ('a', 1),
    ('ab', 2),
    ('a' * 100, 1),
    ('ab@#cd', 6),
    ('ab cd', 5),
    ('ab\ncd', 5),
    ('abcüdef', 7),
])
def test_find_Rotations(input_str, expected):
    assert find_Rotations(input_str) == expected