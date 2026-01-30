import pytest
from data.input_code.03_linked_list import LinkedList, Node

def test_append_empty():
    linked_list = LinkedList()
    linked_list.append(1)
    assert linked_list._size == 1
    assert linked_list.to_list() == [1]

def test_append_nonempty():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    assert linked_list._size == 2
    assert linked_list.to_list() == [1, 2]

def test_prepend_empty():
    linked_list = LinkedList()
    linked_list.prepend('a')
    assert linked_list._size == 1
    assert linked_list.to_list() == ['a']

def test_prepend_nonempty():
    linked_list = LinkedList()
    linked_list.prepend('a')
    linked_list.prepend('b')
    assert linked_list._size == 2
    assert linked_list.to_list() == ['b', 'a']

def test_delete_empty():
    linked_list = LinkedList()
    assert linked_list.delete(1) is False

def test_delete_head():
    linked_list = LinkedList()
    linked_list.append('b')
    assert linked_list.delete('b') is True
    assert linked_list._size == 0
    assert linked_list.to_list() == []

def test_delete_middle():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    linked_list.append(3)
    assert linked_list.delete(2) is True
    assert linked_list._size == 2
    assert linked_list.to_list() == [1, 3]

def test_delete_notfound():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    assert linked_list.delete(4) is False
    assert linked_list._size == 2
    assert linked_list.to_list() == [1, 2]

def test_find_head():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    assert linked_list.find(1) == 0

def test_find_middle():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    linked_list.append(3)
    assert linked_list.find(2) == 1

def test_find_notfound():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    assert linked_list.find(4) == -1

def test_get_valid():
    linked_list = LinkedList()
    linked_list.append(10)
    linked_list.append(20)
    assert linked_list.get(1) == 20

def test_get_negative():
    linked_list = LinkedList()
    linked_list.append(10)
    linked_list.append(20)
    with pytest.raises(IndexError):
        linked_list.get(-1)

def test_get_outofrange():
    linked_list = LinkedList()
    linked_list.append(10)
    linked_list.append(20)
    with pytest.raises(IndexError):
        linked_list.get(2)

def test_to_list_empty():
    linked_list = LinkedList()
    assert linked_list.to_list() == []

def test_to_list_nonempty():
    linked_list = LinkedList()
    linked_list.append(5)
    assert linked_list.to_list() == [5]

def test_len_check():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    linked_list.append(3)
    assert len(linked_list) == 3