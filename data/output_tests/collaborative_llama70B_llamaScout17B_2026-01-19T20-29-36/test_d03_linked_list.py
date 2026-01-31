import pytest
from data.input_code.d03_linked_list import *

def test_init():
    linked_list = LinkedList()
    assert linked_list.head is None
    assert len(linked_list) == 0

@pytest.mark.parametrize("data", [1, 2, 3])
def test_append(data):
    linked_list = LinkedList()
    linked_list.append(data)
    assert linked_list.get(0) == data
    assert len(linked_list) == 1

def test_prepend():
    linked_list = LinkedList()
    linked_list.prepend(0)
    assert linked_list.get(0) == 0
    assert len(linked_list) == 1

@pytest.mark.parametrize("data, expected_index", [(0, 0), (1, 1), (2, 2)])
def test_find(data, expected_index):
    linked_list = LinkedList()
    linked_list.append(0)
    linked_list.append(1)
    linked_list.append(2)
    assert linked_list.find(data) == expected_index

@pytest.mark.parametrize("data, expected", [(0, True), (2, True), (3, False)])
def test_delete(data, expected):
    linked_list = LinkedList()
    linked_list.append(0)
    linked_list.append(1)
    linked_list.append(2)
    assert linked_list.delete(data) == expected

@pytest.mark.parametrize("index, expected", [(0, 0), (1, 1), (2, 2)])
def test_get(index, expected):
    linked_list = LinkedList()
    linked_list.append(0)
    linked_list.append(1)
    linked_list.append(2)
    assert linked_list.get(index) == expected

def test_get_out_of_range():
    linked_list = LinkedList()
    linked_list.append(0)
    linked_list.append(1)
    linked_list.append(2)
    with pytest.raises(IndexError):
        linked_list.get(3)

def test_to_list():
    linked_list = LinkedList()
    linked_list.append(0)
    linked_list.append(1)
    linked_list.append(2)
    assert linked_list.to_list() == [0, 1, 2]

def test_len():
    linked_list = LinkedList()
    linked_list.append(0)
    linked_list.append(1)
    linked_list.append(2)
    assert len(linked_list) == 3

@pytest.mark.parametrize("data", [1, 2, 3])
def test_prepend_multiple(data):
    linked_list = LinkedList()
    linked_list.prepend(0)
    linked_list.prepend(data)
    assert linked_list.get(0) == data
    assert len(linked_list) == 2

def test_delete_head():
    linked_list = LinkedList()
    linked_list.append(0)
    linked_list.append(1)
    assert linked_list.delete(0) == True
    assert linked_list.get(0) == 1

def test_delete_tail():
    linked_list = LinkedList()
    linked_list.append(0)
    linked_list.append(1)
    assert linked_list.delete(1) == True
    assert len(linked_list) == 1

def test_delete_not_found():
    linked_list = LinkedList()
    linked_list.append(0)
    linked_list.append(1)
    assert linked_list.delete(2) == False
    assert len(linked_list) == 2

def test_find_not_found():
    linked_list = LinkedList()
    linked_list.append(0)
    linked_list.append(1)
    assert linked_list.find(2) == -1

def test_get_negative_index():
    linked_list = LinkedList()
    linked_list.append(0)
    with pytest.raises(IndexError):
        linked_list.get(-1)

def test_to_list_empty():
    linked_list = LinkedList()
    assert linked_list.to_list() == []

def test_to_list_single_element():
    linked_list = LinkedList()
    linked_list.append(0)
    assert linked_list.to_list() == [0]

def test_prepend_empty():
    linked_list = LinkedList()
    linked_list.prepend(None)
    assert linked_list.get(0) is None
    assert len(linked_list) == 1

def test_delete_empty():
    linked_list = LinkedList()
    assert linked_list.delete(None) == False
    assert len(linked_list) == 0

def test_find_empty():
    linked_list = LinkedList()
    assert linked_list.find(None) == -1

def test_get_max_index_empty():
    linked_list = LinkedList()
    with pytest.raises(IndexError):
        linked_list.get(0)

def test_append_none():
    linked_list = LinkedList()
    linked_list.append(None)
    assert linked_list.get(0) is None
    assert len(linked_list) == 1

@pytest.mark.parametrize("data", [None, 1, 2, 3])
def test_prepend_multiple_none(data):
    linked_list = LinkedList()
    linked_list.prepend(None)
    linked_list.prepend(data)
    if data is None:
        assert linked_list.get(0) is None
    else:
        assert linked_list.get(0) == data
    assert len(linked_list) == 2

def test_delete_multiple():
    linked_list = LinkedList()
    linked_list.append(0)
    linked_list.append(0)
    linked_list.append(1)
    assert linked_list.delete(0) == True
    assert linked_list.get(0) == 0
    assert len(linked_list) == 2

def test_find_multiple():
    linked_list = LinkedList()
    linked_list.append(0)
    linked_list.append(0)
    linked_list.append(1)
    assert linked_list.find(0) == 0