import pytest
from data.input_code.d05_hotel import HotelReservationSystem, RoomNotFoundError, RoomUnavailableError, InvalidDateError, ReservationNotFoundError
from datetime import date, timedelta

def test_add_room():
    hotel = HotelReservationSystem()
    hotel.add_room(1, 'single', 100.0)
    assert hotel.rooms[1]['type'] == 'single'
    assert hotel.rooms[1]['price_per_night'] == 100.0

def test_add_room_with_zero_price():
    hotel = HotelReservationSystem()
    with pytest.raises(ValueError):
        hotel.add_room(1, 'single', 0.0)

def test_add_room_with_negative_price():
    hotel = HotelReservationSystem()
    with pytest.raises(ValueError):
        hotel.add_room(1, 'single', -100.0)

def test_book_room():
    hotel = HotelReservationSystem()
    hotel.add_room(1, 'single', 100.0)
    res_id = hotel.book_room(1, 'John Doe', date.today() + timedelta(days=1), date.today() + timedelta(days=3))
    assert res_id in hotel.reservations

def test_book_room_with_non_existent_room():
    hotel = HotelReservationSystem()
    with pytest.raises(RoomNotFoundError):
        hotel.book_room(1, 'John Doe', date.today() + timedelta(days=1), date.today() + timedelta(days=3))

def test_book_room_with_invalid_dates():
    hotel = HotelReservationSystem()
    hotel.add_room(1, 'single', 100.0)
    with pytest.raises(InvalidDateError):
        hotel.book_room(1, 'John Doe', date.today() + timedelta(days=3), date.today() + timedelta(days=1))

def test_book_room_with_past_dates():
    hotel = HotelReservationSystem()
    hotel.add_room(1, 'single', 100.0)
    with pytest.raises(InvalidDateError):
        hotel.book_room(1, 'John Doe', date.today() - timedelta(days=1), date.today() + timedelta(days=1))

def test_book_room_with_occupied_room():
    hotel = HotelReservationSystem()
    hotel.add_room(1, 'single', 100.0)
    hotel.book_room(1, 'John Doe', date.today() + timedelta(days=1), date.today() + timedelta(days=3))
    with pytest.raises(RoomUnavailableError):
        hotel.book_room(1, 'Jane Doe', date.today() + timedelta(days=2), date.today() + timedelta(days=4))

def test_cancel_reservation():
    hotel = HotelReservationSystem()
    hotel.add_room(1, 'single', 100.0)
    res_id = hotel.book_room(1, 'John Doe', date.today() + timedelta(days=10), date.today() + timedelta(days=12))
    refund = hotel.cancel_reservation(res_id)
    assert refund == 200.0


def test_cancel_reservation_with_2_to_7_days():
    hotel = HotelReservationSystem()
    hotel.add_room(1, 'single', 100.0)
    res_id = hotel.book_room(1, 'John Doe', date.today() + timedelta(days=5), date.today() + timedelta(days=7))
    refund = hotel.cancel_reservation(res_id)
    assert refund == 100.0

def test_cancel_reservation_with_non_existent_reservation():
    hotel = HotelReservationSystem()
    with pytest.raises(ReservationNotFoundError):
        hotel.cancel_reservation('RES-0001')

def test_get_room_occupancy():
    hotel = HotelReservationSystem()
    hotel.add_room(1, 'single', 100.0)
    hotel.add_room(2, 'double', 200.0)
    hotel.book_room(1, 'John Doe', date.today(), date.today() + timedelta(days=2))
    hotel.book_room(2, 'Jane Doe', date.today(), date.today() + timedelta(days=2))
    occupied_rooms = hotel.get_room_occupancy(date.today())
    assert occupied_rooms == [1, 2]

def test_get_room_occupancy_with_no_occupied_rooms():
    hotel = HotelReservationSystem()
    occupied_rooms = hotel.get_room_occupancy(date.today())
    assert occupied_rooms == []