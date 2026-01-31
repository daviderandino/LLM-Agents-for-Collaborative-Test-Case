import pytest
from data.input_code.d02_stack import *

@pytest.fixture
def stack():
    return Stack()

@pytest.fixture
def queue():
    return Queue()

@pytest.mark.parametrize('item', [1, None, "", [], 10])
def test_stack_push(stack, item):
    stack.push(item)
    assert item in stack

@pytest.mark.parametrize('item', [1, None, "", [], 10])
def test_queue_enqueue(queue, item):
    queue.enqueue(item)
    assert item in queue

def test_stack_pop(stack):
    stack.push(1)
    assert stack.pop() == 1

def test_queue_dequeue(queue):
    queue.enqueue(1)
    assert queue.dequeue() == 1

def test_stack_peek(stack):
    stack.push(1)
    assert stack.peek() == 1

def test_queue_front(queue):
    queue.enqueue(1)
    assert queue.front() == 1

def test_stack_pop_empty(stack):
    with pytest.raises(IndexError):
        stack.pop()

def test_queue_dequeue_empty(queue):
    with pytest.raises(IndexError):
        queue.dequeue()

def test_stack_peek_empty(stack):
    with pytest.raises(IndexError):
        stack.peek()

def test_queue_front_empty(queue):
    with pytest.raises(IndexError):
        queue.front()

def test_stack_is_empty(stack):
    assert stack.is_empty() == True

def test_queue_is_empty(queue):
    assert queue.is_empty() == True

def test_stack_size(stack):
    stack.push(1)
    assert stack.size() == 1

def test_queue_size(queue):
    queue.enqueue(1)
    assert queue.size() == 1

def test_stack_len(stack):
    stack.push(1)
    assert len(stack) == 1

def test_queue_len(queue):
    queue.enqueue(1)
    assert len(queue) == 1

def test_stack_contains(stack):
    stack.push(1)
    assert 1 in stack

def test_queue_contains(queue):
    queue.enqueue(1)
    assert 1 in queue

def test_stack_clear(stack):
    stack.push(1)
    stack.clear()
    assert stack.is_empty() == True

def test_queue_clear(queue):
    queue.enqueue(1)
    queue.clear()
    assert queue.is_empty() == True