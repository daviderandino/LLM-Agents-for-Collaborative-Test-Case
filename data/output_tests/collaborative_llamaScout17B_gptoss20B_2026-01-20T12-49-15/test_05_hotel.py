import pytest
import datetime
from datetime import timedelta
from data.input_code.05_hotel import *

@pytest.fixture
def system():
    return HotelReservationSystem()

# ---------- add_room ----------
@pytest.mark.parametrize(
    "room_number, room_type, price_per_night, expected_exception",
    [
        (101, "single", 100.0, None),
        (102, "double", 0.0, ValueError),
    ],
)
def test_add_room(system, room_number, room_type, price_per_night, expected_exception):
    if expected_exception:
        with pytest.raises(expected_exception):
            system.add_room(room_number, room_type, price_per_night)
    else:
        system.add_room(room_number, room_type, price_per_night)
        assert room_number in system.rooms
        # The key for the room type is stored as 'XXtypeXX'
        assert system.rooms[room_number]["XXtypeXX"] == room_type
        assert system.rooms[room_number]["price_per_night"] == price_per_night

# ---------- book_room ----------
def test_book_room_success(system):
    system.add_room(101, "single", 100.0)
    today = datetime.date.today()
    check_in = today + timedelta(days=10)
    check_out = today + timedelta(days=12)
    res_id = system.book_room(101, "John Doe", check_in, check_out)
    assert "RES-0001" in res_id

def test_book_room_room_not_found(system):
    today = datetime.date.today()
    check_in = today + timedelta(days=10)
    check_out = today + timedelta(days=12)
    with pytest.raises(RoomNotFoundError):
        system.book_room(103, "Jane Doe", check_in, check_out)

def test_book_room_invalid_dates_same_day(system):
    system.add_room(101, "single", 100.0)
    today = datetime.date.today()
    check_in = today + timedelta(days=10)
    check_out = check_in
    with pytest.raises(InvalidDateError):
        system.book_room(101, "John Doe", check_in, check_out)

def test_book_room_invalid_dates_past(system):
    system.add_room(101, "single", 100.0)
    today = datetime.date.today()
    check_in = today - timedelta(days=5)
    check_out = today - timedelta(days=3)
    with pytest.raises(InvalidDateError):
        system.book_room(101, "John Doe", check_in, check_out)

def test_book_room_unavailable(system):
    system.add_room(101, "single", 100.0)
    today = datetime.date.today()
    check_in = today + timedelta(days=10)
    check_out = today + timedelta(days=12)
    # Precondition: book the room first
    system.book_room(101, "Jane Doe", check_in, check_out)
    # Attempt to book the same room for overlapping dates
    with pytest.raises(RoomUnavailableError):
        system.book_room(101, "John Doe", check_in, check_out)

# ---------- cancel_reservation ----------
def test_cancel_reservation_success(system):
    system.add_room(101, "single", 100.0)
    today = datetime.date.today()
    check_in = today + timedelta(days=10)
    check_out = today + timedelta(days=12)
    # Precondition: book a reservation
    res_id = system.book_room(101, "John Doe", check_in, check_out)
    # Cancel the reservation
    refund = system.cancel_reservation(res_id)
    assert refund == 200.0

def test_cancel_reservation_not_found(system):
    with pytest.raises(ReservationNotFoundError):
        system.cancel_reservation("RES-9999")

# ---------- get_room_occupancy ----------
def test_get_room_occupancy(system):
    system.add_room(101, "single", 100.0)
    today = datetime.date.today()
    check_in = today + timedelta(days=10)
    check_out = today + timedelta(days=12)
    # Precondition: book a reservation
    system.book_room(101, "John Doe", check_in, check_out)
    occupancy_date = today + timedelta(days=11)
    occupancy = system.get_room_occupancy(occupancy_date)
    assert occupancy == [101]

import pytest
from data.input_code.05_hotel import *
import datetime
from datetime import timedelta

