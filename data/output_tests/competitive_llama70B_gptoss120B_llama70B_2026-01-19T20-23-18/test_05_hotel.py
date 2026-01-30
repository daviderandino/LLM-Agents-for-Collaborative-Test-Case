import pytest
from data.input_code.05_hotel import *
from datetime import date, timedelta

@pytest.fixture
def hotel_reservation_system():
    return HotelReservationSystem()

def test_add_room(hotel_reservation_system):
    hotel_reservation_system.add_room(1, "single", 100.0)
    assert hotel_reservation_system.rooms[1]['type'] == 'single'
    assert hotel_reservation_system.rooms[1]['price_per_night'] == 100.0

def test_add_room_error():
    hotel_reservation_system = HotelReservationSystem()
    with pytest.raises(ValueError):
        hotel_reservation_system.add_room(1, "single", -1.0)

def test_book_room(hotel_reservation_system):
    hotel_reservation_system.add_room(1, "single", 100.0)
    reservation_id = hotel_reservation_system.book_room(1, "John Doe", date.today() + timedelta(days=1), date.today() + timedelta(days=2))
    assert reservation_id == "RES-0001"

def test_book_room_room_not_found(hotel_reservation_system):
    with pytest.raises(RoomNotFoundError):
        hotel_reservation_system.book_room(1, "John Doe", date.today() + timedelta(days=1), date.today() + timedelta(days=2))

def test_book_room_invalid_dates(hotel_reservation_system):
    hotel_reservation_system.add_room(1, "single", 100.0)
    with pytest.raises(InvalidDateError):
        hotel_reservation_system.book_room(1, "John Doe", date.today() + timedelta(days=2), date.today() + timedelta(days=1))

def test_book_room_room_unavailable(hotel_reservation_system):
    hotel_reservation_system.add_room(1, "single", 100.0)
    hotel_reservation_system.book_room(1, "John Doe", date.today() + timedelta(days=1), date.today() + timedelta(days=2))
    with pytest.raises(RoomUnavailableError):
        hotel_reservation_system.book_room(1, "John Doe", date.today() + timedelta(days=1), date.today() + timedelta(days=2))

def test_cancel_reservation(hotel_reservation_system):
    hotel_reservation_system.add_room(1, "single", 100.0)
    reservation_id = hotel_reservation_system.book_room(1, "John Doe", date.today() + timedelta(days=8), date.today() + timedelta(days=9))
    refund = hotel_reservation_system.cancel_reservation(reservation_id)
    assert refund == 100.0

def test_cancel_reservation_error(hotel_reservation_system):
    with pytest.raises(ReservationNotFoundError):
        hotel_reservation_system.cancel_reservation("RES-0001")

def test_get_room_occupancy(hotel_reservation_system):
    hotel_reservation_system.add_room(1, "single", 100.0)
    hotel_reservation_system.book_room(1, "John Doe", date.today(), date.today() + timedelta(days=1))
    occupied_rooms = hotel_reservation_system.get_room_occupancy(date.today())
    assert occupied_rooms == [1]

def test_get_room_occupancy_empty(hotel_reservation_system):
    occupied_rooms = hotel_reservation_system.get_room_occupancy(date.today())
    assert occupied_rooms == []

def test_book_room_past_date(hotel_reservation_system):
    hotel_reservation_system.add_room(1, "single", 100.0)
    with pytest.raises(InvalidDateError):
        hotel_reservation_system.book_room(
            1,
            "John Doe",
            date(2022, 1, 1),
            date(2022, 1, 2)
        )

def test_cancel_reservation_refund_50_percent(hotel_reservation_system):
    hotel_reservation_system.add_room(1, "single", 100.0)
    check_in = date.today() + timedelta(days=5)
    check_out = check_in + timedelta(days=1)
    res_id = hotel_reservation_system.book_room(1, "John Doe", check_in, check_out)
    refund = hotel_reservation_system.cancel_reservation(res_id)
    assert refund == 50.0

def test_cancel_reservation_refund_0_percent(hotel_reservation_system):
    hotel_reservation_system.add_room(1, "single", 100.0)
    check_in = date.today() + timedelta(days=1)
    check_out = check_in + timedelta(days=1)
    res_id = hotel_reservation_system.book_room(1, "John Doe", check_in, check_out)
    refund = hotel_reservation_system.cancel_reservation(res_id)
    assert refund == 0.0

def test_get_room_occupancy_multiple_rooms():
    system = HotelReservationSystem()
    system.add_room(1, "single", 100.0)
    system.add_room(2, "double", 150.0)

    res1 = Reservation(
        reservation_id="RES-0001",
        room_number=1,
        user_name="Alice",
        check_in=date(2024, 9, 16),
        check_out=date(2024, 9, 17),
        total_price=100.0,
    )
    res2 = Reservation(
        reservation_id="RES-0002",
        room_number=2,
        user_name="Bob",
        check_in=date(2024, 9, 16),
        check_out=date(2024, 9, 18),
        total_price=300.0,
    )
    system.reservations[res1.reservation_id] = res1
    system.reservations[res2.reservation_id] = res2

    occupied = system.get_room_occupancy(date(2024, 9, 16))
    assert occupied == [1, 2]

def test_book_room_edge_case_dates(hotel_reservation_system):
    hotel_reservation_system.add_room(1, "single", 100.0)
    check_in = date.today() + timedelta(days=1)
    check_out = check_in + timedelta(days=1)
    res_id = hotel_reservation_system.book_room(1, "John Doe", check_in, check_out)
    assert res_id == "RES-0001"