import pytest
from data.input_code.d04_linked_list import *

def test_linked_list_init():
    linked_list = LinkedList()
    assert linked_list.head is None
    assert len(linked_list) == 0

@pytest.mark.parametrize('data', [5, 10, 15])
def test_linked_list_append(data):
    linked_list = LinkedList()
    linked_list.append(data)
    assert linked_list.to_list() == [data]

def test_linked_list_append_multiple():
    linked_list = LinkedList()
    linked_list.append(5)
    linked_list.append(10)
    assert linked_list.to_list() == [5, 10]

def test_linked_list_prepend():
    linked_list = LinkedList()
    linked_list.append(5)
    linked_list.prepend(15)
    assert linked_list.to_list() == [15, 5]

@pytest.mark.parametrize('data, expected', [(15, True), (10, True), (20, False)])
def test_linked_list_delete(data, expected):
    linked_list = LinkedList()
    linked_list.append(5)
    linked_list.append(10)
    linked_list.prepend(15)
    assert linked_list.delete(data) == expected

@pytest.mark.parametrize('data, expected', [(5, 0), (10, 1), (20, -1)])
def test_linked_list_find(data, expected):
    linked_list = LinkedList()
    linked_list.append(5)
    linked_list.append(10)
    assert linked_list.find(data) == expected

@pytest.mark.parametrize('index, expected', [(0, 5), (1, 10)])
def test_linked_list_get(index, expected):
    linked_list = LinkedList()
    linked_list.append(5)
    linked_list.append(10)
    assert linked_list.get(index) == expected

def test_linked_list_get_out_of_range():
    linked_list = LinkedList()
    linked_list.append(5)
    linked_list.append(10)
    with pytest.raises(IndexError):
        linked_list.get(2)

def test_linked_list_to_list():
    linked_list = LinkedList()
    linked_list.append(5)
    linked_list.append(10)
    assert linked_list.to_list() == [5, 10]

def test_linked_list_len():
    linked_list = LinkedList()
    linked_list.append(5)
    linked_list.append(10)
    assert len(linked_list) == 2

import pytest
from data.input_code.d04_linked_list import LinkedList

def test_linked_list_delete_head():
    linked_list = LinkedList()
    linked_list.append(5)
    linked_list.append(10)
    assert linked_list.delete(5) is True

def test_linked_list_delete_tail():
    linked_list = LinkedList()
    linked_list.append(5)
    linked_list.append(10)
    assert linked_list.delete(10) is True

def test_linked_list_delete_non_existent():
    linked_list = LinkedList()
    linked_list.append(5)
    linked_list.append(10)
    assert linked_list.delete(20) is False

def test_linked_list_delete_empty_list():
    linked_list = LinkedList()
    assert linked_list.delete(5) is False

def test_linked_list_get_zero_index():
    linked_list = LinkedList()
    linked_list.append(5)
    linked_list.append(10)
    assert linked_list.get(0) == 5

def test_linked_list_get_last_index():
    linked_list = LinkedList()
    linked_list.append(5)
    linked_list.append(10)
    assert linked_list.get(1) == 10

def test_linked_list_get_empty_list():
    linked_list = LinkedList()
    with pytest.raises(IndexError):
        linked_list.get(0)

def test_linked_list_find_head():
    linked_list = LinkedList()
    linked_list.prepend(15)
    linked_list.append(5)
    linked_list.append(10)
    assert linked_list.find(15) == 0

def test_linked_list_find_tail():
    linked_list = LinkedList()
    linked_list.append(5)
    linked_list.append(10)
    assert linked_list.find(10) == 1

def test_linked_list_find_empty_list():
    linked_list = LinkedList()
    assert linked_list.find(5) == -1