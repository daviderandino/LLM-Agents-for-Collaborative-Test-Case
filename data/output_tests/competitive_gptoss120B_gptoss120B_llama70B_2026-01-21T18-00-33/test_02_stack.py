import pytest
from data.input_code.02_stack import Stack, Queue

@pytest.mark.parametrize('item', [10, 20, 30])
def test_Stack_push(item):
    stack = Stack()
    stack.push(item)
    assert item in stack

def test_Stack_pop_empty():
    stack = Stack()
    with pytest.raises(IndexError):
        stack.pop()

def test_Stack_pop_nonempty():
    stack = Stack()
    stack.push(10)
    assert stack.pop() == 10

def test_Stack_peek_empty():
    stack = Stack()
    with pytest.raises(IndexError):
        stack.peek()

def test_Stack_peek_nonempty():
    stack = Stack()
    stack.push(10)
    assert stack.peek() == 10

def test_Stack_is_empty_true():
    stack = Stack()
    assert stack.is_empty()

def test_Stack_is_empty_false():
    stack = Stack()
    stack.push(10)
    assert not stack.is_empty()

def test_Stack_size_empty():
    stack = Stack()
    assert stack.size() == 0

def test_Stack_size_nonempty():
    stack = Stack()
    stack.push(10)
    stack.push(20)
    assert stack.size() == 2

def test_Stack_clear():
    stack = Stack()
    stack.push(10)
    stack.clear()
    assert stack.size() == 0

def test_Stack_len_empty():
    stack = Stack()
    assert len(stack) == 0

def test_Stack_len_nonempty():
    stack = Stack()
    stack.push(10)
    assert len(stack) == 1

def test_Stack_contains_true():
    stack = Stack()
    stack.push(10)
    assert 10 in stack

def test_Stack_contains_false():
    stack = Stack()
    stack.push(10)
    assert 20 not in stack

@pytest.mark.parametrize('item', ['a', 'b', 'c'])
def test_Queue_enqueue(item):
    queue = Queue()
    queue.enqueue(item)
    assert item in queue

def test_Queue_dequeue_empty():
    queue = Queue()
    with pytest.raises(IndexError):
        queue.dequeue()

def test_Queue_dequeue_nonempty():
    queue = Queue()
    queue.enqueue('a')
    assert queue.dequeue() == 'a'

def test_Queue_front_empty():
    queue = Queue()
    with pytest.raises(IndexError):
        queue.front()

def test_Queue_front_nonempty():
    queue = Queue()
    queue.enqueue('a')
    assert queue.front() == 'a'

def test_Queue_is_empty_true():
    queue = Queue()
    assert queue.is_empty()

def test_Queue_is_empty_false():
    queue = Queue()
    queue.enqueue('a')
    assert not queue.is_empty()

def test_Queue_size_empty():
    queue = Queue()
    assert queue.size() == 0

def test_Queue_size_nonempty():
    queue = Queue()
    queue.enqueue('a')
    queue.enqueue('b')
    assert queue.size() == 2

def test_Queue_clear():
    queue = Queue()
    queue.enqueue('a')
    queue.clear()
    assert queue.size() == 0

def test_Queue_len_empty():
    queue = Queue()
    assert len(queue) == 0

def test_Queue_len_nonempty():
    queue = Queue()
    queue.enqueue('a')
    assert len(queue) == 1

def test_Queue_contains_true():
    queue = Queue()
    queue.enqueue('a')
    assert 'a' in queue

def test_Queue_contains_false():
    queue = Queue()
    queue.enqueue('a')
    assert 'b' not in queue