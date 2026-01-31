import pytest
from data.input_code.d03_linked_list import Node, LinkedList


def test_node_initialization():
    node = Node(10)
    assert node.data == 10
    assert node.next is None


def test_append_to_empty_list():
    ll = LinkedList()
    ll.append(1)
    assert ll.head.data == 1
    assert ll.head.next is None
    assert len(ll) == 1
    assert ll.to_list() == [1]


def test_append_to_non_empty_list():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    assert ll.head.data == 1
    assert ll.head.next.data == 2
    assert ll.head.next.next is None
    assert len(ll) == 2
    assert ll.to_list() == [1, 2]


def test_prepend_to_empty_list():
    ll = LinkedList()
    ll.prepend(1)
    assert ll.head.data == 1
    assert ll.head.next is None
    assert len(ll) == 1
    assert ll.to_list() == [1]


def test_prepend_to_non_empty_list():
    ll = LinkedList()
    ll.append(1)
    ll.prepend(2)
    assert ll.head.data == 2
    assert ll.head.next.data == 1
    assert len(ll) == 2
    assert ll.to_list() == [2, 1]


def test_delete_from_empty_list():
    ll = LinkedList()
    assert ll.delete(1) is False
    assert len(ll) == 0
    assert ll.head is None


def test_delete_head():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    assert ll.delete(1) is True
    assert ll.head.data == 2
    assert len(ll) == 1
    assert ll.to_list() == [2]


def test_delete_middle():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    assert ll.delete(2) is True
    assert ll.head.data == 1
    assert ll.head.next.data == 3
    assert ll.head.next.next is None
    assert len(ll) == 2
    assert ll.to_list() == [1, 3]


def test_delete_last():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    assert ll.delete(2) is True
    assert ll.head.data == 1
    assert ll.head.next is None
    assert len(ll) == 1
    assert ll.to_list() == [1]


def test_delete_not_found():
    ll = LinkedList()
    ll.append(1)
    assert ll.delete(2) is False
    assert len(ll) == 1
    assert ll.to_list() == [1]


def test_find_head():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    assert ll.find(1) == 0


def test_find_middle():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    assert ll.find(2) == 1


def test_find_not_found():
    ll = LinkedList()
    ll.append(1)
    assert ll.find(2) == -1


def test_get_valid_indices():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    assert ll.get(0) == 1
    assert ll.get(1) == 2
    assert ll.get(2) == 3


def test_get_negative_index():
    ll = LinkedList()
    ll.append(1)
    with pytest.raises(IndexError):
        ll.get(-1)


def test_get_out_of_range_index():
    ll = LinkedList()
    ll.append(1)
    with pytest.raises(IndexError):
        ll.get(1)  # size is 1, valid indices are 0


def test_to_list_empty():
    ll = LinkedList()
    assert ll.to_list() == []


def test_to_list_non_empty():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    assert ll.to_list() == [1, 2]


def test_len_property():
    ll = LinkedList()
    assert len(ll) == 0
    ll.append(1)
    ll.append(2)
    assert len(ll) == 2


def test_delete_single_element():
    ll = LinkedList()
    ll.append(1)
    assert ll.delete(1) is True
    assert len(ll) == 0
    assert ll.head is None


def test_delete_single_element_not_found():
    ll = LinkedList()
    ll.append(1)
    assert ll.delete(2) is False
    assert len(ll) == 1
    assert ll.head.data == 1


def test_delete_last_element():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    assert ll.delete(2) is True
    assert len(ll) == 1
    assert ll.head.data == 1
    assert ll.head.next is None


def test_delete_head_and_middle_and_last():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    assert ll.delete(1) is True
    assert ll.delete(3) is True
    assert len(ll) == 1
    assert ll.to_list() == [2]


def test_delete_head_and_middle_and_last_all():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    assert ll.delete(1) is True
    assert ll.delete(2) is True
    assert ll.delete(3) is True
    assert len(ll) == 0
    assert ll.head is None


def test_get_index_equals_size_raises():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    with pytest.raises(IndexError):
        ll.get(2)  # size is 2, valid indices are 0 and 1


def test_find_multiple_occurrences():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(1)
    assert ll.find(1) == 0  # first occurrence


def test_append_multiple_and_verify():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    assert ll.to_list() == [1, 2, 3]
    assert len(ll) == 3


def test_prepend_multiple_and_verify():
    ll = LinkedList()
    ll.prepend(3)
    ll.prepend(2)
    ll.prepend(1)
    assert ll.to_list() == [1, 2, 3]
    assert len(ll) == 3


def test_delete_middle_of_three():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    assert ll.delete(2) is True
    assert ll.to_list() == [1, 3]
    assert len(ll) == 2


def test_delete_head_of_three():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    assert ll.delete(1) is True
    assert ll.to_list() == [2, 3]
    assert len(ll) == 2


def test_delete_last_of_three():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    assert ll.delete(3) is True
    assert ll.to_list() == [1, 2]
    assert len(ll) == 2


def test_get_middle_of_three():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    assert ll.get(1) == 2


def test_find_last():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    assert ll.find(3) == 2


def test_find_first_of_multiple():
    ll = LinkedList()
    ll.append(1)
    ll.append(1)
    ll.append(2)
    assert ll.find(1) == 0


def test_delete_nonexistent_after_deletes():
    ll = LinkedList()
    ll.append(1)
    assert ll.delete(1) is True
    assert ll.delete(1) is False


def test_delete_head_when_only_one():
    ll = LinkedList()
    ll.append(1)
    assert ll.delete(1) is True
    assert ll.head is None


def test_delete_head_when_multiple():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    assert ll.delete(1) is True
    assert ll.head.data == 2


def test_delete_middle_when_multiple():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    assert ll.delete(2) is True
    assert ll.head.data == 1
    assert ll.head.next.data == 3


def test_delete_last_when_multiple():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    assert ll.delete(3) is True
    assert ll.head.data == 1
    assert ll.head.next.data == 2


def test_get_first():
    ll = LinkedList()
    ll.append(1)
    assert ll.get(0) == 1


def test_get_last():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    assert ll.get(1) == 2


def test_get_out_of_range():
    ll = LinkedList()
    ll.append(1)
    with pytest.raises(IndexError):
        ll.get(2)


def test_find_not_found_again():
    ll = LinkedList()
    ll.append(1)
    assert ll.find(2) == -1


def test_to_list_after_deletes():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.delete(1)
    assert ll.to_list() == [2]


def test_to_list_after_prepend():
    ll = LinkedList()
    ll.prepend(2)
    ll.prepend(1)
    assert ll.to_list() == [1, 2]


def test_to_list_after_append():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    assert ll.to_list() == [1, 2]


def test_len_after_operations():
    ll = LinkedList()
    ll.append(1)
    ll.prepend(2)
    ll.delete(1)
    assert len(ll) == 1


def test_node_data_and_next_none():
    node = Node(10)
    assert node.data == 10
    assert node.next is None