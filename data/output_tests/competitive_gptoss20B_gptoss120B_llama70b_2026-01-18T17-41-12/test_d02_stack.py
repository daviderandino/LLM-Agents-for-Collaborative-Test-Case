import pytest
from data.input_code.d02_stack import *

# ---------- Stack Tests ----------

def _apply_setup(obj, actions):
    """Utility to apply a list of setup actions to a Stack or Queue instance."""
    for act in actions:
        method = getattr(obj, act["method"])
        method(*act.get("args", []))

# Pop
def test_stack_pop_empty():
    s = Stack()
    with pytest.raises(IndexError):
        s.pop()

def test_stack_pop_after_push():
    s = Stack()
    _apply_setup(s, [{"method": "push", "args": [1]}])
    assert s.pop() == 1

def test_stack_pop_after_clear():
    s = Stack()
    _apply_setup(s, [
        {"method": "push", "args": [9]},
        {"method": "clear", "args": []}
    ])
    with pytest.raises(IndexError):
        s.pop()

# Peek
def test_stack_peek_empty():
    s = Stack()
    with pytest.raises(IndexError):
        s.peek()

def test_stack_peek_after_push():
    s = Stack()
    _apply_setup(s, [{"method": "push", "args": [2]}])
    assert s.peek() == 2

# is_empty
@pytest.mark.parametrize(
    "setup_actions, expected",
    [
        ([], True),                         # default empty
        ([{"method": "push", "args": [3]}], False),
    ],
)
def test_stack_is_empty(setup_actions, expected):
    s = Stack()
    _apply_setup(s, setup_actions)
    assert s.is_empty() is expected

# size
@pytest.mark.parametrize(
    "setup_actions, expected",
    [
        ([], 0),
        ([{"method": "push", "args": [4]},
          {"method": "push", "args": [5]},
          {"method": "push", "args": [6]}], 3),
    ],
)
def test_stack_size(setup_actions, expected):
    s = Stack()
    _apply_setup(s, setup_actions)
    assert s.size() == expected

# clear
def test_stack_clear():
    s = Stack()
    _apply_setup(s, [
        {"method": "push", "args": [7]},
        {"method": "push", "args": [8]},
    ])
    s.clear()
    assert s.size() == 0
    assert s.is_empty() is True

# __len__
@pytest.mark.parametrize(
    "setup_actions, expected",
    [
        ([], 0),
        ([{"method": "push", "args": [10]},
          {"method": "push", "args": [11]},
          {"method": "push", "args": [12]},
          {"method": "push", "args": [13]}], 4),
    ],
)
def test_stack_len(setup_actions, expected):
    s = Stack()
    _apply_setup(s, setup_actions)
    assert len(s) == expected

# __contains__
@pytest.mark.parametrize(
    "setup_actions, item, expected",
    [
        ([{"method": "push", "args": ["a"]}], "a", True),
        ([{"method": "push", "args": ["a"]}], "b", False),
        ([{"method": "push", "args": [None]}], None, True),
        ([{"method": "push", "args": [""]}], "", True),
    ],
)
def test_stack_contains(setup_actions, item, expected):
    s = Stack()
    _apply_setup(s, setup_actions)
    assert (item in s) is expected

# ---------- Queue Tests ----------

# Dequeue
def test_queue_dequeue_empty():
    q = Queue()
    with pytest.raises(IndexError):
        q.dequeue()

def test_queue_dequeue_after_enqueue():
    q = Queue()
    _apply_setup(q, [{"method": "enqueue", "args": [1]}])
    assert q.dequeue() == 1

def test_queue_dequeue_after_clear():
    q = Queue()
    _apply_setup(q, [
        {"method": "enqueue", "args": [9]},
        {"method": "clear", "args": []}
    ])
    with pytest.raises(IndexError):
        q.dequeue()

# Front
def test_queue_front_empty():
    q = Queue()
    with pytest.raises(IndexError):
        q.front()

def test_queue_front_after_enqueue():
    q = Queue()
    _apply_setup(q, [{"method": "enqueue", "args": [2]}])
    assert q.front() == 2

# is_empty
@pytest.mark.parametrize(
    "setup_actions, expected",
    [
        ([], True),
        ([{"method": "enqueue", "args": [3]}], False),
    ],
)
def test_queue_is_empty(setup_actions, expected):
    q = Queue()
    _apply_setup(q, setup_actions)
    assert q.is_empty() is expected

# size
@pytest.mark.parametrize(
    "setup_actions, expected",
    [
        ([], 0),
        ([{"method": "enqueue", "args": [4]},
          {"method": "enqueue", "args": [5]},
          {"method": "enqueue", "args": [6]}], 3),
    ],
)
def test_queue_size(setup_actions, expected):
    q = Queue()
    _apply_setup(q, setup_actions)
    assert q.size() == expected

# clear
def test_queue_clear():
    q = Queue()
    _apply_setup(q, [
        {"method": "enqueue", "args": [7]},
        {"method": "enqueue", "args": [8]},
    ])
    q.clear()
    assert q.size() == 0
    assert q.is_empty() is True

# __len__
@pytest.mark.parametrize(
    "setup_actions, expected",
    [
        ([], 0),
        ([{"method": "enqueue", "args": [10]},
          {"method": "enqueue", "args": [11]},
          {"method": "enqueue", "args": [12]},
          {"method": "enqueue", "args": [13]}], 4),
    ],
)
def test_queue_len(setup_actions, expected):
    q = Queue()
    _apply_setup(q, setup_actions)
    assert len(q) == expected

# __contains__
@pytest.mark.parametrize(
    "setup_actions, item, expected",
    [
        ([{"method": "enqueue", "args": ["x"]}], "x", True),
        ([{"method": "enqueue", "args": ["x"]}], "y", False),
        ([{"method": "enqueue", "args": [None]}], None, True),
        ([{"method": "enqueue", "args": [""]}], "", True),
    ],
)
def test_queue_contains(setup_actions, item, expected):
    q = Queue()
    _apply_setup(q, setup_actions)
    assert (item in q) is expected