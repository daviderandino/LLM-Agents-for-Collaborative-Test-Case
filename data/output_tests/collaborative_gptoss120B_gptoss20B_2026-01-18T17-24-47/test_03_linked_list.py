import pytest
from data.input_code.03_linked_list import *

@pytest.fixture
def empty_list():
    return LinkedList()

@pytest.fixture
def list_one():
    ll = LinkedList()
    ll.append(1)
    return ll

@pytest.fixture
def list_two():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    return ll

@pytest.fixture
def list_three():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    return ll

def _tail_data(ll: LinkedList):
    cur = ll.head
    while cur and cur.next:
        cur = cur.next
    return cur.data if cur else None

# T1: Append to empty list
def test_append_empty(empty_list):
    empty_list.append(1)
    assert empty_list.head.data == 1
    assert empty_list._size == 1

# T2: Append to non‑empty list
def test_append_non_empty(list_one):
    list_one.append(2)
    assert _tail_data(list_one) == 2
    assert list_one._size == 2

# T3: Prepend to empty list
def test_prepend_empty(empty_list):
    empty_list.prepend(10)
    assert empty_list.head.data == 10
    assert empty_list._size == 1

# T4: Prepend to non‑empty list
def test_prepend_non_empty(list_one):
    list_one.prepend(20)
    assert list_one.head.data == 20
    assert list_one.head.next.data == 1
    assert list_one._size == 2

# T5: Delete on empty list returns False
def test_delete_empty(empty_list):
    assert empty_list.delete(5) is False

# T6: Delete non‑existent element returns False
def test_delete_nonexistent(list_two):
    assert list_two.delete(99) is False

# T7: Find existing element returns correct index
def test_find_existing(list_two):
    assert list_two.find(2) == 1

# T8: Find non‑existent element returns -1
def test_find_nonexistent(list_two):
    assert list_two.find(4) == -1

# T9: Get valid index returns element data
def test_get_valid(list_one):
    assert list_one.get(0) == 1

# T10: Get negative index raises IndexError
def test_get_negative_index(list_one):
    with pytest.raises(IndexError):
        list_one.get(-1)

# T11: Get out‑of‑range index raises IndexError
def test_get_out_of_range(list_one):
    with pytest.raises(IndexError):
        list_one.get(3)

# T12: to_list on empty list returns empty list
def test_to_list_empty(empty_list):
    assert empty_list.to_list() == []

# T13: to_list on non‑empty list returns correct sequence
def test_to_list_non_empty(list_three):
    assert list_three.to_list() == [1, 2, 3]

# T14: len on empty list returns 0
def test_len_empty(empty_list):
    assert len(empty_list) == 0

# T15: len on non‑empty list returns correct size
def test_len_non_empty(list_three):
    assert len(list_three) == 3

import pytest
from data.input_code.03_linked_list import *

def test_delete_head_single(list_one):
    # Delete the only element in the list
    assert list_one.delete(1) is True
    assert list_one.head is None
    assert len(list_one) == 0

def test_delete_head_multi(list_two):
    # Delete the head when multiple elements exist
    assert list_two.delete(1) is True
    assert list_two.head.data == 2
    assert len(list_two) == 1

def test_delete_middle(list_three):
    # Delete a middle element (value 2) from a three‑element list
    assert list_three.delete(2) is True
    assert list_three.to_list() == [1, 3]
    assert len(list_three) == 2

def test_delete_tail_two(list_two):
    # Delete the tail element from a two‑element list
    assert list_two.delete(2) is True
    assert list_two.to_list() == [1]
    assert len(list_two) == 1

def test_delete_tail_three(list_three):
    # Delete the tail element from a three‑element list
    assert list_three.delete(3) is True
    assert list_three.to_list() == [1, 2]
    assert len(list_three) == 2

def test_get_last(list_three):
    # Retrieve the last element (index 2) from a three‑element list
    assert list_three.get(2) == 3

def test_get_middle(list_three):
    # Retrieve the middle element (index 1) from a three‑element list
    assert list_three.get(1) == 2

def test_get_empty(empty_list):
    # Attempt to get any element from an empty list should raise IndexError
    with pytest.raises(IndexError):
        empty_list.get(0)