import pytest
from data.input_code.02_stack import Stack, Queue

def test_stack_basic_operations():
    s = Stack()
    # initially empty
    assert s.is_empty()
    assert len(s) == 0
    assert s.size() == 0
    # push various types including None
    items = [1, "a", None, 3.14]
    for idx, item in enumerate(items, 1):
        s.push(item)
        assert s.size() == idx
        assert len(s) == idx
        assert not s.is_empty()
        assert item in s
        assert s.peek() == item  # last pushed
    # pop all items and verify order (LIFO)
    for idx, expected in enumerate(reversed(items), 1):
        top = s.peek()
        assert top == expected
        popped = s.pop()
        assert popped == expected
        assert s.size() == len(items) - idx
    # after all pops, stack is empty again
    assert s.is_empty()
    assert len(s) == 0
    # clear on empty should keep it empty
    s.clear()
    assert s.is_empty()

def test_stack_error_conditions():
    s = Stack()
    with pytest.raises(IndexError) as exc_pop:
        s.pop()
    assert "Pop from empty stack" in str(exc_pop.value)
    with pytest.raises(IndexError) as exc_peek:
        s.peek()
    assert "Peek from empty stack" in str(exc_peek.value)
    # after pushing then clearing, errors persist
    s.push(10)
    s.clear()
    with pytest.raises(IndexError):
        s.pop()
    with pytest.raises(IndexError):
        s.peek()

def test_queue_basic_operations():
    q = Queue()
    # initially empty
    assert q.is_empty()
    assert len(q) == 0
    assert q.size() == 0
    # enqueue various items including None
    items = ["first", None, 42]
    for idx, item in enumerate(items, 1):
        q.enqueue(item)
        assert q.size() == idx
        assert len(q) == idx
        assert not q.is_empty()
        assert item in q
        assert q.front() == items[0]  # front remains first enqueued
    # dequeue all items and verify order (FIFO)
    for idx, expected in enumerate(items, 1):
        front = q.front()
        assert front == expected
        dequeued = q.dequeue()
        assert dequeued == expected
        assert q.size() == len(items) - idx
    # after all dequeues, queue is empty again
    assert q.is_empty()
    assert len(q) == 0
    # clear on empty should keep it empty
    q.clear()
    assert q.is_empty()

def test_queue_error_conditions():
    q = Queue()
    with pytest.raises(IndexError) as exc_deq:
        q.dequeue()
    assert "Dequeue from empty queue" in str(exc_deq.value)
    with pytest.raises(IndexError) as exc_front:
        q.front()
    assert "Front from empty queue" in str(exc_front.value)
    # after enqueue and clear, errors persist
    q.enqueue("x")
    q.clear()
    with pytest.raises(IndexError):
        q.dequeue()
    with pytest.raises(IndexError):
        q.front()