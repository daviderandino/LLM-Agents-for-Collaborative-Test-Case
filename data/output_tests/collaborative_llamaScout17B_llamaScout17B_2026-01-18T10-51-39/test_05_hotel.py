import pytest
from data.input_code.05_hotel import *
import datetime

@pytest.mark.parametrize('reservation_id, expected', [
    ('non-existent-id', ReservationNotFoundError),
    ('', ReservationNotFoundError)
])
def test_cancel_reservation(reservation_id, expected):
    hotel = HotelReservationSystem()
    hotel.add_room(101, 'single', 100.0)
    res_id = hotel.book_room(101, 'John Doe', datetime.date.today() + datetime.timedelta(days=1), datetime.date.today() + datetime.timedelta(days=2))
    if expected:
        with pytest.raises(expected):
            hotel.cancel_reservation(reservation_id)
    else:
        assert res_id  # Ensure res_id is not empty
        refund = hotel.cancel_reservation(res_id)
        assert refund > 0.0

def test_cancel_reservation_valid():
    hotel = HotelReservationSystem()
    hotel.add_room(101, 'single', 100.0)
    res_id = hotel.book_room(101, 'John Doe', datetime.date.today() + datetime.timedelta(days=8), datetime.date.today() + datetime.timedelta(days=9)) # more than 7 days before check-in
    refund = hotel.cancel_reservation(res_id)
    assert refund == 100.0  # 100% refund

def test_cancel_reservation_already_cancelled():
    hotel = HotelReservationSystem()
    hotel.add_room(101, 'single', 100.0)
    res_id = hotel.book_room(101, 'John Doe', datetime.date.today() + datetime.timedelta(days=1), datetime.date.today() + datetime.timedelta(days=2))
    hotel.cancel_reservation(res_id)
    with pytest.raises(ReservationNotFoundError):
        hotel.cancel_reservation(res_id)

def test_cancel_reservation_late_cancel():
    hotel = HotelReservationSystem()
    hotel.add_room(101, 'single', 100.0)
    res_id = hotel.book_room(101, 'John Doe', datetime.date.today() + datetime.timedelta(days=1), datetime.date.today() + datetime.timedelta(days=2))
    refund = hotel.cancel_reservation(res_id)
    assert refund == 0.0  # 0% refund

def test_cancel_reservation_partial_refund():
    hotel = HotelReservationSystem()
    hotel.add_room(101, 'single', 100.0)
    res_id = hotel.book_room(101, 'John Doe', datetime.date.today() + datetime.timedelta(days=7), datetime.date.today() + datetime.timedelta(days=10)) 
    refund = hotel.cancel_reservation(res_id)
    assert refund == 300.0 * 0.5  # 50% refund

import pytest
from data.input_code.05_hotel import *
import datetime

@pytest.mark.parametrize('price_per_night, expected', [
    (0.0, ValueError),
    (-100.0, ValueError)
])
def test_add_room_invalid_price(price_per_night, expected):
    hotel = HotelReservationSystem()
    with pytest.raises(expected):
        hotel.add_room(102, 'double', price_per_night)

def test_book_room_invalid_date_range():
    hotel = HotelReservationSystem()
    hotel.add_room(101, 'single', 100.0)
    with pytest.raises(InvalidDateError):
        hotel.book_room(101, 'Jane Doe', datetime.date.today() + datetime.timedelta(days=2), datetime.date.today() + datetime.timedelta(days=1))

def test_book_room_past_date():
    hotel = HotelReservationSystem()
    hotel.add_room(101, 'single', 100.0)
    with pytest.raises(InvalidDateError):
        hotel.book_room(101, 'Jane Doe', datetime.date.today() - datetime.timedelta(days=1), datetime.date.today() + datetime.timedelta(days=2))

def test_get_room_occupancy_empty():
    hotel = HotelReservationSystem()
    assert hotel.get_room_occupancy(datetime.date.today()) == []

@pytest.mark.parametrize('days_until_checkin, expected_refund', [
    (10, 100.0),  # 100% refund
    (5, 50.0),    # 50% refund
    (1, 0.0)      # 0% refund
])
def test_cancel_reservation_refund_edge_cases(days_until_checkin, expected_refund):
    hotel = HotelReservationSystem()
    hotel.add_room(101, 'single', 100.0)
    check_in = datetime.date.today() + datetime.timedelta(days=days_until_checkin)
    res_id = hotel.book_room(101, 'John Doe', check_in, check_in + datetime.timedelta(days=1))
    refund = hotel.cancel_reservation(res_id)
    assert refund == expected_refund

import pytest
from data.input_code.05_hotel import *
import datetime

def test_book_room_missing_room_not_found():
    hotel = HotelReservationSystem()
    hotel.add_room(101, 'single', 100.0)
    with pytest.raises(RoomNotFoundError):
        hotel.book_room(102, 'Jane Doe', datetime.date.today() + datetime.timedelta(days=1), datetime.date.today() + datetime.timedelta(days=2))

@pytest.mark.parametrize('setup, expected', [
    (['add_room', 101, 'single', 100.0, 'book_room', 101, 'Jane Doe', datetime.date.today() + datetime.timedelta(days=1), datetime.date.today() + datetime.timedelta(days=2)], RoomUnavailableError)
])
def test_book_room_missing_room_unavailable(setup, expected):
    hotel = HotelReservationSystem()
    for i, item in enumerate(setup):
        if item == 'add_room':
            hotel.add_room(setup[i+1], setup[i+2], setup[i+3])
        elif item == 'book_room':
            hotel.book_room(setup[i+1], setup[i+2], setup[i+3], setup[i+4])
    with pytest.raises(expected):
        hotel.book_room(101, 'John Doe', datetime.date.today() + datetime.timedelta(days=1), datetime.date.today() + datetime.timedelta(days=2))

def test_get_room_occupancy_single_room():
    hotel = HotelReservationSystem()
    hotel.add_room(101, 'single', 100.0)
    hotel.book_room(101, 'Jane Doe', datetime.date.today() + datetime.timedelta(days=1), datetime.date.today() + datetime.timedelta(days=2))
    assert hotel.get_room_occupancy(datetime.date.today() + datetime.timedelta(days=1)) == [101]

def test_get_room_occupancy_multiple_rooms():
    hotel = HotelReservationSystem()
    hotel.add_room(101, 'single', 100.0)
    hotel.add_room(102, 'double', 200.0)
    hotel.book_room(101, 'Jane Doe', datetime.date.today() + datetime.timedelta(days=1), datetime.date.today() + datetime.timedelta(days=2))
    hotel.book_room(102, 'John Doe', datetime.date.today() + datetime.timedelta(days=1), datetime.date.today() + datetime.timedelta(days=2))
    assert set(hotel.get_room_occupancy(datetime.date.today() + datetime.timedelta(days=1))) == {101, 102}

def test_book_room_zero_nights():
    hotel = HotelReservationSystem()
    hotel.add_room(101, 'single', 100.0)
    with pytest.raises(InvalidDateError):
        hotel.book_room(101, 'Jane Doe', datetime.date.today() + datetime.timedelta(days=1), datetime.date.today() + datetime.timedelta(days=1))