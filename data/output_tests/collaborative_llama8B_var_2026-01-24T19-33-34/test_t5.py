import pytest
from fib import *

@pytest.mark.parametrize('n, expected', [
    (0, 1),
    (1, 0)
])
def test_count_ways_base_cases(n, expected):
    assert count_ways(n) == expected

def test_count_ways_large_input():
    assert count_ways(100) == 354224848179261915075

def test_count_ways_negative_input():
    with pytest.raises(ValueError):
        count_ways(-1)

def test_count_ways_non_integer_input():
    with pytest.raises(TypeError):
        count_ways(3.5)

def test_count_ways_non_integer_input_type():
    with pytest.raises(TypeError):
        count_ways('a')

def test_count_ways_non_integer_input_type2():
    with pytest.raises(TypeError):
        count_ways(None)

def test_count_ways_non_integer_input_type3():
    with pytest.raises(TypeError):
        count_ways(True)

def test_count_ways_non_integer_input_type4():
    with pytest.raises(TypeError):
        count_ways(False)

def test_count_ways_non_integer_input_type5():
    with pytest.raises(TypeError):
        count_ways([1, 2, 3])

def test_count_ways_non_integer_input_type6():
    with pytest.raises(TypeError):
        count_ways({'a': 1})

def test_count_ways_non_integer_input_type7():
    with pytest.raises(TypeError):
        count_ways((1, 2, 3))

def test_count_ways_non_integer_input_type8():
    with pytest.raises(TypeError):
        count_ways({'a', 1})

def test_count_ways_non_integer_input_type9():
    with pytest.raises(TypeError):
        count_ways({1, 2, 3})

def test_count_ways_non_integer_input_type10():
    with pytest.raises(TypeError):
        count_ways(1.5)

def test_count_ways_non_integer_input_type11():
    with pytest.raises(TypeError):
        count_ways('1.5')

def test_count_ways_non_integer_input_type12():
    with pytest.raises(TypeError):
        count_ways(1j)

def test_count_ways_non_integer_input_type13():
    with pytest.raises(TypeError):
        count_ways('1j')