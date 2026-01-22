import pytest
from data.input_code.d03_stack import *

# Stack tests

def test_stack_init():
    stack = Stack()
    assert stack.is_empty() == True

@pytest.mark.parametrize("item", [5, "item", 3.14])
def test_stack_push(item):
    stack = Stack()
    stack.push(item)
    assert stack.size() == 1
    assert item in stack

def test_stack_pop():
    stack = Stack()
    stack.push(5)
    assert stack.pop() == 5
    assert stack.is_empty() == True

def test_stack_pop_error():
    stack = Stack()
    with pytest.raises(IndexError):
        stack.pop()

def test_stack_peek():
    stack = Stack()
    stack.push(5)
    assert stack.peek() == 5
    assert stack.size() == 1

def test_stack_peek_error():
    stack = Stack()
    with pytest.raises(IndexError):
        stack.peek()

@pytest.mark.parametrize("item", [5, "item", 3.14])
def test_stack_contains(item):
    stack = Stack()
    stack.push(item)
    assert item in stack

def test_stack_contains_false():
    stack = Stack()
    stack.push(5)
    assert 10 not in stack

def test_stack_is_empty_false():
    stack = Stack()
    stack.push(5)
    assert stack.is_empty() == False

def test_stack_is_empty_true():
    stack = Stack()
    assert stack.is_empty() == True

def test_stack_size():
    stack = Stack()
    stack.push(5)
    assert stack.size() == 1

def test_stack_size_empty():
    stack = Stack()
    assert stack.size() == 0

def test_stack_clear():
    stack = Stack()
    stack.push(5)
    stack.clear()
    assert stack.is_empty() == True

def test_stack_len():
    stack = Stack()
    stack.push(5)
    assert len(stack) == 1

def test_stack_len_empty():
    stack = Stack()
    assert len(stack) == 0

# Queue tests

def test_queue_init():
    queue = Queue()
    assert queue.is_empty() == True

@pytest.mark.parametrize("item", [5, "item", 3.14])
def test_queue_enqueue(item):
    queue = Queue()
    queue.enqueue(item)
    assert queue.size() == 1
    assert item in queue

def test_queue_dequeue():
    queue = Queue()
    queue.enqueue(5)
    assert queue.dequeue() == 5
    assert queue.is_empty() == True

def test_queue_dequeue_error():
    queue = Queue()
    with pytest.raises(IndexError):
        queue.dequeue()

def test_queue_front():
    queue = Queue()
    queue.enqueue(5)
    assert queue.front() == 5
    assert queue.size() == 1

def test_queue_front_error():
    queue = Queue()
    with pytest.raises(IndexError):
        queue.front()

@pytest.mark.parametrize("item", [5, "item", 3.14])
def test_queue_contains(item):
    queue = Queue()
    queue.enqueue(item)
    assert item in queue

def test_queue_contains_false():
    queue = Queue()
    queue.enqueue(5)
    assert 10 not in queue

def test_queue_is_empty_false():
    queue = Queue()
    queue.enqueue(5)
    assert queue.is_empty() == False

def test_queue_is_empty_true():
    queue = Queue()
    assert queue.is_empty() == True

def test_queue_size():
    queue = Queue()
    queue.enqueue(5)
    assert queue.size() == 1

def test_queue_size_empty():
    queue = Queue()
    assert queue.size() == 0

def test_queue_clear():
    queue = Queue()
    queue.enqueue(5)
    queue.clear()
    assert queue.is_empty() == True

def test_queue_len():
    queue = Queue()
    queue.enqueue(5)
    assert len(queue) == 1

def test_queue_len_empty():
    queue = Queue()
    assert len(queue) == 0