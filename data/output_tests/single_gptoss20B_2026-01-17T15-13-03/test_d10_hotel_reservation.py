import pytest
import datetime
from data.input_code.d10_hotel_reservation import (
    HotelReservationSystem,
    RoomNotFoundError,
    RoomUnavailableError,
    InvalidDateError,
    ReservationNotFoundError,
)

# Helper to create a date offset from today
def offset_days(days: int) -> datetime.date:
    return datetime.date.today() + datetime.timedelta(days=days)

def test_add_room_valid_and_overwrite():
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

def test_is_room_available_no_reservations():
    system = HotelReservationSystem()
    assert system._is_room_available(201, offset_days(1), offset_days(3)) is True

def test_is_room_available_different_room():
    system = HotelReservationSystem()
    system.add_room(301, "Single", 80.0)
    res_id = system.book_room(301, "Alice", offset_days(1), offset_days(3))
    # Check availability for a different room
    assert system._is_room_available(302, offset_days(1), offset_days(3)) is True

def test_is_room_available_non_overlapping():
    system = HotelReservationSystem()
    system.add_room(401, "Single", 80.0)
    system.book_room(401, "Bob", offset_days(1), offset_days(3))
    # Non-overlapping: after existing reservation
    assert system._is_room_available(401, offset_days(3), offset_days(5)) is True
    # Non-overlapping: before existing reservation
    assert system._is_room_available(401, offset_days(-2), offset_days(0)) is True

def test_is_room_available_overlapping_and_boundary():
    system = HotelReservationSystem()
    system.add_room(501, "Single", 80.0)
    system.book_room(501, "Carol", offset_days(1), offset_days(5))
    # Overlap: check_in inside existing
    assert system._is_room_available(501, offset_days(2), offset_days(4)) is False
    # Overlap: check_out inside existing
    assert system._is_room_available(501, offset_days(0), offset_days(3)) is False
    # Overlap: fully contains existing
    assert system._is_room_available(501, offset_days(0), offset_days(6)) is False
    # No overlap: check_in equals existing check_out
    assert system._is_room_available(501, offset_days(5), offset_days(7)) is True
    # No overlap: check_out equals existing check_in
    assert system._is_room_available(501, offset_days(-1), offset_days(1)) is True

def test_book_room_room_not_found():
    system = HotelReservationSystem()
    with pytest.raises(RoomNotFoundError):
        system.book_room(999, "Dave", offset_days(1), offset_days(3))

def test_book_room_invalid_dates_and_past():
    system = HotelReservationSystem()
    system.add_room(601, "Single", 80.0)
    # check_in >= check_out
    with pytest.raises(InvalidDateError):
        system.book_room(601, "Eve", offset_days(5), offset_days(3))
    # check_in in the past
    with pytest.raises(InvalidDateError):
        system.book_room(601, "Eve", offset_days(-1), offset_days(1))

def test_book_room_unavailable_and_successful():
    system = HotelReservationSystem()
    system.add_room(701, "Single", 80.0)
    # First reservation
    res_id1 = system.book_room(701, "Frank", offset_days(1), offset_days(4))
    assert res_id1 == "RES-0001"
    # Overlapping reservation should fail
    with pytest.raises(RoomUnavailableError):
        system.book_room(701, "Grace", offset_days(3), offset_days(5))
    # Non-overlapping reservation should succeed
    res_id2 = system.book_room(701, "Heidi", offset_days(4), offset_days(6))
    assert res_id2 == "RES-0002"
    # Check price calculation
    reservation = system.reservations[res_id1]
    expected_nights = (offset_days(4) - offset_days(1)).days
    expected_price = round(expected_nights * 80.0, 2)
    assert reservation.total_price == expected_price

def test_cancel_reservation_not_found():
    system = HotelReservationSystem()
    with pytest.raises(ReservationNotFoundError):
        system.cancel_reservation("NONEXISTENT")

def test_cancel_reservation_refund_policy():
    system = HotelReservationSystem()
    system.add_room(801, "Single", 100.0)
    # >7 days
    res_id1 = system.book_room(801, "Ivan", offset_days(8), offset_days(10))
    refund1 = system.cancel_reservation(res_id1)
    assert refund1 == system.reservations.get(res_id1, None) is None or refund1 == 200.0
    # 2-7 days
    res_id2 = system.book_room(801, "Judy", offset_days(3), offset_days(5))
    refund2 = system.cancel_reservation(res_id2)
    assert refund2 == round(200.0 * 0.5, 2)
    # <2 days
    res_id3 = system.book_room(801, "Karl", offset_days(1), offset_days(2))
    refund3 = system.cancel_reservation(res_id3)
    assert refund3 == 0.0

