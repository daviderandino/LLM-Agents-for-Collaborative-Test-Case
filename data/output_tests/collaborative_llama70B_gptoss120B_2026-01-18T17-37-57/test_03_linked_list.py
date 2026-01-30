import pytest
from data.input_code.03_linked_list import *

def build_linked_list(values):
    """Utility to create a LinkedList populated with the given iterable of values."""
    ll = LinkedList()
    for v in values:
        ll.append(v)
    return ll

def test_linkedlist_init():
    ll = LinkedList()
    assert ll.head is None
    assert len(ll) == 0

def test_node_init():
    node = Node(10)
    assert node.data == 10
    assert node.next is None

@pytest.mark.parametrize(
    "initial, new_data, expected_list, expected_len",
    [
        ([], 10, [10], 1),                     # append to empty list
        ([10], 20, [10, 20], 2),               # append to non‑empty list
    ],
)
def test_append(initial, new_data, expected_list, expected_len):
    ll = build_linked_list(initial)
    ll.append(new_data)
    assert ll.to_list() == expected_list
    assert len(ll) == expected_len

@pytest.mark.parametrize(
    "initial, new_data, expected_list, expected_len",
    [
        ([], 10, [10], 1),                     # prepend to empty list
        ([10], 20, [20, 10], 2),               # prepend to non‑empty list
    ],
)
def test_prepend(initial, new_data, expected_list, expected_len):
    ll = build_linked_list(initial)
    ll.prepend(new_data)
    assert ll.to_list() == expected_list
    assert len(ll) == expected_len

@pytest.mark.parametrize(
    "setup_vals, del_val, expected_result, expected_list, expected_len",
    [
        ([10], 10, True, [], 0),                         # delete head (single element)
        ([10, 20], 20, True, [10], 1),                   # delete tail
        ([10, 20, 30], 20, True, [10, 30], 2),           # delete middle
        ([10, 20, 30], 40, False, [10, 20, 30], 3),      # delete non‑existent
    ],
)
def test_delete(setup_vals, del_val, expected_result, expected_list, expected_len):
    ll = build_linked_list(setup_vals)
    result = ll.delete(del_val)
    assert result is expected_result
    assert ll.to_list() == expected_list
    assert len(ll) == expected_len

@pytest.mark.parametrize(
    "setup_vals, find_val, expected_index",
    [
        ([10], 10, 0),                     # find head
        ([10, 20], 20, 1),                 # find tail
        ([10, 20, 30], 20, 1),             # find middle
        ([10, 20, 30], 40, -1),            # not found
    ],
)
def test_find(setup_vals, find_val, expected_index):
    ll = build_linked_list(setup_vals)
    assert ll.find(find_val) == expected_index

@pytest.mark.parametrize(
    "setup_vals, index, expected_value",
    [
        ([10], 0, 10),                     # get head
        ([10, 20], 1, 20),                 # get tail
        ([10, 20, 30], 1, 20),             # get middle
    ],
)
def test_get_success(setup_vals, index, expected_value):
    ll = build_linked_list(setup_vals)
    assert ll.get(index) == expected_value

def test_get_out_of_range():
    ll = build_linked_list([10, 20, 30])
    with pytest.raises(IndexError):
        ll.get(10)

def test_to_list():
    ll = build_linked_list([10, 20, 30])
    assert ll.to_list() == [10, 20, 30]

def test_len():
    ll = build_linked_list([10, 20, 30])
    assert len(ll) == 3

import pytest
from data.input_code.03_linked_list import *

def test_get_negative_index_raises():
    ll = LinkedList()
    ll.append(1)
    with pytest.raises(IndexError):
        ll.get(-1)

def test_delete_from_empty_returns_false():
    ll = LinkedList()
    result = ll.delete(10)
    assert result is False
    assert ll.to_list() == []
    assert len(ll) == 0

def test_prepend_to_empty_updates_size():
    ll = LinkedList()
    result = ll.prepend(10)
    assert result is None
    assert ll.to_list() == [10]
    assert len(ll) == 1

def test_find_in_empty_returns_minus_one():
    ll = LinkedList()
    assert ll.find(10) == -1

def test_to_list_empty_returns_empty_list():
    ll = LinkedList()
    assert ll.to_list() == []