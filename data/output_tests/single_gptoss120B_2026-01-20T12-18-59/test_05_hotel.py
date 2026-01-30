import datetime
import pytest
from data.input_code.05_hotel import (
    HotelReservationSystem,
    RoomNotFoundError,
    RoomUnavailableError,
    InvalidDateError,
    ReservationNotFoundError,
)

@pytest.fixture
def fixed_today(monkeypatch):
    """Patch datetime.date.today() to a constant date for deterministic tests."""
    fixed = datetime.date(2023, 1, 1)
    class FixedDate(datetime.date):
        @classmethod
        def today(cls):
            return fixed
    monkeypatch.setattr(datetime, "date", FixedDate)
    return fixed

@pytest.fixture
def system(fixed_today):
    sys = HotelReservationSystem()
    sys.add_room(101, "single", 100.0)
    sys.add_room(102, "double", 150.5)
    return sys

def test_add_room_invalid_price():
    sys = HotelReservationSystem()
    with pytest.raises(ValueError):
        sys.add_room(201, "suite", -10)

def test_book_room_success_and_price_calculation(system, fixed_today):
    check_in = fixed_today + datetime.timedelta(days=2)
    check_out = check_in + datetime.timedelta(days=3)  # 3 nights
    res_id = system.book_room(101, "Alice", check_in, check_out)
    assert res_id.startswith("RES-")
    reservation = system.reservations[res_id]
    assert reservation.room_number == 101
    assert reservation.user_name == "Alice"
    assert reservation.check_in == check_in
    assert reservation.check_out == check_out
    # price = 3 nights * 100.0 = 300.0
    assert reservation.total_price == 300.0

def test_book_room_not_found(system, fixed_today):
    check_in = fixed_today + datetime.timedelta(days=1)
    check_out = check_in + datetime.timedelta(days=2)
    with pytest.raises(RoomNotFoundError):
        system.book_room(999, "Bob", check_in, check_out)

def test_book_room_invalid_dates_checkout_before_checkin(system, fixed_today):
    check_in = fixed_today + datetime.timedelta(days=5)
    check_out = check_in  # same day -> invalid
    with pytest.raises(InvalidDateError):
        system.book_room(101, "Carol", check_in, check_out)

def test_book_room_invalid_dates_past_booking(system, fixed_today):
    past_date = fixed_today - datetime.timedelta(days=1)
    future_date = fixed_today + datetime.timedelta(days=1)
    with pytest.raises(InvalidDateError):
        system.book_room(101, "Dave", past_date, future_date)

def test_book_room_unavailable(system, fixed_today):
    # First reservation occupies 101 from day 2 to day 5
    first_check_in = fixed_today + datetime.timedelta(days=2)
    first_check_out = first_check_in + datetime.timedelta(days=3)
    system.book_room(101, "Eve", first_check_in, first_check_out)

    # Overlapping attempt
    overlap_check_in = fixed_today + datetime.timedelta(days=3)
    overlap_check_out = overlap_check_in + datetime.timedelta(days=2)
    with pytest.raises(RoomUnavailableError):
        system.book_room(101, "Frank", overlap_check_in, overlap_check_out)

def test_cancel_reservation_refund_full(system, fixed_today):
    check_in = fixed_today + datetime.timedelta(days=10)  # >7 days away
    check_out = check_in + datetime.timedelta(days=2)
    res_id = system.book_room(102, "Grace", check_in, check_out)
    reservation = system.reservations[res_id]
    refund = system.cancel_reservation(res_id)
    assert refund == reservation.total_price

def test_cancel_reservation_refund_half(system, fixed_today):
    check_in = fixed_today + datetime.timedelta(days=5)  # between 2 and 7 days
    check_out = check_in + datetime.timedelta(days=2)
    res_id = system.book_room(102, "Heidi", check_in, check_out)
    reservation = system.reservations[res_id]
    refund = system.cancel_reservation(res_id)
    expected = round(reservation.total_price * 0.5, 2)
    assert refund == expected

def test_cancel_reservation_refund_none(system, fixed_today):
    check_in = fixed_today + datetime.timedelta(days=1)  # <2 days away
    check_out = check_in + datetime.timedelta(days=2)
    res_id = system.book_room(102, "Ivan", check_in, check_out)
    refund = system.cancel_reservation(res_id)
    assert refund == 0.0

def test_cancel_reservation_not_found(system):
    with pytest.raises(ReservationNotFoundError):
        system.cancel_reservation("NON-EXISTENT")

def test_get_room_occupancy_multiple(system, fixed_today):
    # Reservation 1: room 101 occupied days 2-4
    r1_in = fixed_today + datetime.timedelta(days=2)
    r1_out = r1_in + datetime.timedelta(days=2)
    system.book_room(101, "Judy", r1_in, r1_out)

    # Reservation 2: room 102 occupied days 3-5
    r2_in = fixed_today + datetime.timedelta(days=3)
    r2_out = r2_in + datetime.timedelta(days=2)
    system.book_room(102, "Ken", r2_in, r2_out)

    # Date where both rooms occupied
    date_both = fixed_today + datetime.timedelta(days=3)
    occupied = system.get_room_occupancy(date_both)
    assert occupied == [101, 102]

    # Date where only room 101 occupied
    date_one = fixed_today + datetime.timedelta(days=2)
    occupied = system.get_room_occupancy(date_one)
    assert occupied == [101]

    # Date with no occupancy
    date_none = fixed_today + datetime.timedelta(days=6)
    occupied = system.get_room_occupancy(date_none)
    assert occupied == []