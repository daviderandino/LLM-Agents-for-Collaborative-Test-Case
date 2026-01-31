import pytest
from data.input_code.d03_linked_list import *

def run_setup(setup):
    linked_list = LinkedList()
    for step in setup:
        getattr(linked_list, step['method'])(**step['args'])
    return linked_list

@pytest.mark.parametrize('setup, data', [
    ([], 10),
    ([{'method': 'append', 'args': {'data': 1}}], 2)
])
def test_append(setup, data):
    linked_list = run_setup(setup)
    linked_list.append(data)
    assert len(linked_list) == len(setup) + 1
    if len(setup) == 0:
        assert linked_list.get(0) == data
    else:
        assert linked_list.get(len(setup)) == data

@pytest.mark.parametrize('setup, data', [
    ([], 5),
    ([{'method': 'append', 'args': {'data': 1}}], 0)
])
def test_prepend(setup, data):
    linked_list = run_setup(setup)
    linked_list.prepend(data)
    assert len(linked_list) == len(setup) + 1
    assert linked_list.get(0) == data

@pytest.mark.parametrize('setup, data, expected', [
    ([], 1, False),
    ([{'method': 'append', 'args': {'data': 7}}, {'method': 'append', 'args': {'data': 8}}], 7, True),
    ([{'method': 'append', 'args': {'data': 1}}, {'method': 'append', 'args': {'data': 2}}, {'method': 'append', 'args': {'data': 3}}], 2, True),
    ([{'method': 'append', 'args': {'data': 4}}, {'method': 'append', 'args': {'data': 5}}], 99, False)
])
def test_delete(setup, data, expected):
    linked_list = run_setup(setup)
    assert linked_list.delete(data) == expected

@pytest.mark.parametrize('setup, data, expected', [
    ([{'method': 'append', 'args': {'data': 'a'}}, {'method': 'append', 'args': {'data': 'b'}}, {'method': 'append', 'args': {'data': 'c'}}], 'b', 1),
    ([{'method': 'append', 'args': {'data': 100}}], 200, -1)
])
def test_find(setup, data, expected):
    linked_list = run_setup(setup)
    assert linked_list.find(data) == expected

@pytest.mark.parametrize('setup, index, expected', [
    ([{'method': 'append', 'args': {'data': 'first'}}, {'method': 'append', 'args': {'data': 'second'}}], 0, 'first'),
    ([{'method': 'append', 'args': {'data': 'x'}}, {'method': 'append', 'args': {'data': 'y'}}, {'method': 'append', 'args': {'data': 'z'}}], 2, 'z')
])
def test_get_valid(setup, index, expected):
    linked_list = run_setup(setup)
    assert linked_list.get(index) == expected

def test_get_invalid():
    linked_list = LinkedList()
    linked_list.append(0)
    with pytest.raises(IndexError):
        linked_list.get(-1)
    with pytest.raises(IndexError):
        linked_list.get(5)

@pytest.mark.parametrize('setup, expected', [
    ([{'method': 'prepend', 'args': {'data': 3}}, {'method': 'append', 'args': {'data': 4}}, {'method': 'prepend', 'args': {'data': 2}}, {'method': 'append', 'args': {'data': 5}}], [2, 3, 4, 5]),
    ([], []),
    ([{'method': 'append', 'args': {'data': 1}}], [1])
])
def test_to_list(setup, expected):
    linked_list = run_setup(setup)
    assert linked_list.to_list() == expected

@pytest.mark.parametrize('setup, expected', [
    ([{'method': 'append', 'args': {'data': 'a'}}, {'method': 'prepend', 'args': {'data': 'b'}}, {'method': 'append', 'args': {'data': 'c'}}], 3),
    ([], 0),
    ([{'method': 'append', 'args': {'data': 1}}], 1)
])
def test_len(setup, expected):
    linked_list = run_setup(setup)
    assert len(linked_list) == expected