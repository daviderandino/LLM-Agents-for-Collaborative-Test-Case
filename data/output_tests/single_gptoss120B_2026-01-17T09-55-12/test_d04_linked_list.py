import pytest
from data.input_code.d04_linked_list import LinkedList

def test_append_len_to_list_and_get():
    ll = LinkedList()
    # Append elements
    ll.append(1)
    ll.append(2)
    ll.append(3)
    # Verify length
    assert len(ll) == 3
    # Verify order via to_list
    assert ll.to_list() == [1, 2, 3]
    # Verify get by index
    assert ll.get(0) == 1
    assert ll.get(1) == 2
    assert ll.get(2) == 3

def test_prepend_order_and_find():
    ll = LinkedList()
    ll.prepend('a')
    ll.prepend('b')
    ll.prepend('c')
    # List should be ['c', 'b', 'a']
    assert ll.to_list() == ['c', 'b', 'a']
    assert len(ll) == 3
    # Find indices
    assert ll.find('c') == 0
    assert ll.find('b') == 1
    assert ll.find('a') == 2
    # Not found
    assert ll.find('z') == -1

def test_delete_various_cases():
    ll = LinkedList()
    # Populate list
    for val in [1, 2, 3, 4]:
        ll.append(val)
    # Delete head
    assert ll.delete(1) is True
    assert ll.to_list() == [2, 3, 4]
    assert len(ll) == 3
    # Delete middle element
    assert ll.delete(3) is True
    assert ll.to_list() == [2, 4]
    assert len(ll) == 2
    # Delete tail element
    assert ll.delete(4) is True
    assert ll.to_list() == [2]
    assert len(ll) == 1
    # Attempt to delete non‑existent element
    assert ll.delete(99) is False
    assert ll.to_list() == [2]
    # Delete remaining element
    assert ll.delete(2) is True
    assert ll.to_list() == []
    assert len(ll) == 0
    # Delete from empty list
    assert ll.delete(1) is False

def test_find_get_edge_cases():
    ll = LinkedList()
    for val in [10, 20, 30]:
        ll.append(val)
    # Valid finds
    assert ll.find(10) == 0
    assert ll.find(20) == 1
    assert ll.find(30) == 2
    # Invalid find
    assert ll.find(40) == -1
    # Valid gets
    assert ll.get(0) == 10
    assert ll.get(2) == 30
    # Out of range gets
    with pytest.raises(IndexError):
        ll.get(-1)
    with pytest.raises(IndexError):
        ll.get(3)  # size is 3, valid indices are 0‑2