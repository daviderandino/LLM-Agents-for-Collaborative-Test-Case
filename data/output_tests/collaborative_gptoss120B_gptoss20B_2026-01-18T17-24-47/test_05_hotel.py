import pytest
import datetime
from data.input_code.05_hotel import *

# Helper to get a date offset from today
def future(days: int) -> datetime.date:
    return datetime.date.today() + datetime.timedelta(days=days)

# ----------------------------------------------------------------------
# Fixtures
# ----------------------------------------------------------------------
@pytest.fixture
def empty_system():
    """A fresh HotelReservationSystem with no rooms."""
    return HotelReservationSystem()


@pytest.fixture
def system_with_rooms():
    """System with two rooms added (101 and 102)."""
    sys = HotelReservationSystem()
    sys.add_room(101, "Deluxe", 150.0)
    sys.add_room(102, "Standard", 100.0)
    return sys


@pytest.fixture
def system_with_overlap_reservation(system_with_rooms):
    """
    System that already has a reservation for room 101.
    The reservation is set in the future relative to the current date.
    """
    check_in = future(30)          # 30 days from today
    check_out = check_in + datetime.timedelta(days=5)  # 5‑night stay
    system_with_rooms.book_room(
        room_number=101,
        user_name="Existing",
        check_in=check_in,
        check_out=check_out,
    )
    return system_with_rooms


# ----------------------------------------------------------------------
# Tests for add_room
# ----------------------------------------------------------------------
@pytest.mark.parametrize(
    "room_number, room_type, price, expect_exception",
    [
        (101, "Deluxe", 150.0, None),          # T1 – valid addition
        (102, "Standard", 0.0, ValueError),   # T2 – non‑positive price
    ],
)
def test_add_room(empty_system, room_number, room_type, price, expect_exception):
    if expect_exception:
        with pytest.raises(expect_exception):
            empty_system.add_room(room_number, room_type, price)
    else:
        empty_system.add_room(room_number, room_type, price)
        assert room_number in empty_system.rooms
        assert empty_system.rooms[room_number]["price_per_night"] == price


# ----------------------------------------------------------------------
# Tests for _is_room_available
# ----------------------------------------------------------------------
@pytest.mark.parametrize(
    "check_in_offset, check_out_offset, expected",
    [
        (32, 38, False),  # T3 – overlaps with existing reservation (30‑35)
        (36, 40, True),   # T4 – starts after existing reservation ends
    ],
)
def test_is_room_available(system_with_overlap_reservation,
                           check_in_offset, check_out_offset, expected):
    check_in = future(check_in_offset)
    check_out = future(check_out_offset)
    result = system_with_overlap_reservation._is_room_available(
        room_number=101,
        check_in=check_in,
        check_out=check_out,
    )
    assert result is expected


# ----------------------------------------------------------------------
# Tests for book_room error handling
# ----------------------------------------------------------------------
@pytest.mark.parametrize(
    "room_number, user_name, check_in, check_out, expected_exc",
    [
        (999, "Alice", future(60), future(64), RoomNotFoundError),          # T5 – room missing
        (101, "Bob", future(70), future(70), InvalidDateError),           # T6 – same day
        (101, "Carol", datetime.date.today() - datetime.timedelta(days=10),
         datetime.date.today() - datetime.timedelta(days=5), InvalidDateError),  # T7 – past dates
        (101, "Dave", future(32), future(38), RoomUnavailableError),      # T8 – overlaps
    ],
)
def test_book_room_errors(system_with_overlap_reservation,
                          room_number, user_name, check_in, check_out, expected_exc):
    with pytest.raises(expected_exc):
        system_with_overlap_reservation.book_room(
            room_number=room_number,
            user_name=user_name,
            check_in=check_in,
            check_out=check_out,
        )


def test_book_room_success(system_with_rooms):
    """T9 – successful booking returns the first reservation ID."""
    res_id = system_with_rooms.book_room(
        room_number=101,
        user_name="Eve",
        check_in=future(90),
        check_out=future(94),   # 4 nights
    )
    assert res_id == "RES-0001"
    assert res_id in system_with_rooms.reservations
    reservation = system_with_rooms.reservations[res_id]
    assert reservation.room_number == 101
    assert reservation.user_name == "Eve"


# ----------------------------------------------------------------------
# Tests for cancel_reservation
# ----------------------------------------------------------------------
def test_cancel_reservation_not_found(system_with_rooms):
    """T10 – cancelling a non‑existent reservation."""
    with pytest.raises(ReservationNotFoundError):
        system_with_rooms.cancel_reservation("RES-9999")


@pytest.mark.parametrize(
    "days_until_checkin, expected_refund",
    [
        (10, 200.0),   # T11 – >7 days → full refund (2 nights × 100)
        (5, 100.0),    # T12 – 2‑7 days → 50% refund
        (1, 0.0),      # T13 – <2 days → no refund
    ],
)
def test_cancel_reservation_refund(system_with_rooms, days_until_checkin, expected_refund):
    """Create a reservation with a known total price and cancel it."""
    today = datetime.date.today()
    check_in = today + datetime.timedelta(days=days_until_checkin)
    check_out = check_in + datetime.timedelta(days=2)  # 2 nights
    # price per night = 100.0 (room 102)
    res_id = system_with_rooms.book_room(
        room_number=102,
        user_name="Tester",
        check_in=check_in,
        check_out=check_out,
    )
    # total_price = 2 * 100 = 200.0
    refund = system_with_rooms.cancel_reservation(res_id)
    assert refund == expected_refund


# ----------------------------------------------------------------------
# Tests for get_room_occupancy
# ----------------------------------------------------------------------
def test_get_room_occupancy_empty(system_with_rooms):
    """T14 – no reservations on the given date."""
    date = future(200)
    assert system_with_rooms.get_room_occupancy(date) == []


def test_get_room_occupancy_sorted():
    """T15 – two rooms occupied on the same date, result sorted."""
    sys = HotelReservationSystem()
    sys.add_room(101, "Deluxe", 150.0)
    sys.add_room(102, "Standard", 100.0)

    # Both reservations cover the same future date
    sys.book_room(
        room_number=101,
        user_name="User1",
        check_in=future(300),
        check_out=future(310),
    )
    sys.book_room(
        room_number=102,
        user_name="User2",
        check_in=future(305),
        check_out=future(308),
    )

    occupied = sys.get_room_occupancy(future(306))
    assert occupied == [101, 102]