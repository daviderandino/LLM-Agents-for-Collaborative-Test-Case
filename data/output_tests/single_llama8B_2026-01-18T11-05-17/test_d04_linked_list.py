import pytest
from data.input_code.d04_linked_list import Node, LinkedList

def test_node_init():
    node = Node(5)
    assert node.data == 5
    assert node.next is None

def test_linked_list_init():
    linked_list = LinkedList()
    assert linked_list.head is None
    assert linked_list._size == 0

def test_append():
    linked_list = LinkedList()
    linked_list.append(5)
    assert linked_list.head.data == 5
    assert linked_list._size == 1

def test_append_multiple():
    linked_list = LinkedList()
    linked_list.append(5)
    linked_list.append(10)
    linked_list.append(15)
    assert linked_list.head.data == 5
    assert linked_list.head.next.data == 10
    assert linked_list.head.next.next.data == 15
    assert linked_list._size == 3

def test_prepend():
    linked_list = LinkedList()
    linked_list.prepend(5)
    assert linked_list.head.data == 5
    assert linked_list._size == 1

def test_prepend_multiple():
    linked_list = LinkedList()
    linked_list.prepend(5)
    linked_list.prepend(10)
    linked_list.prepend(15)
    assert linked_list.head.data == 15
    assert linked_list.head.next.data == 10
    assert linked_list.head.next.next.data == 5
    assert linked_list._size == 3

def test_delete():
    linked_list = LinkedList()
    linked_list.append(5)
    linked_list.append(10)
    linked_list.append(15)
    assert linked_list.delete(10)
    assert linked_list.head.data == 5
    assert linked_list.head.next.data == 15
    assert linked_list._size == 2

def test_delete_not_found():
    linked_list = LinkedList()
    linked_list.append(5)
    linked_list.append(10)
    linked_list.append(15)
    assert not linked_list.delete(20)
    assert linked_list.head.data == 5
    assert linked_list.head.next.data == 10
    assert linked_list.head.next.next.data == 15
    assert linked_list._size == 3

def test_find():
    linked_list = LinkedList()
    linked_list.append(5)
    linked_list.append(10)
    linked_list.append(15)
    assert linked_list.find(10) == 1
    assert linked_list.find(20) == -1

def test_get():
    linked_list = LinkedList()
    linked_list.append(5)
    linked_list.append(10)
    linked_list.append(15)
    assert linked_list.get(1) == 10
    with pytest.raises(IndexError):
        linked_list.get(-1)

def test_get_out_of_range():
    linked_list = LinkedList()
    linked_list.append(5)
    linked_list.append(10)
    linked_list.append(15)
    with pytest.raises(IndexError):
        linked_list.get(3)

def test_to_list():
    linked_list = LinkedList()
    linked_list.append(5)
    linked_list.append(10)
    linked_list.append(15)
    assert linked_list.to_list() == [5, 10, 15]

def test_len():
    linked_list = LinkedList()
    linked_list.append(5)
    linked_list.append(10)
    linked_list.append(15)
    assert len(linked_list) == 3