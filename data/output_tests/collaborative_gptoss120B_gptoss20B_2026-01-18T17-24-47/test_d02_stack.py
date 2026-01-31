import pytest
from data.input_code.d02_stack import *

# ---------- Stack Tests ----------

def test_stack_push_peek_pop_sequence():
    s = Stack()
    # push
    s.push("a")
    assert s.size() == 1  # size after push
    # peek
    assert s.peek() == "a"  # peek result
    # pop
    assert s.pop() == "a"   # pop result
    # size after pop
    assert s.size() == 0

def test_stack_pop_empty_raises():
    s = Stack()
    with pytest.raises(IndexError):
        s.pop()

def test_stack_peek_empty_raises():
    s = Stack()
    with pytest.raises(IndexError):
        s.peek()

def test_stack_clear_and_is_empty():
    s = Stack()
    s.push("b")
    s.clear()
    assert s.is_empty() is True

@pytest.mark.parametrize(
    "items,contains_item,expected",
    [
        (["c"], "c", True),
        (["c"], "d", False),
    ],
)
def test_stack_contains(items, contains_item, expected):
    s = Stack()
    for it in items:
        s.push(it)
    assert (contains_item in s) is expected

def test_stack_none_and_empty_string_handling():
    s = Stack()
    s.push(None)
    s.push("")
    # peek should return the last pushed item ("")
    assert s.peek() == ""
    # pop first should return ""
    assert s.pop() == ""
    # pop second should return None
    assert s.pop() is None

# ---------- Queue Tests ----------

def test_queue_enqueue_front_dequeue_sequence():
    q = Queue()
    # enqueue
    q.enqueue("x")
    assert q.size() == 1  # size after enqueue
    # front
    assert q.front() == "x"  # front result
    # dequeue
    assert q.dequeue() == "x"  # dequeue result
    # size after dequeue
    assert q.size() == 0

def test_queue_dequeue_empty_raises():
    q = Queue()
    with pytest.raises(IndexError):
        q.dequeue()

def test_queue_front_empty_raises():
    q = Queue()
    with pytest.raises(IndexError):
        q.front()

def test_queue_clear_and_is_empty():
    q = Queue()
    q.enqueue("y")
    q.clear()
    assert q.is_empty() is True

@pytest.mark.parametrize(
    "items,contains_item,expected",
    [
        (["z"], "z", True),
        (["z"], "w", False),
    ],
)
def test_queue_contains(items, contains_item, expected):
    q = Queue()
    for it in items:
        q.enqueue(it)
    assert (contains_item in q) is expected

def test_queue_none_and_empty_string_handling():
    q = Queue()
    q.enqueue(None)
    q.enqueue("")
    # front should be the first enqueued item (None)
    assert q.front() is None
    # dequeue first returns None
    assert q.dequeue() is None
    # dequeue second returns empty string
    assert q.dequeue() == ""

import pytest
from data.input_code.d02_stack import *

def test_stack_len_empty():
    s = Stack()
    assert len(s) == 0

def test_stack_contains_empty():
    s = Stack()
    assert ("anything" in s) is False

def test_queue_len_empty():
    q = Queue()
    assert len(q) == 0

def test_queue_contains_empty():
    q = Queue()
    assert ("anything" in q) is False