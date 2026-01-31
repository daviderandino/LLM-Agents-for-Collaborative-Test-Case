import pytest
from data.input_code.d03_linked_list import LinkedList, Node

def test_node_init():
    node = Node(1)
    assert node.data == 1
    assert node.next is None

def test_linked_list_init():
    linked_list = LinkedList()
    assert linked_list.head is None
    assert linked_list._size == 0

def test_append():
    linked_list = LinkedList()
    linked_list.append(1)
    assert linked_list.head.data == 1
    assert linked_list._size == 1
    linked_list.append(2)
    assert linked_list.head.next.data == 2
    assert linked_list._size == 2

def test_prepend():
    linked_list = LinkedList()
    linked_list.prepend(1)
    assert linked_list.head.data == 1
    assert linked_list._size == 1
    linked_list.prepend(2)
    assert linked_list.head.data == 2
    assert linked_list.head.next.data == 1
    assert linked_list._size == 2

def test_delete():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    linked_list.append(3)
    assert linked_list.delete(2)
    assert linked_list.to_list() == [1, 3]
    assert linked_list._size == 2
    assert not linked_list.delete(4)
    assert linked_list.to_list() == [1, 3]
    assert linked_list._size == 2

def test_delete_head():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    linked_list.append(3)
    assert linked_list.delete(1)
    assert linked_list.to_list() == [2, 3]
    assert linked_list._size == 2

def test_delete_empty():
    linked_list = LinkedList()
    assert not linked_list.delete(1)
    assert linked_list.to_list() == []
    assert linked_list._size == 0

def test_find():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    linked_list.append(3)
    assert linked_list.find(2) == 1
    assert linked_list.find(4) == -1

def test_get():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    linked_list.append(3)
    assert linked_list.get(1) == 2
    with pytest.raises(IndexError):
        linked_list.get(3)
    with pytest.raises(IndexError):
        linked_list.get(-1)

def test_to_list():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    linked_list.append(3)
    assert linked_list.to_list() == [1, 2, 3]

def test_len():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    linked_list.append(3)
    assert len(linked_list) == 3