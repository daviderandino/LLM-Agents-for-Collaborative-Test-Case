import pytest
from data.input_code.t2 import *

def test_similar_elements_HappyPath():
    assert similar_elements((1, 2, 3), (2, 3, 4)) == (2, 3)

def test_similar_elements_IdenticalSets():
    assert similar_elements((1, 2, 3), (1, 2, 3)) == (1, 2, 3)

def test_similar_elements_NoCommonElements():
    assert similar_elements((1, 2, 3), (4, 5, 6)) == ()

def test_similar_elements_EmptySet():
    assert similar_elements((), (2, 3, 4)) == ()

def test_similar_elements_EmptySet2():
    assert similar_elements((1, 2, 3), ()) == ()