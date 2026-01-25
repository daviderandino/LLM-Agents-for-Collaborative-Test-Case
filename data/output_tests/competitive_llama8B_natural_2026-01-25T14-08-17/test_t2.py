import pytest
from data.input_code.t2 import *

test_tup1 = (1,2,3)
test_tup2 = (1,2,3)
test_tup3 = (4,5,6)
test_tup4 = (1,1,1)
test_tup5 = (1,2,2)
test_tup6 = ()
test_tup7 = (1,2)
test_tup8 = (1,2,None)
test_tup9 = (1,2)
test_tup10 = (1,2,None)

def test_similar_elements_happy_path_identical():
    assert similar_elements(test_tup1, test_tup2) == (1,2,3)

def test_similar_elements_happy_path_no_common():
    assert similar_elements(test_tup1, test_tup3) == ()

def test_similar_elements_happy_path_all_common():
    assert similar_elements(test_tup4, test_tup4) == (1,)

def test_similar_elements_happy_path_duplicate():
    assert similar_elements(test_tup5, test_tup7) == (1,2)

def test_similar_elements_boundary_empty_tup1():
    assert similar_elements(test_tup6, test_tup7) == ()

def test_similar_elements_boundary_empty_tup2():
    assert similar_elements(test_tup7, test_tup6) == ()