def test_cancel_reservation_removal_and_occupancy():
    system = HotelReservationSystem()
    system.add_room(901, "Single", 120.0)
    res_id = system.book_room(901, "Laura", offset_days(1), offset_days(3))
    # Ensure occupancy before cancellation
    occ_before = system.get_room_occupancy(offset_days(1))
    assert 901 in occ_before
    # Cancel reservation
    system.cancel_reservation(res_id)
    # Ensure occupancy after cancellation
    occ_after = system.get_room_occupancy(offset_days(1))
    assert 901 not in occ_after

def test_get_room_occupancy_empty_and_boundary():
    system = HotelReservationSystem()
    # No reservations
    assert system.get_room_occupancy(offset_days(1)) == []
    # Add reservation
    system.add_room(1001, "Single", 90.0)
    res_id = system.book_room(1001, "Mallory", offset_days(2), offset_days(5))
    # Occupied on check_in date
    assert system.get_room_occupancy(offset_days(2)) == [1001]
    # Occupied on a middle date
    assert system.get_room_occupancy(offset_days(3)) == [1001]
    # Not occupied on check_out date
    assert system.get_room_occupancy(offset_days(5)) == []

def test_get_room_occupancy_multiple_and_sorted():
    system = HotelReservationSystem()
    system.add_room(1101, "Single", 90.0)
    system.add_room(1102, "Double", 110.0)
    system.add_room(1103, "Suite", 150.0)
    # Book overlapping reservations on the same date
    system.book_room(1101, "Nina", offset_days(1), offset_days(4))
    system.book_room(1103, "Oscar", offset_days(1), offset_days(4))
    system.book_room(1102, "Peggy", offset_days(2), offset_days(5))
    # Occupancy on day 2 should include 1101, 1102, 1103 sorted
    assert system.get_room_occupancy(offset_days(2)) == [1101, 1102, 1103]
    # Occupancy on day 1 should include 1101, 1103
    assert system.get_room_occupancy(offset_days(1)) == [1101, 1103]
    # Occupancy on day 4 should include 1102 only
    assert system.get_room_occupancy(offset_days(4)) == [1102]

def test_reservation_id_format_and_increment():
    system = HotelReservationSystem()
    system.add_room(1201, "Single", 80.0)
    res_id1 = system.book_room(1201, "Quentin", offset_days(1), offset_days(2))
    res_id2 = system.book_room(1201, "Ruth", offset_days(2), offset_days(3))
    assert res_id1 == "RES-0001"
    assert res_id2 == "RES-0002"

def test_total_price_rounding():
    system = HotelReservationSystem()
    system.add_room(1301, "Single", 99.99)
    res_id = system.book_room(1301, "Steve", offset_days(1), offset_days(4))
    reservation = system.reservations[res_id]
    # 3 nights * 99.99 = 299.97
    assert reservation.total_price == 299.97

def test_book_room_and_get_occupancy_integration():
    system = HotelReservationSystem()
    system.add_room(1401, "Single", 70.0)
    system.add_room(1402, "Double", 90.0)
    # Book both rooms on overlapping dates
    system.book_room(1401, "Trudy", offset_days(1), offset_days(3))
    system.book_room(1402, "Uma", offset_days(2), offset_days(4))
    # Occupancy on day 2 should list both rooms sorted
    assert system.get_room_occupancy(offset_days(2)) == [1401, 1402]
    # Occupancy on day 1 should list only 1401
    assert system.get_room_occupancy(offset_days(1)) == [1401]
    # Occupancy on day 3 should list only 1402
    assert system.get_room_occupancy(offset_days(3)) == [1402]
    # Occupancy on day 4 should be empty
    assert system.get_room_occupancy(offset_days(4)) == []

def test_cancel_reservation_refund_exact_boundaries():
    system = HotelReservationSystem()
    system.add_room(1501, "Single", 120.0)
    # Exactly 7 days before check-in
    res_id1 = system.book_room(1501, "Victor", offset_days(7), offset_days(8))
    refund1 = system.cancel_reservation(res_id1)
    assert refund1 == round(120.0 * 0.5, 2)
    # Exactly 2 days before check-in
    res_id2 = system.book_room(1501, "Wendy", offset_days(2), offset_days(3))
    refund2 = system.cancel_reservation(res_id2)
    assert refund2 == round(120.0 * 0.5, 2)
    # Exactly 8 days before check-in
    res_id3 = system.book_room(1501, "Xavier", offset_days(8), offset_days(9))
    refund3 = system.cancel_reservation(res_id3)
    assert refund3 == 120.0
    # Exactly 1 day before check-in
    res_id4 = system.book_room(1501, "Yvonne", offset_days(1), offset_days(2))
    refund4 = system.cancel_reservation(res_id4)
    assert refund4 == 0.0
    # Exactly 0 days before check-in (today)
    res_id5 = system.book_room(1501, "Zack", offset_days(0), offset_days(1))
    refund5 = system.cancel_reservation(res_id5)
    assert refund5 == 0.0