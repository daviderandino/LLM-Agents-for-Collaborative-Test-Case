import pytest
from data.input_code.d02_stack import Stack, Queue


@pytest.fixture
def empty_stack():
    return Stack()


@pytest.fixture
def empty_queue():
    return Queue()


def test_stack_initial_state(empty_stack):
    assert empty_stack.is_empty() is True
    assert len(empty_stack) == 0
    assert empty_stack.size() == 0


def test_stack_push_and_inspection(empty_stack):
    empty_stack.push(5)
    assert empty_stack.is_empty() is False
    assert empty_stack.size() == 1
    assert len(empty_stack) == 1
    assert empty_stack.peek() == 5
    assert 5 in empty_stack
    assert empty_stack.__contains__(5) is True


def test_stack_pop_success(empty_stack):
    empty_stack.push(5)
    popped = empty_stack.pop()
    assert popped == 5
    assert empty_stack.is_empty() is True
    assert len(empty_stack) == 0


@pytest.mark.parametrize(
    "method, args, exc",
    [
        ("pop", (), IndexError),
        ("peek", (), IndexError),
    ],
)
def test_stack_exceptions(empty_stack, method, args, exc):
    with pytest.raises(exc):
        getattr(empty_stack, method)(*args)


def test_stack_clear(empty_stack):
    empty_stack.push(5)
    empty_stack.clear()
    assert empty_stack.is_empty() is True
    assert len(empty_stack) == 0
    assert empty_stack.size() == 0


def test_queue_initial_state(empty_queue):
    assert empty_queue.is_empty() is True
    assert len(empty_queue) == 0
    assert empty_queue.size() == 0


def test_queue_enqueue_and_inspection(empty_queue):
    empty_queue.enqueue(5)
    assert empty_queue.is_empty() is False
    assert empty_queue.size() == 1
    assert len(empty_queue) == 1
    assert empty_queue.front() == 5
    assert 5 in empty_queue
    assert empty_queue.__contains__(5) is True


def test_queue_dequeue_success(empty_queue):
    empty_queue.enqueue(5)
    dequeued = empty_queue.dequeue()
    assert dequeued == 5
    assert empty_queue.is_empty() is True
    assert len(empty_queue) == 0


@pytest.mark.parametrize(
    "method, args, exc",
    [
        ("dequeue", (), IndexError),
        ("front", (), IndexError),
    ],
)
def test_queue_exceptions(empty_queue, method, args, exc):
    with pytest.raises(exc):
        getattr(empty_queue, method)(*args)


def test_queue_clear(empty_queue):
    empty_queue.enqueue(5)
    empty_queue.clear()
    assert empty_queue.is_empty() is True
    assert len(empty_queue) == 0
    assert empty_queue.size() == 0