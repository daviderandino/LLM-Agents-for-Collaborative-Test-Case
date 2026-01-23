import pytest
from data.input_code.d04_linked_list import *

@pytest.fixture
def empty_list():
    """Provides a fresh empty LinkedList."""
    return LinkedList()

@pytest.fixture
def two_item_list():
    """Provides a LinkedList with elements [5, 10] appended in order."""
    lst = LinkedList()
    lst.append(5)
    lst.append(10)
    return lst

def test_init(empty_list):
    assert empty_list.head is None
    assert len(empty_list) == 0

@pytest.mark.parametrize(
    "data,expected_list",
    [
        (5, [5]),                # append to empty list
        (10, [5, 10]),           # append to non‑empty list (after previous append)
    ],
)
def test_append(empty_list, data, expected_list):
    # Build up the list step‑by‑step according to the parametrization order
    for value in expected_list:
        empty_list.append(value)
    assert empty_list.to_list() == expected_list
    assert len(empty_list) == len(expected_list)

@pytest.mark.parametrize(
    "data,expected_list",
    [
        (5, [5]),                # prepend to empty list
        (10, [10, 5]),           # prepend to non‑empty list (after previous prepend)
    ],
)
def test_prepend(empty_list, data, expected_list):
    # Prepend values in reverse order so that the final list matches expected_list
    for value in reversed(expected_list):
        empty_list.prepend(value)
    assert empty_list.to_list() == expected_list
    assert len(empty_list) == len(expected_list)

@pytest.mark.parametrize(
    "delete_value,expected_result,expected_list",
    [
        (5, True, [10]),   # delete head
        (10, True, [5]),   # delete tail
        (15, False, [5, 10]),  # delete non‑existent
    ],
)
def test_delete(delete_value, expected_result, expected_list):
    lst = LinkedList()
    lst.append(5)
    lst.append(10)
    result = lst.delete(delete_value)
    assert result is expected_result
    assert lst.to_list() == expected_list
    # size should match the resulting list length
    assert len(lst) == len(expected_list)

@pytest.mark.parametrize(
    "search_value,expected_index",
    [
        (5, 0),   # find head
        (10, 1),  # find tail
        (15, -1), # find non‑existent
    ],
)
def test_find(search_value, expected_index):
    lst = LinkedList()
    lst.append(5)
    lst.append(10)
    assert lst.find(search_value) == expected_index

@pytest.mark.parametrize(
    "index,expected",
    [
        (0, 5),   # get head
        (1, 10),  # get tail
    ],
)
def test_get_valid(index, expected):
    lst = LinkedList()
    lst.append(5)
    lst.append(10)
    assert lst.get(index) == expected

def test_get_out_of_range():
    lst = LinkedList()
    lst.append(5)
    lst.append(10)
    with pytest.raises(IndexError):
        lst.get(2)

def test_to_list_and_len():
    lst = LinkedList()
    lst.append(5)
    lst.append(10)
    assert lst.to_list() == [5, 10]
    assert len(lst) == 2

import pytest

@pytest.mark.parametrize(
    "initial_values,delete_value,expected_result,expected_list,expected_len",
    [
        ([5], 5, True, [], 0),          # delete head when list has one node
        ([], 5, False, [], 0),          # delete from empty list
    ],
)
def test_delete_edge_cases(initial_values, delete_value, expected_result, expected_list, expected_len):
    lst = LinkedList()
    for val in initial_values:
        lst.append(val)
    result = lst.delete(delete_value)
    assert result is expected_result
    assert lst.to_list() == expected_list
    assert len(lst) == expected_len


@pytest.mark.parametrize(
    "index,expected_exception",
    [
        (0, IndexError),   # get from empty list
    ],
)
def test_get_empty_list_raises(index, expected_exception):
    lst = LinkedList()
    with pytest.raises(expected_exception):
        lst.get(index)


def test_find_in_empty_list():
    lst = LinkedList()
    assert lst.find(5) == -1


def test_prepend_empty_list_updates_size():
    lst = LinkedList()
    lst.prepend(5)
    assert len(lst) == 1
    assert lst.head is not None
    assert lst.head.data == 5
    assert lst.to_list() == [5]


def test_append_empty_list_updates_size():
    lst = LinkedList()
    lst.append(5)
    assert len(lst) == 1
    assert lst.head is not None
    assert lst.head.data == 5
    assert lst.to_list() == [5]

import pytest

@pytest.mark.parametrize(
    "initial,delete_value,expected_result,expected_list",
    [
        ([5, 10], 10, True, [5]),   # delete tail node
        ([5], 15, False, [5]),      # delete non‑existent node from list with one node
    ],
)
def test_delete_additional_cases(initial, delete_value, expected_result, expected_list):
    lst = LinkedList()
    for v in initial:
        lst.append(v)
    result = lst.delete(delete_value)
    assert result is expected_result
    assert lst.to_list() == expected_list
    assert len(lst) == len(expected_list)


