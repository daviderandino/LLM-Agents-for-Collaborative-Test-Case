import pytest
import datetime
from datetime import timedelta
from data.input_code.d05_hotel import (
    HotelReservationSystem,
    RoomNotFoundError,
    RoomUnavailableError,
    InvalidDateError,
    ReservationNotFoundError,
)


@pytest.fixture
def system():
    """Provides a fresh HotelReservationSystem for each test."""
    return HotelReservationSystem()


# ----------------------------------------------------------------------
# add_room tests
# ----------------------------------------------------------------------
@pytest.mark.parametrize(
    "room_number, room_type, price, expected_exception",
    [
        (101, "single", 100.0, None),          # valid addition
        (102, "double", 0.0, ValueError),     # non‑positive price
    ],
)
def test_add_room(system, room_number, room_type, price, expected_exception):
    if expected_exception:
        with pytest.raises(expected_exception):
            system.add_room(room_number, room_type, price)
    else:
        system.add_room(room_number, room_type, price)
        assert room_number in system.rooms
        assert system.rooms[room_number]["type"] == room_type
        assert system.rooms[room_number]["price_per_night"] == price


# ----------------------------------------------------------------------
# book_room success
# ----------------------------------------------------------------------
def test_book_room_success(system):
    # precondition: add the room first
    system.add_room(101, "single", 100.0)

    # use future dates to avoid "booking in the past" error
    check_in = datetime.date.today() + timedelta(days=10)
    check_out = datetime.date.today() + timedelta(days=12)

    res_id = system.book_room(101, "John Doe", check_in, check_out)
    assert "RES-0001" in res_id


# ----------------------------------------------------------------------
# book_room error cases
# ----------------------------------------------------------------------
@pytest.mark.parametrize(
    "room_number, check_in, check_out, expected_exc",
    [
        # room does not exist
        (103, datetime.date(2024, 9, 20), datetime.date(2024, 9, 22), RoomNotFoundError),
        # checkout on same day (invalid date range)
        (101, datetime.date(2024, 9, 20), datetime.date(2024, 9, 20), InvalidDateError),
        # booking in the past
        (101, datetime.date.today() - timedelta(days=1), datetime.date.today() + timedelta(days=1), InvalidDateError),
    ],
)
def test_book_room_errors(system, room_number, check_in, check_out, expected_exc):
    # ensure room 101 exists for the cases that need it
    if room_number == 101:
        system.add_room(101, "single", 100.0)

    with pytest.raises(expected_exc):
        system.book_room(room_number, "John Doe", check_in, check_out)


def test_book_room_unavailable_error(system):
    # add room and create an initial reservation
    system.add_room(101, "single", 100.0)
    first_check_in = datetime.date.today() + timedelta(days=10)
    first_check_out = datetime.date.today() + timedelta(days=12)
    system.book_room(101, "Jane Doe", first_check_in, first_check_out)

    # attempt overlapping reservation
    with pytest.raises(RoomUnavailableError):
        system.book_room(101, "John Doe", first_check_in, first_check_out)


# ----------------------------------------------------------------------
# cancel_reservation tests (refund policy)
# ----------------------------------------------------------------------
@pytest.mark.parametrize(
    "days_until_checkin, expected_refund",
    [
        (10, 200.0),   # >7 days → 100% refund
        (5, 100.0),    # 2‑7 days → 50% refund
        (1, 0.0),      # <2 days → 0% refund
    ],
)
def test_cancel_reservation_refund(system, days_until_checkin, expected_refund):
    system.add_room(101, "single", 100.0)

    check_in = datetime.date.today() + timedelta(days=days_until_checkin)
    check_out = check_in + timedelta(days=2)  # 2‑night stay → total 200.0

    res_id = system.book_room(101, "John Doe", check_in, check_out)
    refund = system.cancel_reservation(res_id)
    assert refund == expected_refund


def test_cancel_reservation_not_found(system):
    with pytest.raises(ReservationNotFoundError):
        system.cancel_reservation("RES-9999")


# ----------------------------------------------------------------------
# get_room_occupancy tests
# ----------------------------------------------------------------------
def test_get_room_occupancy_no_reservations(system):
    target_date = datetime.date(2024, 9, 20)
    assert system.get_room_occupancy(target_date) == []


def test_get_room_occupancy_with_reservation(system):
    system.add_room(101, "single", 100.0)

    # future reservation dates
    check_in = datetime.date.today() + timedelta(days=10)
    check_out = datetime.date.today() + timedelta(days=12)
    system.book_room(101, "John Doe", check_in, check_out)

    # date within the reservation period
    assert system.get_room_occupancy(datetime.date.today() + timedelta(days=11)) == [101]

    # date equal to check_out is not occupied
    assert system.get_room_occupancy(check_out) == []