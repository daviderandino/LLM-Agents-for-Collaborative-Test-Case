import pytest
from data.input_code.05_hotel import HotelReservationSystem, RoomNotFoundError, RoomUnavailableError, InvalidDateError, ReservationNotFoundError
from datetime import date, timedelta

@pytest.fixture
def hotel_system():
    return HotelReservationSystem()

def test_add_room(hotel_system):
    hotel_system.add_room(1, "single", 100.0)
    assert hotel_system.rooms[1] == {'type': 'single', 'price_per_night': 100.0}

def test_add_room_error(hotel_system):
    with pytest.raises(ValueError):
        hotel_system.add_room(1, "single", -1.0)

def test_book_room(hotel_system):
    hotel_system.add_room(1, "single", 100.0)
    today = date.today()
    res_id = hotel_system.book_room(1, "John Doe", today + timedelta(days=1), today + timedelta(days=3))
    assert res_id == "RES-0001"

def test_book_room_room_not_found(hotel_system):
    with pytest.raises(RoomNotFoundError):
        hotel_system.book_room(2, "John Doe", date.today() + timedelta(days=1), date.today() + timedelta(days=3))

def test_book_room_invalid_dates(hotel_system):
    hotel_system.add_room(1, "single", 100.0)
    with pytest.raises(InvalidDateError):
        hotel_system.book_room(1, "John Doe", date.today() + timedelta(days=3), date.today() + timedelta(days=1))

def test_book_room_room_unavailable(hotel_system):
    hotel_system.add_room(1, "single", 100.0)
    hotel_system.book_room(1, "John Doe", date.today() + timedelta(days=1), date.today() + timedelta(days=3))
    with pytest.raises(RoomUnavailableError):
        hotel_system.book_room(1, "John Doe", date.today() + timedelta(days=2), date.today() + timedelta(days=4))

def test_cancel_reservation(hotel_system):
    hotel_system.add_room(1, "single", 100.0)
    today = date.today()
    res_id = hotel_system.book_room(1, "John Doe", today + timedelta(days=10), today + timedelta(days=12))
    refund = hotel_system.cancel_reservation(res_id)
    assert refund == 200.0

def test_cancel_reservation_not_found(hotel_system):
    with pytest.raises(ReservationNotFoundError):
        hotel_system.cancel_reservation("RES-0001")

def test_get_room_occupancy(hotel_system):
    hotel_system.add_room(1, "single", 100.0)
    today = date.today()
    hotel_system.book_room(1, "John Doe", today + timedelta(days=1), today + timedelta(days=3))
    occupied_rooms = hotel_system.get_room_occupancy(today + timedelta(days=2))
    assert occupied_rooms == [1]

def test_get_room_occupancy_empty(hotel_system):
    occupied_rooms = hotel_system.get_room_occupancy(date.today() + timedelta(days=10))
    assert occupied_rooms == []

def test_book_room_past_date(hotel_system):
    hotel_system.add_room(1, "single", 100.0)
    with pytest.raises(InvalidDateError):
        hotel_system.book_room(1, "John Doe", date.today() - timedelta(days=1), date.today() + timedelta(days=1))

def test_cancel_reservation_50_percent_refund(hotel_system):
    hotel_system.add_room(1, "single", 100.0)
    today = date.today()
    res_id = hotel_system.book_room(1, "John Doe", today + timedelta(days=5), today + timedelta(days=7))
    refund = hotel_system.cancel_reservation(res_id)
    assert refund == 100.0

def test_cancel_reservation_0_percent_refund(hotel_system):
    hotel_system.add_room(1, "single", 100.0)
    today = date.today()
    res_id = hotel_system.book_room(1, "John Doe", today + timedelta(days=1), today + timedelta(days=3))
    refund = hotel_system.cancel_reservation(res_id)
    assert refund == 0.0

def test_get_room_occupancy_multiple_rooms(hotel_system):
    hotel_system.add_room(1, "single", 100.0)
    hotel_system.add_room(2, "single", 100.0)
    today = date.today()
    hotel_system.book_room(1, "John Doe", today + timedelta(days=1), today + timedelta(days=3))
    hotel_system.book_room(2, "Jane Doe", today + timedelta(days=1), today + timedelta(days=3))
    occupied_rooms = hotel_system.get_room_occupancy(today + timedelta(days=2))
    assert occupied_rooms == [1, 2]

def test_book_room_edge_case(hotel_system):
    hotel_system.add_room(1, "single", 100.0)
    today = date.today()
    with pytest.raises(InvalidDateError):
        hotel_system.book_room(1, "John Doe", today + timedelta(days=1), today + timedelta(days=1))