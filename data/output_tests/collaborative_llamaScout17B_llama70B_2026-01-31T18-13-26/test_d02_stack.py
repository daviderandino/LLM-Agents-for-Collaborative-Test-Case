import pytest
from data.input_code.d02_stack import Stack, Queue

@pytest.mark.parametrize('expected', [
    (None)
])
def test_stack_init(expected):
    stack = Stack()
    assert stack._items == []

@pytest.mark.parametrize('item, expected', [
    (5, None)
])
def test_stack_push(item, expected):
    stack = Stack()
    stack.push(item)
    assert stack._items == [item]

@pytest.mark.parametrize('item, expected', [
    (5, 5)
])
def test_stack_pop(item, expected):
    stack = Stack()
    stack.push(item)
    assert stack.pop() == expected

def test_stack_pop_empty():
    stack = Stack()
    with pytest.raises(IndexError):
        stack.pop()

@pytest.mark.parametrize('item, expected', [
    (5, 5)
])
def test_stack_peek(item, expected):
    stack = Stack()
    stack.push(item)
    assert stack.peek() == expected

def test_stack_peek_empty():
    stack = Stack()
    with pytest.raises(IndexError):
        stack.peek()

@pytest.mark.parametrize('expected', [
    (True)
])
def test_stack_is_empty(expected):
    stack = Stack()
    assert stack.is_empty() == expected

@pytest.mark.parametrize('item, expected', [
    (5, False)
])
def test_stack_is_not_empty(item, expected):
    stack = Stack()
    stack.push(item)
    assert stack.is_empty() == expected

@pytest.mark.parametrize('item, expected', [
    (5, 1)
])
def test_stack_size(item, expected):
    stack = Stack()
    stack.push(item)
    assert stack.size() == expected

@pytest.mark.parametrize('item, expected', [
    (5, None)
])
def test_stack_clear(item, expected):
    stack = Stack()
    stack.push(item)
    stack.clear()
    assert stack._items == []

@pytest.mark.parametrize('item, expected', [
    (5, 1)
])
def test_stack_len(item, expected):
    stack = Stack()
    stack.push(item)
    assert len(stack) == expected

@pytest.mark.parametrize('item, expected', [
    (5, True)
])
def test_stack_contains(item, expected):
    stack = Stack()
    stack.push(item)
    assert stack._items == [item] and item in stack._items

@pytest.mark.parametrize('item, expected', [
    (10, False)
])
def test_stack_not_contains(item, expected):
    stack = Stack()
    stack.push(5)
    assert item not in stack._items

@pytest.mark.parametrize('expected', [
    (None)
])
def test_queue_init(expected):
    queue = Queue()
    assert queue._items == []

@pytest.mark.parametrize('item, expected', [
    (5, None)
])
def test_queue_enqueue(item, expected):
    queue = Queue()
    queue.enqueue(item)
    assert queue._items == [item]

@pytest.mark.parametrize('item, expected', [
    (5, 5)
])
def test_queue_dequeue(item, expected):
    queue = Queue()
    queue.enqueue(item)
    assert queue.dequeue() == expected

def test_queue_dequeue_empty():
    queue = Queue()
    with pytest.raises(IndexError):
        queue.dequeue()

@pytest.mark.parametrize('item, expected', [
    (5, 5)
])
def test_queue_front(item, expected):
    queue = Queue()
    queue.enqueue(item)
    assert queue.front() == expected

def test_queue_front_empty():
    queue = Queue()
    with pytest.raises(IndexError):
        queue.front()

@pytest.mark.parametrize('expected', [
    (True)
])
def test_queue_is_empty(expected):
    queue = Queue()
    assert queue.is_empty() == expected

@pytest.mark.parametrize('item, expected', [
    (5, False)
])
def test_queue_is_not_empty(item, expected):
    queue = Queue()
    queue.enqueue(item)
    assert queue.is_empty() == expected

@pytest.mark.parametrize('item, expected', [
    (5, 1)
])
def test_queue_size(item, expected):
    queue = Queue()
    queue.enqueue(item)
    assert queue.size() == expected

@pytest.mark.parametrize('item, expected', [
    (5, None)
])
def test_queue_clear(item, expected):
    queue = Queue()
    queue.enqueue(item)
    queue.clear()
    assert queue._items == []

@pytest.mark.parametrize('item, expected', [
    (5, 1)
])
def test_queue_len(item, expected):
    queue = Queue()
    queue.enqueue(item)
    assert len(queue) == expected

@pytest.mark.parametrize('item, expected', [
    (5, True)
])
def test_queue_contains(item, expected):
    queue = Queue()
    queue.enqueue(item)
    assert queue._items == [item] and item in queue._items

@pytest.mark.parametrize('item, expected', [
    (10, False)
])
def test_queue_not_contains(item, expected):
    queue = Queue()
    queue.enqueue(5)
    assert item not in queue._items

@pytest.mark.parametrize('item, expected', [
    (5, False)
])
def test_stack_contains_false(item, expected):
    stack = Stack()
    assert item not in stack

@pytest.mark.parametrize('item, expected', [
    (5, False)
])
def test_queue_contains_false(item, expected):
    queue = Queue()
    assert item not in queue