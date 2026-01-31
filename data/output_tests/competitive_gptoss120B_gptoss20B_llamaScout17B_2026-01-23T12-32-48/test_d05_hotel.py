import pytest
import datetime
from data.input_code.d05_hotel import *

# ---------- Add Room ----------
@pytest.mark.parametrize(
    "room_number, room_type, price_per_night, expected_exception",
    [
        (101, "single", 100.0, None),
        (102, "double", 0.0, ValueError),
    ],
)
def test_add_room(room_number, room_type, price_per_night, expected_exception):
    system = HotelReservationSystem()
    if expected_exception:
        with pytest.raises(expected_exception):
            system.add_room(room_number, room_type, price_per_night)
    else:
        system.add_room(room_number, room_type, price_per_night)
        assert room_number in system.rooms
        assert system.rooms[room_number]["price_per_night"] == price_per_night


# ---------- Book Room ----------
def test_book_success():
    system = HotelReservationSystem()
    system.add_room(101, "single", 100.0)
    res_id = system.book_room(
        101,
        "Alice",
        datetime.date(2099, 1, 2),
        datetime.date(2099, 1, 4),
    )
    assert res_id == "RES-0001"
    assert res_id in system.reservations
    res = system.reservations[res_id]
    assert res.room_number == 101
    assert res.user_name == "Alice"
    assert res.check_in == datetime.date(2099, 1, 2)
    assert res.check_out == datetime.date(2099, 1, 4)
    assert res.total_price == 200.0


def test_book_room_not_found():
    system = HotelReservationSystem()
    system.add_room(101, "single", 100.0)
    with pytest.raises(RoomNotFoundError):
        system.book_room(
            999,
            "Bob",
            datetime.date(2099, 2, 1),
            datetime.date(2099, 2, 3),
        )


def test_book_invalid_dates_order():
    system = HotelReservationSystem()
    system.add_room(101, "single", 100.0)
    with pytest.raises(InvalidDateError):
        system.book_room(
            101,
            "Carol",
            datetime.date(2099, 3, 5),
            datetime.date(2099, 3, 5),
        )


def test_book_past_date():
    system = HotelReservationSystem()
    system.add_room(101, "single", 100.0)
    past_date = datetime.date.today() - datetime.timedelta(days=1)
    future_date = past_date + datetime.timedelta(days=2)
    with pytest.raises(InvalidDateError):
        system.book_room(101, "Dave", past_date, future_date)


def test_book_unavailable():
    system = HotelReservationSystem()
    system.add_room(101, "single", 100.0)
    # First reservation
    system.book_room(
        101,
        "Alice",
        datetime.date(2099, 1, 2),
        datetime.date(2099, 1, 4),
    )
    # Overlapping reservation
    with pytest.raises(RoomUnavailableError):
        system.book_room(
            101,
            "Eve",
            datetime.date(2099, 1, 3),
            datetime.date(2099, 1, 5),
        )


# ---------- Cancel Reservation ----------
def _create_system_with_reservations():
    """Helper to create a system with three future reservations."""
    system = HotelReservationSystem()
    system.add_room(101, "single", 100.0)
    # Reservation 1: far future >7 days
    system.book_room(
        101,
        "User1",
        datetime.date(2099, 1, 10),
        datetime.date(2099, 1, 12),
    )
    # Reservation 2: far future >7 days
    system.book_room(
        101,
        "User2",
        datetime.date(2099, 1, 15),
        datetime.date(2099, 1, 17),
    )
    # Reservation 3: far future >7 days
    system.book_room(
        101,
        "User3",
        datetime.date(2099, 1, 20),
        datetime.date(2099, 1, 22),
    )
    return system


def test_cancel_full_refund():
    system = _create_system_with_reservations()
    # Reservation 4: far future >7 days
    res_id = system.book_room(
        101,
        "User4",
        datetime.date(2099, 1, 25),
        datetime.date(2099, 1, 27),
    )
    assert res_id == "RES-0004"
    # Cancel reservation 4
    refund = system.cancel_reservation(res_id)
    # Total price for 2 nights at $100
    assert refund == 200.0


def test_cancel_half_refund():
    system = _create_system_with_reservations()
    # Reservation 4: 5 days ahead
    future_date = datetime.date.today() + datetime.timedelta(days=5)
    res_id = system.book_room(
        101,
        "User4",
        future_date,
        future_date + datetime.timedelta(days=2),
    )
    assert res_id == "RES-0004"
    refund = system.cancel_reservation(res_id)
    # Total price for 2 nights at $100
    assert refund == 100.0


def test_cancel_no_refund():
    system = _create_system_with_reservations()
    # Reservation 4: 1 day ahead
    future_date = datetime.date.today() + datetime.timedelta(days=1)
    res_id = system.book_room(
        101,
        "User4",
        future_date,
        future_date + datetime.timedelta(days=2),
    )
    assert res_id == "RES-0004"
    refund = system.cancel_reservation(res_id)
    assert refund == 0.0


def test_cancel_not_found():
    system = HotelReservationSystem()
    system.add_room(101, "single", 100.0)
    with pytest.raises(ReservationNotFoundError):
        system.cancel_reservation("NON_EXISTENT")


# ---------- Get Room Occupancy ----------
def test_get_room_occupancy_occupied():
    system = HotelReservationSystem()
    system.add_room(101, "single", 100.0)
    system.book_room(
        101,
        "Alice",
        datetime.date(2099, 1, 2),
        datetime.date(2099, 1, 4),
    )
    occupied = system.get_room_occupancy(datetime.date(2099, 1, 2))
    assert occupied == [101]


def test_get_room_occupancy_empty():
    system = HotelReservationSystem()
    system.add_room(101, "single", 100.0)
    occupied = system.get_room_occupancy(datetime.date(2099, 12, 31))
    assert occupied == []