import pytest
from data.input_code.d03_linked_list import *


@pytest.fixture
def empty_list():
    """Provide a fresh empty LinkedList for each test."""
    return LinkedList()


def test_append_to_empty(empty_list):
    empty_list.append(5)
    assert empty_list.head is not None
    assert empty_list.head.data == 5
    assert len(empty_list) == 1


def test_append_to_non_empty(empty_list):
    empty_list.append(5)
    empty_list.append(10)
    # verify tail node
    current = empty_list.head
    while current.next:
        current = current.next
    assert current.data == 10
    assert len(empty_list) == 2


def test_prepend_to_empty(empty_list):
    empty_list.prepend(15)
    assert empty_list.head is not None
    assert empty_list.head.data == 15
    assert len(empty_list) == 1


def test_prepend_to_non_empty(empty_list):
    empty_list.prepend(15)
    empty_list.prepend(20)
    assert empty_list.head.data == 20
    assert empty_list.head.next.data == 15
    assert len(empty_list) == 2


@pytest.mark.parametrize(
    "initial, delete_val, expected_result, expected_len",
    [
        ([5, 10], 5, True, 1),          # delete head
        ([5, 10, 15], 10, True, 2),     # delete middle
        ([5, 10], 25, False, 2),        # delete non‑existent
    ],
)
def test_delete(initial, delete_val, expected_result, expected_len):
    ll = LinkedList()
    for v in initial:
        ll.append(v)
    result = ll.delete(delete_val)
    assert result is expected_result
    assert len(ll) == expected_len


@pytest.mark.parametrize(
    "initial, find_val, expected_index",
    [
        ([15, 10, 25], 15, 0),   # head node
        ([15, 10, 25], 10, 1),   # middle node
        ([15, 10, 25], 25, 2),   # tail node
        ([15, 10, 25], 99, -1),  # not found
    ],
)
def test_find(initial, find_val, expected_index):
    ll = LinkedList()
    for v in initial:
        ll.append(v)
    assert ll.find(find_val) == expected_index


@pytest.mark.parametrize(
    "setup_ops, index, expected",
    [
        (["prepend 15", "prepend 20"], 0, 20),
        (["prepend 15", "prepend 20"], 1, 15),
    ],
)
def test_get_success(setup_ops, index, expected):
    ll = LinkedList()
    for op in setup_ops:
        action, val = op.split()
        if action == "append":
            ll.append(int(val))
        else:  # prepend
            ll.prepend(int(val))
    assert ll.get(index) == expected


@pytest.mark.parametrize(
    "setup_ops, index, exc",
    [
        (["prepend 15", "prepend 20"], -1, IndexError),
        (["prepend 15", "prepend 20"], 10, IndexError),
    ],
)
def test_get_errors(setup_ops, index, exc):
    ll = LinkedList()
    for op in setup_ops:
        action, val = op.split()
        if action == "append":
            ll.append(int(val))
        else:
            ll.prepend(int(val))
    with pytest.raises(exc):
        ll.get(index)


def test_to_list_and_len():
    ll = LinkedList()
    ll.prepend(15)
    ll.prepend(20)  # list is now [20, 15]
    assert ll.to_list() == [20, 15]
    assert len(ll) == 2