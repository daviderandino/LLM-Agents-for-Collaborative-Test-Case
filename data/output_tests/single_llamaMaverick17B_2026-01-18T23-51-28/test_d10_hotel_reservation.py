import pytest
from datetime import date, timedelta
from data.input_code.d10_hotel_reservation import (
    HotelReservationSystem,
    RoomNotFoundError,
    RoomUnavailableError,
    InvalidDateError,
    ReservationNotFoundError
)

def test_add_room_valid():
    hotel = HotelReservationSystem()
    hotel.add_room(1, "Single", 100.0)
    assert hotel.rooms[1]['price_per_night'] == 100.0

def test_add_room_invalid_price():
    hotel = HotelReservationSystem()
    with pytest.raises(ValueError):
        hotel.add_room(1, "Single", -100.0)

def test_book_room_room_not_found():
    hotel = HotelReservationSystem()
    with pytest.raises(RoomNotFoundError):
        hotel.book_room(1, "John", date.today(), date.today() + timedelta(days=1))

def test_book_room_invalid_dates():
    hotel = HotelReservationSystem()
    hotel.add_room(1, "Single", 100.0)
    with pytest.raises(InvalidDateError):
        hotel.book_room(1, "John", date.today() + timedelta(days=1), date.today())

def test_book_room_past_date():
    hotel = HotelReservationSystem()
    hotel.add_room(1, "Single", 100.0)
    with pytest.raises(InvalidDateError):
        hotel.book_room(1, "John", date.today() - timedelta(days=1), date.today())

def test_book_room_unavailable():
    hotel = HotelReservationSystem()
    hotel.add_room(1, "Single", 100.0)
    hotel.book_room(1, "John", date.today(), date.today() + timedelta(days=1))
    with pytest.raises(RoomUnavailableError):
        hotel.book_room(1, "Jane", date.today(), date.today() + timedelta(days=1))

def test_book_room_success():
    hotel = HotelReservationSystem()
    hotel.add_room(1, "Single", 100.0)
    res_id = hotel.book_room(1, "John", date.today() + timedelta(days=1), date.today() + timedelta(days=2))
    assert res_id.startswith("RES-")
    assert res_id in hotel.reservations

def test_cancel_reservation_not_found():
    hotel = HotelReservationSystem()
    with pytest.raises(ReservationNotFoundError):
        hotel.cancel_reservation("RES-0001")

def test_cancel_reservation_refund_policy():
    hotel = HotelReservationSystem()
    hotel.add_room(1, "Single", 100.0)
    res_id = hotel.book_room(1, "John", date.today() + timedelta(days=10), date.today() + timedelta(days=11))
    assert hotel.cancel_reservation(res_id) == 100.0
    
    res_id = hotel.book_room(1, "John", date.today() + timedelta(days=5), date.today() + timedelta(days=6))
    assert hotel.cancel_reservation(res_id) == 50.0
    
    res_id = hotel.book_room(1, "John", date.today() + timedelta(days=1), date.today() + timedelta(days=2))
    assert hotel.cancel_reservation(res_id) == 0.0

def test_get_room_occupancy():
    hotel = HotelReservationSystem()
    hotel.add_room(1, "Single", 100.0)
    hotel.add_room(2, "Double", 200.0)
    hotel.book_room(1, "John", date.today(), date.today() + timedelta(days=1))
    hotel.book_room(2, "Jane", date.today() + timedelta(days=1), date.today() + timedelta(days=2))
    assert hotel.get_room_occupancy(date.today()) == [1]
    assert hotel.get_room_occupancy(date.today() + timedelta(days=1)) == [2]