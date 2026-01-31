import pytest
import datetime
from datetime import timedelta
from data.input_code.d05_hotel import *

# Helper function to create a HotelReservationSystem instance with some rooms
def create_hotel_reservation_system():
    hrs = HotelReservationSystem()
    hrs.add_room(101, 'single', 100.0)
    hrs.add_room(102, 'double', 200.0)
    return hrs

def test_add_room_success():
    hrs = HotelReservationSystem()
    hrs.add_room(101, 'single', 100.0)
    assert 101 in hrs.rooms
    assert hrs.rooms[101]['type'] == 'single'
    assert hrs.rooms[101]['price_per_night'] == 100.0

@pytest.mark.parametrize('room_number, room_type, price_per_night, expected', [
    (102, 'double', 0.0, ValueError)
])
def test_add_room_error(room_number, room_type, price_per_night, expected):
    hrs = HotelReservationSystem()
    with pytest.raises(expected):
        hrs.add_room(room_number, room_type, price_per_night)

@pytest.mark.parametrize('room_number, user_name, check_in, check_out, expected', [
    # Use dates relative to today to avoid past booking errors
    (101, 'John Doe',
     datetime.date.today() + timedelta(days=1),
     datetime.date.today() + timedelta(days=3),
     'RES-0001')
])
def test_book_room_success(room_number, user_name, check_in, check_out, expected):
    hrs = create_hotel_reservation_system()
    res_id = hrs.book_room(room_number, user_name, check_in, check_out)
    assert res_id.startswith('RES-')

@pytest.mark.parametrize('room_number, user_name, check_in, check_out, expected', [
    # Room does not exist
    (103, 'Jane Doe',
     datetime.date.today() + timedelta(days=1),
     datetime.date.today() + timedelta(days=3),
     RoomNotFoundError),
    # Check-in after check-out
    (101, 'John Doe',
     datetime.date.today() + timedelta(days=5),
     datetime.date.today() + timedelta(days=3),
     InvalidDateError),
    # Dates in the past
    (101, 'John Doe',
     datetime.date(2022, 9, 20),
     datetime.date(2022, 9, 22),
     InvalidDateError)
])
def test_book_room_error(room_number, user_name, check_in, check_out, expected):
    hrs = create_hotel_reservation_system()
    with pytest.raises(expected):
        hrs.book_room(room_number, user_name, check_in, check_out)

def test_cancel_reservation_success():
    hrs = create_hotel_reservation_system()
    # Book a reservation in the future
    check_in = datetime.date.today() + timedelta(days=1)
    check_out = datetime.date.today() + timedelta(days=3)
    res_id = hrs.book_room(101, 'John Doe', check_in, check_out)
    refund = hrs.cancel_reservation(res_id)
    # Since cancellation is less than 2 days before check-in, no refund
    assert refund == 0.0

@pytest.mark.parametrize('reservation_id, expected', [
    ('RES-0002', ReservationNotFoundError)
])
def test_cancel_reservation_error(reservation_id, expected):
    hrs = create_hotel_reservation_system()
    with pytest.raises(expected):
        hrs.cancel_reservation(reservation_id)

def test_get_room_occupancy():
    hrs = create_hotel_reservation_system()
    # Book a reservation in the future
    check_in = datetime.date.today() + timedelta(days=1)
    check_out = datetime.date.today() + timedelta(days=3)
    hrs.book_room(101, 'John Doe', check_in, check_out)
    # Occupancy on a date within the reservation period
    occupied_rooms = hrs.get_room_occupancy(check_in + timedelta(days=1))
    assert occupied_rooms == [101]

@pytest.mark.parametrize('room_number, user_name, check_in, check_out, expected', [
    (101, 'John Doe',
     datetime.date.today() + timedelta(days=7),
     datetime.date.today() + timedelta(days=7),
     InvalidDateError),
])
def test_book_room_edge(room_number, user_name, check_in, check_out, expected):
    hrs = create_hotel_reservation_system()
    with pytest.raises(expected):
        hrs.book_room(room_number, user_name, check_in, check_out)

def test_cancel_refund_100():
    hrs = create_hotel_reservation_system()
    check_in = datetime.date.today() + timedelta(days=8)
    check_out = datetime.date.today() + timedelta(days=10)
    res_id = hrs.book_room(101, 'John Doe', check_in, check_out)
    # Capture total price before cancellation
    total_price = hrs.reservations[res_id].total_price
    refund = hrs.cancel_reservation(res_id)
    assert refund == total_price

@pytest.mark.parametrize('reservation_id, expected', [
    ('RES-0002', 100.0),
])
def test_cancel_refund_50(reservation_id, expected):
    hrs = create_hotel_reservation_system()
    # Manually create a reservation for testing
    check_in = datetime.date.today() + timedelta(days=5)
    check_out = datetime.date.today() + timedelta(days=7)
    hrs._reservation_counter += 1
    res_id = f"RES-{hrs._reservation_counter:04d}"
    new_reservation = Reservation(
        reservation_id=res_id,
        room_number=101,
        user_name='Test',
        check_in=check_in,
        check_out=check_out,
        total_price=200.0
    )
    hrs.reservations[res_id] = new_reservation
    refund = hrs.cancel_reservation(res_id)
    assert refund == expected

def test_get_occupancy_edge():
    hrs = create_hotel_reservation_system()
    check_in = datetime.date.today() + timedelta(days=1)
    check_out = datetime.date.today() + timedelta(days=3)
    hrs.book_room(101, 'John Doe', check_in, check_out)
    occupied_rooms = hrs.get_room_occupancy(check_in)
    assert occupied_rooms == [101]

@pytest.mark.parametrize('room_number, user_name, check_in, check_out, expected', [
    (101, 'Jane Doe',
     datetime.date.today() + timedelta(days=1),
     datetime.date.today() + timedelta(days=3),
     RoomUnavailableError),
])
def test_book_room_double_booking(room_number, user_name, check_in, check_out, expected):
    hrs = create_hotel_reservation_system()
    hrs.book_room(101, 'John Doe', check_in, check_out)
    with pytest.raises(expected):
        hrs.book_room(room_number, user_name, check_in, check_out)