def test_book_room_edge_case(system):
    system.add_room(101, "single", 100.0)
    check_in = datetime.date.today() + timedelta(days=7)
    check_out = datetime.date.today() + timedelta(days=14)
    res_id = system.book_room(101, "John Doe", check_in, check_out)
    assert res_id == "RES-0001"

def test_cancel_reservation_edge_case(system):
    system.add_room(101, "single", 50.0)
    check_in = datetime.date.today() + timedelta(days=10)
    check_out = datetime.date.today() + timedelta(days=12)
    res_id = system.book_room(101, "John Doe", check_in, check_out)
    assert res_id == "RES-0001"
    refund = system.cancel_reservation(res_id)
    assert refund == 100.0

def test_cancel_reservation_boundary(system):
    system.add_room(101, "single", 100.0)
    check_in = datetime.date.today() + timedelta(days=7)
    check_out = datetime.date.today() + timedelta(days=9)
    res_id = system.book_room(101, "John Doe", check_in, check_out)
    assert res_id == "RES-0001"
    refund = system.cancel_reservation(res_id)
    assert refund == 100.0

def test_get_room_occupancy_edge_case(system):
    occupancy_date = datetime.date.today() - timedelta(days=1)
    occupancy = system.get_room_occupancy(occupancy_date)
    assert occupancy == []

def test_book_room_multiple_reservations(system):
    system.add_room(101, "single", 100.0)
    system.add_room(102, "double", 100.0)
    # First reservation
    check_in1 = datetime.date.today() + timedelta(days=5)
    check_out1 = datetime.date.today() + timedelta(days=7)
    res_id1 = system.book_room(101, "Alice", check_in1, check_out1)
    assert res_id1 == "RES-0001"
    # Second reservation
    check_in2 = datetime.date.today() + timedelta(days=10)
    check_out2 = datetime.date.today() + timedelta(days=12)
    res_id2 = system.book_room(102, "Jane Doe", check_in2, check_out2)
    assert res_id2 == "RES-0002"

import pytest
import datetime
from datetime import timedelta
from data.input_code.05_hotel import *

def test_cancel_reservation_2_days_before_checkin(system):
    system.add_room(101, "single", 50.0)
    today = datetime.date.today()
    check_in = today + timedelta(days=2)
    check_out = today + timedelta(days=4)
    res_id = system.book_room(101, "Alice", check_in, check_out)
    assert res_id == "RES-0001"
    refund = system.cancel_reservation(res_id)
    assert refund == 50.0

def test_cancel_reservation_1_day_before_checkin(system):
    system.add_room(101, "single", 50.0)
    today = datetime.date.today()
    check_in = today + timedelta(days=1)
    check_out = today + timedelta(days=3)
    res_id = system.book_room(101, "Bob", check_in, check_out)
    assert res_id == "RES-0001"
    refund = system.cancel_reservation(res_id)
    assert refund == 0.0

def test_book_room_same_day_checkin(system):
    system.add_room(101, "single", 100.0)
    today = datetime.date.today()
    check_in = today + timedelta(days=10)
    check_out = today + timedelta(days=12)
    res_id = system.book_room(101, "John Doe", check_in, check_out)
    assert res_id == "RES-0001"

def test_get_room_occupancy_checkin_date(system):
    system.add_room(101, "single", 100.0)
    today = datetime.date.today()
    check_in = today + timedelta(days=10)
    check_out = today + timedelta(days=12)
    system.book_room(101, "John Doe", check_in, check_out)
    occupancy_date = today + timedelta(days=10)
    occupancy = system.get_room_occupancy(occupancy_date)
    assert occupancy == [101]

def test_get_room_occupancy_checkout_date(system):
    system.add_room(101, "single", 100.0)
    today = datetime.date.today()
    check_in = today + timedelta(days=10)
    check_out = today + timedelta(days=12)
    system.book_room(101, "John Doe", check_in, check_out)
    occupancy_date = today + timedelta(days=12)
    occupancy = system.get_room_occupancy(occupancy_date)
    assert occupancy == []