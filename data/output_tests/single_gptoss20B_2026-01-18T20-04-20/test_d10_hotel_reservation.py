import pytest
import datetime
from data.input_code.d10_hotel_reservation import (
    HotelReservationSystem,
    RoomNotFoundError,
    RoomUnavailableError,
    InvalidDateError,
    ReservationNotFoundError,
    Reservation,
)

# Helper to patch datetime.date.today()
@pytest.fixture
def fixed_today(monkeypatch):
    fixed_date = datetime.date(2023, 1, 1)
    class FixedDate(datetime.date):
        @classmethod
        def today(cls):
            return fixed_date
    monkeypatch.setattr(datetime, "date", FixedDate)
    return fixed_date

def test_add_room_success_and_overwrite():
    system = HotelReservationSystem()
    system.add_room(101, "Single", 100.0)
    assert system.rooms[101]["type"] == "Single"
    assert system.rooms[101]["price_per_night"] == 100.0
    # Overwrite existing room
    system.add_room(101, "Double", 150.0)
    assert system.rooms[101]["type"] == "Double"
    assert system.rooms[101]["price_per_night"] == 150.0

def test_add_room_invalid_price():
    system = HotelReservationSystem()
    with pytest.raises(ValueError):
        system.add_room(102, "Suite", 0.0)
    with pytest.raises(ValueError):
        system.add_room(103, "Suite", -50.0)

def test_book_room_success_and_price_calculation(fixed_today):
    system = HotelReservationSystem()
    system.add_room(201, "Single", 120.0)
    check_in = datetime.date(2023, 1, 10)
    check_out = datetime.date(2023, 1, 15)  # 5 nights
    res_id = system.book_room(201, "Alice", check_in, check_out)
    assert res_id in system.reservations
    reservation = system.reservations[res_id]
    assert reservation.room_number == 201
    assert reservation.user_name == "Alice"
    assert reservation.check_in == check_in
    assert reservation.check_out == check_out
    assert reservation.total_price == round(5 * 120.0, 2)

def test_book_room_room_not_found(fixed_today):
    system = HotelReservationSystem()
    check_in = datetime.date(2023, 1, 10)
    check_out = datetime.date(2023, 1, 12)
    with pytest.raises(RoomNotFoundError):
        system.book_room(999, "Bob", check_in, check_out)

def test_book_room_invalid_date_check_in_ge_check_out(fixed_today):
    system = HotelReservationSystem()
    system.add_room(301, "Single", 80.0)
    check_in = datetime.date(2023, 1, 15)
    check_out = datetime.date(2023, 1, 15)
    with pytest.raises(InvalidDateError):
        system.book_room(301, "Carol", check_in, check_out)

def test_book_room_invalid_date_past(fixed_today):
    system = HotelReservationSystem()
    system.add_room(302, "Single", 80.0)
    check_in = datetime.date(2022, 12, 31)  # past relative to fixed_today
    check_out = datetime.date(2023, 1, 5)
    with pytest.raises(InvalidDateError):
        system.book_room(302, "Dave", check_in, check_out)

def test_book_room_room_unavailable(fixed_today):
    system = HotelReservationSystem()
    system.add_room(401, "Single", 90.0)
    # First reservation
    check_in1 = datetime.date(2023, 1, 20)
    check_out1 = datetime.date(2023, 1, 25)
    system.book_room(401, "Eve", check_in1, check_out1)
    # Overlapping reservation
    check_in2 = datetime.date(2023, 1, 24)
    check_out2 = datetime.date(2023, 1, 28)
    with pytest.raises(RoomUnavailableError):
        system.book_room(401, "Frank", check_in2, check_out2)

def test_is_room_available_no_reservations():
    system = HotelReservationSystem()
    system.add_room(501, "Single", 70.0)
    check_in = datetime.date(2023, 2, 1)
    check_out = datetime.date(2023, 2, 5)
    assert system._is_room_available(501, check_in, check_out) is True

