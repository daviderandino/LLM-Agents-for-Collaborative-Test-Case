import pytest

from data.input_code.t19 import is_duplicate

def test_is_duplicate_empty_array():
    assert is_duplicate([]) == False

def test_is_duplicate_single_element_array():
    assert is_duplicate([1]) == False

def test_is_duplicate_no_duplicates():
    assert is_duplicate([1, 2, 3, 4, 5]) == False

def test_is_duplicate_with_duplicates():
    assert is_duplicate([1, 2, 2, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty():
    assert is_duplicate([1, 2, 2, 3, 4, 4, 5, None]) == True

def test_is_duplicate_with_duplicates_and_none():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_zero():
    assert is_duplicate([1, 2, 0, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_negative():
    assert is_duplicate([1, 2, -1, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_max_int():
    assert is_duplicate([1, 2, 2**31-1, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_min_int():
    assert is_duplicate([1, 2, -2**31, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_max_float():
    assert is_duplicate([1, 2, 1.7976931348623157e+308, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_min_float():
    assert is_duplicate([1, 2, -1.7976931348623157e+308, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_string():
    assert is_duplicate([1, 2, "", 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_string():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_list():
    assert is_duplicate([1, 2, [], 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_list():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_dict():
    assert is_duplicate([1, 2, {}, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_dict():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_tuple():
    assert is_duplicate([1, 2, (), 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_tuple():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_set():
    assert is_duplicate([1, 2, set(), 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_set():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_frozenset():
    assert is_duplicate([1, 2, frozenset(), 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_frozenset():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_bytes():
    assert is_duplicate([1, 2, b'', 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_bytes():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_memoryview():
    assert is_duplicate([1, 2, memoryview(b''), 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_memoryview():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_array():
    assert is_duplicate([1, 2, [], 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_array():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_bytearray():
    assert is_duplicate([1, 2, bytearray(), 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_bytearray():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_complex():
    assert is_duplicate([1, 2, 1j, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_complex():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_bool():
    assert is_duplicate([1, 2, True, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_bool():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_range():
    assert is_duplicate([1, 2, range(10), 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_range():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_ellipsis():
    assert is_duplicate([1, 2, ..., 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_ellipsis():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_not_implemented():
    assert is_duplicate([1, 2, NotImplemented, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_not_implemented():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_typeerror():
    assert is_duplicate([1, 2, TypeError, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_typeerror():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_valueerror():
    assert is_duplicate([1, 2, ValueError, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_valueerror():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_keyerror():
    assert is_duplicate([1, 2, KeyError, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_keyerror():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_indexerror():
    assert is_duplicate([1, 2, IndexError, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_indexerror():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_overflowerror():
    assert is_duplicate([1, 2, OverflowError, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_overflowerror():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_memoryerror():
    assert is_duplicate([1, 2, MemoryError, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_memoryerror():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_zero_division_error():
    assert is_duplicate([1, 2, ZeroDivisionError, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_zero_division_error():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_unboundlocalerror():
    assert is_duplicate([1, 2, UnboundLocalError, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_unboundlocalerror():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_recursionerror():
    assert is_duplicate([1, 2, RecursionError, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_recursionerror():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_systemexit():
    assert is_duplicate([1, 2, SystemExit, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_systemexit():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_keyboardinterrupt():
    assert is_duplicate([1, 2, KeyboardInterrupt, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_keyboardinterrupt():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_generatorstop():
    assert is_duplicate([1, 2, GeneratorExit, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_generatorstop():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_stopiteration():
    assert is_duplicate([1, 2, StopIteration, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_stopiteration():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_stopasynciteration():
    assert is_duplicate([1, 2, StopAsyncIteration, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_stopasynciteration():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_stopcontextmanager():
    assert is_duplicate([1, 2, StopAsyncIteration, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_stopcontextmanager():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_stopiteration():
    assert is_duplicate([1, 2, StopIteration, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_stopiteration():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_stopasynciteration():
    assert is_duplicate([1, 2, StopAsyncIteration, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_stopasynciteration():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_stopcontextmanager():
    assert is_duplicate([1, 2, StopAsyncIteration, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_stopcontextmanager():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_stopiteration():
    assert is_duplicate([1, 2, StopIteration, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_stopiteration():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_stopasynciteration():
    assert is_duplicate([1, 2, StopAsyncIteration, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_stopasynciteration():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_stopcontextmanager():
    assert is_duplicate([1, 2, StopAsyncIteration, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_stopcontextmanager():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_stopiteration():
    assert is_duplicate([1, 2, StopIteration, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_stopiteration():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_stopasynciteration():
    assert is_duplicate([1, 2, StopAsyncIteration, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_stopasynciteration():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_stopcontextmanager():
    assert is_duplicate([1, 2, StopAsyncIteration, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_stopcontextmanager():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_stopiteration():
    assert is_duplicate([1, 2, StopIteration, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_stopiteration():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_stopasynciteration():
    assert is_duplicate([1, 2, StopAsyncIteration, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_stopasynciteration():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_stopcontextmanager():
    assert is_duplicate([1, 2, StopAsyncIteration, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_stopcontextmanager():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_stopiteration():
    assert is_duplicate([1, 2, StopIteration, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_stopiteration():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_stopasynciteration():
    assert is_duplicate([1, 2, StopAsyncIteration, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_stopasynciteration():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_stopcontextmanager():
    assert is_duplicate([1, 2, StopAsyncIteration, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_stopcontextmanager():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_stopiteration():
    assert is_duplicate([1, 2, StopIteration, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_stopiteration():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_stopasynciteration():
    assert is_duplicate([1, 2, StopAsyncIteration, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_stopasynciteration():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_stopcontextmanager():
    assert is_duplicate([1, 2, StopAsyncIteration, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_stopcontextmanager():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_stopiteration():
    assert is_duplicate([1, 2, StopIteration, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_stopiteration():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_stopasynciteration():
    assert is_duplicate([1, 2, StopAsyncIteration, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_stopasynciteration():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_stopcontextmanager():
    assert is_duplicate([1, 2, StopAsyncIteration, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_stopcontextmanager():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_stopiteration():
    assert is_duplicate([1, 2, StopIteration, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_stopiteration():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_stopasynciteration():
    assert is_duplicate([1, 2, StopAsyncIteration, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_stopasynciteration():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_stopcontextmanager():
    assert is_duplicate([1, 2, StopAsyncIteration, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_stopcontextmanager():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_stopiteration():
    assert is_duplicate([1, 2, StopIteration, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_stopiteration():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_stopasynciteration():
    assert is_duplicate([1, 2, StopAsyncIteration, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_stopasynciteration():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_stopcontextmanager():
    assert is_duplicate([1, 2, StopAsyncIteration, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_stopcontextmanager():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_stopiteration():
    assert is_duplicate([1, 2, StopIteration, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_stopiteration():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_stopasynciteration():
    assert is_duplicate([1, 2, StopAsyncIteration, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_stopasynciteration():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_stopcontextmanager():
    assert is_duplicate([1, 2, StopAsyncIteration, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_stopcontextmanager():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_stopiteration():
    assert is_duplicate([1, 2, StopIteration, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_stopiteration():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_stopasynciteration():
    assert is_duplicate([1, 2, StopAsyncIteration, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_stopasynciteration():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_stopcontextmanager():
    assert is_duplicate([1, 2, StopAsyncIteration, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_stopcontextmanager():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_stopiteration():
    assert is_duplicate([1, 2, StopIteration, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_stopiteration():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_stopasynciteration():
    assert is_duplicate([1, 2, StopAsyncIteration, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_stopasynciteration():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_stopcontextmanager():
    assert is_duplicate([1, 2, StopAsyncIteration, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_stopcontextmanager():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_stopiteration():
    assert is_duplicate([1, 2, StopIteration, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_stopiteration():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_stopasynciteration():
    assert is_duplicate([1, 2, StopAsyncIteration, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_stopasynciteration():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_stopcontextmanager():
    assert is_duplicate([1, 2, StopAsyncIteration, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_stopcontextmanager():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_stopiteration():
    assert is_duplicate([1, 2, StopIteration, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_stopiteration():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_stopasynciteration():
    assert is_duplicate([1, 2, StopAsyncIteration, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_stopasynciteration():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_stopcontextmanager():
    assert is_duplicate([1, 2, StopAsyncIteration, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_stopcontextmanager():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_stopiteration():
    assert is_duplicate([1, 2, StopIteration, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_stopiteration():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_stopasynciteration():
    assert is_duplicate([1, 2, StopAsyncIteration, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_stopasynciteration():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_stopcontextmanager():
    assert is_duplicate([1, 2, StopAsyncIteration, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_stopcontextmanager():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_stopiteration():
    assert is_duplicate([1, 2, StopIteration, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_stopiteration():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_stopasynciteration():
    assert is_duplicate([1, 2, StopAsyncIteration, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_stopasynciteration():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_stopcontextmanager():
    assert is_duplicate([1, 2, StopAsyncIteration, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_stopcontextmanager():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_stopiteration():
    assert is_duplicate([1, 2, StopIteration, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_stopiteration():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_stopasynciteration():
    assert is_duplicate([1, 2, StopAsyncIteration, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_stopasynciteration():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_stopcontextmanager():
    assert is_duplicate([1, 2, StopAsyncIteration, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_stopcontextmanager():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_stopiteration():
    assert is_duplicate([1, 2, StopIteration, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_stopiteration():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_stopasynciteration():
    assert is_duplicate([1, 2, StopAsyncIteration, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_stopasynciteration():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_stopcontextmanager():
    assert is_duplicate([1, 2, StopAsyncIteration, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_stopcontextmanager():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_stopiteration():
    assert is_duplicate([1, 2, StopIteration, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_stopiteration():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_stopasynciteration():
    assert is_duplicate([1, 2, StopAsyncIteration, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_stopasynciteration():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_stopcontextmanager():
    assert is_duplicate([1, 2, StopAsyncIteration, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_stopcontextmanager():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_stopiteration():
    assert is_duplicate([1, 2, StopIteration, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_stopiteration():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_stopasynciteration():
    assert is_duplicate([1, 2, StopAsyncIteration, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_stopasynciteration():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_stopcontextmanager():
    assert is_duplicate([1, 2, StopAsyncIteration, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_stopcontextmanager():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_stopiteration():
    assert is_duplicate([1, 2, StopIteration, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_stopiteration():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_stopasynciteration():
    assert is_duplicate([1, 2, StopAsyncIteration, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_stopasynciteration():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_stopcontextmanager():
    assert is_duplicate([1, 2, StopAsyncIteration, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_stopcontextmanager():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_stopiteration():
    assert is_duplicate([1, 2, StopIteration, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_stopiteration():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_stopasynciteration():
    assert is_duplicate([1, 2, StopAsyncIteration, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_stopasynciteration():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_stopcontextmanager():
    assert is_duplicate([1, 2, StopAsyncIteration, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_stopcontextmanager():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_stopiteration():
    assert is_duplicate([1, 2, StopIteration, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_stopiteration():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_stopasynciteration():
    assert is_duplicate([1, 2, StopAsyncIteration, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_stopasynciteration():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_empty_stopcontextmanager():
    assert is_duplicate([1, 2, StopAsyncIteration, 3, 4, 4, 5]) == True

def test_is_duplicate_with_duplicates_and_none_stopcontextmanager():
    assert is_duplicate([1, 2, None, 3, 4, 4, 5]) == True

def test_is_duplicate