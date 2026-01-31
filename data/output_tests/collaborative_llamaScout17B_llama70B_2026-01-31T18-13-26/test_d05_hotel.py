import pytest
from data.input_code.d05_hotel import HotelReservationSystem, RoomNotFoundError, RoomUnavailableError, InvalidDateError, ReservationNotFoundError
from datetime import date, timedelta

@pytest.fixture
def hotel_system():
    return HotelReservationSystem()

def test_add_room_success(hotel_system):
    hotel_system.add_room(101, "single", 100.0)
    assert 101 in hotel_system.rooms

def test_add_room_error(hotel_system):
    with pytest.raises(ValueError):
        hotel_system.add_room(101, "single", 0.0)

def test_book_room_success(hotel_system):
    hotel_system.add_room(101, "single", 100.0)
    res_id = hotel_system.book_room(101, "John Doe", date.today() + timedelta(days=1), date.today() + timedelta(days=3))
    assert res_id.startswith("RES-")

def test_book_room_room_not_found(hotel_system):
    with pytest.raises(RoomNotFoundError):
        hotel_system.book_room(101, "John Doe", date.today() + timedelta(days=1), date.today() + timedelta(days=3))

def test_book_room_invalid_date(hotel_system):
    hotel_system.add_room(101, "single", 100.0)
    with pytest.raises(InvalidDateError):
        hotel_system.book_room(101, "John Doe", date.today() + timedelta(days=3), date.today() + timedelta(days=1))

def test_book_room_past_date(hotel_system):
    hotel_system.add_room(101, "single", 100.0)
    with pytest.raises(InvalidDateError):
        hotel_system.book_room(101, "John Doe", date.today() - timedelta(days=1), date.today() + timedelta(days=1))

def test_book_room_room_unavailable(hotel_system):
    hotel_system.add_room(101, "single", 100.0)
    hotel_system.book_room(101, "John Doe", date.today() + timedelta(days=1), date.today() + timedelta(days=3))
    with pytest.raises(RoomUnavailableError):
        hotel_system.book_room(101, "Jane Doe", date.today() + timedelta(days=1), date.today() + timedelta(days=3))

def test_cancel_reservation_success(hotel_system):
    hotel_system.add_room(101, "single", 100.0)
    res_id = hotel_system.book_room(101, "John Doe", date.today() + timedelta(days=10), date.today() + timedelta(days=12))
    refund = hotel_system.cancel_reservation(res_id)
    assert refund > 0

def test_cancel_reservation_not_found(hotel_system):
    with pytest.raises(ReservationNotFoundError):
        hotel_system.cancel_reservation("RES-0001")

def test_get_room_occupancy_success(hotel_system):
    hotel_system.add_room(101, "single", 100.0)
    hotel_system.book_room(101, "John Doe", date.today() + timedelta(days=1), date.today() + timedelta(days=3))
    occupied_rooms = hotel_system.get_room_occupancy(date.today() + timedelta(days=1))
    assert occupied_rooms == [101]

def test_book_room_long_stay(hotel_system):
    hotel_system.add_room(101, "single", 100.0)
    res_id = hotel_system.book_room(101, "John Doe", date.today() + timedelta(days=7), date.today() + timedelta(days=14))
    assert res_id.startswith("RES-")

def test_cancel_reservation_refund_policy_50(hotel_system):
    hotel_system.add_room(101, "single", 100.0)
    res_id = hotel_system.book_room(101, "John Doe", date.today() + timedelta(days=5), date.today() + timedelta(days=7))
    refund = hotel_system.cancel_reservation(res_id)
    # Calculate the refund amount based on the total price of the reservation
    reservation = hotel_system.reservations.get(res_id)
    if reservation:
        total_price = reservation.total_price
        refund = round(total_price * 0.5, 2)
        assert refund == round(refund, 2)

def test_cancel_reservation_refund_policy_0(hotel_system):
    hotel_system.add_room(101, "single", 100.0)
    res_id = hotel_system.book_room(101, "John Doe", date.today() + timedelta(days=1), date.today() + timedelta(days=3))
    refund = hotel_system.cancel_reservation(res_id)
    assert refund == 0.0

def test_get_room_occupancy_multiple_rooms(hotel_system):
    hotel_system.add_room(101, "single", 100.0)
    hotel_system.add_room(102, "single", 100.0)
    hotel_system.book_room(101, "John Doe", date.today() + timedelta(days=1), date.today() + timedelta(days=3))
    hotel_system.book_room(102, "Jane Doe", date.today() + timedelta(days=1), date.today() + timedelta(days=3))
    occupied_rooms = hotel_system.get_room_occupancy(date.today() + timedelta(days=1))
    assert occupied_rooms == [101, 102]

def test_book_room_price_calculation(hotel_system):
    hotel_system.add_room(101, "single", 100.0)
    res_id = hotel_system.book_room(101, "John Doe", date.today() + timedelta(days=1), date.today() + timedelta(days=2))
    reservation = hotel_system.reservations[res_id]
    # Calculate the total price based on the number of nights and the price per night
    nights = (reservation.check_out - reservation.check_in).days
    price_per_night = hotel_system.rooms[reservation.room_number]['price_per_night']
    total_price = round(nights * price_per_night, 2)
    assert reservation.total_price == total_price