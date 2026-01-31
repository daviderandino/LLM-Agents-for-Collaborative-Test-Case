import pytest
import datetime
from data.input_code.d05_hotel import *

# ----------------------------------------------------------------------
# Fixtures
# ----------------------------------------------------------------------
@pytest.fixture
def system():
    """Provides a fresh HotelReservationSystem for each test."""
    return HotelReservationSystem()

@pytest.fixture
def fixed_today(monkeypatch):
    """Helper to patch datetime.date.today() to a desired date."""
    def _set(date):
        class FixedDate(datetime.date):
            @classmethod
            def today(cls):
                return date
        monkeypatch.setattr(datetime, "date", FixedDate)
    return _set

# ----------------------------------------------------------------------
# Test add_room
# ----------------------------------------------------------------------
@pytest.mark.parametrize(
    "room_number, room_type, price, expect_exception",
    [
        (101, "Deluxe", 150.0, None),          # TC01_add_room_success
        (102, "Standard", 0, ValueError),     # TC02_add_room_invalid_price
    ],
)
def test_add_room(system, room_number, room_type, price, expect_exception):
    if expect_exception:
        with pytest.raises(expect_exception):
            system.add_room(room_number, room_type, price)
    else:
        system.add_room(room_number, room_type, price)
        assert room_number in system.rooms
        assert system.rooms[room_number]["price_per_night"] == price

# ----------------------------------------------------------------------
# Test book_room – happy path and error branches
# ----------------------------------------------------------------------
def test_book_room_success(system, fixed_today):
    # set today so that check‑in is in the future (>7 days)
    fixed_today(datetime.date(2099, 1, 1))
    system.add_room(101, "Deluxe", 150.0)
    res_id = system.book_room(
        101,
        "Alice",
        datetime.date(2099, 1, 10),
        datetime.date(2099, 1, 15),
    )
    assert res_id == "RES-0001"

def test_book_room_not_found(system):
    system.add_room(101, "Deluxe", 150.0)
    with pytest.raises(RoomNotFoundError):
        system.book_room(
            999,
            "Bob",
            datetime.date(2099, 2, 1),
            datetime.date(2099, 2, 5),
        )

def test_book_room_invalid_dates_same_day(system):
    system.add_room(101, "Deluxe", 150.0)
    with pytest.raises(InvalidDateError):
        system.book_room(
            101,
            "Carol",
            datetime.date(2099, 3, 10),
            datetime.date(2099, 3, 10),
        )

def test_book_room_invalid_dates_past(system):
    system.add_room(101, "Deluxe", 150.0)
    with pytest.raises(InvalidDateError):
        system.book_room(
            101,
            "Dave",
            datetime.date(2000, 1, 1),
            datetime.date(2000, 1, 5),
        )

def test_book_room_unavailable_overlap(system, fixed_today):
    # today = 2099‑01‑01, create an initial reservation
    fixed_today(datetime.date(2099, 1, 1))
    system.add_room(101, "Deluxe", 150.0)
    system.book_room(
        101,
        "Alice",
        datetime.date(2099, 1, 10),
        datetime.date(2099, 1, 15),
    )
    # overlapping request
    with pytest.raises(RoomUnavailableError):
        system.book_room(
            101,
            "Eve",
            datetime.date(2099, 1, 12),
            datetime.date(2099, 1, 18),
        )

def test_book_room_edge_no_overlap(system, fixed_today):
    # today = 2099‑01‑01, previous reservation ends on 15th
    fixed_today(datetime.date(2099, 1, 1))
    system.add_room(101, "Deluxe", 150.0)
    system.book_room(
        101,
        "Alice",
        datetime.date(2099, 1, 10),
        datetime.date(2099, 1, 15),
    )
    # new reservation starts exactly at previous check_out
    res_id = system.book_room(
        101,
        "Frank",
        datetime.date(2099, 1, 15),
        datetime.date(2099, 1, 20),
    )
    assert res_id == "RES-0002"

# ----------------------------------------------------------------------
# Test cancel_reservation – various refund policies
# ----------------------------------------------------------------------
def test_cancel_reservation_not_found(system):
    with pytest.raises(ReservationNotFoundError):
        system.cancel_reservation("NON-EXISTENT")

def test_cancel_refund_full(system, fixed_today):
    # today far enough from check‑in (>7 days)
    fixed_today(datetime.date(2099, 1, 1))
    system.add_room(101, "Deluxe", 150.0)
    res_id = system.book_room(
        101,
        "Alice",
        datetime.date(2099, 1, 10),
        datetime.date(2099, 1, 15),
    )
    refund = system.cancel_reservation(res_id)
    assert refund == 750.0  # 5 nights × 150.0

def test_cancel_refund_half(system, fixed_today):
    # today such that check‑in is 5 days away (2‑7 days window)
    fixed_today(datetime.date(2099, 1, 10))
    system.add_room(101, "Deluxe", 150.0)
    res_id = system.book_room(
        101,
        "Frank",
        datetime.date(2099, 1, 15),
        datetime.date(2099, 1, 20),
    )
    refund = system.cancel_reservation(res_id)
    assert refund == 375.0  # 50 % of 750.0

def test_cancel_no_refund(system, fixed_today):
    # today such that check‑in is tomorrow (<2 days)
    fixed_today(datetime.date(2099, 1, 10))
    system.add_room(101, "Deluxe", 150.0)
    # create reservation with check‑in tomorrow
    res_id = system.book_room(
        101,
        "Grace",
        datetime.date(2099, 1, 11),
        datetime.date(2099, 1, 13),
    )
    refund = system.cancel_reservation(res_id)
    assert refund == 0.0

# ----------------------------------------------------------------------
# Test get_room_occupancy
# ----------------------------------------------------------------------
def test_get_room_occupancy_occupied(system, fixed_today):
    fixed_today(datetime.date(2099, 1, 1))
    system.add_room(101, "Deluxe", 150.0)
    system.book_room(
        101,
        "Alice",
        datetime.date(2099, 1, 10),
        datetime.date(2099, 1, 15),
    )
    occupied = system.get_room_occupancy(datetime.date(2099, 1, 13))
    assert occupied == [101]

def test_get_room_occupancy_empty(system, fixed_today):
    fixed_today(datetime.date(2099, 1, 1))
    system.add_room(101, "Deluxe", 150.0)
    # No reservations on the queried date
    occupied = system.get_room_occupancy(datetime.date(2099, 2, 1))
    assert occupied == []