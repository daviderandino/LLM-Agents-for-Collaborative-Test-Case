import pytest
import datetime
from datetime import timedelta
from data.input_code.d05_hotel import *

@pytest.fixture
def system_no_reservations():
    """Hotel system with rooms but no reservations."""
    system = HotelReservationSystem()
    system.add_room(101, "Single", 100.0)
    system.add_room(102, "Double", 150.0)
    system.add_room(103, "Suite", 200.0)
    return system

@pytest.fixture
def system_with_reservation():
    """Hotel system with a reservation for room 101."""
    system = HotelReservationSystem()
    system.add_room(101, "Single", 100.0)
    system.add_room(102, "Double", 150.0)
    system.add_room(103, "Suite", 200.0)
    # Add a reservation for room 101 from 2099-01-01 to 2099-01-05
    system.book_room(
        101,
        "TestUser",
        datetime.date(2099, 1, 1),
        datetime.date(2099, 1, 5)
    )
    return system

@pytest.fixture
def system_for_cancellation():
    """Hotel system with reservations for cancellation tests."""
    system = HotelReservationSystem()
    system.add_room(101, "Single", 100.0)
    system.add_room(102, "Double", 150.0)
    system.add_room(103, "Suite", 200.0)
    today = datetime.date.today()
    # Reservation 1: RES-0001 (used in T11)
    system.book_room(
        102,
        "Eve",
        today + timedelta(days=10),
        today + timedelta(days=15)
    )
    # Reservation 2: RES-0002 (>7 days before check-in)
    system.book_room(
        101,
        "User2",
        today + timedelta(days=10),
        today + timedelta(days=12)
    )
    # Reservation 3: RES-0003 (2-7 days before check-in)
    system.book_room(
        101,
        "User3",
        today + timedelta(days=5),
        today + timedelta(days=7)
    )
    # Reservation 4: RES-0004 (<2 days before check-in)
    system.book_room(
        101,
        "User4",
        today + timedelta(days=1),
        today + timedelta(days=2)
    )
    return system

# ---------- Tests for add_room ----------
@pytest.mark.parametrize(
    "room_number, room_type, price, expected_exception",
    [
        (101, "Single", 100.0, None),
        (102, "Double", 0, ValueError),
        (103, "Suite", -50, ValueError),
    ],
)
def test_add_room(system_no_reservations, room_number, room_type, price, expected_exception):
    if expected_exception:
        with pytest.raises(expected_exception):
            system_no_reservations.add_room(room_number, room_type, price)
    else:
        system_no_reservations.add_room(room_number, room_type, price)
        assert room_number in system_no_reservations.rooms
        assert system_no_reservations.rooms[room_number]["price_per_night"] == price

# ---------- Tests for _is_room_available ----------
def test_is_room_available_no_reservations(system_no_reservations):
    assert system_no_reservations._is_room_available(
        101,
        datetime.date(2099, 1, 1),
        datetime.date(2099, 1, 5)
    ) is True

def test_is_room_available_overlapping(system_with_reservation):
    assert system_with_reservation._is_room_available(
        101,
        datetime.date(2099, 1, 2),
        datetime.date(2099, 1, 4)
    ) is False

def test_is_room_available_non_overlapping(system_with_reservation):
    assert system_with_reservation._is_room_available(
        101,
        datetime.date(2099, 1, 5),
        datetime.date(2099, 1, 10)
    ) is True

# ---------- Tests for book_room ----------
def test_book_room_room_not_found(system_no_reservations):
    with pytest.raises(RoomNotFoundError):
        system_no_reservations.book_room(
            999,
            "Alice",
            datetime.date(2099, 1, 1),
            datetime.date(2099, 1, 5)
        )

def test_book_room_invalid_date_order(system_no_reservations):
    with pytest.raises(InvalidDateError):
        system_no_reservations.book_room(
            101,
            "Bob",
            datetime.date(2099, 1, 5),
            datetime.date(2099, 1, 1)
        )

def test_book_room_past_check_in():
    system = HotelReservationSystem()
    system.add_room(101, "Single", 100.0)
    past_date = datetime.date.today() - timedelta(days=1)
    with pytest.raises(InvalidDateError):
        system.book_room(
            101,
            "Charlie",
            past_date,
            past_date + timedelta(days=4)
        )

def test_book_room_unavailable(system_with_reservation):
    with pytest.raises(RoomUnavailableError):
        system_with_reservation.book_room(
            101,
            "David",
            datetime.date(2099, 1, 3),
            datetime.date(2099, 1, 7)
        )

def test_book_room_success(system_no_reservations):
    res_id = system_no_reservations.book_room(
        102,
        "Eve",
        datetime.date(2099, 1, 10),
        datetime.date(2099, 1, 15)
    )
    assert res_id == "RES-0001"
    assert res_id in system_no_reservations.reservations

# ---------- Tests for cancel_reservation ----------
def test_cancel_reservation_not_found(system_for_cancellation):
    with pytest.raises(ReservationNotFoundError):
        system_for_cancellation.cancel_reservation("RES-9999")

def test_cancel_reservation_full_refund(system_for_cancellation):
    refund = system_for_cancellation.cancel_reservation("RES-0002")
    assert refund == 200.0  # 2 nights * 100.0

def test_cancel_reservation_half_refund(system_for_cancellation):
    refund = system_for_cancellation.cancel_reservation("RES-0003")
    assert refund == 100.0  # 2 nights * 100.0 * 0.5

def test_cancel_reservation_no_refund(system_for_cancellation):
    refund = system_for_cancellation.cancel_reservation("RES-0004")
    assert refund == 0.0

# ---------- Tests for get_room_occupancy ----------
@pytest.fixture
def occupancy_system():
    system = HotelReservationSystem()
    system.add_room(101, "Single", 100.0)
    system.add_room(102, "Double", 150.0)
    return system

def test_get_room_occupancy_empty(occupancy_system):
    assert occupancy_system.get_room_occupancy(datetime.date(2099, 1, 1)) == []

def test_get_room_occupancy_single(occupancy_system):
    occupancy_system.book_room(
        101,
        "User",
        datetime.date(2099, 3, 1),
        datetime.date(2099, 3, 2)
    )
    assert occupancy_system.get_room_occupancy(datetime.date(2099, 3, 1)) == [101]

def test_get_room_occupancy_multiple(occupancy_system):
    occupancy_system.book_room(
        101,
        "User1",
        datetime.date(2099, 4, 1),
        datetime.date(2099, 4, 2)
    )
    occupancy_system.book_room(
        102,
        "User2",
        datetime.date(2099, 4, 1),
        datetime.date(2099, 4, 3)
    )
    assert occupancy_system.get_room_occupancy(datetime.date(2099, 4, 1)) == [101, 102]