import pytest
import datetime
from datetime import timedelta
from data.input_code.05_hotel import *

# ----------------------------------------------------------------------
# Fixtures
# ----------------------------------------------------------------------
@pytest.fixture
def system():
    """HotelReservationSystem with all required rooms pre‑added."""
    sys = HotelReservationSystem()
    sys.add_room(101, "Deluxe", 120.0)
    sys.add_room(102, "Suite", 150.0)
    sys.add_room(103, "Standard", 80.0)
    sys.add_room(104, "Economy", 50.0)
    return sys


# ----------------------------------------------------------------------
# add_room tests
# ----------------------------------------------------------------------
@pytest.mark.parametrize(
    "room_number, room_type, price, expected_exception",
    [
        (102, "Standard", 0.0, ValueError),   # price <= 0 triggers ValueError
    ],
)
def test_add_room_invalid_price(room_number, room_type, price, expected_exception):
    sys = HotelReservationSystem()
    with pytest.raises(expected_exception):
        sys.add_room(room_number, room_type, price)


# ----------------------------------------------------------------------
# book_room error handling
# ----------------------------------------------------------------------
@pytest.mark.parametrize(
    "room_number, user_name, check_in, check_out, expected_exception",
    [
        (999, "Alice", datetime.date(2023, 1, 5), datetime.date(2023, 1, 7), RoomNotFoundError),
        (101, "Bob", datetime.date(2023, 1, 10), datetime.date(2023, 1, 10), InvalidDateError),  # same day
        (101, "Carol", datetime.date(2022, 12, 30), datetime.date(2023, 1, 2), InvalidDateError),  # past
    ],
)
def test_book_room_invalid(system, room_number, user_name, check_in, check_out, expected_exception):
    with pytest.raises(expected_exception):
        system.book_room(room_number, user_name, check_in, check_out)


def test_book_room_unavailable(system):
    today = datetime.date.today()
    # First, a successful booking for room 101
    res_id = system.book_room(
        101,
        "Dave",
        today + timedelta(days=5),
        today + timedelta(days=7),
    )
    assert res_id == "RES-0001"

    # Overlapping request should raise RoomUnavailableError
    with pytest.raises(RoomUnavailableError):
        system.book_room(
            101,
            "Eve",
            today + timedelta(days=6),
            today + timedelta(days=8),
        )


# ----------------------------------------------------------------------
# book_room successful paths
# ----------------------------------------------------------------------
@pytest.mark.parametrize(
    "room_number, user_name, check_in_offset, check_out_offset, price_per_night",
    [
        (102, "Frank", 10, 12, 150.0),
        (103, "Grace", 4, 6, 80.0),
        (104, "Heidi", 2, 3, 50.0),
    ],
)
def test_book_room_success(
    system, room_number, user_name, check_in_offset, check_out_offset, price_per_night
):
    today = datetime.date.today()
    check_in = today + timedelta(days=check_in_offset)
    check_out = today + timedelta(days=check_out_offset)
    res_id = system.book_room(room_number, user_name, check_in, check_out)

    # Reservation IDs always start with "RES-" and are unique per system instance
    assert isinstance(res_id, str) and res_id.startswith("RES-")

    reservation = system.reservations[res_id]
    expected_price = round((check_out - check_in).days * price_per_night, 2)
    assert reservation.total_price == expected_price


# ----------------------------------------------------------------------
# cancel_reservation tests
# ----------------------------------------------------------------------
def test_cancel_reservation_not_found(system):
    with pytest.raises(ReservationNotFoundError):
        system.cancel_reservation("RES-9999")


@pytest.mark.parametrize(
    "room_number, check_in_offset, nights, price_per_night, expected_factor",
    [
        # >7 days until check‑in → full refund (factor 1.0)
        (102, 20, 2, 150.0, 1.0),
        # 2‑7 days until check‑in → 50% refund (factor 0.5)
        (103, 5, 2, 80.0, 0.5),
        # <2 days until check‑in → no refund (factor 0.0)
        (104, 1, 1, 50.0, 0.0),
    ],
)
def test_cancel_reservation_refund(
    system, room_number, check_in_offset, nights, price_per_night, expected_factor
):
    today = datetime.date.today()
    check_in = today + timedelta(days=check_in_offset)
    check_out = check_in + timedelta(days=nights)
    # Book the reservation
    res_id = system.book_room(room_number, "Tester", check_in, check_out)
    total_price = round(nights * price_per_night, 2)
    # Cancel and verify refund
    refund = system.cancel_reservation(res_id)
    expected_refund = round(total_price * expected_factor, 2)
    assert refund == expected_refund


# ----------------------------------------------------------------------
# get_room_occupancy tests
# ----------------------------------------------------------------------
def test_get_room_occupancy(system):
    today = datetime.date.today()
    # Create a reservation for room 101 spanning days 5‑6 (inclusive start, exclusive end)
    system.book_room(
        101,
        "Occupant",
        today + timedelta(days=5),
        today + timedelta(days=7),
    )
    occupied_date = today + timedelta(days=6)  # falls inside the reservation
    empty_date = today + timedelta(days=8)     # after the reservation ends
    assert system.get_room_occupancy(occupied_date) == [101]
    assert system.get_room_occupancy(empty_date) == []