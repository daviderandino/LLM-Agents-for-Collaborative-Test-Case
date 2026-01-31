import pytest
from data.input_code.d03_linked_list import LinkedList, Node

@pytest.mark.parametrize('data, expected_list, expected_size', [
    (10, [10], 1)
])
def test_append_empty(data, expected_list, expected_size):
    linked_list = LinkedList()
    linked_list.append(data)
    assert linked_list.to_list() == expected_list
    assert len(linked_list) == expected_size

@pytest.mark.parametrize('setup, data, expected_list, expected_size', [
    ([5], 15, [5, 15], 2)
])
def test_append_nonempty(setup, data, expected_list, expected_size):
    linked_list = LinkedList()
    for item in setup:
        linked_list.append(item)
    linked_list.append(data)
    assert linked_list.to_list() == expected_list
    assert len(linked_list) == expected_size

@pytest.mark.parametrize('data, expected_list, expected_size', [
    (20, [20], 1)
])
def test_prepend_empty(data, expected_list, expected_size):
    linked_list = LinkedList()
    linked_list.prepend(data)
    assert linked_list.to_list() == expected_list
    assert len(linked_list) == expected_size

@pytest.mark.parametrize('setup, data, expected_list, expected_size', [
    ([30], 25, [25, 30], 2)
])
def test_prepend_nonempty(setup, data, expected_list, expected_size):
    linked_list = LinkedList()
    for item in setup:
        linked_list.append(item)
    linked_list.prepend(data)
    assert linked_list.to_list() == expected_list
    assert len(linked_list) == expected_size

@pytest.mark.parametrize('setup, data, expected_result, expected_list, expected_size', [
    ([1, 2, 3], 1, True, [2, 3], 2)
])
def test_delete_head(setup, data, expected_result, expected_list, expected_size):
    linked_list = LinkedList()
    for item in setup:
        linked_list.append(item)
    result = linked_list.delete(data)
    assert result == expected_result
    assert linked_list.to_list() == expected_list
    assert len(linked_list) == expected_size

@pytest.mark.parametrize('setup, data, expected_result, expected_list, expected_size', [
    ([4, 5, 6], 5, True, [4, 6], 2)
])
def test_delete_middle(setup, data, expected_result, expected_list, expected_size):
    linked_list = LinkedList()
    for item in setup:
        linked_list.append(item)
    result = linked_list.delete(data)
    assert result == expected_result
    assert linked_list.to_list() == expected_list
    assert len(linked_list) == expected_size

@pytest.mark.parametrize('setup, data, expected_result, expected_list, expected_size', [
    ([7, 8], 9, False, [7, 8], 2)
])
def test_delete_notfound(setup, data, expected_result, expected_list, expected_size):
    linked_list = LinkedList()
    for item in setup:
        linked_list.append(item)
    result = linked_list.delete(data)
    assert result == expected_result
    assert linked_list.to_list() == expected_list
    assert len(linked_list) == expected_size

def test_delete_empty():
    linked_list = LinkedList()
    result = linked_list.delete(10)
    assert result == False
    assert linked_list.to_list() == []
    assert len(linked_list) == 0

@pytest.mark.parametrize('setup, data, expected_index', [
    ([11, 12, 13], 12, 1)
])
def test_find_existing(setup, data, expected_index):
    linked_list = LinkedList()
    for item in setup:
        linked_list.append(item)
    index = linked_list.find(data)
    assert index == expected_index

@pytest.mark.parametrize('setup, data, expected_index', [
    ([14, 15], 16, -1)
])
def test_find_notfound(setup, data, expected_index):
    linked_list = LinkedList()
    for item in setup:
        linked_list.append(item)
    index = linked_list.find(data)
    assert index == expected_index

@pytest.mark.parametrize('setup, index, expected_data', [
    ([17, 18, 19], 1, 18)
])
def test_get_valid(setup, index, expected_data):
    linked_list = LinkedList()
    for item in setup:
        linked_list.append(item)
    data = linked_list.get(index)
    assert data == expected_data

@pytest.mark.parametrize('setup, index', [
    ([20, 21], -1),
    ([22, 23], 2)
])
def test_get_invalid(setup, index):
    linked_list = LinkedList()
    for item in setup:
        linked_list.append(item)
    with pytest.raises(IndexError):
        linked_list.get(index)

def test_to_list_empty():
    linked_list = LinkedList()
    result = linked_list.to_list()
    assert result == []

@pytest.mark.parametrize('setup, expected_length', [
    ([24, 25, 26], 3)
])
def test_len(setup, expected_length):
    linked_list = LinkedList()
    for item in setup:
        linked_list.append(item)
    length = len(linked_list)
    assert length == expected_length