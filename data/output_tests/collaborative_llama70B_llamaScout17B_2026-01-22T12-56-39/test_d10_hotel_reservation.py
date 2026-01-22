import pytest
from data.input_code.d10_hotel_reservation import *
import datetime

@pytest.fixture
def hotel_reservation_system():
    return HotelReservationSystem()

def test_book_room_edge_case_same_day(hotel_reservation_system):
    hotel_reservation_system.add_room(1, "single", 100.0)
    check_in = datetime.date.today()
    check_out = check_in + datetime.timedelta(days=1)
    result = hotel_reservation_system.book_room(1, "John Doe", check_in, check_out)
    assert result.startswith("RES-")

def test_book_room_invalid_dates(hotel_reservation_system):
    hotel_reservation_system.add_room(1, "single", 100.0)
    check_in = datetime.date.today() + datetime.timedelta(days=1)
    check_out = check_in
    with pytest.raises(InvalidDateError):
        hotel_reservation_system.book_room(1, "John Doe", check_in, check_out)

def test_book_room_past_date(hotel_reservation_system):
    hotel_reservation_system.add_room(1, "single", 100.0)
    check_in = datetime.date.today() - datetime.timedelta(days=1)
    check_out = check_in + datetime.timedelta(days=1)
    with pytest.raises(InvalidDateError):
        hotel_reservation_system.book_room(1, "John Doe", check_in, check_out)

def test_book_room_non_existent_room(hotel_reservation_system):
    check_in = datetime.date.today() + datetime.timedelta(days=1)
    check_out = check_in + datetime.timedelta(days=1)
    with pytest.raises(RoomNotFoundError):
        hotel_reservation_system.book_room(1, "John Doe", check_in, check_out)

def test_book_room_unavailable_room(hotel_reservation_system):
    hotel_reservation_system.add_room(1, "single", 100.0)
    check_in = datetime.date.today() + datetime.timedelta(days=1)
    check_out = check_in + datetime.timedelta(days=1)
    hotel_reservation_system.book_room(1, "John Doe", check_in, check_out)
    check_in_new = check_in
    check_out_new = check_out
    with pytest.raises(RoomUnavailableError):
        hotel_reservation_system.book_room(1, "Jane Doe", check_in_new, check_out_new)

@pytest.mark.parametrize("days_until_checkin, expected_refund", [
    (10, 100.0),  # 100% refund
    (5, 50.0),    # 50% refund
    (1, 0.0)      # 0% refund
])
def test_cancel_reservation(hotel_reservation_system, days_until_checkin, expected_refund):
    hotel_reservation_system.add_room(1, "single", 100.0)
    check_in = datetime.date.today() + datetime.timedelta(days=days_until_checkin)
    check_out = check_in + datetime.timedelta(days=1)
    res_id = hotel_reservation_system.book_room(1, "John Doe", check_in, check_out)
    refund = hotel_reservation_system.cancel_reservation(res_id)
    assert refund == expected_refund

def test_get_room_occupancy(hotel_reservation_system):
    hotel_reservation_system.add_room(1, "single", 100.0)
    check_in = datetime.date.today() + datetime.timedelta(days=1)
    check_out = check_in + datetime.timedelta(days=1)
    hotel_reservation_system.book_room(1, "John Doe", check_in, check_out)
    occupied_rooms = hotel_reservation_system.get_room_occupancy(check_in)
    assert occupied_rooms == [1]

    # Test for unoccupied room
    occupied_rooms = hotel_reservation_system.get_room_occupancy(datetime.date.today())
    assert occupied_rooms == []

def test_add_room_price_zero(hotel_reservation_system):
    with pytest.raises(ValueError):
        hotel_reservation_system.add_room(1, "single", 0.0)

@pytest.mark.parametrize("check_in, check_out, expected", [
    ("2024-01-01", "2024-01-01", InvalidDateError),
    ("2024-01-02", "2024-01-01", InvalidDateError)
])
def test_book_room_invalid_date_range(hotel_reservation_system, check_in, check_out, expected):
    hotel_reservation_system.add_room(1, "single", 100.0)
    check_in_date = datetime.datetime.strptime(check_in, "%Y-%m-%d").date()
    check_out_date = datetime.datetime.strptime(check_out, "%Y-%m-%d").date()
    with pytest.raises(expected):
        hotel_reservation_system.book_room(1, "John Doe", check_in_date, check_out_date)

def test_cancel_reservation_non_existent_reservation(hotel_reservation_system):
    with pytest.raises(ReservationNotFoundError):
        hotel_reservation_system.cancel_reservation("RES-0001")

def test_get_room_occupancy_no_reservations(hotel_reservation_system):
    occupied_rooms = hotel_reservation_system.get_room_occupancy(datetime.date.today())
    assert occupied_rooms == []

def test_get_room_occupancy_multiple_reservations(hotel_reservation_system):
    hotel_reservation_system.add_room(1, "single", 100.0)
    hotel_reservation_system.add_room(2, "double", 150.0)
    check_in = datetime.date.today() + datetime.timedelta(days=1)
    check_out = check_in + datetime.timedelta(days=1)
    hotel_reservation_system.book_room(1, "John Doe", check_in, check_out)
    hotel_reservation_system.book_room(2, "Jane Doe", check_in, check_out)
    occupied_rooms = hotel_reservation_system.get_room_occupancy(check_in)
    assert occupied_rooms == [1, 2]

def test_book_room_multiple_reservations_same_room(hotel_reservation_system):
    hotel_reservation_system.add_room(1, "single", 100.0)
    check_in = datetime.date.today() + datetime.timedelta(days=1)
    check_out = check_in + datetime.timedelta(days=1)
    hotel_reservation_system.book_room(1, "John Doe", check_in, check_out)
    with pytest.raises(RoomUnavailableError):
        hotel_reservation_system.book_room(1, "Jane Doe", check_in, check_out)

def test_book_room_multiple_reservations_different_rooms(hotel_reservation_system):
    hotel_reservation_system.add_room(1, "single", 100.0)
    check_in = datetime.date.today() + datetime.timedelta(days=1)
    check_out = check_in + datetime.timedelta(days=1)
    hotel_reservation_system.book_room(1, "John Doe", check_in, check_out)
    with pytest.raises(RoomNotFoundError):
        hotel_reservation_system.book_room(2, "Jane Doe", check_in, check_out)