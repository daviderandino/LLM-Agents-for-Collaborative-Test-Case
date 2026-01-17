import pytest
import datetime
from datetime import timedelta
from data.input_code.d10_hotel_reservation import *

@pytest.fixture
def hotel_system():
    return HotelReservationSystem()

@pytest.mark.parametrize('room_number, room_type, price_per_night, expected_exception', [
    (101, 'single', 100.0, None),
    (101, 'single', 0.0, ValueError)
])
def test_add_room(hotel_system, room_number, room_type, price_per_night, expected_exception):
    if expected_exception:
        with pytest.raises(expected_exception):
            hotel_system.add_room(room_number, room_type, price_per_night)
    else:
        hotel_system.add_room(room_number, room_type, price_per_night)
        assert room_number in hotel_system.rooms

@pytest.mark.parametrize('room_number, user_name, check_in, check_out, expected_exception, precondition', [
    # Valid booking in the future
    (101, 'John Doe', datetime.date.today() + timedelta(days=10), datetime.date.today() + timedelta(days=12), None, None),
    # Room not found
    (102, 'John Doe', datetime.date.today() + timedelta(days=10), datetime.date.today() + timedelta(days=12), RoomNotFoundError, None),
    # Check-in after check-out
    (101, 'John Doe', datetime.date.today() + timedelta(days=12), datetime.date.today() + timedelta(days=10), InvalidDateError, None),
    # Check-in in the past
    (101, 'John Doe', datetime.date.today() - timedelta(days=1), datetime.date.today() + timedelta(days=1), InvalidDateError, None),
    # Room unavailable due to existing reservation
    (101, 'John Doe', datetime.date.today() + timedelta(days=10), datetime.date.today() + timedelta(days=12), RoomUnavailableError,
     lambda system: system.book_room(101, 'Jane Doe', datetime.date.today() + timedelta(days=10), datetime.date.today() + timedelta(days=12)))
])
def test_book_room(hotel_system, room_number, user_name, check_in, check_out, expected_exception, precondition):
    hotel_system.add_room(101, 'single', 100.0)
    if precondition:
        precondition(hotel_system)
    if expected_exception:
        with pytest.raises(expected_exception):
            hotel_system.book_room(room_number, user_name, check_in, check_out)
    else:
        reservation_id = hotel_system.book_room(room_number, user_name, check_in, check_out)
        assert reservation_id.startswith('RES-')

@pytest.mark.parametrize('reservation_id, expected_refund, precondition', [
    # Reservation exists and is more than 7 days away from today
    ('RES-0001', 200.0, lambda system: system.book_room(101, 'John Doe', datetime.date.today() + timedelta(days=10), datetime.date.today() + timedelta(days=12))),
    # Reservation does not exist
    ('RES-0002', ReservationNotFoundError, None)
])
def test_cancel_reservation(hotel_system, reservation_id, expected_refund, precondition):
    hotel_system.add_room(101, 'single', 100.0)
    if precondition:
        precondition(hotel_system)
    if isinstance(expected_refund, type) and issubclass(expected_refund, Exception):
        with pytest.raises(expected_refund):
            hotel_system.cancel_reservation(reservation_id)
    else:
        refund = hotel_system.cancel_reservation(reservation_id)
        assert refund == expected_refund

def test_get_room_occupancy(hotel_system):
    hotel_system.add_room(101, 'single', 100.0)
    check_in = datetime.date.today() + timedelta(days=1)
    check_out = check_in + timedelta(days=2)
    hotel_system.book_room(101, 'John Doe', check_in, check_out)
    occupied_rooms = hotel_system.get_room_occupancy(check_in + timedelta(days=1))
    assert occupied_rooms == [101]

import datetime
from datetime import timedelta

def test_cancel_reservation_2_7_days(hotel_system):
    # Setup
    hotel_system.add_room(101, 'single', 100.0)
    # Dummy reservations to reach RES-0003
    hotel_system.book_room(101, 'Dummy1', datetime.date.today() + timedelta(days=20),
                           datetime.date.today() + timedelta(days=22))
    hotel_system.book_room(101, 'Dummy2', datetime.date.today() + timedelta(days=30),
                           datetime.date.today() + timedelta(days=32))
    # Target reservation: 5 days from today, 2 nights
    check_in = datetime.date.today() + timedelta(days=5)
    check_out = check_in + timedelta(days=2)
    res_id = hotel_system.book_room(101, 'John Doe', check_in, check_out)
    assert res_id == 'RES-0003'
    # Action & Assertion
    refund = hotel_system.cancel_reservation(res_id)
    assert refund == 100.0  # 50% of 200.0

def test_cancel_reservation_less_2_days(hotel_system):
    # Setup
    hotel_system.add_room(101, 'single', 100.0)
    # Dummy reservations to reach RES-0004
    hotel_system.book_room(101, 'Dummy1', datetime.date.today() + timedelta(days=20),
                           datetime.date.today() + timedelta(days=22))
    hotel_system.book_room(101, 'Dummy2', datetime.date.today() + timedelta(days=30),
                           datetime.date.today() + timedelta(days=32))
    hotel_system.book_room(101, 'Dummy3', datetime.date.today() + timedelta(days=40),
                           datetime.date.today() + timedelta(days=42))
    # Target reservation: 1 day from today, 1 night
    check_in = datetime.date.today() + timedelta(days=1)
    check_out = check_in + timedelta(days=1)
    res_id = hotel_system.book_room(101, 'John Doe', check_in, check_out)
    assert res_id == 'RES-0004'
    # Action & Assertion
    refund = hotel_system.cancel_reservation(res_id)
    assert refund == 0.0  # < 2 days => no refund

def test_cancel_reservation_edge_cases(hotel_system):
    # Setup
    hotel_system.add_room(101, 'single', 100.0)
    # Dummy reservations to reach RES-0005
    hotel_system.book_room(101, 'Dummy1', datetime.date.today() + timedelta(days=20),
                           datetime.date.today() + timedelta(days=22))
    hotel_system.book_room(101, 'Dummy2', datetime.date.today() + timedelta(days=30),
                           datetime.date.today() + timedelta(days=32))
    hotel_system.book_room(101, 'Dummy3', datetime.date.today() + timedelta(days=40),
                           datetime.date.today() + timedelta(days=42))
    hotel_system.book_room(101, 'Dummy4', datetime.date.today() + timedelta(days=50),
                           datetime.date.today() + timedelta(days=52))
    # Target reservation: 8 days from today, 2 nights
    check_in = datetime.date.today() + timedelta(days=8)
    check_out = check_in + timedelta(days=2)
    res_id = hotel_system.book_room(101, 'John Doe', check_in, check_out)
    assert res_id == 'RES-0005'
    # Action & Assertion
    refund = hotel_system.cancel_reservation(res_id)
    assert refund == 200.0  # > 7 days => full refund

def test_book_room_edge_cases(hotel_system):
    hotel_system.add_room(101, 'single', 100.0)
    check_in = datetime.date.today() + timedelta(days=7)
    check_out = datetime.date.today() + timedelta(days=14)
    res_id = hotel_system.book_room(101, 'John Doe', check_in, check_out)
    assert res_id.startswith('RES-')

def test_get_room_occupancy_edge_cases(hotel_system):
    hotel_system.add_room(101, 'single', 100.0)
    date_to_check = datetime.date.today() + timedelta(days=1)
    occupied_rooms = hotel_system.get_room_occupancy(date_to_check)
    assert occupied_rooms == []