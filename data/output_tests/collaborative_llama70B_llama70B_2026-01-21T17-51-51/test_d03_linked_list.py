import pytest
from data.input_code.d03_linked_list import LinkedList, Node

def setup_append(data):
    linked_list = LinkedList()
    linked_list.append(data)
    return linked_list

def setup_prepend(data):
    linked_list = LinkedList()
    linked_list.prepend(data)
    return linked_list

@pytest.mark.parametrize('data, expected', [
    (1, None)
])
def test_init(data, expected):
    linked_list = LinkedList()
    assert linked_list.head is None
    assert linked_list._size == 0

@pytest.mark.parametrize('data, expected', [
    (1, None)
])
def test_append(data, expected):
    linked_list = LinkedList()
    linked_list.append(data)
    assert linked_list.head.data == data
    assert linked_list._size == 1

def test_append_multi():
    linked_list = setup_append(1)
    linked_list.append(2)
    assert linked_list.head.data == 1
    assert linked_list.head.next.data == 2
    assert linked_list._size == 2

@pytest.mark.parametrize('data, expected', [
    (0, None)
])
def test_prepend(data, expected):
    linked_list = LinkedList()
    linked_list.prepend(data)
    assert linked_list.head.data == data
    assert linked_list._size == 1

def test_prepend_multi():
    linked_list = setup_append(1)
    linked_list.prepend(0)
    assert linked_list.head.data == 0
    assert linked_list.head.next.data == 1
    assert linked_list._size == 2

def test_delete():
    linked_list = setup_append(1)
    assert linked_list.delete(1) is True
    assert linked_list.head is None
    assert linked_list._size == 0

def test_delete_not_found():
    linked_list = setup_append(1)
    assert linked_list.delete(2) is False
    assert linked_list.head.data == 1
    assert linked_list._size == 1

def test_find():
    linked_list = setup_append(1)
    assert linked_list.find(1) == 0

def test_find_not_found():
    linked_list = setup_append(1)
    assert linked_list.find(2) == -1

def test_get():
    linked_list = setup_append(1)
    assert linked_list.get(0) == 1

def test_get_out_of_range():
    linked_list = setup_append(1)
    with pytest.raises(IndexError):
        linked_list.get(1)

def test_to_list():
    linked_list = setup_append(1)
    assert linked_list.to_list() == [1]

def test_len():
    linked_list = setup_append(1)
    assert len(linked_list) == 1

def test_delete_empty():
    linked_list = LinkedList()
    assert linked_list.delete(1) is False
    assert linked_list.head is None
    assert linked_list._size == 0

def test_prepend_multi_data():
    linked_list = LinkedList()
    linked_list.prepend(1)
    linked_list.prepend(2.0)
    linked_list.prepend("string")
    assert linked_list.head.data == "string"
    assert linked_list.head.next.data == 2.0
    assert linked_list.head.next.next.data == 1
    assert linked_list._size == 3

def test_append_multi_data():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2.0)
    linked_list.append("string")
    assert linked_list.head.data == 1
    assert linked_list.head.next.data == 2.0
    assert linked_list.head.next.next.data == "string"
    assert linked_list._size == 3

def test_find_multi_data():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2.0)
    linked_list.append("string")
    assert linked_list.find("string") == 2

def test_get_negative_index():
    linked_list = LinkedList()
    linked_list.append(1)
    with pytest.raises(IndexError):
        linked_list.get(-1)

def test_to_list_multi_data():
    linked_list = LinkedList()
    linked_list.append("string")
    linked_list.append(1)
    linked_list.append(2.0)
    assert linked_list.to_list() == ["string", 1, 2.0]

def test_len_empty():
    linked_list = LinkedList()
    assert len(linked_list) == 0

def setup_delete_head_multi():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    linked_list.append(3)
    return linked_list

def setup_delete_tail():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    linked_list.append(3)
    return linked_list

def setup_delete_middle():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    linked_list.append(3)
    return linked_list

def setup_get_last_index():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    linked_list.append(3)
    return linked_list

def setup_find_multi_data_head():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2.0)
    linked_list.append('string')
    return linked_list

def setup_find_multi_data_tail():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2.0)
    linked_list.append('string')
    return linked_list

def setup_prepend_delete():
    linked_list = LinkedList()
    linked_list.prepend(1)
    return linked_list

def setup_append_prepend_delete():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.prepend(0)
    return linked_list

@pytest.mark.parametrize('linked_list, data, expected', [
    (setup_delete_head_multi(), 1, True),
])
def test_delete_head_multi(linked_list, data, expected):
    assert linked_list.delete(data) == expected
    assert linked_list.head.data == 2
    assert linked_list._size == 2

@pytest.mark.parametrize('linked_list, data, expected', [
    (setup_delete_tail(), 3, True),
])
def test_delete_tail(linked_list, data, expected):
    assert linked_list.delete(data) == expected
    assert linked_list.head.data == 1
    assert linked_list.head.next.data == 2
    assert linked_list._size == 2

@pytest.mark.parametrize('linked_list, data, expected', [
    (setup_delete_middle(), 2, True),
])
def test_delete_middle(linked_list, data, expected):
    assert linked_list.delete(data) == expected
    assert linked_list.head.data == 1
    assert linked_list.head.next.data == 3
    assert linked_list._size == 2

@pytest.mark.parametrize('linked_list, index, expected', [
    (setup_get_last_index(), 2, 3),
])
def test_get_last_index(linked_list, index, expected):
    assert linked_list.get(index) == expected

@pytest.mark.parametrize('linked_list, data, expected', [
    (setup_find_multi_data_head(), 1, 0),
])
def test_find_multi_data_head(linked_list, data, expected):
    assert linked_list.find(data) == expected

@pytest.mark.parametrize('linked_list, data, expected', [
    (setup_find_multi_data_tail(), 'string', 2),
])
def test_find_multi_data_tail(linked_list, data, expected):
    assert linked_list.find(data) == expected

@pytest.mark.parametrize('linked_list, data, expected', [
    (setup_prepend_delete(), 1, True),
])
def test_prepend_delete(linked_list, data, expected):
    assert linked_list.delete(data) == expected
    assert linked_list.head is None
    assert linked_list._size == 0

@pytest.mark.parametrize('linked_list, data, expected', [
    (setup_append_prepend_delete(), 1, True),
])
def test_append_prepend_delete(linked_list, data, expected):
    assert linked_list.delete(data) == expected
    assert linked_list.head.data == 0
    assert linked_list._size == 1