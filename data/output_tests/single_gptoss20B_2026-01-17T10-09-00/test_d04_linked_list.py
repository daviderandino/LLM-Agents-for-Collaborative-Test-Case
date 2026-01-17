import pytest
from data.input_code.d04_linked_list import LinkedList


def test_append_and_len():
    ll = LinkedList()
    assert len(ll) == 0
    ll.append(1)
    ll.append(2)
    ll.append(3)
    assert len(ll) == 3
    assert ll.to_list() == [1, 2, 3]
    assert ll.head.data == 1


def test_prepend_and_len():
    ll = LinkedList()
    ll.prepend(3)
    ll.prepend(2)
    ll.prepend(1)
    assert len(ll) == 3
    assert ll.to_list() == [1, 2, 3]
    assert ll.head.data == 1


def test_delete_head():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    assert ll.delete(1) is True
    assert ll.head.data == 2
    assert len(ll) == 2
    assert ll.to_list() == [2, 3]


def test_delete_middle():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    assert ll.delete(2) is True
    assert len(ll) == 2
    assert ll.to_list() == [1, 3]


def test_delete_tail():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    assert ll.delete(3) is True
    assert len(ll) == 2
    assert ll.to_list() == [1, 2]


def test_delete_nonexistent_and_empty():
    ll = LinkedList()
    assert ll.delete(5) is False  # empty list
    ll.append(1)
    assert ll.delete(5) is False  # element not present
    assert len(ll) == 1
    assert ll.to_list() == [1]


def test_find():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    ll.append(2)
    assert ll.find(2) == 1  # first occurrence
    assert ll.find(3) == 2
    assert ll.find(4) == -1


def test_get_valid_and_invalid():
    ll = LinkedList()
    ll.append(10)
    ll.append(20)
    ll.append(30)
    assert ll.get(0) == 10
    assert ll.get(1) == 20
    assert ll.get(2) == 30
    with pytest.raises(IndexError):
        ll.get(-1)
    with pytest.raises(IndexError):
        ll.get(3)


def test_to_list_empty_and_single():
    ll = LinkedList()
    assert ll.to_list() == []
    ll.append(42)
    assert ll.to_list() == [42]


def test_len_property_and_combination():
    ll = LinkedList()
    assert len(ll) == 0
    ll.append(1)
    assert len(ll) == 1
    ll.prepend(0)
    assert len(ll) == 2
    ll.append(2)
    assert len(ll) == 3
    assert ll.to_list() == [0, 1, 2]


def test_delete_all_elements():
    ll = LinkedList()
    for i in range(5):
        ll.append(i)
    for i in range(5):
        assert ll.delete(i) is True
    assert len(ll) == 0
    assert ll.head is None
    assert ll.to_list() == []


def test_duplicate_deletion_and_find():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(1)
    ll.append(3)
    # find should return first index
    assert ll.find(1) == 0
    # delete should remove first occurrence
    assert ll.delete(1) is True
    assert ll.to_list() == [2, 1, 3]
    # find again
    assert ll.find(1) == 1
    # delete second occurrence
    assert ll.delete(1) is True
    assert ll.to_list() == [2, 3]
    # delete remaining
    assert ll.delete(2) is True
    assert ll.delete(3) is True
    assert ll.to_list() == []
    assert len(ll) == 0
    assert ll.head is None