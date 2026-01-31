import pytest
from data.input_code.d03_linked_list import *

def build_list(initial):
    ll = LinkedList()
    for item in initial:
        ll.append(item)
    return ll

@pytest.mark.parametrize(
    "initial, data, expected",
    [
        ([], 1, [1]),
        ([1], 2, [1, 2]),
    ],
)
def test_append(initial, data, expected):
    ll = build_list(initial)
    ll.append(data)
    assert ll.to_list() == expected

@pytest.mark.parametrize(
    "initial, data, expected",
    [
        ([], "a", ["a"]),
        ([1, 2], 0, [0, 1, 2]),
    ],
)
def test_prepend(initial, data, expected):
    ll = build_list(initial)
    ll.prepend(data)
    assert ll.to_list() == expected

@pytest.mark.parametrize(
    "initial, data, expected",
    [
        ([], 5, False),
        ([5, 6, 7], 5, {"result": True, "list": [6, 7]}),
        ([1, 2, 3], 2, {"result": True, "list": [1, 3]}),
        ([1, 2, 3], 3, {"result": True, "list": [1, 2]}),
        ([1, 2, 3], 4, False),
    ],
)
def test_delete(initial, data, expected):
    ll = build_list(initial)
    result = ll.delete(data)
    if isinstance(expected, dict):
        assert result == expected["result"]
        assert ll.to_list() == expected["list"]
    else:
        assert result == expected

@pytest.mark.parametrize(
    "initial, data, expected",
    [
        ([10, 20, 30], 20, 1),
        ([10, 20, 30], 40, -1),
    ],
)
def test_find(initial, data, expected):
    ll = build_list(initial)
    assert ll.find(data) == expected

@pytest.mark.parametrize(
    "initial, index, expected",
    [
        ([5, 6, 7], 1, 6),
    ],
)
def test_get_valid(initial, index, expected):
    ll = build_list(initial)
    assert ll.get(index) == expected

@pytest.mark.parametrize(
    "initial, index",
    [
        ([5, 6, 7], -1),
        ([5, 6, 7], 3),
    ],
)
def test_get_invalid(initial, index):
    ll = build_list(initial)
    with pytest.raises(IndexError):
        ll.get(index)

def test_to_list_empty():
    ll = build_list([])
    assert ll.to_list() == []

def test_len_after_operations():
    ll = build_list([1, 2, 3])
    assert len(ll) == 3