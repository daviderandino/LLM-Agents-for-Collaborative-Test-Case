import pytest
from data.input_code.02_stack import Stack, Queue

# --------------------- Stack Tests --------------------- #

def test_stack_is_empty():
    stack = Stack()
    assert stack.is_empty() is True

def test_stack_size_empty():
    stack = Stack()
    assert stack.size() == 0

@pytest.mark.parametrize("item", [42])
def test_stack_push_and_peek(item):
    stack = Stack()
    stack.push(item)
    assert stack.peek() == item

@pytest.mark.parametrize("item", [42])
def test_stack_push_and_pop(item):
    stack = Stack()
    stack.push(item)
    assert stack.pop() == item

def test_stack_pop_empty_raises():
    stack = Stack()
    with pytest.raises(IndexError):
        stack.pop()

def test_stack_peek_empty_raises():
    stack = Stack()
    with pytest.raises(IndexError):
        stack.peek()

def test_stack_clear():
    stack = Stack()
    stack.push(1)
    stack.clear()
    assert stack.is_empty() is True

def test_stack_len_after_push():
    stack = Stack()
    stack.push(1)
    assert len(stack) == 1

@pytest.mark.parametrize("item,expected", [
    (42, True),
    (99, False),
])
def test_stack_contains(item, expected):
    stack = Stack()
    stack.push(42)
    assert (item in stack) is expected

# --------------------- Queue Tests --------------------- #

def test_queue_is_empty():
    queue = Queue()
    assert queue.is_empty() is True

def test_queue_size_empty():
    queue = Queue()
    assert queue.size() == 0

@pytest.mark.parametrize("item", [99])
def test_queue_enqueue_and_front(item):
    queue = Queue()
    queue.enqueue(item)
    assert queue.front() == item

@pytest.mark.parametrize("item", [99])
def test_queue_enqueue_and_dequeue(item):
    queue = Queue()
    queue.enqueue(item)
    assert queue.dequeue() == item

def test_queue_dequeue_empty_raises():
    queue = Queue()
    with pytest.raises(IndexError):
        queue.dequeue()

def test_queue_front_empty_raises():
    queue = Queue()
    with pytest.raises(IndexError):
        queue.front()

def test_queue_clear():
    queue = Queue()
    queue.enqueue(1)
    queue.clear()
    assert queue.is_empty() is True

def test_queue_len_after_enqueue():
    queue = Queue()
    queue.enqueue(1)
    assert len(queue) == 1

@pytest.mark.parametrize("item,expected", [
    (99, True),
    (42, False),
])
def test_queue_contains(item, expected):
    queue = Queue()
    queue.enqueue(99)
    assert (item in queue) is expected