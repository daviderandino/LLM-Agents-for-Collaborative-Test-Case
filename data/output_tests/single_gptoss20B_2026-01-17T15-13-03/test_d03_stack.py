import pytest
from data.input_code.d03_stack import Stack, Queue


# --------------------- Stack Tests --------------------- #

def test_stack_push_and_pop():
    s = Stack()
    s.push(1)
    s.push(2)
    s.push(3)
    assert s.size() == 3
    assert s.pop() == 3
    assert s.pop() == 2
    assert s.pop() == 1
    assert s.is_empty()
    assert len(s) == 0


def test_stack_pop_empty_raises():
    s = Stack()
    with pytest.raises(IndexError, match="Pop from empty stack"):
        s.pop()


def test_stack_peek_empty_raises():
    s = Stack()
    with pytest.raises(IndexError, match="Peek from empty stack"):
        s.peek()


def test_stack_peek_returns_last():
    s = Stack()
    s.push('a')
    s.push('b')
    assert s.peek() == 'b'
    assert s.size() == 2  # peek should not remove
    assert s.pop() == 'b'


def test_stack_is_empty_and_size():
    s = Stack()
    assert s.is_empty()
    assert s.size() == 0
    s.push(42)
    assert not s.is_empty()
    assert s.size() == 1
    s.pop()
    assert s.is_empty()
    assert s.size() == 0


def test_stack_clear():
    s = Stack()
    s.push(1)
    s.push(2)
    s.clear()
    assert s.is_empty()
    assert s.size() == 0
    with pytest.raises(IndexError, match="Pop from empty stack"):
        s.pop()


def test_stack_len_and_contains():
    s = Stack()
    s.push('x')
    s.push('y')
    assert len(s) == 2
    assert 'x' in s
    assert 'y' in s
    assert 'z' not in s
    s.pop()
    assert 'y' not in s
    assert len(s) == 1


def test_stack_push_none():
    s = Stack()
    s.push(None)
    assert s.peek() is None
    assert s.pop() is None
    assert s.is_empty()


# --------------------- Queue Tests --------------------- #

def test_queue_enqueue_and_dequeue():
    q = Queue()
    q.enqueue('first')
    q.enqueue('second')
    q.enqueue('third')
    assert q.size() == 3
    assert q.dequeue() == 'first'
    assert q.dequeue() == 'second'
    assert q.dequeue() == 'third'
    assert q.is_empty()
    assert len(q) == 0


def test_queue_dequeue_empty_raises():
    q = Queue()
    with pytest.raises(IndexError, match="Dequeue from empty queue"):
        q.dequeue()


def test_queue_front_empty_raises():
    q = Queue()
    with pytest.raises(IndexError, match="Front from empty queue"):
        q.front()


def test_queue_front_returns_first():
    q = Queue()
    q.enqueue('alpha')
    q.enqueue('beta')
    assert q.front() == 'alpha'
    assert q.size() == 2  # front should not remove
    assert q.dequeue() == 'alpha'


def test_queue_is_empty_and_size():
    q = Queue()
    assert q.is_empty()
    assert q.size() == 0
    q.enqueue(99)
    assert not q.is_empty()
    assert q.size() == 1
    q.dequeue()
    assert q.is_empty()
    assert q.size() == 0


def test_queue_clear():
    q = Queue()
    q.enqueue('x')
    q.enqueue('y')
    q.clear()
    assert q.is_empty()
    assert q.size() == 0
    with pytest.raises(IndexError, match="Dequeue from empty queue"):
        q.dequeue()


def test_queue_len_and_contains():
    q = Queue()
    q.enqueue('a')
    q.enqueue('b')
    assert len(q) == 2
    assert 'a' in q
    assert 'b' in q
    assert 'c' not in q
    q.dequeue()
    assert 'a' not in q
    assert len(q) == 1


def test_queue_enqueue_none():
    q = Queue()
    q.enqueue(None)
    assert q.front() is None
    assert q.dequeue() is None
    assert q.is_empty()