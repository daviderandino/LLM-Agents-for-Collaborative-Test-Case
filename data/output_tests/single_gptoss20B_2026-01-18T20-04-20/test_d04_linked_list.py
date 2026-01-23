import pytest
from data.input_code.d04_linked_list import LinkedList


def test_append_empty_and_nonempty():
    ll = LinkedList()
    # Append to empty list
    ll.append(1)
    assert ll.head.data == 1
    assert ll._size == 1
    assert ll.to_list() == [1]
    # Append to non-empty list
    ll.append(2)
    assert ll.head.data == 1
    assert ll.head.next.data == 2
    assert ll._size == 2
    assert ll.to_list() == [1, 2]


def test_prepend():
    ll = LinkedList()
    ll.prepend(1)
    assert ll.head.data == 1
    assert ll._size == 1
    assert ll.to_list() == [1]
    ll.prepend(2)
    assert ll.head.data == 2
    assert ll.head.next.data == 1
    assert ll._size == 2
    assert ll.to_list() == [2, 1]


def test_delete_empty():
    ll = LinkedList()
    assert ll.delete(1) is False
    assert ll._size == 0
    assert ll.head is None


def test_delete_head():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    assert ll.delete(1) is True
    assert ll.head.data == 2
    assert ll._size == 2
    assert ll.to_list() == [2, 3]


def test_delete_middle():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    assert ll.delete(2) is True
    assert ll.head.data == 1
    assert ll.head.next.data == 3
    assert ll._size == 2
    assert ll.to_list() == [1, 3]


def test_delete_tail():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    assert ll.delete(3) is True
    assert ll.head.data == 1
    assert ll.head.next.data == 2
    assert ll._size == 2
    assert ll.to_list() == [1, 2]


def test_delete_not_found():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    assert ll.delete(4) is False
    assert ll._size == 3
    assert ll.to_list() == [1, 2, 3]


def test_delete_single_element():
    ll = LinkedList()
    ll.append(1)
    assert ll.delete(1) is True
    assert ll.head is None
    assert ll._size == 0
    assert ll.to_list() == []


def test_find():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    assert ll.find(1) == 0
    assert ll.find(2) == 1
    assert ll.find(3) == 2
    assert ll.find(4) == -1


def test_get_valid():
    ll = LinkedList()
    ll.append(10)
    ll.append(20)
    ll.append(30)
    assert ll.get(0) == 10
    assert ll.get(1) == 20
    assert ll.get(2) == 30


def test_get_invalid():
    ll = LinkedList()
    ll.append(10)
    ll.append(20)
    with pytest.raises(IndexError):
        ll.get(-1)
    with pytest.raises(IndexError):
        ll.get(2)  # size is 2, valid indices 0 and 1


def test_to_list_empty():
    ll = LinkedList()
    assert ll.to_list() == []


def test_len():
    ll = LinkedList()
    assert len(ll) == 0
    ll.append(1)
    assert len(ll) == 1
    ll.prepend(2)
    assert len(ll) == 2
    ll.delete(1)
    assert len(ll) == 1


def test_none_data():
    ll = LinkedList()
    ll.append(None)
    ll.prepend(None)
    assert ll.to_list() == [None, None]
    assert ll.find(None) == 0
    assert ll.get(0) is None
    assert ll.delete(None) is True
    assert ll.to_list() == [None]
    assert ll.find(None) == 0
    assert ll.delete(None) is True
    assert ll.to_list() == []


def test_boundary_values():
    ll = LinkedList()
    ll.append(5)
    assert ll.get(0) == 5
    with pytest.raises(IndexError):
        ll.get(1)
    ll.append(6)
    assert ll.get(1) == 6
    with pytest.raises(IndexError):
        ll.get(2)


def test_delete_all_and_reuse():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    assert ll.delete(1) is True
    assert ll.delete(2) is True
    assert ll.delete(3) is True
    assert ll.head is None
    assert ll._size == 0
    assert ll.to_list() == []
    # Reuse after empty
    ll.append(7)
    assert ll.to_list() == [7]
    assert ll._size == 1


def test_get_after_delete():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    ll.delete(2)
    assert ll.get(0) == 1
    assert ll.get(1) == 3
    with pytest.raises(IndexError):
        ll.get(2)


def test_find_after_delete():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    ll.delete(2)
    assert ll.find(2) == -1
    assert ll.find(1) == 0
    assert ll.find(3) == 1


def test_delete_head_and_tail():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    ll.delete(1)
    ll.delete(3)
    assert ll.to_list() == [2]
    assert ll._size == 1