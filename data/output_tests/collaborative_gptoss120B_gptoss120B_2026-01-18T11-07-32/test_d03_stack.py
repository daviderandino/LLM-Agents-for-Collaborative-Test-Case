import pytest
from data.input_code.d03_stack import *

@pytest.fixture
def stack():
    return Stack()

@pytest.fixture
def queue():
    return Queue()


# ---------- Stack Tests ----------

def test_stack_push_returns_none(stack):
    result = stack.push(42)
    assert result is None
    assert stack.size() == 1

def test_stack_pop_after_push(stack):
    stack.push(99)
    assert stack.pop() == 99

def test_stack_pop_raises_on_empty(stack):
    with pytest.raises(IndexError):
        stack.pop()

def test_stack_peek_after_push(stack):
    stack.push("top")
    assert stack.peek() == "top"

def test_stack_peek_raises_on_empty(stack):
    with pytest.raises(IndexError):
        stack.peek()

def test_stack_is_empty_initial(stack):
    assert stack.is_empty() is True

def test_stack_size_after_multiple_pushes(stack):
    stack.push(1)
    stack.push(2)
    assert stack.size() == 2

def test_stack_clear_returns_none_and_empties(stack):
    stack.push("x")
    result = stack.clear()
    assert result is None
    assert stack.is_empty() is True

def test_stack_len_mirrors_size(stack):
    stack.push("a")
    stack.push("b")
    assert len(stack) == 2

def test_stack_contains_existing_item(stack):
    stack.push(7)
    assert (7 in stack) is True


# ---------- Queue Tests ----------

def test_queue_enqueue_returns_none(queue):
    result = queue.enqueue("first")
    assert result is None
    assert queue.size() == 1

def test_queue_dequeue_after_enqueue(queue):
    queue.enqueue("alpha")
    assert queue.dequeue() == "alpha"

def test_queue_dequeue_raises_on_empty(queue):
    with pytest.raises(IndexError):
        queue.dequeue()

def test_queue_front_after_enqueue(queue):
    queue.enqueue(123)
    assert queue.front() == 123

def test_queue_front_raises_on_empty(queue):
    with pytest.raises(IndexError):
        queue.front()

def test_queue_is_empty_initial(queue):
    assert queue.is_empty() is True

def test_queue_size_after_multiple_enqueues(queue):
    queue.enqueue("x")
    queue.enqueue("y")
    assert queue.size() == 2

def test_queue_clear_returns_none_and_empties(queue):
    queue.enqueue("z")
    result = queue.clear()
    assert result is None
    assert queue.is_empty() is True

def test_queue_len_mirrors_size(queue):
    queue.enqueue(1)
    queue.enqueue(2)
    assert len(queue) == 2

def test_queue_contains_existing_item(queue):
    queue.enqueue("needle")
    assert ("needle" in queue) is True