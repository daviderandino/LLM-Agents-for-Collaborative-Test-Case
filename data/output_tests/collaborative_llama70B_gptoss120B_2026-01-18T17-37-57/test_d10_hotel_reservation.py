import pytest
import datetime
from data.input_code.d10_hotel_reservation import *

@pytest.fixture
def fixed_today(monkeypatch):
    """Freeze datetime.date.today() to 2024-09-15 for deterministic tests."""
    class FixedDate(datetime.date):
        @classmethod
        def today(cls):
            return datetime.date(2024, 9, 15)
    monkeypatch.setattr(datetime, "date", FixedDate)
    return FixedDate.today()

@pytest.fixture
def system():
    """Provide a fresh HotelReservationSystem instance for each test."""
    return HotelReservationSystem()

def test_add_room_success(system):
    system.add_room(room_number=1, room_type="single", price_per_night=100.0)
    assert 1 in system.rooms
    assert system.rooms[1]["type"] == "single"
    assert system.rooms[1]["price_per_night"] == 100.0

def test_add_room_invalid_price(system):
    with pytest.raises(ValueError):
        system.add_room(room_number=1, room_type="single", price_per_night=-1.0)

@pytest.mark.parametrize(
    "offset_start, nights, expected_id, expected_price",
    [
        (5, 2, "RES-0001", 200.0),   # check-in 2024-09-20, 2 nights
    ],
)
def test_book_room_success(system, fixed_today, offset_start, nights, expected_id, expected_price):
    system.add_room(room_number=1, room_type="single", price_per_night=100.0)
    check_in = fixed_today + datetime.timedelta(days=offset_start)
    check_out = check_in + datetime.timedelta(days=nights)
    res_id = system.book_room(
        room_number=1,
        user_name="John Doe",
        check_in=check_in,
        check_out=check_out,
    )
    assert res_id == expected_id
    assert res_id in system.reservations
    reservation = system.reservations[res_id]
    assert reservation.total_price == expected_price

def test_book_room_not_found(system, fixed_today):
    with pytest.raises(RoomNotFoundError):
        system.book_room(
            room_number=2,
            user_name="John Doe",
            check_in=fixed_today + datetime.timedelta(days=5),
            check_out=fixed_today + datetime.timedelta(days=7),
        )

def test_book_room_invalid_dates(system, fixed_today):
    system.add_room(room_number=1, room_type="single", price_per_night=100.0)
    with pytest.raises(InvalidDateError):
        system.book_room(
            room_number=1,
            user_name="John Doe",
            check_in=fixed_today + datetime.timedelta(days=7),
            check_out=fixed_today + datetime.timedelta(days=5),  # checkout before checkin
        )

def test_book_room_unavailable(system, fixed_today):
    system.add_room(room_number=1, room_type="single", price_per_night=100.0)
    # First reservation occupies the dates
    system.book_room(
        room_number=1,
        user_name="John Doe",
        check_in=fixed_today + datetime.timedelta(days=5),   # 2024-09-20
        check_out=fixed_today + datetime.timedelta(days=7),  # 2024-09-22
    )
    # Overlapping reservation should fail
    with pytest.raises(RoomUnavailableError):
        system.book_room(
            room_number=1,
            user_name="Jane Smith",
            check_in=fixed_today + datetime.timedelta(days=6),   # 2024-09-21
            check_out=fixed_today + datetime.timedelta(days=8),  # 2024-09-23
        )

@pytest.mark.parametrize(
    "days_until_checkin, expected_refund",
    [
        (10, 200.0),   # >7 days → full refund
        (5, 100.0),    # 2-7 days → 50% refund
        (1, 0.0),      # <2 days → no refund
    ],
)
def test_cancel_reservation_refund(system, days_until_checkin, expected_refund, fixed_today):
    system.add_room(room_number=1, room_type="single", price_per_night=100.0)
    check_in = fixed_today + datetime.timedelta(days=days_until_checkin)
    check_out = check_in + datetime.timedelta(days=2)
    res_id = system.book_room(
        room_number=1,
        user_name="John Doe",
        check_in=check_in,
        check_out=check_out,
    )
    refund = system.cancel_reservation(reservation_id=res_id)
    assert refund == expected_refund

def test_cancel_reservation_not_found(system):
    with pytest.raises(ReservationNotFoundError):
        system.cancel_reservation(reservation_id="RES-9999")

def test_get_room_occupancy(system, fixed_today):
    system.add_room(room_number=1, room_type="single", price_per_night=100.0)
    system.add_room(room_number=2, room_type="double", price_per_night=150.0)
    # Book room 1 for 2024-09-20 to 2024-09-22
    system.book_room(
        room_number=1,
        user_name="John Doe",
        check_in=fixed_today + datetime.timedelta(days=5),   # 2024-09-20
        check_out=fixed_today + datetime.timedelta(days=7),  # 2024-09-22
    )
    # Book room 2 for 2024-09-21 to 2024-09-23
    system.book_room(
        room_number=2,
        user_name="Jane Smith",
        check_in=fixed_today + datetime.timedelta(days=6),   # 2024-09-21
        check_out=fixed_today + datetime.timedelta(days=8),  # 2024-09-23
    )
    occupancy = system.get_room_occupancy(date=fixed_today + datetime.timedelta(days=6))  # 2024-09-21
    assert occupancy == [1, 2]

import pytest
import datetime
from data.input_code.d10_hotel_reservation import *

def test_book_room_in_past(system, fixed_today):
    # Booking dates before the frozen today (2024-09-15)
    check_in = datetime.date(2024, 9, 10)
    check_out = datetime.date(2024, 9, 12)
    system.add_room(room_number=1, room_type="single", price_per_night=100.0)
    with pytest.raises(InvalidDateError):
        system.book_room(
            room_number=1,
            user_name="John Doe",
            check_in=check_in,
            check_out=check_out,
        )

def test_cancel_reservation_no_refund(system, fixed_today):
    # Reservation with <2 days until check‑in should yield 0 refund
    system.add_room(room_number=1, room_type="single", price_per_night=100.0)
    check_in = fixed_today + datetime.timedelta(days=1)   # 2024-09-16
    check_out = check_in + datetime.timedelta(days=2)    # 2024-09-18
    res_id = system.book_room(
        room_number=1,
        user_name="John Doe",
        check_in=check_in,
        check_out=check_out,
    )
    refund = system.cancel_reservation(reservation_id=res_id)
    assert refund == 0.0

def test_get_room_occupancy_empty(system, fixed_today):
    # No rooms/reservations added; occupancy should be empty list
    occupancy = system.get_room_occupancy(date=fixed_today)
    assert occupancy == []

@pytest.mark.parametrize(
    "check_in_str, check_out_str",
    [
        ("2024-09-20", "2024-09-20"),  # zero nights
        ("2024-09-20", "2024-09-20"),  # same day check‑in/check‑out (duplicate case)
    ],
)
def test_book_room_invalid_zero_nights(system, check_in_str, check_out_str):
    system.add_room(room_number=1, room_type="single", price_per_night=100.0)
    check_in = datetime.datetime.strptime(check_in_str, "%Y-%m-%d").date()
    check_out = datetime.datetime.strptime(check_out_str, "%Y-%m-%d").date()
    with pytest.raises(InvalidDateError):
        system.book_room(
            room_number=1,
            user_name="John Doe",
            check_in=check_in,
            check_out=check_out,
        )