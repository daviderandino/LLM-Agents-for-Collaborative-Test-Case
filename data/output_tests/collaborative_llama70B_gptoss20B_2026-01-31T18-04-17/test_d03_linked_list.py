import pytest
from data.input_code.d03_linked_list import *

def build_list():
    """Helper to create a LinkedList with elements 0, 1, 2."""
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.prepend(0)
    return ll

def test_init():
    ll = LinkedList()
    assert ll.head is None
    assert len(ll) == 0

def test_append():
    ll = LinkedList()
    ll.append(1)
    assert ll.head.data == 1
    assert ll.head.next is None
    assert len(ll) == 1

def test_prepend():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.prepend(0)
    assert ll.head.data == 0
    assert ll.head.next.data == 1
    assert ll.head.next.next.data == 2
    assert len(ll) == 3

@pytest.mark.parametrize("data,expected", [
    (0, True),   # delete head
    (1, True),   # delete middle
    (2, True),   # delete tail
    (3, False),  # not found
])
def test_delete(data, expected):
    ll = build_list()
    result = ll.delete(data)
    assert result == expected
    # Verify size after deletion
    if expected:
        assert len(ll) == 2
    else:
        assert len(ll) == 3

@pytest.mark.parametrize("data,expected", [
    (0, 0),
    (1, 1),
    (2, 2),
    (3, -1),
])
def test_find(data, expected):
    ll = build_list()
    assert ll.find(data) == expected

@pytest.mark.parametrize("index,expected", [
    (0, 0),
    (1, 1),
    (2, 2),
])
def test_get(index, expected):
    ll = build_list()
    assert ll.get(index) == expected

def test_get_out_of_range():
    ll = build_list()
    with pytest.raises(IndexError):
        ll.get(3)

def test_to_list():
    ll = build_list()
    assert ll.to_list() == [0, 1, 2]

def test_len():
    ll = build_list()
    assert len(ll) == 3