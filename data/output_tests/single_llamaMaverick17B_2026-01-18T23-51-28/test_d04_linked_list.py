import pytest
from data.input_code.d04_linked_list import LinkedList, Node

def test_node_init():
    node = Node("data")
    assert node.data == "data"
    assert node.next is None

def test_linked_list_init():
    linked_list = LinkedList()
    assert linked_list.head is None
    assert len(linked_list) == 0

def test_append():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    assert linked_list.to_list() == [1, 2]
    assert len(linked_list) == 2

def test_prepend():
    linked_list = LinkedList()
    linked_list.prepend(1)
    linked_list.prepend(2)
    assert linked_list.to_list() == [2, 1]
    assert len(linked_list) == 2

def test_delete():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    linked_list.append(3)
    assert linked_list.delete(2) is True
    assert linked_list.to_list() == [1, 3]
    assert len(linked_list) == 2
    assert linked_list.delete(4) is False
    assert linked_list.to_list() == [1, 3]

def test_delete_head():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    assert linked_list.delete(1) is True
    assert linked_list.to_list() == [2]
    assert len(linked_list) == 1

def test_delete_empty_list():
    linked_list = LinkedList()
    assert linked_list.delete(1) is False

def test_find():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    linked_list.append(3)
    assert linked_list.find(2) == 1
    assert linked_list.find(4) == -1

def test_find_empty_list():
    linked_list = LinkedList()
    assert linked_list.find(1) == -1

def test_get():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    linked_list.append(3)
    assert linked_list.get(1) == 2

def test_get_out_of_range():
    linked_list = LinkedList()
    linked_list.append(1)
    with pytest.raises(IndexError):
        linked_list.get(1)
    with pytest.raises(IndexError):
        linked_list.get(-1)

def test_to_list():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    assert linked_list.to_list() == [1, 2]

def test_to_list_empty():
    linked_list = LinkedList()
    assert linked_list.to_list() == []

def test_len():
    linked_list = LinkedList()
    assert len(linked_list) == 0
    linked_list.append(1)
    assert len(linked_list) == 1