def test_is_room_available_overlap(fixed_today):
    system = HotelReservationSystem()
    system.add_room(601, "Single", 70.0)
    # Existing reservation
    check_in1 = datetime.date(2023, 1, 10)
    check_out1 = datetime.date(2023, 1, 15)
    system.book_room(601, "Grace", check_in1, check_out1)
    # Overlap check
    check_in2 = datetime.date(2023, 1, 14)
    check_out2 = datetime.date(2023, 1, 20)
    assert system._is_room_available(601, check_in2, check_out2) is False

def test_cancel_reservation_not_found():
    system = HotelReservationSystem()
    with pytest.raises(ReservationNotFoundError):
        system.cancel_reservation("NON-EXISTENT")


def test_cancel_reservation_refund_50(fixed_today):
    system = HotelReservationSystem()
    system.add_room(801, "Single", 80.0)
    check_in = datetime.date(2023, 1, 8)  # 7 days from fixed_today
    check_out = datetime.date(2023, 1, 10)
    res_id = system.book_room(801, "Ivan", check_in, check_out)
    refund = system.cancel_reservation(res_id)
    expected_refund = round(((check_out - check_in).days * 80.0) * 0.5, 2)
    assert refund == expected_refund

def test_cancel_reservation_refund_0(fixed_today):
    system = HotelReservationSystem()
    system.add_room(901, "Single", 60.0)
    check_in = datetime.date(2023, 1, 2)  # 1 day from fixed_today
    check_out = datetime.date(2023, 1, 3)
    res_id = system.book_room(901, "Judy", check_in, check_out)
    refund = system.cancel_reservation(res_id)
    assert refund == 0.0

def test_get_room_occupancy_no_reservations(fixed_today):
    system = HotelReservationSystem()
    date_to_check = datetime.date(2023, 1, 5)
    assert system.get_room_occupancy(date_to_check) == []

def test_get_room_occupancy_with_reservations_boundary(fixed_today):
    system = HotelReservationSystem()
    system.add_room(1001, "Single", 50.0)
    system.add_room(1002, "Double", 70.0)
    # Reservation 1: 2023-01-02 to 2023-01-05
    res1_id = system.book_room(1001, "Kate", datetime.date(2023, 1, 2), datetime.date(2023, 1, 5))
    # Reservation 2: 2023-01-04 to 2023-01-06
    res2_id = system.book_room(1002, "Leo", datetime.date(2023, 1, 4), datetime.date(2023, 1, 6))
    # Check date 2023-01-02: only room 1001
    assert system.get_room_occupancy(datetime.date(2023, 1, 2)) == [1001]
    # Check date 2023-01-04: both rooms
    assert system.get_room_occupancy(datetime.date(2023, 1, 4)) == [1001, 1002]
    # Check date 2023-01-05: only room 1002 (since 1001 ends on 5)
    assert system.get_room_occupancy(datetime.date(2023, 1, 5)) == [1002]
    # Check date 2023-01-06: none
    assert system.get_room_occupancy(datetime.date(2023, 1, 6)) == []

def test_get_room_occupancy_sorted(fixed_today):
    system = HotelReservationSystem()
    system.add_room(2001, "Single", 50.0)
    system.add_room(2002, "Double", 70.0)
    system.add_room(2003, "Suite", 90.0)
    # Create reservations on same date
    system.book_room(2003, "Mia", datetime.date(2023, 1, 10), datetime.date(2023, 1, 12))
    system.book_room(2001, "Nina", datetime.date(2023, 1, 10), datetime.date(2023, 1, 12))
    system.book_room(2002, "Oscar", datetime.date(2023, 1, 10), datetime.date(2023, 1, 12))
    occupied = system.get_room_occupancy(datetime.date(2023, 1, 10))
    assert occupied == [2001, 2002, 2003]
    # Ensure order is ascending
    assert occupied == sorted(occupied)