@pytest.mark.parametrize(
    "initial,index,expected",
    [
        ([5, 10], 0, 5),               # get head node
        ([5, 10], 1, 10),              # get tail node
        ([5, 10], -1, IndexError),     # get with negative index
    ],
)
def test_get_additional_cases(initial, index, expected):
    lst = LinkedList()
    for v in initial:
        lst.append(v)
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            lst.get(index)
    else:
        assert lst.get(index) == expected

def test_delete_from_empty_list_returns_false():
    lst = LinkedList()
    result = lst.delete(5)
    assert result is False
    assert lst.to_list() == []
    assert len(lst) == 0


def test_get_negative_index_empty_list_raises():
    lst = LinkedList()
    with pytest.raises(IndexError):
        lst.get(-1)


def test_prepend_then_delete_then_get_sequence():
    lst = LinkedList()
    lst.prepend(5)
    assert lst.to_list() == [5]
    assert len(lst) == 1

    delete_result = lst.delete(5)
    assert delete_result is True
    assert lst.to_list() == []
    assert len(lst) == 0

    with pytest.raises(IndexError):
        lst.get(0)


def test_delete_tail_then_delete_again():
    lst = LinkedList()
    lst.append(5)
    lst.append(10)

    first_delete = lst.delete(10)
    assert first_delete is True
    assert lst.to_list() == [5]
    assert len(lst) == 1

    second_delete = lst.delete(10)
    assert second_delete is False
    assert lst.to_list() == [5]
    assert len(lst) == 1

@pytest.mark.parametrize(
    "initial,delete_value,expected_result,expected_list,expected_len",
    [
        ([5], 5, True, [], 0),  # delete head when list has one node
    ],
)
def test_delete_head_single_node(initial, delete_value, expected_result, expected_list, expected_len):
    lst = LinkedList()
    for v in initial:
        lst.append(v)
    result = lst.delete(delete_value)
    assert result is expected_result
    assert lst.to_list() == expected_list
    assert len(lst) == expected_len


def test_get_negative_index_non_empty():
    lst = LinkedList()
    lst.append(5)
    lst.append(10)
    with pytest.raises(IndexError):
        lst.get(-1)


def test_prepend_delete_get_sequence():
    lst = LinkedList()
    lst.prepend(5)          # list: [5]
    lst.prepend(10)         # list: [10, 5]
    delete_result = lst.delete(5)
    assert delete_result is True
    # after deletion, list should be [10]
    assert lst.to_list() == [10]
    assert len(lst) == 1
    # get the remaining element
    assert lst.get(0) == 10


def test_delete_tail_then_prepend():
    lst = LinkedList()
    lst.append(5)
    lst.append(10)          # list: [5, 10]
    delete_result = lst.delete(10)
    assert delete_result is True
    assert lst.to_list() == [5]
    lst.prepend(20)         # list: [20, 5]
    assert lst.to_list() == [20, 5]
    assert len(lst) == 2
    assert lst.get(0) == 20
    assert lst.get(1) == 5


def test_find_head_node():
    lst = LinkedList()
    lst.append(5)
    lst.append(10)
    assert lst.find(5) == 0


def test_to_list_empty_after_delete():
    lst = LinkedList()
    lst.append(5)
    delete_result = lst.delete(5)
    assert delete_result is True
    assert lst.to_list() == []
    assert len(lst) == 0

import pytest

@pytest.mark.parametrize(
    "data,expected",
    [
        (5, False),  # Delete non-existent node from empty list
    ],
)
def test_delete_nonexistent_empty(empty_list, data, expected):
    result = empty_list.delete(data)
    assert result is expected
    assert empty_list.to_list() == []
    assert len(empty_list) == 0


def test_get_negative_index_single_node():
    lst = LinkedList()
    lst.append(5)  # single node list
    with pytest.raises(IndexError):
        lst.get(-1)


def test_prepend_delete_head_then_get():
    lst = LinkedList()
    lst.prepend(5)          # list becomes [5]
    delete_result = lst.delete(5)  # delete head
    assert delete_result is True
    assert lst.to_list() == []
    assert len(lst) == 0
    with pytest.raises(IndexError):
        lst.get(0)

@pytest.mark.parametrize(
    "initial,delete_value,expected_result,expected_list",
    [
        ([5, 10], 5, True, [10]),   # delete head from non‑empty list
        ([5, 10], 15, False, [5, 10]),  # delete non‑existent tail
    ],
)
def test_delete_various_cases(initial, delete_value, expected_result, expected_list):
    lst = LinkedList()
    for v in initial:
        lst.append(v)
    result = lst.delete(delete_value)
    assert result is expected_result
    assert lst.to_list() == expected_list
    assert len(lst) == len(expected_list)


