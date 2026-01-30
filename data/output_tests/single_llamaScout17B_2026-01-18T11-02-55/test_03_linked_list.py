import pytest
from data.input_code.03_linked_list import Node, LinkedList

def test_node_init():
    node = Node(1)
    assert node.data == 1
    assert node.next is None

def test_linked_list_init():
    linked_list = LinkedList()
    assert linked_list.head is None
    assert linked_list._size == 0

def test_append_empty_list():
    linked_list = LinkedList()
    linked_list.append(1)
    assert linked_list.head.data == 1
    assert linked_list._size == 1

def test_append_non_empty_list():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    assert linked_list.head.data == 1
    assert linked_list.head.next.data == 2
    assert linked_list._size == 2

def test_prepend_empty_list():
    linked_list = LinkedList()
    linked_list.prepend(1)
    assert linked_list.head.data == 1
    assert linked_list._size == 1

def test_prepend_non_empty_list():
    linked_list = LinkedList()
    linked_list.append(2)
    linked_list.prepend(1)
    assert linked_list.head.data == 1
    assert linked_list.head.next.data == 2
    assert linked_list._size == 2

def test_delete_head():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    assert linked_list.delete(1) == True
    assert linked_list.head.data == 2
    assert linked_list._size == 1

def test_delete_tail():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    assert linked_list.delete(2) == True
    assert linked_list.head.data == 1
    assert linked_list.head.next is None
    assert linked_list._size == 1

def test_delete_middle():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    linked_list.append(3)
    assert linked_list.delete(2) == True
    assert linked_list.head.data == 1
    assert linked_list.head.next.data == 3
    assert linked_list._size == 2

def test_delete_not_found():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    assert linked_list.delete(3) == False
    assert linked_list._size == 2

def test_delete_empty_list():
    linked_list = LinkedList()
    assert linked_list.delete(1) == False

def test_find_head():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    assert linked_list.find(1) == 0

def test_find_tail():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    assert linked_list.find(2) == 1

def test_find_middle():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    linked_list.append(3)
    assert linked_list.find(2) == 1

def test_find_not_found():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    assert linked_list.find(3) == -1

def test_find_empty_list():
    linked_list = LinkedList()
    assert linked_list.find(1) == -1

def test_get_head():
    linked_list = LinkedList()
    linked_list.append(1)
    assert linked_list.get(0) == 1

def test_get_tail():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    assert linked_list.get(1) == 2

def test_get_middle():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    linked_list.append(3)
    assert linked_list.get(1) == 2

def test_get_index_out_of_range():
    linked_list = LinkedList()
    linked_list.append(1)
    with pytest.raises(IndexError):
        linked_list.get(1)

def test_get_negative_index():
    linked_list = LinkedList()
    linked_list.append(1)
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
    linked_list.append(1)
    linked_list.append(2)
    assert len(linked_list) == 2

def test_len_empty():
    linked_list = LinkedList()
    assert len(linked_list) == 0