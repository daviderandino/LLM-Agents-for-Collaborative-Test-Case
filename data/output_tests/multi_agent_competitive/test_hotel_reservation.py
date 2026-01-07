import pytest
from data.input_code.hotel_reservation import *
import datetime

@pytest.fixture
def hotel_reservation_system():
    return HotelReservationSystem()

@pytest.mark.parametrize('room_number, room_type, price_per_night, expected', [
    (101, 'single', 100.0, None),
])
def test_add_room_success(hotel_reservation_system, room_number, room_type, price_per_night, expected):
    assert hotel_reservation_system.add_room(room_number, room_type, price_per_night) == expected

def test_add_room_error(hotel_reservation_system):
    with pytest.raises(ValueError):
        hotel_reservation_system.add_room(101, 'single', 0.0)

@pytest.mark.parametrize('room_number, user_name, check_in, check_out, expected', [
    (101, 'John Doe', datetime.date(2030, 1, 10), datetime.date(2030, 1, 12), 'RES-0001'),
])
def test_book_room_success(hotel_reservation_system, room_number, user_name, check_in, check_out, expected):
    hotel_reservation_system.add_room(room_number, 'single', 100.0)
    assert hotel_reservation_system.book_room(room_number, user_name, check_in, check_out) == expected

@pytest.mark.parametrize('room_number, user_name, check_in, check_out, expected_exception', [
    (102, 'John Doe', datetime.date(2030, 1, 1), datetime.date(2030, 1, 3), RoomNotFoundError),
    (101, 'John Doe', datetime.date(2030, 1, 1), datetime.date(2030, 1, 1), InvalidDateError),
    (101, 'John Doe', datetime.date(2024, 9, 15), datetime.date(2024, 9, 17), InvalidDateError),
])
def test_book_room_error(hotel_reservation_system, room_number, user_name, check_in, check_out, expected_exception):
    hotel_reservation_system.add_room(101, 'single', 100.0)
    with pytest.raises(expected_exception):
        hotel_reservation_system.book_room(room_number, user_name, check_in, check_out)

def test_book_room_unavailable(hotel_reservation_system):
    hotel_reservation_system.add_room(101, 'single', 100.0)
    hotel_reservation_system.book_room(101, 'John Doe', datetime.date(2030, 1, 1), datetime.date(2030, 1, 3))
    with pytest.raises(RoomUnavailableError):
        hotel_reservation_system.book_room(101, 'Jane Doe', datetime.date(2030, 1, 1), datetime.date(2030, 1, 3))

@pytest.mark.parametrize('check_in, check_out, expected_refund', [
    (datetime.date(2030, 1, 10), datetime.date(2030, 1, 12), 200.0),  
    (datetime.date.today() + datetime.timedelta(days=5), datetime.date.today() + datetime.timedelta(days=7), 100.0),  
    (datetime.date.today() + datetime.timedelta(days=1), datetime.date.today() + datetime.timedelta(days=3), 0.0),  
])
def test_cancel_reservation_success(hotel_reservation_system, check_in, check_out, expected_refund):
    hotel_reservation_system.add_room(101, 'single', 100.0)
    res_id = hotel_reservation_system.book_room(101, 'John Doe', check_in, check_out)
    assert hotel_reservation_system.cancel_reservation(res_id) == expected_refund

def test_cancel_reservation_error(hotel_reservation_system):
    with pytest.raises(ReservationNotFoundError):
        hotel_reservation_system.cancel_reservation('RES-0002')

@pytest.mark.parametrize('date, expected', [
    (datetime.date(2024, 9, 20), []),
])
def test_get_room_occupancy(hotel_reservation_system, date, expected):
    assert hotel_reservation_system.get_room_occupancy(date) == expected

@pytest.mark.parametrize('room_number, check_in, check_out, expected', [
    (101, datetime.date(2024, 9, 20), datetime.date(2024, 9, 22), True),
])
def test_is_room_available(hotel_reservation_system, room_number, check_in, check_out, expected):
    hotel_reservation_system.add_room(room_number, 'single', 100.0)
    assert hotel_reservation_system._is_room_available(room_number, check_in, check_out) == expected

@pytest.mark.parametrize('room_number, room_type, price_per_night, expected', [
    (101, 'single', 100.0, None),
])
def test_add_room_success_new(hotel_reservation_system, room_number, room_type, price_per_night, expected):
    assert hotel_reservation_system.add_room(room_number, room_type, price_per_night) == expected

def test_add_room_error_new(hotel_reservation_system):
    with pytest.raises(ValueError):
        hotel_reservation_system.add_room(101, 'single', 0.0)