@pytest.mark.parametrize(
    "initial,index,expected",
    [
        ([5, 10], 1, 10),  # get last index from non‑empty list
    ],
)
def test_get_last_index(initial, index, expected):
    lst = LinkedList()
    for v in initial:
        lst.append(v)
    assert lst.get(index) == expected


def test_prepend_delete_get_sequence_empty(empty_list):
    # prepend on empty list
    empty_list.prepend(5)
    assert empty_list.to_list() == [5]
    assert len(empty_list) == 1

    # delete the only element
    delete_result = empty_list.delete(5)
    assert delete_result is True
    assert empty_list.to_list() == []
    assert len(empty_list) == 0

    # subsequent get should raise IndexError
    with pytest.raises(IndexError):
        empty_list.get(0)


def test_delete_head_twice():
    lst = LinkedList()
    lst.append(5)  # list: [5]

    first_delete = lst.delete(5)
    assert first_delete is True
    assert lst.to_list() == []
    assert len(lst) == 0

    second_delete = lst.delete(5)
    assert second_delete is False
    assert lst.to_list() == []
    assert len(lst) == 0

def test_delete_head_twice_on_empty_list(empty_list):
    # First deletion attempt on empty list
    result1 = empty_list.delete(5)
    assert result1 is False
    # Second deletion attempt on still empty list
    result2 = empty_list.delete(5)
    assert result2 is False
    assert empty_list.to_list() == []
    assert len(empty_list) == 0


def test_get_index_zero_on_empty_list_raises(empty_list):
    with pytest.raises(IndexError):
        empty_list.get(0)


def test_prepend_delete_tail_get_sequence():
    lst = LinkedList()
    lst.prepend(5)   # list becomes [5]
    lst.prepend(10)  # list becomes [10, 5]
    # Delete the tail element (5)
    delete_result = lst.delete(5)
    assert delete_result is True
    assert lst.to_list() == [10]
    assert len(lst) == 1
    # Retrieve the remaining element
    assert lst.get(0) == 10


def test_delete_from_empty_list_returns_false(empty_list):
    result = empty_list.delete(10)  # any value; list is empty
    assert result is False
    assert empty_list.to_list() == []
    assert len(empty_list) == 0


def test_get_index_zero_after_deleting_single_node():
    lst = LinkedList()
    lst.append(5)          # list: [5]
    delete_result = lst.delete(5)
    assert delete_result is True
    with pytest.raises(IndexError):
        lst.get(0)

def test_delete_head_twice_on_single_node():
    lst = LinkedList()
    lst.append(5)            # list: [5]
    first = lst.delete(5)    # should delete head
    assert first is True
    second = lst.delete(5)   # second delete should fail
    assert second is False
    assert lst.to_list() == []
    assert len(lst) == 0


def test_get_negative_index_on_single_node():
    lst = LinkedList()
    lst.append(5)            # list: [5]
    with pytest.raises(IndexError):
        lst.get(-1)


def test_prepend_delete_get_on_single_node():
    lst = LinkedList()
    lst.append(10)           # start with [10]
    lst.prepend(5)           # list becomes [5, 10]
    delete_result = lst.delete(5)  # delete head (5)
    assert delete_result is True
    assert lst.to_list() == [10]
    assert lst.get(0) == 10
    assert len(lst) == 1


def test_delete_tail_on_single_node():
    lst = LinkedList()
    lst.append(5)            # list: [5]
    result = lst.delete(5)   # delete the only (tail) node
    assert result is True
    assert lst.to_list() == []
    assert len(lst) == 0

def test_delete_head_twice_on_single_node():
    lst = LinkedList()
    lst.append(5)
    # First deletion removes the head
    assert lst.delete(5) is True
    # Second deletion should fail because the list is now empty
    assert lst.delete(5) is False
    assert lst.to_list() == []
    assert len(lst) == 0


def test_get_negative_index_on_empty_list_raises(empty_list):
    with pytest.raises(IndexError):
        empty_list.get(-1)


def test_prepend_delete_tail_then_get_on_single_node():
    lst = LinkedList()
    lst.prepend(10)
    assert lst.to_list() == [10]
    # Delete the tail (which is also the head in this single‑node list)
    assert lst.delete(10) is True
    assert lst.to_list() == []
    # Subsequent get should raise IndexError
    with pytest.raises(IndexError):
        lst.get(0)


def test_delete_nonexistent_on_single_node():
    lst = LinkedList()
    lst.append(5)
    # Attempt to delete a value that does not exist
    assert lst.delete(15) is False
    assert lst.to_list() == [5]
    assert len(lst) == 1