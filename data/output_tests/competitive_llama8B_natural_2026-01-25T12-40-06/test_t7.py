import pytest
from data.input_code.t7 import *

def test_find_char_long_normal_text():
    assert find_char_long("The quick brown fox jumped over the lazy dog") == ['quick', 'brown', 'jumped', 'over', 'lazy']

def test_find_char_long_boundary_condition_1():
    assert find_char_long("A cat dog") == []

def test_find_char_long_boundary_condition_2():
    assert find_char_long("Code code") == ['Code', 'code']

def test_find_char_long_boundary_condition_3():
    assert find_char_long("Programming language") == ['Programming', 'language']

def test_find_char_long_edge_case():
    assert find_char_long("") == []

def test_find_char_long_exception_path():
    with pytest.raises(TypeError):
        find_char_long(None)

def test_find_char_long_special_character_handling():
    assert find_char_long("Hello, world!") == ['Hello', 'world']

def test_find_char_long_punctuation_handling():
    assert find_char_long("Hello,") == ['Hello']

