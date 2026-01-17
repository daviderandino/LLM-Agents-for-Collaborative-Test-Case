import pytest
from data.input_code.d04_linked_list import Node, LinkedList


def test_append_to_empty_list():
    ll = LinkedList()
    ll.append(10)
    assert ll.head.data == 10
    assert ll.head.next is None
    assert len(ll) == 1
    assert ll.to_list() == [10]


def test_append_multiple_elements():
    ll = LinkedList()
    for val in [1, 2, 3]:
        ll.append(val)
    assert ll.head.data == 1
    assert ll.head.next.data == 2
    assert ll.head.next.next.data == 3
    assert ll.head.next.next.next is None
    assert len(ll) == 3
    assert ll.to_list() == [1, 2, 3]


def test_prepend_to_empty_list():
    ll = LinkedList()
    ll.prepend(5)
    assert ll.head.data == 5
    assert ll.head.next is None
    assert len(ll) == 1
    assert ll.to_list() == [5]




def test_delete_head_single_element():
    ll = LinkedList()
    ll.append(42)
    assert ll.delete(42) is True
    assert ll.head is None
    assert len(ll) == 0
    assert ll.to_list() == []


def test_delete_head_multiple_elements():
    ll = LinkedList()
    for val in [10, 20, 30]:
        ll.append(val)
    assert ll.delete(10) is True
    assert ll.head.data == 20
    assert len(ll) == 2
    assert ll.to_list() == [20, 30]


def test_delete_middle_element():
    ll = LinkedList()
    for val in [1, 2, 3, 4]:
        ll.append(val)
    assert ll.delete(3) is True
    assert ll.to_list() == [1, 2, 4]
    assert len(ll) == 3


def test_delete_tail_element():
    ll = LinkedList()
    for val in [7, 8, 9]:
        ll.append(val)
    assert ll.delete(9) is True
    assert ll.to_list() == [7, 8]
    assert len(ll) == 2


def test_delete_not_found():
    ll = LinkedList()
    for val in [5, 6, 7]:
        ll.append(val)
    assert ll.delete(10) is False
    assert ll.to_list() == [5, 6, 7]
    assert len(ll) == 3


def test_delete_on_empty_list():
    ll = LinkedList()
    assert ll.delete(1) is False
    assert len(ll) == 0
    assert ll.to_list() == []


def test_find_in_empty_list():
    ll = LinkedList()
    assert ll.find(99) == -1


def test_find_present_elements():
    ll = LinkedList()
    for val in [4, 5, 6]:
        ll.append(val)
    assert ll.find(4) == 0
    assert ll.find(5) == 1
    assert ll.find(6) == 2


def test_find_not_present():
    ll = LinkedList()
    for val in [1, 2, 3]:
        ll.append(val)
    assert ll.find(99) == -1


def test_get_valid_indices():
    ll = LinkedList()
    for val in [10, 20, 30]:
        ll.append(val)
    assert ll.get(0) == 10
    assert ll.get(1) == 20
    assert ll.get(2) == 30


def test_get_invalid_negative_index():
    ll = LinkedList()
    ll.append(1)
    with pytest.raises(IndexError):
        ll.get(-1)


def test_get_invalid_out_of_range_index():
    ll = LinkedList()
    ll.append(1)
    with pytest.raises(IndexError):
        ll.get(1)  # size is 1, valid indices are 0


def test_to_list_output():
    ll = LinkedList()
    for val in [9, 8, 7]:
        ll.append(val)
    assert ll.to_list() == [9, 8, 7]


def test_len_property():
    ll = LinkedList()
    assert len(ll) == 0
    ll.append(1)
    assert len(ll) == 1
    ll.prepend(2)
    assert len(ll) == 2
    ll.delete(1)
    assert len(ll) == 1


def test_append_and_prepend_none_data():
    ll = LinkedList()
    ll.append(None)
    ll.prepend(None)
    assert ll.to_list() == [None, None]
    assert len(ll) == 2
    assert ll.find(None) == 0
    assert ll.delete(None) is True
    assert ll.to_list() == [None]
    assert len(ll) == 1
    assert ll.delete(None) is True
    assert ll.to_list() == []
    assert len(ll) == 0


def test_multiple_occurrences_deletion():
    ll = LinkedList()
    for val in [1, 2, 2, 3]:
        ll.append(val)
    assert ll.delete(2) is True
    assert ll.to_list() == [1, 2, 3]
    assert ll.find(2) == 1
    assert len(ll) == 3


def test_get_after_deletion():
    ll = LinkedList()
    for val in [5, 6, 7]:
        ll.append(val)
    ll.delete(6)
    assert ll.get(0) == 5
    assert ll.get(1) == 7
    with pytest.raises(IndexError):
        ll.get(2)


def test_get_after_deletion_of_only_element():
    ll = LinkedList()
    ll.append(42)
    ll.delete(42)
    assert ll.head is None
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.get(0)
    assert ll.to_list() == []


def test_delete_on_empty_list_returns_false():
    ll = LinkedList()
    assert ll.delete(10) is False
    assert len(ll) == 0
    assert ll.head is None
    assert ll.to_list() == []


def test_find_after_deletion_of_first_occurrence():
    ll = LinkedList()
    for val in [1, 2, 3, 2]:
        ll.append(val)
    ll.delete(2)
    assert ll.find(2) == 2  # second occurrence now at index 2
    assert ll.to_list() == [1, 3, 2]
    assert len(ll) == 3
    assert ll.get(2) == 2
    with pytest.raises(IndexError):
        ll.get(3)