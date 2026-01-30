import pytest
from data.input_code.03_linked_list import *

def _make_linked_list(values):
    """Utility to create a LinkedList with the given iterable of values using append."""
    ll = LinkedList()
    for v in values:
        ll.append(v)
    return ll

def test_node_initialization():
    node = Node(10)
    assert node.data == 10
    assert node.next is None

def test_linkedlist_initialization():
    ll = LinkedList()
    assert ll.head is None
    assert ll._size == 0  # internal size should start at 0

def test_append_and_len_and_to_list():
    ll = LinkedList()
    ll.append(10)
    ll.append(20)
    ll.append(30)
    assert len(ll) == 3
    assert ll.to_list() == [10, 20, 30]

def test_prepend_and_order():
    ll = LinkedList()
    ll.prepend(30)
    ll.prepend(20)
    ll.prepend(10)
    assert len(ll) == 3
    assert ll.to_list() == [10, 20, 30]

@pytest.mark.parametrize(
    "initial, delete_val, expected_result, expected_len, expected_list",
    [
        ([10, 20, 30], 10, True, 2, [20, 30]),   # delete head
        ([10, 20, 30], 20, True, 2, [10, 30]),   # delete middle
        ([10, 20, 30], 30, True, 2, [10, 20]),   # delete tail
        ([10, 20, 30], 40, False, 3, [10, 20, 30]),  # not found
        ([], 10, False, 0, []),                 # delete from empty list
    ],
)
def test_delete(initial, delete_val, expected_result, expected_len, expected_list):
    ll = _make_linked_list(initial)
    result = ll.delete(delete_val)
    assert result is expected_result
    assert len(ll) == expected_len
    assert ll.to_list() == expected_list

@pytest.mark.parametrize(
    "initial, find_val, expected_index",
    [
        ([10, 20, 30], 10, 0),   # head
        ([10, 20, 30], 20, 1),   # middle
        ([10, 20, 30], 30, 2),   # tail
        ([10, 20, 30], 40, -1),  # not present
        ([], 10, -1),            # empty list
    ],
)
def test_find(initial, find_val, expected_index):
    ll = _make_linked_list(initial)
    assert ll.find(find_val) == expected_index

@pytest.mark.parametrize(
    "initial, index, expected_value",
    [
        ([10, 20, 30], 0, 10),
        ([10, 20, 30], 1, 20),
        ([10, 20, 30], 2, 30),
    ],
)
def test_get_valid_index(initial, index, expected_value):
    ll = _make_linked_list(initial)
    assert ll.get(index) == expected_value

@pytest.mark.parametrize(
    "initial, index",
    [
        ([10, 20, 30], -1),
        ([10, 20, 30], 3),
        ([], 0),
    ],
)
def test_get_invalid_index_raises(initial, index):
    ll = _make_linked_list(initial)
    with pytest.raises(IndexError):
        ll.get(index)

def test_len_property():
    ll = LinkedList()
    assert len(ll) == 0
    ll.append(10)
    assert len(ll) == 1
    ll.prepend(5)
    assert len(ll) == 2