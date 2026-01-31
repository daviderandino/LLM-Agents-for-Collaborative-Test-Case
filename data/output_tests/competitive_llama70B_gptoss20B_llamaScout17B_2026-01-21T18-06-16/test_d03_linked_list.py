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
    linked_list.prepend(1)
    linked_list.prepend(0)
    assert linked_list.get(0) == 0
    assert linked_list.get(1) == 1
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
        assert len(linked_list) == 1

@pytest.mark.parametrize("data, expected", [
    (0, 0),
    (1, 1),
    (2, -1)
])
def test_find(data, expected):
    linked_list = LinkedList()
    linked_list.append(0)
    linked_list.append(1)
    assert linked_list.find(data) == expected

@pytest.mark.parametrize("index, expected", [
    (0, 0),
    (1, 1),
    (2, IndexError)
])
def test_get(index, expected):
    linked_list = LinkedList()
    linked_list.append(0)
    linked_list.append(1)
    if expected == IndexError:
        with pytest.raises(IndexError):
            linked_list.get(index)
    else:
        assert linked_list.get(index) == expected

def test_to_list():
    linked_list = LinkedList()
    linked_list.append(0)
    linked_list.append(1)
    assert linked_list.to_list() == [0, 1]

def test_len():
    linked_list = LinkedList()
    linked_list.append(0)
    linked_list.append(1)
    assert len(linked_list) == 2

def test_prepend_empty():
    linked_list = LinkedList()
    linked_list.prepend(1)
    assert linked_list.get(0) == 1
    assert len(linked_list) == 1

def test_delete_head():
    linked_list = LinkedList()
    linked_list.append(1)
    assert linked_list.delete(1) is True
    assert len(linked_list) == 0

def test_delete_tail():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    assert linked_list.delete(2) is True
    assert len(linked_list) == 1
    assert linked_list.get(0) == 1

def test_delete_non_existent():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    assert linked_list.delete(3) is False
    assert len(linked_list) == 2

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

def test_to_list_empty():
    linked_list = LinkedList()
    assert linked_list.to_list() == []

def test_len_empty():
    linked_list = LinkedList()
    assert len(linked_list) == 0

import pytest
from data.input_code.d03_linked_list import LinkedList

def test_delete_empty():
    linked_list = LinkedList()
    assert linked_list.delete(1) is False

def test_prepend_multiple():
    linked_list = LinkedList()
    for d in [3, 2, 1]:
        linked_list.prepend(d)
    assert linked_list.to_list() == [1, 2, 3]

def test_append_multiple():
    linked_list = LinkedList()
    for d in [1, 2, 3]:
        linked_list.append(d)
    assert linked_list.to_list() == [1, 2, 3]

def test_find_empty():
    linked_list = LinkedList()
    assert linked_list.find(1) == -1

def test_get_negative_index():
    linked_list = LinkedList()
    with pytest.raises(IndexError):
        linked_list.get(-1)

def test_to_list_single():
    linked_list = LinkedList()
    linked_list.append(1)
    assert linked_list.to_list() == [1]

def test_len_single():
    linked_list = LinkedList()
    linked_list.append(1)
    assert len(linked_list) == 1