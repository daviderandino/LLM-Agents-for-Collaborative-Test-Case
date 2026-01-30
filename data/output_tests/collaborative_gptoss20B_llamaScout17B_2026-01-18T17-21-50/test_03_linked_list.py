import pytest
from data.input_code.03_linked_list import *

@pytest.mark.parametrize("data, expected", [
    (10, None),
    (20, None)
])
def test_append(data, expected):
    linked_list = LinkedList()
    linked_list.append(data)
    if expected is None:
        assert len(linked_list) == 1
    else:
        assert False

def test_prepend():
    linked_list = LinkedList()
    linked_list.prepend(5)
    assert len(linked_list) == 1
    assert linked_list.get(0) == 5

@pytest.mark.parametrize("data, expected", [
    (1, True),  # delete existing node
    (3, False),  # delete non-existing node
])
def test_delete(data, expected):
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    assert linked_list.delete(data) == expected

@pytest.mark.parametrize("data, expected", [
    (2, 1),
    (5, -1)
])
def test_find(data, expected):
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    assert linked_list.find(data) == expected

@pytest.mark.parametrize("index, expected", [
    (0, 1),
    (1, 2),
    (-1, "IndexError"),
    (2, "IndexError")
])
def test_get(index, expected):
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    if expected == "IndexError":
        with pytest.raises(IndexError):
            linked_list.get(index)
    else:
        assert linked_list.get(index) == expected

@pytest.mark.parametrize("expected", [
    [],
    [1, 2]
])
def test_to_list(expected):
    linked_list = LinkedList()
    if expected:
        linked_list.append(1)
        linked_list.append(2)
    assert linked_list.to_list() == expected

def test_len():
    linked_list = LinkedList()
    assert len(linked_list) == 0
    linked_list.append(1)
    linked_list.append(2)
    assert len(linked_list) == 2

@pytest.mark.parametrize("input_data, expected", [
    ([1, 2, 3], [1, 2, 3])
])
def test_append_multiple(input_data, expected):
    linked_list = LinkedList()
    for data in input_data:
        linked_list.append(data)
    assert linked_list.to_list() == expected

@pytest.mark.parametrize("input_data, expected", [
    ([1, 2, 3], [3, 2, 1])
])
def test_prepend_multiple(input_data, expected):
    linked_list = LinkedList()
    for data in input_data:
        linked_list.prepend(data)
    assert linked_list.to_list() == expected

def test_delete_middle_return():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    linked_list.append(3)
    assert linked_list.delete(2) == True

def test_delete_middle_len():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    linked_list.append(3)
    linked_list.delete(2)
    assert len(linked_list) == 2

def test_delete_last_return():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    assert linked_list.delete(2) == True

def test_delete_last_len():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    linked_list.delete(2)
    assert len(linked_list) == 1

def test_delete_head_multiple_return():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    linked_list.append(3)
    assert linked_list.delete(1) == True

def test_delete_head_multiple_len():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    linked_list.append(3)
    linked_list.delete(1)
    assert len(linked_list) == 2

def test_delete_empty():
    linked_list = LinkedList()
    assert linked_list.delete(1) == False

def test_find_empty():
    linked_list = LinkedList()
    assert linked_list.find(1) == -1

def test_find_first():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    assert linked_list.find(1) == 0

def test_get_after_prepend_nonempty():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    linked_list.prepend(5)
    assert linked_list.get(0) == 5

@pytest.mark.parametrize("index, expected", [
    (1, "IndexError")
])
def test_get_index_out_of_range_after_delete(index, expected):
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    linked_list.delete(1)
    if expected == "IndexError":
        with pytest.raises(IndexError):
            linked_list.get(index)