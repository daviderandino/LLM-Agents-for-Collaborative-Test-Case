import pytest
from data.input_code.d03_stack import *

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
def test_stack_init(empty_stack):
    assert len(empty_stack) == 0
    assert empty_stack.is_empty()
    assert empty_stack.size() == 0

def test_stack_push_and_state(stack_one_item):
    assert stack_one_item.size() == 1
    assert not stack_one_item.is_empty()
    assert len(stack_one_item) == 1
    assert 5 in stack_one_item
    assert stack_one_item.peek() == 5

def test_stack_pop_success(stack_one_item):
    assert stack_one_item.pop() == 5
    # after pop the stack should be empty again
    assert stack_one_item.is_empty()
    assert len(stack_one_item) == 0

@pytest.mark.parametrize("method_name,exception", [
    ("pop", IndexError),
    ("peek", IndexError),
])
def test_stack_error_on_empty(empty_stack, method_name, exception):
    method = getattr(empty_stack, method_name)
    with pytest.raises(exception):
        method()

def test_stack_clear(stack_one_item):
    stack_one_item.clear()
    assert stack_one_item.is_empty()
    assert len(stack_one_item) == 0
    assert stack_one_item.size() == 0

# ---------- Queue Tests ----------
def test_queue_init(empty_queue):
    assert len(empty_queue) == 0
    assert empty_queue.is_empty()
    assert empty_queue.size() == 0

def test_queue_enqueue_and_state(queue_one_item):
    assert queue_one_item.size() == 1
    assert not queue_one_item.is_empty()
    assert len(queue_one_item) == 1
    assert 5 in queue_one_item
    assert queue_one_item.front() == 5

def test_queue_dequeue_success(queue_one_item):
    assert queue_one_item.dequeue() == 5
    # after dequeue the queue should be empty again
    assert queue_one_item.is_empty()
    assert len(queue_one_item) == 0

@pytest.mark.parametrize("method_name,exception", [
    ("dequeue", IndexError),
    ("front", IndexError),
])
def test_queue_error_on_empty(empty_queue, method_name, exception):
    method = getattr(empty_queue, method_name)
    with pytest.raises(exception):
        method()

def test_queue_clear(queue_one_item):
    queue_one_item.clear()
    assert queue_one_item.is_empty()
    assert len(queue_one_item) == 0
    assert queue_one_item.size() == 0