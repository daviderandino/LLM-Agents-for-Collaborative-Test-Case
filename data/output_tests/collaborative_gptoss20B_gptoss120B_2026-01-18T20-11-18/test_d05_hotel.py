import pytest
import datetime
from data.input_code.d05_hotel import *

@pytest.fixture
def system(monkeypatch):
    # Freeze today's date to 2023-01-01 for deterministic tests
    fixed_today = datetime.date(2023, 1, 1)

    class FixedDate(datetime.date):
        @classmethod
        def today(cls):
            return fixed_today

    monkeypatch.setattr(datetime, 'date', FixedDate)

    sys = HotelReservationSystem()
    # Add rooms
    sys.add_room(101, 'Deluxe', 150.0)
    sys.add_room(102, 'Standard', 120.0)
    sys.add_room(103, 'Suite', 200.0)
    sys.add_room(202, 'Standard', 100.0)

    # Create reservations for refund and occupancy tests
    # RES-0001: full refund (>7 days)
    sys.book_room(102, 'User1', datetime.date(2023, 1, 25), datetime.date(2023, 1, 30))
    # RES-0002: half refund (2-7 days)
    sys.book_room(103, 'User2', datetime.date(2023, 1, 5), datetime.date(2023, 1, 10))
    # RES-0003: no refund (<2 days)
    sys.book_room(202, 'User3', datetime.date(2023, 1, 2), datetime.date(2023, 1, 4))
    # RES-0004: occupancy on 2023-01-11
    sys.book_room(101, 'User4', datetime.date(2023, 1, 10), datetime.date(2023, 1, 12))
    # RES-0005: occupancy on 2023-01-13 (room 101)
    sys.book_room(101, 'User5', datetime.date(2023, 1, 12), datetime.date(2023, 1, 14))
    # RES-0006: occupancy on 2023-01-13 (room 202)
    sys.book_room(202, 'User6', datetime.date(2023, 1, 13), datetime.date(2023, 1, 15))

    return sys

# ---------- Add Room Tests ----------
@pytest.mark.parametrize(
    "room_number, room_type, price_per_night",
    [
        (101, "Deluxe", 150.0),
        (102, "Standard", 120.0),
    ],
)
def test_add_room_success(system, room_number, room_type, price_per_night):
    system.add_room(room_number, room_type, price_per_night)
    assert room_number in system.rooms
    assert system.rooms[room_number]["type"] == room_type
    assert system.rooms[room_number]["price_per_night"] == price_per_night

@pytest.mark.parametrize(
    "room_number, room_type, price_per_night",
    [
        (103, "Suite", 0),
        (104, "Deluxe", -50),
    ],
)
def test_add_room_invalid_price(system, room_number, room_type, price_per_night):
    with pytest.raises(ValueError):
        system.add_room(room_number, room_type, price_per_night)

# ---------- Book Room Tests ----------
def test_book_room_success(system):
    # Free the room that is already booked for the same dates
    system.cancel_reservation("RES-0004")
    res_id = system.book_room(
        101,
        "Alice",
        datetime.date(2023, 1, 10),
        datetime.date(2023, 1, 12),
    )
    assert res_id == "RES-0007"

def test_book_room_room_not_found(system):
    with pytest.raises(RoomNotFoundError):
        system.book_room(
            999,
            "Bob",
            datetime.date(2023, 1, 10),
            datetime.date(2023, 1, 12),
        )

def test_book_room_invalid_dates_checkin_after_checkout(system):
    with pytest.raises(InvalidDateError):
        system.book_room(
            101,
            "Carol",
            datetime.date(2023, 1, 15),
            datetime.date(2023, 1, 10),
        )

def test_book_room_invalid_dates_checkin_equals_checkout(system):
    with pytest.raises(InvalidDateError):
        system.book_room(
            101,
            "Dave",
            datetime.date(2023, 1, 10),
            datetime.date(2023, 1, 10),
        )

def test_book_room_past_checkin(system):
    with pytest.raises(InvalidDateError):
        system.book_room(
            101,
            "Eve",
            datetime.date(2022, 12, 31),
            datetime.date(2023, 1, 2),
        )

def test_book_room_unavailable(system):
    # Free the room that is already booked for the same dates
    system.cancel_reservation("RES-0004")
    # First book a reservation that occupies the room
    system.book_room(
        101,
        "Frank",
        datetime.date(2023, 1, 10),
        datetime.date(2023, 1, 12),
    )
    # Attempt to book overlapping dates
    with pytest.raises(RoomUnavailableError):
        system.book_room(
            101,
            "Grace",
            datetime.date(2023, 1, 11),
            datetime.date(2023, 1, 13),
        )

# ---------- Cancel Reservation Tests ----------
@pytest.mark.parametrize(
    "reservation_id, expected_refund",
    [
        ("RES-0002", 500.0),  # half refund
        ("RES-0003", 0.0),    # no refund
        ("RES-0004", 300.0),  # full refund
    ],
)
def test_cancel_reservation(system, reservation_id, expected_refund):
    refund = system.cancel_reservation(reservation_id)
    assert refund == expected_refund

def test_cancel_reservation_not_found(system):
    with pytest.raises(ReservationNotFoundError):
        system.cancel_reservation("RES-9999")

# ---------- Get Room Occupancy Tests ----------
@pytest.mark.parametrize(
    "date_str, expected_rooms",
    [
        ("2023-01-20", []),          # no active reservations
        ("2023-01-11", [101]),       # single reservation
        ("2023-01-13", [101, 202]),  # multiple overlapping reservations
        ("2023-01-15", []),          # edge case: check_out date
    ],
)
def test_get_room_occupancy(system, date_str, expected_rooms):
    date = datetime.date.fromisoformat(date_str)
    occupied = system.get_room_occupancy(date)
    assert occupied == expected_rooms