@pytest.mark.parametrize('room_number, user_name, check_in, check_out, expected', [
    (101, 'John Doe', datetime.date(2030, 1, 10), datetime.date(2030, 1, 12), 'RES-0001'),
])
def test_book_room_success_new(hotel_reservation_system, room_number, user_name, check_in, check_out, expected):
    hotel_reservation_system.add_room(room_number, 'single', 100.0)
    assert hotel_reservation_system.book_room(room_number, user_name, check_in, check_out) == expected

@pytest.mark.parametrize('room_number, user_name, check_in, check_out, expected_exception', [
    (102, 'John Doe', datetime.date(2030, 1, 1), datetime.date(2030, 1, 3), RoomNotFoundError),
    (101, 'John Doe', datetime.date(2030, 1, 1), datetime.date(2030, 1, 1), InvalidDateError),
    (101, 'John Doe', datetime.date(2024, 9, 15), datetime.date(2024, 9, 17), InvalidDateError),
    (101, 'John Doe', datetime.date(2030, 1, 1), datetime.date(2030, 1, 3), RoomUnavailableError),
])
def test_book_room_error_new(hotel_reservation_system, room_number, user_name, check_in, check_out, expected_exception):
    hotel_reservation_system.add_room(101, 'single', 100.0)
    hotel_reservation_system.book_room(101, 'Jane Doe', datetime.date(2030, 1, 1), datetime.date(2030, 1, 3))
    with pytest.raises(expected_exception):
        hotel_reservation_system.book_room(room_number, user_name, check_in, check_out)

@pytest.mark.parametrize('reservation_id, expected', [
    ('RES-0001', 200.0),
])
def test_cancel_reservation_success_new(hotel_reservation_system, reservation_id, expected):
    hotel_reservation_system.add_room(101, 'single', 100.0)
    hotel_reservation_system.book_room(101, 'John Doe', datetime.date(2030, 1, 10), datetime.date(2030, 1, 12))
    assert hotel_reservation_system.cancel_reservation(reservation_id) == expected

def test_cancel_reservation_error_new(hotel_reservation_system):
    with pytest.raises(ReservationNotFoundError):
        hotel_reservation_system.cancel_reservation('RES-0002')

@pytest.mark.parametrize('date, expected', [
    (datetime.date(2024, 9, 20), []),
])
def test_get_room_occupancy_new(hotel_reservation_system, date, expected):
    assert hotel_reservation_system.get_room_occupancy(date) == expected

@pytest.mark.parametrize('room_number, check_in, check_out, expected', [
    (101, datetime.date(2024, 9, 20), datetime.date(2024, 9, 22), True),
])
def test_is_room_available_new(hotel_reservation_system, room_number, check_in, check_out, expected):
    hotel_reservation_system.add_room(room_number, 'single', 100.0)
    assert hotel_reservation_system._is_room_available(room_number, check_in, check_out) == expected

def test_cancel_reservation_edge_case(hotel_reservation_system):
    hotel_reservation_system.add_room(101, 'single', 100.0)
    res_id = hotel_reservation_system.book_room(101, 'John Doe', datetime.date.today(), datetime.date.today() + datetime.timedelta(days=1))
    assert hotel_reservation_system.cancel_reservation(res_id) == 0.0

@pytest.mark.parametrize('date, expected', [
    (datetime.date(2030, 1, 11), [101]),
])
def test_get_room_occupancy_partial(hotel_reservation_system, date, expected):
    hotel_reservation_system.add_room(101, 'single', 100.0)
    hotel_reservation_system.book_room(101, 'John Doe', datetime.date(2030, 1, 10), datetime.date(2030, 1, 12))
    assert hotel_reservation_system.get_room_occupancy(date) == expected

def test_book_room_same_day(hotel_reservation_system):
    hotel_reservation_system.add_room(101, 'single', 100.0)
    with pytest.raises(InvalidDateError):
        hotel_reservation_system.book_room(101, 'John Doe', datetime.date.today(), datetime.date.today())

@pytest.mark.parametrize('room_number, check_in, check_out, expected', [
    (101, datetime.date(2030, 1, 1), datetime.date(2030, 1, 3), False),
])
def test_is_room_available_overlap(hotel_reservation_system, room_number, check_in, check_out, expected):
    hotel_reservation_system.add_room(room_number, 'single', 100.0)
    hotel_reservation_system.book_room(room_number, 'Jane Doe', datetime.date(2030, 1, 1), datetime.date(2030, 1, 3))
    assert hotel_reservation_system._is_room_available(room_number, check_in, check_out) == expected