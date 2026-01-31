import pytest
from data.input_code.d05_hotel import HotelReservationSystem, RoomNotFoundError, RoomUnavailableError, InvalidDateError, ReservationNotFoundError
from datetime import date, timedelta

@pytest.fixture
def hotel_system():
    return HotelReservationSystem()

def test_add_room_success(hotel_system):
    hotel_system.add_room(101, "Deluxe", 150.0)
    assert 101 in hotel_system.rooms

def test_add_room_value_error(hotel_system):
    with pytest.raises(ValueError):
        hotel_system.add_room(102, "Standard", 0.0)

def test_book_room_room_not_found(hotel_system):
    with pytest.raises(RoomNotFoundError):
        hotel_system.book_room(999, "Alice", date(2099, 1, 10), date(2099, 1, 12))

def test_book_room_invalid_date_order(hotel_system):
    hotel_system.add_room(101, "Deluxe", 150.0)
    with pytest.raises(InvalidDateError):
        hotel_system.book_room(101, "Bob", date(2099, 1, 15), date(2099, 1, 10))

def test_book_room_invalid_date_past(hotel_system):
    hotel_system.add_room(101, "Deluxe", 150.0)
    with pytest.raises(InvalidDateError):
        hotel_system.book_room(101, "Carol", date(2000, 1, 1), date(2000, 1, 5))

def test_book_room_unavailable(hotel_system):
    hotel_system.add_room(101, "Deluxe", 150.0)
    hotel_system.book_room(101, "Eve", date(2099, 2, 1), date(2099, 2, 5))
    with pytest.raises(RoomUnavailableError):
        hotel_system.book_room(101, "Dave", date(2099, 2, 1), date(2099, 2, 5))

def test_book_room_success(hotel_system):
    hotel_system.add_room(101, "Deluxe", 150.0)
    res_id = hotel_system.book_room(101, "Eve", date(2099, 3, 1), date(2099, 3, 4))
    assert res_id == "RES-0001"

def test_cancel_reservation_not_found(hotel_system):
    with pytest.raises(ReservationNotFoundError):
        hotel_system.cancel_reservation("NONEXISTENT")

def test_cancel_reservation_full_refund(hotel_system):
    hotel_system.add_room(101, "Deluxe", 150.0)
    res_id = hotel_system.book_room(101, "Eve", date.today() + timedelta(days=10), date.today() + timedelta(days=12))
    refund = hotel_system.cancel_reservation(res_id)
    assert refund == 300.0

def test_cancel_reservation_half_refund(hotel_system):
    hotel_system.add_room(101, "Deluxe", 150.0)
    res_id = hotel_system.book_room(101, "Eve", date.today() + timedelta(days=3), date.today() + timedelta(days=5))
    refund = hotel_system.cancel_reservation(res_id)
    assert refund == 150.0

def test_cancel_reservation_no_refund(hotel_system):
    hotel_system.add_room(101, "Deluxe", 150.0)
    res_id = hotel_system.book_room(101, "Eve", date.today() + timedelta(days=1), date.today() + timedelta(days=3))
    refund = hotel_system.cancel_reservation(res_id)
    assert refund == 0.0

def test_get_room_occupancy(hotel_system):
    hotel_system.add_room(101, "Deluxe", 150.0)
    hotel_system.book_room(101, "Eve", date(2099, 3, 1), date(2099, 3, 4))
    occupied_rooms = hotel_system.get_room_occupancy(date(2099, 3, 2))
    assert occupied_rooms == [101]