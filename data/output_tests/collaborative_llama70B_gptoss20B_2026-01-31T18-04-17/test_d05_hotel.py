import pytest
import datetime
from datetime import timedelta
from data.input_code.d05_hotel import *

@pytest.fixture
def system():
    """Return a fresh HotelReservationSystem with one room added."""
    sys = HotelReservationSystem()
    sys.add_room(1, "single", 100.0)
    return sys

# ---------- add_room ----------
@pytest.mark.parametrize(
    "room_number, room_type, price_per_night, expected_exception",
    [
        (1, "single", 100.0, None),          # T1_OK_add_room
        (1, "single", -100.0, ValueError),   # T2_ERR_add_room
    ],
)
def test_add_room(room_number, room_type, price_per_night, expected_exception):
    sys = HotelReservationSystem()
    if expected_exception is None:
        sys.add_room(room_number, room_type, price_per_night)
        assert sys.rooms[room_number]["price_per_night"] == price_per_night
    else:
        with pytest.raises(expected_exception):
            sys.add_room(room_number, room_type, price_per_night)

# ---------- book_room ----------
def test_book_room_success(system):
    """T3_OK_book_room"""
    today = datetime.date.today()
    check_in = today + timedelta(days=10)
    check_out = check_in + timedelta(days=5)
    res_id = system.book_room(1, "John Doe", check_in, check_out)
    assert res_id == "RES-0001"

def test_book_room_room_not_found(system):
    """T4_ERR_book_room_room_not_found"""
    today = datetime.date.today()
    check_in = today + timedelta(days=10)
    check_out = check_in + timedelta(days=5)
    with pytest.raises(RoomNotFoundError):
        system.book_room(2, "John Doe", check_in, check_out)

def test_book_room_invalid_dates(system):
    """T5_ERR_book_room_invalid_dates"""
    today = datetime.date.today()
    check_in = today + timedelta(days=5)
    check_out = today + timedelta(days=2)  # check_out before check_in
    with pytest.raises(InvalidDateError):
        system.book_room(1, "John Doe", check_in, check_out)

def test_book_room_room_unavailable(system):
    """T6_ERR_book_room_room_unavailable"""
    today = datetime.date.today()
    check_in = today + timedelta(days=10)
    check_out = check_in + timedelta(days=5)
    # First booking succeeds
    system.book_room(1, "John Doe", check_in, check_out)
    # Second booking for same dates should fail
    with pytest.raises(RoomUnavailableError):
        system.book_room(1, "Jane Smith", check_in, check_out)

# ---------- cancel_reservation ----------
def test_cancel_reservation(system):
    """T7_OK_cancel_reservation"""
    today = datetime.date.today()
    check_in = today + timedelta(days=10)
    check_out = check_in + timedelta(days=5)
    res_id = system.book_room(1, "John Doe", check_in, check_out)
    refund = system.cancel_reservation(res_id)
    assert refund == 500.0  # 5 nights * 100.0

def test_cancel_reservation_not_found(system):
    """T8_ERR_cancel_reservation_not_found"""
    with pytest.raises(ReservationNotFoundError):
        system.cancel_reservation("RES-0002")

# ---------- get_room_occupancy ----------
def test_get_room_occupancy(system):
    """T9_OK_get_room_occupancy"""
    today = datetime.date.today()
    check_in = today + timedelta(days=10)
    check_out = check_in + timedelta(days=5)
    system.book_room(1, "John Doe", check_in, check_out)
    # Pick a date within the booking period
    occupancy_date = check_in + timedelta(days=2)
    occupied = system.get_room_occupancy(occupancy_date)
    assert occupied == [1]

def test_get_room_occupancy_empty(system):
    """T10_OK_get_room_occupancy_empty"""
    # Date far in the future where no reservations exist
    future_date = datetime.date.today() + timedelta(days=365)
    occupied = system.get_room_occupancy(future_date)
    assert occupied == []

import pytest
import datetime
from datetime import timedelta
from data.input_code.d05_hotel import *

# ---------- T11_ERR_book_room_past_date ----------
def test_book_room_past_date(system):
    """T11_ERR_book_room_past_date"""
    check_in = datetime.date.today() - timedelta(days=1)
    check_out = datetime.date.today() + timedelta(days=5)
    with pytest.raises(InvalidDateError):
        system.book_room(1, "John Doe", check_in, check_out)

# ---------- T12_OK_cancel_reservation_partial_refund ----------
def test_cancel_reservation_partial_refund(system):
    """T12_OK_cancel_reservation_partial_refund"""
    # Book a room 5 days in advance for 1 night
    check_in = datetime.date.today() + timedelta(days=5)
    check_out = check_in + timedelta(days=1)
    res_id = system.book_room(1, "John Doe", check_in, check_out)
    refund = system.cancel_reservation(res_id)
    assert refund == 50.0  # 50% of 100.0

# ---------- T13_ERR_cancel_reservation_zero_refund ----------
def test_cancel_reservation_zero_refund(system):
    """T13_ERR_cancel_reservation_zero_refund"""
    # Book a room 1 day in advance for 1 night
    check_in = datetime.date.today() + timedelta(days=1)
    check_out = check_in + timedelta(days=1)
    res_id = system.book_room(1, "John Doe", check_in, check_out)
    refund = system.cancel_reservation(res_id)
    assert refund == 0.0

# ---------- T14_OK_get_room_occupancy_multiple_rooms ----------
def test_get_room_occupancy_multiple_rooms(system):
    """T14_OK_get_room_occupancy_multiple_rooms"""
    # Add a second room
    system.add_room(2, "double", 150.0)
    # Book both rooms for the same dates
    check_in = datetime.date.today() + timedelta(days=10)
    check_out = check_in + timedelta(days=5)
    system.book_room(1, "Alice", check_in, check_out)
    system.book_room(2, "Bob", check_in, check_out)
    # Check occupancy on a date within the booking period
    occupancy_date = check_in + timedelta(days=2)
    occupied = system.get_room_occupancy(occupancy_date)
    assert occupied == [1, 2]

# ---------- T15_OK_book_room_same_room_different_dates ----------
def test_book_room_same_room_different_dates(system):
    """T15_OK_book_room_same_room_different_dates"""
    # First booking (RES-0001)
    check_in1 = datetime.date.today() + timedelta(days=15)
    check_out1 = check_in1 + timedelta(days=5)
    system.book_room(1, "John Doe", check_in1, check_out1)
    # Second booking (RES-0002) on non‑overlapping dates
    check_in2 = datetime.date.today() + timedelta(days=25)
    check_out2 = check_in2 + timedelta(days=5)
    res_id = system.book_room(1, "Jane Smith", check_in2, check_out2)
    assert res_id == "RES-0002"