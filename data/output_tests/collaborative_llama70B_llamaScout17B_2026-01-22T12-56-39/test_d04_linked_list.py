import pytest
from data.input_code.d04_linked_list import *

def test_init():
    linked_list = LinkedList()
    assert linked_list.head is None
    assert len(linked_list) == 0

@pytest.mark.parametrize("data", [1, 2, 3])
def test_append(data):
    linked_list = LinkedList()
    linked_list.append(data)
    assert linked_list.find(data) != -1
    assert len(linked_list) == 1

def test_prepend():
    linked_list = LinkedList()
    linked_list.prepend(1)
    linked_list.prepend(0)
    assert linked_list.get(0) == 0
    assert len(linked_list) == 2

@pytest.mark.parametrize("data, expected", [
    (1, True),
    (2, True),
    (3, False)
])
def test_delete(data, expected):
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    assert linked_list.delete(data) == expected
    if expected:
        assert linked_list.find(data) == -1

@pytest.mark.parametrize("data, expected", [
    (1, 0),
    (2, 1),
    (3, -1)
])
def test_find(data, expected):
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    assert linked_list.find(data) == expected

@pytest.mark.parametrize("index, expected", [
    (0, 1),
    (1, 2)
])
def test_get(index, expected):
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    assert linked_list.get(index) == expected

def test_get_index_error():
    linked_list = LinkedList()
    linked_list.append(1)
    with pytest.raises(IndexError):
        linked_list.get(1)

@pytest.mark.parametrize("input_list, expected", [
    ([], []),
    ([1], [1]),
    ([1, 2], [1, 2])
])
def test_to_list(input_list, expected):
    linked_list = LinkedList()
    for data in input_list:
        linked_list.append(data)
    assert linked_list.to_list() == expected

def test_len():
    linked_list = LinkedList()
    assert len(linked_list) == 0
    linked_list.append(1)
    assert len(linked_list) == 1
    linked_list.append(2)
    assert len(linked_list) == 2

def test_prepend_empty():
    linked_list = LinkedList()
    linked_list.prepend(1)
    assert linked_list.get(0) == 1
    assert len(linked_list) == 1

@pytest.mark.parametrize("data, expected", [
    (1, True),
    (2, True),
    (3, False)
])
def test_delete_node(data, expected):
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    result = linked_list.delete(data)
    assert result == expected

def test_delete_head():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    assert linked_list.delete(1) == True
    assert linked_list.get(0) == 2

def test_delete_tail():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    assert linked_list.delete(2) == True
    assert len(linked_list) == 1

def test_delete_non_existent():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    assert linked_list.delete(3) == False

@pytest.mark.parametrize("index, expected", [
    (0, 1),
    (1, 2)
])
def test_get_node(index, expected):
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    assert linked_list.get(index) == expected

def test_get_head():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    assert linked_list.get(0) == 1

def test_get_tail():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    assert linked_list.get(1) == 2

@pytest.mark.parametrize("data, expected", [
    (1, 0),
    (2, 1),
    (3, -1)
])
def test_find_node(data, expected):
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    assert linked_list.find(data) == expected

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

def test_find_non_existent():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    assert linked_list.find(3) == -1

def test_delete_empty():
    linked_list = LinkedList()
    assert linked_list.delete(1) == False

def test_prepend_delete():
    linked_list = LinkedList()
    linked_list.prepend(0)
    linked_list.prepend(1)
    assert linked_list.delete(0) == True

def test_find_empty():
    linked_list = LinkedList()
    assert linked_list.find(1) == -1

def test_get_out_of_range_negative():
    linked_list = LinkedList()
    linked_list.append(1)
    with pytest.raises(IndexError):
        linked_list.get(-1)

def test_to_list_empty():
    linked_list = LinkedList()
    assert linked_list.to_list() == []

def test_delete_all_nodes():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    assert linked_list.delete(1) == True
    assert linked_list.delete(2) == True
    assert len(linked_list) == 0

def test_prepend_delete_prepended_node():
    linked_list = LinkedList()
    linked_list.prepend(0)
    linked_list.prepend(1)
    assert linked_list.delete(0) == True
    assert len(linked_list) == 1

def test_get_after_delete():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    linked_list.delete(1)
    assert linked_list.get(0) == 2

def test_find_after_delete():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    linked_list.delete(1)
    assert linked_list.find(2) == 0

def test_to_list_after_delete():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    linked_list.delete(1)
    assert linked_list.to_list() == [2]

def test_len_after_delete():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    linked_list.delete(1)
    assert len(linked_list) == 1

def test_delete_head_prepended():
    linked_list = LinkedList()
    linked_list.prepend(0)
    linked_list.append(1)
    assert linked_list.delete(0) == True
    assert len(linked_list) == 1

def test_delete_tail_prepended():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.prepend(0)
    assert linked_list.delete(0) == True
    assert len(linked_list) == 1

def test_prepend_delete_prepended():
    linked_list = LinkedList()
    linked_list.prepend(0)
    linked_list.prepend(1)
    linked_list.delete(1)
    assert len(linked_list) == 1

def test_get_after_prepend_delete():
    linked_list = LinkedList()
    linked_list.prepend(0)
    linked_list.prepend(1)
    linked_list.delete(0)
    assert linked_list.get(0) == 1

def test_find_after_prepend_delete():
    linked_list = LinkedList()
    linked_list.prepend(0)
    linked_list.prepend(1)
    linked_list.delete(0)
    assert linked_list.find(1) == 0

def test_to_list_after_prepend_delete():
    linked_list = LinkedList()
    linked_list.prepend(0)
    linked_list.prepend(1)
    linked_list.delete(0)
    assert linked_list.to_list() == [1]

def test_len_after_prepend_delete():
    linked_list = LinkedList()
    linked_list.prepend(0)
    linked_list.prepend(1)
    linked_list.delete(0)
    assert len(linked_list) == 1

def test_delete_middle():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    linked_list.append(3)
    assert linked_list.delete(2) == True
    assert len(linked_list) == 2

def test_prepend_delete_middle():
    linked_list = LinkedList()
    linked_list.prepend(1)
    linked_list.append(2)
    linked_list.append(3)
    assert linked_list.delete(2) == True
    assert len(linked_list) == 2

@pytest.mark.parametrize("index, expected", [
    (1, 3)
])
def test_get_after_delete_middle(index, expected):
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    linked_list.append(3)
    linked_list.delete(2)
    assert linked_list.get(index) == expected

@pytest.mark.parametrize("data, expected", [
    (3, 1)
])
def test_find_after_delete_middle(data, expected):
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    linked_list.append(3)
    linked_list.delete(2)
    assert linked_list.find(data) == expected

def test_to_list_after_delete_middle():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    linked_list.append(3)
    linked_list.delete(2)
    assert linked_list.to_list() == [1, 3]

def test_len_after_delete_middle():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    linked_list.append(3)
    linked_list.delete(2)
    assert len(linked_list) == 2