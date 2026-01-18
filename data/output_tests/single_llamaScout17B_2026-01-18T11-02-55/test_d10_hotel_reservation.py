import pytest
from data.input_code.d10_hotel_reservation import (
    HotelReservationSystem,
    RoomNotFoundError,
    RoomUnavailableError,
    InvalidDateError,
    ReservationNotFoundError,
    Reservation
)

def test_add_room():
    hrs = HotelReservationSystem()
    hrs.add_room(101, 'Single', 100.0)
    assert hrs.rooms[101] == {'type': 'Single', 'price_per_night': 100.0}

def test_add_room_overwrite():
    hrs = HotelReservationSystem()
    hrs.add_room(101, 'Single', 100.0)
    hrs.add_room(101, 'Double', 150.0)
    assert hrs.rooms[101] == {'type': 'Double', 'price_per_night': 150.0}

def test_add_room_invalid_price():
    hrs = HotelReservationSystem()
    with pytest.raises(ValueError):
        hrs.add_room(101, 'Single', 0.0)







def test_cancel_reservation_not_found():
    hrs = HotelReservationSystem()
    with pytest.raises(ReservationNotFoundError):
        hrs.cancel_reservation('RES-0001')



