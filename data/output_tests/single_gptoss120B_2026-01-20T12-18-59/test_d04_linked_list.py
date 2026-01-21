import pytest
from data.input_code.d04_linked_list import LinkedList, Node

def test_append_and_len_and_to_list():
    ll = LinkedList()
    # Append first element (head is None branch)
    ll.append(1)
    assert ll.head is not None
    assert ll.head.data == 1
    assert len(ll) == 1
    assert ll.to_list() == [1]
    # Append second element (head exists branch)
    ll.append(2)
    assert len(ll) == 2
    assert ll.to_list() == [1, 2]
    # Append None as data
    ll.append(None)
    assert len(ll) == 3
    assert ll.to_list() == [1, 2, None]

def test_prepend_and_len():
    ll = LinkedList()
    # Prepend into empty list
    ll.prepend('a')
    assert ll.head.data == 'a'
    assert len(ll) == 1
    assert ll.to_list() == ['a']
    # Prepend another element
    ll.prepend('b')
    assert ll.head.data == 'b'
    assert len(ll) == 2
    assert ll.to_list() == ['b', 'a']

def test_delete_head_and_empty():
    ll = LinkedList()
    # Delete from empty list returns False
    assert ll.delete(10) is False
    # Populate list
    ll.append(1)
    ll.append(2)
    ll.append(3)
    # Delete head
    assert ll.delete(1) is True
    assert ll.head.data == 2
    assert len(ll) == 2
    assert ll.to_list() == [2, 3]

def test_delete_middle_tail_and_not_found():
    ll = LinkedList()
    ll.append('x')
    ll.append('y')
    ll.append('z')
    # Delete middle element
    assert ll.delete('y') is True
    assert ll.to_list() == ['x', 'z']
    assert len(ll) == 2
    # Delete tail element
    assert ll.delete('z') is True
    assert ll.to_list() == ['x']
    assert len(ll) == 1
    # Attempt to delete non‑existent element
    assert ll.delete('not-there') is False
    assert ll.to_list() == ['x']
    assert len(ll) == 1

def test_find_various_data_and_not_found():
    ll = LinkedList()
    ll.append(None)
    ll.append("")
    ll.append("data")
    # Find each existing element
    assert ll.find(None) == 0
    assert ll.find("") == 1
    assert ll.find("data") == 2
    # Not found returns -1
    assert ll.find("missing") == -1

def test_get_valid_and_invalid_indices():
    ll = LinkedList()
    ll.append(10)
    ll.append(20)
    ll.append(30)
    # Valid indices
    assert ll.get(0) == 10
    assert ll.get(2) == 30
    # Negative index raises
    with pytest.raises(IndexError):
        ll.get(-1)
    # Index equal to size raises
    with pytest.raises(IndexError):
        ll.get(3)

def test_len_consistency_after_operations():
    ll = LinkedList()
    assert len(ll) == 0
    ll.append(1)
    ll.append(2)
    assert len(ll) == 2
    ll.prepend(0)
    assert len(ll) == 3
    ll.delete(2)
    assert len(ll) == 2
    ll.delete(0)
    ll.delete(1)
    assert len(ll) == 0
    # After all deletions, to_list should be empty
    assert ll.to_list() == []