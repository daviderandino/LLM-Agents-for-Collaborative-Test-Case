import pytest
from data.input_code.t9 import *

@pytest.mark.parametrize('str, expected', [
    ('a', 1),
    ('ab', 2),
    ('abc', 3),
    ('abcde', 5)
])
def test_find_Rotations_edge_cases(str, expected):
    assert find_Rotations(str) == expected

@pytest.mark.parametrize('str1, str2, expected', [
    ('abcabcabc', 3),
    ('abcde', 'xyz', 5),
    ('', 0),
    (None, None)
])
def test_find_Rotations_normal_cases(str1, str2, expected):
    if str1 is None or str2 is None:
        with pytest.raises(TypeError):
            find_Rotations(str1)
    else:
        assert find_Rotations(str1, str2) == expected

@pytest.mark.parametrize('str1, str2, expected', [
    ('abcabcabc', 3),
    ('abcde', 'xyz', 5),
    ('', 0),
    ('abc', 'abc', 1),
    ('abc', 'def', 3),
    ('abc', 'abcabc', 2),
    ('abc', 'abcabcabc', 3),
    ('abc', 'abcabcabcabc', 4),
    ('abc', 'abcabcabcabcabc', 5),
])
def test_find_Rotations_normal_cases_rotations(str1, str2, expected):
    assert find_Rotations(str1, str2) == expected

@pytest.mark.parametrize('str1, str2, expected', [
    ('abcabcabc', 3),
    ('abcde', 'xyz', 5),
    ('', 0),
    (None, None)
])
def test_find_Rotations_normal_cases_rotations_none(str1, str2, expected):
    if str1 is None or str2 is None:
        with pytest.raises(TypeError):
            find_Rotations(str1, str2)
    else:
        assert find_Rotations(str1, str2) == expected