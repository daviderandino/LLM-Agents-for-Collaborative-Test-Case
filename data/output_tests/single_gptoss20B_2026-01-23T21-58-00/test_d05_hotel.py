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
    return HotelReservationSystem()

def test_add_room_success(system):
    system.add_room(101, "Deluxe", 100.0)
    assert system.rooms[101]["type"] == "Deluxe"
    assert system.rooms[101]["price_per_night"] == 100.0

def test_add_room_overwrite(system):
    system.add_room(101, "Deluxe", 100.0)
    system.add_room(101, "Suite", 200.0)
    assert system.rooms[101]["type"] == "Suite"
    assert system.rooms[101]["price_per_night"] == 200.0

def test_add_room_invalid_price(system):
    with pytest.raises(ValueError):
        system.add_room(102, "Standard", 0)
    with pytest.raises(ValueError):
        system.add_room(103, "Standard", -10)

def test_is_room_available_no_reservations(system):
    today = datetime.date.today()
    assert system._is_room_available(101, today, today + timedelta(days=1))

def test_is_room_available_different_room(system):
    system.add_room(101, "Deluxe", 100.0)
    system.add_room(102, "Suite", 200.0)
    check_in = datetime.date.today() + timedelta(days=1)
    check_out = check_in + timedelta(days=2)
    system.book_room(101, "Alice", check_in, check_out)
    assert system._is_room_available(102, check_in, check_out)

def test_is_room_available_overlapping(system):
    system.add_room(101, "Deluxe", 100.0)
    check_in = datetime.date.today() + timedelta(days=1)
    check_out = check_in + timedelta(days=2)
    system.book_room(101, "Alice", check_in, check_out)
    # Overlap
    assert not system._is_room_available(101, check_in - timedelta(days=1), check_out + timedelta(days=1))
    # Non-overlap before
    assert system._is_room_available(101, check_in - timedelta(days=3), check_in - timedelta(days=1))
    # Non-overlap after
    assert system._is_room_available(101, check_out + timedelta(days=1), check_out + timedelta(days=3))

def test_book_room_success(system):
    system.add_room(101, "Deluxe", 100.0)
    check_in = datetime.date.today() + timedelta(days=1)
    check_out = check_in + timedelta(days=2)
    res_id = system.book_room(101, "Alice", check_in, check_out)
    assert res_id in system.reservations
    reservation = system.reservations[res_id]
    assert reservation.room_number == 101
    assert reservation.user_name == "Alice"
    assert reservation.check_in == check_in
    assert reservation.check_out == check_out
    assert reservation.total_price == 200.0

def test_book_room_room_not_found(system):
    check_in = datetime.date.today() + timedelta(days=1)
    check_out = check_in + timedelta(days=1)
    with pytest.raises(RoomNotFoundError):
        system.book_room(999, "Bob", check_in, check_out)

def test_book_room_invalid_dates(system):
    system.add_room(101, "Deluxe", 100.0)
    check_in = datetime.date.today() + timedelta(days=1)
    check_out = check_in
    with pytest.raises(InvalidDateError):
        system.book_room(101, "Alice", check_in, check_out)
    check_out = check_in - timedelta(days=1)
    with pytest.raises(InvalidDateError):
        system.book_room(101, "Alice", check_in, check_out)

def test_book_room_past_date(system):
    system.add_room(101, "Deluxe", 100.0)
    check_in = datetime.date.today() - timedelta(days=1)
    check_out = datetime.date.today() + timedelta(days=1)
    with pytest.raises(InvalidDateError):
        system.book_room(101, "Alice", check_in, check_out)

def test_book_room_unavailable(system):
    system.add_room(101, "Deluxe", 100.0)
    check_in = datetime.date.today() + timedelta(days=1)
    check_out = check_in + timedelta(days=2)
    system.book_room(101, "Alice", check_in, check_out)
    with pytest.raises(RoomUnavailableError):
        system.book_room(101, "Bob", check_in + timedelta(days=1), check_out + timedelta(days=1))


def test_reservation_id_increment(system):
    system.add_room(101, "Deluxe", 100.0)
    check_in = datetime.date.today() + timedelta(days=1)
    res_id1 = system.book_room(101, "Alice", check_in, check_in + timedelta(days=1))
    res_id2 = system.book_room(101, "Bob", check_in + timedelta(days=2), check_in + timedelta(days=3))
    assert res_id1 == "RES-0001"
    assert res_id2 == "RES-0002"

def test_cancel_reservation_full_refund(system):
    system.add_room(101, "Deluxe", 100.0)
    check_in = datetime.date.today() + timedelta(days=8)
    res_id = system.book_room(101, "Alice", check_in, check_in + timedelta(days=1))
    refund = system.cancel_reservation(res_id)
    assert refund == 100.0
    assert res_id not in system.reservations

def test_cancel_reservation_half_refund(system):
    system.add_room(101, "Deluxe", 100.0)
    check_in = datetime.date.today() + timedelta(days=5)
    res_id = system.book_room(101, "Alice", check_in, check_in + timedelta(days=1))
    refund = system.cancel_reservation(res_id)
    assert refund == 50.0
    assert res_id not in system.reservations

