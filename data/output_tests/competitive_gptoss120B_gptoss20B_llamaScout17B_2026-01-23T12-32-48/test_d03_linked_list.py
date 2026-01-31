import pytest
from data.input_code.d03_linked_list import *

def build_list(values):
    """Helper to create a LinkedList from an iterable of values."""
    ll = LinkedList()
    for v in values:
        ll.append(v)
    return ll

@pytest.mark.parametrize(
    "setup, data, expected_len, expected_list",
    [
        ([], 10, 1, [10]),          # T1_append_empty
        ([1], 2, 2, [1, 2]),        # T2_append_nonempty
    ],
)
def test_append(setup, data, expected_len, expected_list):
    ll = build_list(setup)
    ll.append(data)
    assert len(ll) == expected_len
    assert ll.to_list() == expected_list

def test_prepend():
    ll = build_list([1, 2])
    ll.prepend(0)
    assert ll.to_list() == [0, 1, 2]
    assert len(ll) == 3

@pytest.mark.parametrize(
    "setup, data, expected",
    [
        ([], 5, False),            # T4_delete_empty
        ([1, 2, 3], 1, True),      # T5_delete_head
        ([1, 2, 3], 2, True),      # T6_delete_middle
        ([1, 2, 3], 4, False),     # T7_delete_notfound
    ],
)
def test_delete(setup, data, expected):
    ll = build_list(setup)
    result = ll.delete(data)
    assert result is expected
    # Verify list contents after deletion
    if expected:
        assert data not in ll.to_list()
    else:
        assert ll.to_list() == setup

@pytest.mark.parametrize(
    "setup, data, expected",
    [
        ([], 1, -1),                # T8_find_empty
        ([10, 20, 30], 20, 1),      # T9_find_middle
        ([10, 20, 30], 40, -1),     # T10_find_notfound
    ],
)
def test_find(setup, data, expected):
    ll = build_list(setup)
    assert ll.find(data) == expected

@pytest.mark.parametrize(
    "setup, index, expected",
    [
        ([5, 6, 7], 0, 5),          # T11_get_zero
        ([5, 6, 7], 2, 7),          # T12_get_last
        ([1], -1, "IndexError"),    # T13_get_negative
        ([1, 2], 2, "IndexError"),  # T14_get_out_of_range
    ],
)
def test_get(setup, index, expected):
    ll = build_list(setup)
    if isinstance(expected, str) and expected == "IndexError":
        with pytest.raises(IndexError):
            ll.get(index)
    else:
        assert ll.get(index) == expected

@pytest.mark.parametrize(
    "setup, expected_len",
    [
        ([1, 2, 3, 4], 4),          # T15_len
    ],
)
def test_len(setup, expected_len):
    ll = build_list(setup)
    assert len(ll) == expected_len

@pytest.mark.parametrize(
    "setup, expected_list",
    [
        ([9, 8, 7], [9, 8, 7]),     # T16_to_list
    ],
)
def test_to_list(setup, expected_list):
    ll = build_list(setup)
    assert ll.to_list() == expected_list