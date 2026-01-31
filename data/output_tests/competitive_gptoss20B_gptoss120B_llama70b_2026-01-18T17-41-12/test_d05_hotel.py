import pytest
from data.input_code.d05_hotel import *
from datetime import date, timedelta

@pytest.fixture
def hotel_system():
    return HotelReservationSystem()

def test_add_room_success(hotel_system):
    hotel_system.add_room(101, "single", 120.0)
    assert 101 in hotel_system.rooms

def test_add_room_error():
    hotel_system = HotelReservationSystem()
    with pytest.raises(ValueError):
        hotel_system.add_room(102, "double", 0)

def test_book_room_success(hotel_system):
    hotel_system.add_room(101, "single", 120.0)
    check_in = date.today() + timedelta(days=1)
    check_out = check_in + timedelta(days=2)
    res_id = hotel_system.book_room(101, "Alice", check_in, check_out)
    assert res_id in hotel_system.reservations

def test_book_room_room_not_found(hotel_system):
    check_in = date.today() + timedelta(days=1)
    check_out = check_in + timedelta(days=2)
    with pytest.raises(RoomNotFoundError):
        hotel_system.book_room(101, "Alice", check_in, check_out)

def test_book_room_room_unavailable(hotel_system):
    hotel_system.add_room(101, "single", 120.0)
    check_in = date.today() + timedelta(days=1)
    check_out = check_in + timedelta(days=2)
    hotel_system.book_room(101, "Alice", check_in, check_out)
    with pytest.raises(RoomUnavailableError):
        hotel_system.book_room(101, "Bob", check_in + timedelta(days=1), check_out + timedelta(days=1))

def test_book_room_invalid_date(hotel_system):
    hotel_system.add_room(101, "single", 120.0)
    check_in = date.today() + timedelta(days=1)
    check_out = check_in
    with pytest.raises(InvalidDateError):
        hotel_system.book_room(101, "Alice", check_in, check_out)

def test_book_room_past_date(hotel_system):
    hotel_system.add_room(101, "single", 120.0)
    check_in = date.today() - timedelta(days=1)
    check_out = check_in + timedelta(days=2)
    with pytest.raises(InvalidDateError):
        hotel_system.book_room(101, "Alice", check_in, check_out)

def test_cancel_reservation_success(hotel_system):
    hotel_system.add_room(101, "single", 120.0)
    check_in = date.today() + timedelta(days=10)
    check_out = check_in + timedelta(days=2)
    res_id = hotel_system.book_room(101, "Alice", check_in, check_out)
    # Capture reservation details before cancellation
    reservation = hotel_system.reservations[res_id]
    refund = hotel_system.cancel_reservation(res_id)
    assert refund == reservation.total_price

def test_cancel_reservation_not_found(hotel_system):
    with pytest.raises(ReservationNotFoundError):
        hotel_system.cancel_reservation("RES-9999")

def test_get_room_occupancy(hotel_system):
    hotel_system.add_room(101, "single", 120.0)
    check_in = date.today() + timedelta(days=1)
    check_out = check_in + timedelta(days=2)
    hotel_system.book_room(101, "Alice", check_in, check_out)
    occupied_rooms = hotel_system.get_room_occupancy(check_in)
    assert occupied_rooms == [101]

def test_get_room_occupancy_empty(hotel_system):
    occupied_rooms = hotel_system.get_room_occupancy(date.today())
    assert occupied_rooms == []

def test_cancel_reservation_half_refund(hotel_system):
    hotel_system.add_room(101, "single", 120.0)
    check_in = date.today() + timedelta(days=5)
    check_out = check_in + timedelta(days=2)
    res_id = hotel_system.book_room(101, "Alice", check_in, check_out)
    # Capture reservation details before cancellation
    reservation = hotel_system.reservations[res_id]
    refund = hotel_system.cancel_reservation(res_id)
    expected_refund = round(reservation.total_price * 0.5, 2)
    assert refund == expected_refund

def test_cancel_reservation_no_refund(hotel_system):
    hotel_system.add_room(101, "single", 120.0)
    check_in = date.today() + timedelta(days=1)
    check_out = check_in + timedelta(days=2)
    res_id = hotel_system.book_room(101, "Alice", check_in, check_out)
    refund = hotel_system.cancel_reservation(res_id)
    assert refund == 0.0