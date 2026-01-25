import pytest
from data.input_code.t19 import *


def test_is_duplicate_empty_set():
    with pytest.raises(TypeError):
        is_duplicate(None)


def test_is_duplicate_non_iterable():
    with pytest.raises(TypeError):
        is_duplicate(123)



def test_is_duplicate_non_iterable_type():
    with pytest.raises(TypeError):
        is_duplicate(123)


def test_is_duplicate_non_iterable_empty():
    with pytest.raises(TypeError):
        is_duplicate(None)

def test_is_duplicate_non_hashable_empty():
    with pytest.raises(TypeError):
        is_duplicate(None)

def test_is_duplicate_non_iterable():
    with pytest.raises(TypeError):
        is_duplicate(123)


def test_is_duplicate_non_iterable():
    with pytest.raises(TypeError):
        is_duplicate(123)