def test_cancel_reservation_no_refund(system):
    system.add_room(101, "Deluxe", 100.0)
    check_in = datetime.date.today() + timedelta(days=1)
    res_id = system.book_room(101, "Alice", check_in, check_in + timedelta(days=1))
    refund = system.cancel_reservation(res_id)
    assert refund == 0.0
    assert res_id not in system.reservations

def test_cancel_reservation_not_found(system):
    with pytest.raises(ReservationNotFoundError):
        system.cancel_reservation("NON-EXISTENT")

def test_cancel_reservation_half_refund_rounding(system):
    system.add_room(101, "Deluxe", 10.555)
    check_in = datetime.date.today() + timedelta(days=5)
    res_id = system.book_room(101, "Alice", check_in, check_in + timedelta(days=1))
    refund = system.cancel_reservation(res_id)
    assert refund == 5.28  # 10.56 * 0.5


def test_get_room_occupancy(system):
    system.add_room(101, "Deluxe", 100.0)
    system.add_room(102, "Suite", 200.0)
    today = datetime.date.today()
    # Reservation for room 101 from today+1 to today+3
    system.book_room(101, "Alice", today + timedelta(days=1), today + timedelta(days=3))
    # Reservation for room 102 from today+2 to today+4
    system.book_room(102, "Bob", today + timedelta(days=2), today + timedelta(days=4))
    # Occupancy on today+2 should include both rooms
    occ = system.get_room_occupancy(today + timedelta(days=2))
    assert occ == [101, 102]
    # Occupancy on today+1 should include only 101
    occ = system.get_room_occupancy(today + timedelta(days=1))
    assert occ == [101]
    # Occupancy on today+3 should include only 102 (since 101 ends at 3 exclusive)
    occ = system.get_room_occupancy(today + timedelta(days=3))
    assert occ == [102]
    # Occupancy on today should be empty
    occ = system.get_room_occupancy(today)
    assert occ == []

def test_get_room_occupancy_sorted(system):
    system.add_room(101, "Deluxe", 100.0)
    system.add_room(103, "Suite", 200.0)
    system.add_room(102, "Standard", 150.0)
    today = datetime.date.today()
    system.book_room(103, "Alice", today + timedelta(days=1), today + timedelta(days=3))
    system.book_room(101, "Bob", today + timedelta(days=1), today + timedelta(days=3))
    system.book_room(102, "Carol", today + timedelta(days=1), today + timedelta(days=3))
    occ = system.get_room_occupancy(today + timedelta(days=1))
    assert occ == [101, 102, 103]

def test_get_room_occupancy_excludes_checkout(system):
    system.add_room(101, "Deluxe", 100.0)
    today = datetime.date.today()
    system.book_room(101, "Alice", today + timedelta(days=1), today + timedelta(days=3))
    occ = system.get_room_occupancy(today + timedelta(days=3))
    assert occ == []

def test_get_room_occupancy_before_after(system):
    system.add_room(101, "Deluxe", 100.0)
    today = datetime.date.today()
    system.book_room(101, "Alice", today + timedelta(days=5), today + timedelta(days=7))
    occ_before = system.get_room_occupancy(today + timedelta(days=4))
    occ_after = system.get_room_occupancy(today + timedelta(days=7))
    assert occ_before == []
    assert occ_after == []

def test_get_room_occupancy_empty(system):
    today = datetime.date.today()
    occ = system.get_room_occupancy(today)
    assert occ == []

def test_book_room_id_format(system):
    system.add_room(101, "Deluxe", 100.0)
    check_in = datetime.date.today() + timedelta(days=1)
    res_id = system.book_room(101, "Alice", check_in, check_in + timedelta(days=1))
    assert res_id.startswith("RES-")
    assert len(res_id) == 8  # RES-0001

def test_book_after_overwrite_price(system):
    system.add_room(101, "Deluxe", 100.0)
    check_in = datetime.date.today() + timedelta(days=1)
    res_id1 = system.book_room(101, "Alice", check_in, check_in + timedelta(days=1))
    assert system.reservations[res_id1].total_price == 100.0
    # Overwrite price
    system.add_room(101, "Suite", 200.0)
    res_id2 = system.book_room(101, "Bob", check_in + timedelta(days=2), check_in + timedelta(days=3))
    assert system.reservations[res_id2].total_price == 200.0

def test_book_room_adjacent(system):
    system.add_room(101, "Deluxe", 100.0)
    today = datetime.date.today()
    res1 = system.book_room(101, "Alice", today + timedelta(days=1), today + timedelta(days=3))
    # Next reservation starts at check_out
    res2 = system.book_room(101, "Bob", today + timedelta(days=3), today + timedelta(days=5))
    assert res2 in system.reservations
    assert system.reservations[res2].check_in == today + timedelta(days=3)
    assert system.reservations[res2].check_out == today + timedelta(days=5)