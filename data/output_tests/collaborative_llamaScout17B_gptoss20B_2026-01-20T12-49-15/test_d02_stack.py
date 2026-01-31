import pytest
from data.input_code.d02_stack import *

# Fixtures for Stack
@pytest.fixture
def empty_stack():
    return Stack()

@pytest.fixture
def stack_with_item():
    s = Stack()
    s.push(5)
    return s

# Fixtures for Queue
@pytest.fixture
def empty_queue():
    return Queue()

@pytest.fixture
def queue_with_item():
    q = Queue()
    q.enqueue(5)
    return q

# Stack tests
def test_T1_S_init(empty_stack):
    assert empty_stack.is_empty() is True

def test_T2_S_push(empty_stack):
    empty_stack.push(5)
    assert empty_stack.size() == 1
    assert empty_stack.peek() == 5

def test_T3_S_pop(stack_with_item):
    result = stack_with_item.pop()
    assert result == 5
    assert stack_with_item.is_empty() is True

def test_T4_S_pop_empty(empty_stack):
    with pytest.raises(IndexError):
        empty_stack.pop()

def test_T5_S_peek(stack_with_item):
    assert stack_with_item.peek() == 5

def test_T6_S_peek_empty(empty_stack):
    with pytest.raises(IndexError):
        empty_stack.peek()

def test_T7_S_is_empty(stack_with_item):
    assert stack_with_item.is_empty() is False

def test_T8_S_is_empty_empty(empty_stack):
    assert empty_stack.is_empty() is True

def test_T9_S_size(stack_with_item):
    assert stack_with_item.size() == 1

def test_T10_S_clear(stack_with_item):
    stack_with_item.clear()
    assert stack_with_item.is_empty() is True

def test_T11_S_len(empty_stack):
    assert len(empty_stack) == 0

@pytest.mark.parametrize("item,expected", [
    (5, True),
    (10, False),
])
def test_T12_T13_S_contains(stack_with_item, item, expected):
    assert (item in stack_with_item) is expected

# Queue tests
def test_T14_Q_init(empty_queue):
    assert empty_queue.is_empty() is True

def test_T15_Q_enqueue(empty_queue):
    empty_queue.enqueue(5)
    assert empty_queue.size() == 1
    assert empty_queue.front() == 5

def test_T16_Q_dequeue(queue_with_item):
    result = queue_with_item.dequeue()
    assert result == 5
    assert queue_with_item.is_empty() is True

def test_T17_Q_dequeue_empty(empty_queue):
    with pytest.raises(IndexError):
        empty_queue.dequeue()

def test_T18_Q_front(queue_with_item):
    assert queue_with_item.front() == 5

def test_T19_Q_front_empty(empty_queue):
    with pytest.raises(IndexError):
        empty_queue.front()

def test_T20_Q_is_empty(queue_with_item):
    assert queue_with_item.is_empty() is False

def test_T21_Q_is_empty_empty(empty_queue):
    assert empty_queue.is_empty() is True

def test_T22_Q_size(queue_with_item):
    assert queue_with_item.size() == 1

def test_T23_Q_clear(queue_with_item):
    queue_with_item.clear()
    assert queue_with_item.is_empty() is True

def test_T24_Q_len(empty_queue):
    assert len(empty_queue) == 0

@pytest.mark.parametrize("item,expected", [
    (5, True),
    (10, False),
])
def test_T25_T26_Q_contains(queue_with_item, item, expected):
    assert (item in queue_with_item) is expected