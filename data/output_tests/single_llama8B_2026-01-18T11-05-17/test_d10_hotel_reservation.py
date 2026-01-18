import pytest
from data.input_code.d10_hotel_reservation import HotelReservationSystem, RoomNotFoundError, RoomUnavailableError, InvalidDateError, ReservationNotFoundError
from datetime import date, timedelta
from typing import List, Dict

def test_hotel_reservation_system_init():
    hotel = HotelReservationSystem()
    assert hotel.rooms == {}
    assert hotel.reservations == {}
    assert hotel._reservation_counter == 0

def test_add_room():
    hotel = HotelReservationSystem()
    hotel.add_room(1, 'single', 100.0)
    assert hotel.rooms == {1: {'type': 'single', 'price_per_night': 100.0}}
    hotel.add_room(1, 'single', 100.0)
    assert hotel.rooms == {1: {'type': 'single', 'price_per_night': 100.0}}

def test_add_room_invalid_price():
    hotel = HotelReservationSystem()
    with pytest.raises(ValueError):
        hotel.add_room(1, 'single', 0.0)

def test_book_room():
    hotel = HotelReservationSystem()
    hotel.add_room(1, 'single', 100.0)
    reservation_id = hotel.book_room(1, 'John Doe', date.today(), date.today() + timedelta(days=1))
    assert reservation_id.startswith('RES-')
    assert hotel.reservations[reservation_id].room_number == 1

def test_book_room_invalid_dates():
    hotel = HotelReservationSystem()
    hotel.add_room(1, 'single', 100.0)
    with pytest.raises(InvalidDateError):
        hotel.book_room(1, 'John Doe', date.today(), date.today())
    with pytest.raises(InvalidDateError):
        hotel.book_room(1, 'John Doe', date.today() + timedelta(days=1), date.today())

def test_book_room_invalid_room():
    hotel = HotelReservationSystem()
    with pytest.raises(RoomNotFoundError):
        hotel.book_room(1, 'John Doe', date.today(), date.today() + timedelta(days=1))

def test_book_room_unavailable():
    hotel = HotelReservationSystem()
    hotel.add_room(1, 'single', 100.0)
    hotel.book_room(1, 'John Doe', date.today(), date.today() + timedelta(days=1))
    with pytest.raises(RoomUnavailableError):
        hotel.book_room(1, 'Jane Doe', date.today(), date.today() + timedelta(days=1))


def test_cancel_reservation_not_found():
    hotel = HotelReservationSystem()
    with pytest.raises(ReservationNotFoundError):
        hotel.cancel_reservation('RES-0001')

