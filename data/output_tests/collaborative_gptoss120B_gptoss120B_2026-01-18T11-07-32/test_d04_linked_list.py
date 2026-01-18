import pytest
from data.input_code.d04_linked_list import *

def build_linked_list(initial):
    """Utility to create a LinkedList populated with the given iterable."""
    ll = LinkedList()
    for item in initial:
        ll.append(item)
    return ll

# ---------- Append ----------
@pytest.mark.parametrize(
    "initial, data, expected",
    [
        ([], 1, [1]),                # T1_AppendEmpty
        ([1], 2, [1, 2]),            # T2_AppendNonEmpty
    ],
    ids=["T1_AppendEmpty", "T2_AppendNonEmpty"]
)
def test_append(initial, data, expected):
    ll = build_linked_list(initial)
    ll.append(data)
    assert ll.to_list() == expected
    assert len(ll) == len(expected)

# ---------- Prepend ----------
@pytest.mark.parametrize(
    "initial, data, expected",
    [
        ([], 5, [5]),                # T3_PrependEmpty
        ([1], 0, [0, 1]),            # T4_PrependNonEmpty
    ],
    ids=["T3_PrependEmpty", "T4_PrependNonEmpty"]
)
def test_prepend(initial, data, expected):
    ll = build_linked_list(initial)
    ll.prepend(data)
    assert ll.to_list() == expected
    assert len(ll) == len(expected)

# ---------- Delete ----------
@pytest.mark.parametrize(
    "initial, data, expected_result, expected_list",
    [
        ([], 10, False, []),                     # T5_DeleteEmpty
        ([5, 6], 5, True, [6]),                  # T6_DeleteHead
        ([1, 2, 3], 2, True, [1, 3]),            # T7_DeleteMiddle
        ([1, 3], 99, False, [1, 3]),             # T8_DeleteNotFound
    ],
    ids=["T5_DeleteEmpty", "T6_DeleteHead", "T7_DeleteMiddle", "T8_DeleteNotFound"]
)
def test_delete(initial, data, expected_result, expected_list):
    ll = build_linked_list(initial)
    result = ll.delete(data)
    assert result is expected_result
    assert ll.to_list() == expected_list
    assert len(ll) == len(expected_list)

# ---------- Find ----------
@pytest.mark.parametrize(
    "initial, data, expected_index",
    [
        ([7, 8, 9], 7, 0),      # T9_FindHead
        ([7, 8, 9], 9, 2),      # T10_FindTail
        ([7, 8, 9], 5, -1),     # T11_FindNotFound
    ],
    ids=["T9_FindHead", "T10_FindTail", "T11_FindNotFound"]
)
def test_find(initial, data, expected_index):
    ll = build_linked_list(initial)
    assert ll.find(data) == expected_index

# ---------- Get ----------
@pytest.mark.parametrize(
    "initial, index, expected",
    [
        ([10, 20], 0, 10),                     # T12_GetValidZero
        ([10, 20], 1, 20),                     # T13_GetValidLast
    ],
    ids=["T12_GetValidZero", "T13_GetValidLast"]
)
def test_get_valid(initial, index, expected):
    ll = build_linked_list(initial)
    assert ll.get(index) == expected

@pytest.mark.parametrize(
    "initial, index, exc",
    [
        ([1], -1, IndexError),                 # T14_GetNegativeIndex
        ([1], 1, IndexError),                  # T15_GetOutOfRange
    ],
    ids=["T14_GetNegativeIndex", "T15_GetOutOfRange"]
)
def test_get_exceptions(initial, index, exc):
    ll = build_linked_list(initial)
    with pytest.raises(exc):
        ll.get(index)

# ---------- to_list ----------
@pytest.mark.parametrize(
    "initial, expected",
    [
        ([], []),                               # T16_ToListEmpty
        ([4, 5, 6], [4, 5, 6]),                 # T17_ToListPopulated
    ],
    ids=["T16_ToListEmpty", "T17_ToListPopulated"]
)
def test_to_list(initial, expected):
    ll = build_linked_list(initial)
    assert ll.to_list() == expected

# ---------- __len__ ----------
def test_len_initial_empty():
    ll = LinkedList()
    assert len(ll) == 0                                 # T18_LengthAfterOps

def test_len_after_append_prepend():
    ll = LinkedList()
    ll.append(1)
    ll.prepend(0)
    assert len(ll) == 2                                 # T19_LengthAfterAppendPrepend