import pytest
from data.input_code.d02_stack import *

@pytest.fixture
def stack():
    return Stack()

@pytest.fixture
def queue():
    return Queue()

@pytest.mark.parametrize('item', [1])
def test_stack_push(stack, item):
    stack.push(item)
    assert item in stack

def test_stack_pop(stack):
    stack.push(1)
    assert stack.pop() == 1

def test_stack_pop_error(stack):
    with pytest.raises(IndexError):
        stack.pop()

def test_stack_peek(stack):
    stack.push(1)
    assert stack.peek() == 1

def test_stack_peek_error(stack):
    with pytest.raises(IndexError):
        stack.peek()

def test_stack_is_empty_true(stack):
    assert stack.is_empty()

def test_stack_is_empty_false(stack):
    stack.push(1)
    assert not stack.is_empty()

def test_stack_size(stack):
    stack.push(1)
    stack.push(2)
    assert stack.size() == 2

def test_stack_clear(stack):
    stack.push(1)
    stack.clear()
    assert stack.is_empty()

def test_stack_len(stack):
    stack.push(1)
    stack.push(2)
    stack.push(3)
    assert len(stack) == 3

@pytest.mark.parametrize('item', [1])
def test_stack_contains_true(stack, item):
    stack.push(item)
    assert item in stack

@pytest.mark.parametrize('item', [2])
def test_stack_contains_false(stack, item):
    stack.push(1)
    assert item not in stack

def test_queue_enqueue(queue):
    queue.enqueue(10)
    assert 10 in queue

def test_queue_dequeue(queue):
    queue.enqueue(10)
    assert queue.dequeue() == 10

def test_queue_dequeue_error(queue):
    with pytest.raises(IndexError):
        queue.dequeue()

def test_queue_front(queue):
    queue.enqueue(10)
    queue.enqueue(20)
    assert queue.front() == 10

def test_queue_front_error(queue):
    with pytest.raises(IndexError):
        queue.front()

def test_queue_is_empty_true(queue):
    assert queue.is_empty()

def test_queue_is_empty_false(queue):
    queue.enqueue(10)
    assert not queue.is_empty()

def test_queue_size(queue):
    queue.enqueue(10)
    queue.enqueue(20)
    assert queue.size() == 2

def test_queue_clear(queue):
    queue.enqueue(10)
    queue.clear()
    assert queue.is_empty()

def test_queue_len(queue):
    queue.enqueue(10)
    queue.enqueue(20)
    queue.enqueue(30)
    assert len(queue) == 3

@pytest.mark.parametrize('item', [10])
def test_queue_contains_true(queue, item):
    queue.enqueue(item)
    assert item in queue

@pytest.mark.parametrize('item', [20])
def test_queue_contains_false(queue, item):
    queue.enqueue(10)
    assert item not in queue