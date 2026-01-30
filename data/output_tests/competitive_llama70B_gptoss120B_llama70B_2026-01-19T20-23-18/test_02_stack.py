import pytest
from data.input_code.02_stack import *

# ---------- Fixtures ----------
@pytest.fixture
def empty_stack():
    return Stack()

@pytest.fixture
def stack_one_item():
    s = Stack()
    s.push(5)
    return s

@pytest.fixture
def empty_queue():
    return Queue()

@pytest.fixture
def queue_one_item():
    q = Queue()
    q.enqueue(5)
    return q

# ---------- Stack Tests ----------
def test_stack_initial_state(empty_stack):
    assert empty_stack.is_empty()
    assert empty_stack.size() == 0
    assert len(empty_stack) == 0

def test_stack_push_and_state(stack_one_item):
    # after push, stack should not be empty and size should be 1
    assert not stack_one_item.is_empty()
    assert stack_one_item.size() == 1
    assert len(stack_one_item) == 1
    # peek should return the pushed item
    assert stack_one_item.peek() == 5
    # __contains__ via 'in'
    assert 5 in stack_one_item

@pytest.mark.parametrize(
    "method,expected",
    [
        ("pop", 5),
        ("peek", 5),
    ],
)
def test_stack_pop_and_peek(stack_one_item, method, expected):
    # call the method dynamically
    result = getattr(stack_one_item, method)()
    assert result == expected
    # after pop, stack becomes empty
    if method == "pop":
        assert stack_one_item.is_empty()
        assert stack_one_item.size() == 0

def test_stack_pop_error(empty_stack):
    with pytest.raises(IndexError):
        empty_stack.pop()

def test_stack_peek_error(empty_stack):
    with pytest.raises(IndexError):
        empty_stack.peek()

@pytest.mark.parametrize(
    "item,expected",
    [
        (5, True),
        (10, False),
    ],
)
def test_stack_contains(stack_one_item, item, expected):
    assert (item in stack_one_item) is expected

def test_stack_clear(stack_one_item):
    stack_one_item.clear()
    assert stack_one_item.is_empty()
    assert stack_one_item.size() == 0

# ---------- Queue Tests ----------
def test_queue_initial_state(empty_queue):
    assert empty_queue.is_empty()
    assert empty_queue.size() == 0
    assert len(empty_queue) == 0

def test_queue_enqueue_and_state(queue_one_item):
    # after enqueue, queue should not be empty and size should be 1
    assert not queue_one_item.is_empty()
    assert queue_one_item.size() == 1
    assert len(queue_one_item) == 1
    # front should return the enqueued item
    assert queue_one_item.front() == 5
    # __contains__ via 'in'
    assert 5 in queue_one_item

@pytest.mark.parametrize(
    "method,expected",
    [
        ("dequeue", 5),
        ("front", 5),
    ],
)
def test_queue_dequeue_and_front(queue_one_item, method, expected):
    result = getattr(queue_one_item, method)()
    assert result == expected
    # after dequeue, queue becomes empty
    if method == "dequeue":
        assert queue_one_item.is_empty()
        assert queue_one_item.size() == 0

def test_queue_dequeue_error(empty_queue):
    with pytest.raises(IndexError):
        empty_queue.dequeue()

def test_queue_front_error(empty_queue):
    with pytest.raises(IndexError):
        empty_queue.front()

@pytest.mark.parametrize(
    "item,expected",
    [
        (5, True),
        (10, False),
    ],
)
def test_queue_contains(queue_one_item, item, expected):
    assert (item in queue_one_item) is expected

def test_queue_clear(queue_one_item):
    queue_one_item.clear()
    assert queue_one_item.is_empty()
    assert queue_one_item.size() == 0