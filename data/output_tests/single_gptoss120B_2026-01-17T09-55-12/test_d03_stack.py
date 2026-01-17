import pytest
from data.input_code.d03_stack import Stack, Queue

@pytest.fixture
def empty_stack():
    return Stack()

@pytest.fixture
def populated_stack():
    s = Stack()
    for i in range(5):
        s.push(i)
    return s

@pytest.fixture
def empty_queue():
    return Queue()

@pytest.fixture
def populated_queue():
    q = Queue()
    for i in range(5):
        q.enqueue(i)
    return q

def test_stack_push_peek_pop_size_contains_len_is_empty_and_clear(empty_stack, populated_stack):
    # initially empty
    assert empty_stack.is_empty()
    assert len(empty_stack) == 0
    with pytest.raises(IndexError):
        empty_stack.pop()
    with pytest.raises(IndexError):
        empty_stack.peek()

    # push items
    empty_stack.push('a')
    empty_stack.push('b')
    assert empty_stack.size() == 2
    assert len(empty_stack) == 2
    assert not empty_stack.is_empty()
    assert empty_stack.peek() == 'b'
    assert 'a' in empty_stack
    assert 'c' not in empty_stack

    # pop items LIFO
    assert empty_stack.pop() == 'b'
    assert empty_stack.pop() == 'a'
    assert empty_stack.is_empty()

    # test populated stack behavior
    assert populated_stack.size() == 5
    assert len(populated_stack) == 5
    assert not populated_stack.is_empty()
    # peek should be last pushed (4)
    assert populated_stack.peek() == 4
    # pop all and verify order
    popped = [populated_stack.pop() for _ in range(5)]
    assert popped == [4, 3, 2, 1, 0]
    assert populated_stack.is_empty()

    # clear should reset
    populated_stack.push('x')
    populated_stack.clear()
    assert populated_stack.is_empty()
    assert len(populated_stack) == 0

def test_queue_enqueue_front_dequeue_size_contains_len_is_empty_and_clear(empty_queue, populated_queue):
    # initially empty
    assert empty_queue.is_empty()
    assert len(empty_queue) == 0
    with pytest.raises(IndexError):
        empty_queue.dequeue()
    with pytest.raises(IndexError):
        empty_queue.front()

    # enqueue items
    empty_queue.enqueue('first')
    empty_queue.enqueue('second')
    assert empty_queue.size() == 2
    assert len(empty_queue) == 2
    assert not empty_queue.is_empty()
    assert empty_queue.front() == 'first'
    assert 'second' in empty_queue
    assert 'third' not in empty_queue

    # dequeue FIFO
    assert empty_queue.dequeue() == 'first'
    assert empty_queue.dequeue() == 'second'
    assert empty_queue.is_empty()

    # test populated queue behavior
    assert populated_queue.size() == 5
    assert len(populated_queue) == 5
    assert not populated_queue.is_empty()
    # front should be first enqueued (0)
    assert populated_queue.front() == 0
    # dequeue all and verify order
    dequeued = [populated_queue.dequeue() for _ in range(5)]
    assert dequeued == [0, 1, 2, 3, 4]
    assert populated_queue.is_empty()

    # clear should reset
    populated_queue.enqueue('y')
    populated_queue.clear()
    assert populated_queue.is_empty()
    assert len(populated_queue) == 0