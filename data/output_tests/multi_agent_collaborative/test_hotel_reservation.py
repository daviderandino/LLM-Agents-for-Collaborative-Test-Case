import pytest
from data.input_code.hotel_reservation import (
    HotelReservationSystem,
    RoomNotFoundError,
    RoomUnavailableError,
    InvalidDateError,
    ReservationNotFoundError,
    Reservation
)
from datetime import date, timedelta

@pytest.fixture
def hotel_reservation_system():
    return HotelReservationSystem()

def test_add_room(hotel_reservation_system):
    hotel_reservation_system.add_room(1, 'single', 100.0)
    assert hotel_reservation_system.rooms == {1: {'type': 'single', 'price_per_night': 100.0}}

def test_add_room_overwrite(hotel_reservation_system):
    hotel_reservation_system.add_room(1, 'single', 100.0)
    hotel_reservation_system.add_room(1, 'double', 200.0)
    assert hotel_reservation_system.rooms == {1: {'type': 'double', 'price_per_night': 200.0}}

def test_add_room_invalid_price(hotel_reservation_system):
    with pytest.raises(ValueError):
        hotel_reservation_system.add_room(1, 'single', -100.0)

def test_book_room(hotel_reservation_system):
    hotel_reservation_system.add_room(1, 'single', 100.0)
    check_in = date.today() + timedelta(days=1)
    check_out = check_in + timedelta(days=1)
    reservation_id = hotel_reservation_system.book_room(1, 'John Doe', check_in, check_out)
    assert reservation_id in hotel_reservation_system.reservations

def test_book_room_non_string_user_name(hotel_reservation_system):
    hotel_reservation_system.add_room(1, 'single', 100.0)
    check_in = date.today() + timedelta(days=1)
    check_out = check_in + timedelta(days=1)
    with pytest.raises(TypeError):
        hotel_reservation_system.book_room(1, 123, check_in, check_out)

def test_book_room_non_integer_room_number(hotel_reservation_system):
    with pytest.raises(TypeError):
        hotel_reservation_system.book_room('a', 'John Doe', date.today() + timedelta(days=1), date.today() + timedelta(days=2))

def test_book_room_negative_room_number(hotel_reservation_system):
    with pytest.raises(RoomNotFoundError):
        hotel_reservation_system.book_room(-1, 'John Doe', date.today() + timedelta(days=1), date.today() + timedelta(days=2))

def test_book_room_room_not_found(hotel_reservation_system):
    check_in = date.today() + timedelta(days=1)
    check_out = check_in + timedelta(days=1)
    with pytest.raises(RoomNotFoundError):
        hotel_reservation_system.book_room(1, 'John Doe', check_in, check_out)

def test_book_room_invalid_dates(hotel_reservation_system):
    hotel_reservation_system.add_room(1, 'single', 100.0)
    check_in = date.today() + timedelta(days=1)
    check_out = check_in - timedelta(days=1)
    with pytest.raises(InvalidDateError):
        hotel_reservation_system.book_room(1, 'John Doe', check_in, check_out)

def test_book_room_check_in_before_today(hotel_reservation_system):
    hotel_reservation_system.add_room(1, 'single', 100.0)
    check_in = date.today() - timedelta(days=1)
    check_out = check_in + timedelta(days=1)
    with pytest.raises(InvalidDateError):
        hotel_reservation_system.book_room(1, 'John Doe', check_in, check_out)

def test_book_room_room_unavailable(hotel_reservation_system):
    hotel_reservation_system.add_room(1, 'single', 100.0)
    check_in = date.today() + timedelta(days=1)
    check_out = check_in + timedelta(days=1)
    hotel_reservation_system.book_room(1, 'John Doe', check_in, check_out)
    with pytest.raises(RoomUnavailableError):
        hotel_reservation_system.book_room(1, 'Jane Doe', check_in, check_out)

def test_cancel_reservation(hotel_reservation_system):
    hotel_reservation_system.add_room(1, 'single', 100.0)
    check_in = date.today() + timedelta(days=10)
    check_out = check_in + timedelta(days=1)
    reservation_id = hotel_reservation_system.book_room(1, 'John Doe', check_in, check_out)
    refund = hotel_reservation_system.cancel_reservation(reservation_id)
    assert refund == 100.0

def test_cancel_reservation_seven_days_before(hotel_reservation_system):
    hotel_reservation_system.add_room(1, 'single', 100.0)
    check_in = date.today() + timedelta(days=7)
    check_out = check_in + timedelta(days=1)
    reservation_id = hotel_reservation_system.book_room(1, 'John Doe', check_in, check_out)
    refund = hotel_reservation_system.cancel_reservation(reservation_id)
    assert refund == 100.0

def test_cancel_reservation_two_days_before(hotel_reservation_system):
    hotel_reservation_system.add_room(1, 'single', 100.0)
    check_in = date.today() + timedelta(days=2)
    check_out = check_in + timedelta(days=1)
    reservation_id = hotel_reservation_system.book_room(1, 'John Doe', check_in, check_out)
    refund = hotel_reservation_system.cancel_reservation(reservation_id)
    assert refund == 50.0

def test_cancel_reservation_one_day_before(hotel_reservation_system):
    hotel_reservation_system.add_room(1, 'single', 100.0)
    check_in = date.today() + timedelta(days=1)
    check_out = check_in + timedelta(days=1)
    reservation_id = hotel_reservation_system.book_room(1, 'John Doe', check_in, check_out)
    refund = hotel_reservation_system.cancel_reservation(reservation_id)
    assert refund == 0.0

def test_cancel_reservation_non_existent_reservation_id(hotel_reservation_system):
    with pytest.raises(ReservationNotFoundError):
        hotel_reservation_system.cancel_reservation('RES-0001')

def test_get_room_occupancy(hotel_reservation_system):
    hotel_reservation_system.add_room(1, 'single', 100.0)
    check_in = date.today()
    check_out = check_in + timedelta(days=1)
    hotel_reservation_system.book_room(1, 'John Doe', check_in, check_out)
    occupied_rooms = hotel_reservation_system.get_room_occupancy(check_in)
    assert occupied_rooms == [1]

def test_get_room_occupancy_no_reservations(hotel_reservation_system):
    occupied_rooms = hotel_reservation_system.get_room_occupancy(date.today())
    assert occupied_rooms == []

def test_book_room_on_first_day_of_year(hotel_reservation_system):
    hotel_reservation_system.add_room(1, 'single', 100.0)
    check_in = date(date.today().year, 1, 1) + timedelta(days=1)
    check_out = check_in + timedelta(days=1)
    reservation_id = hotel_reservation_system.book_room(1, 'John Doe', check_in, check_out)
    assert reservation_id in hotel_reservation_system.reservations

def test_book_room_on_leap_day(hotel_reservation_system):
    hotel_reservation_system.add_room(1, 'single', 100.0)
    check_in = date(date.today().year, 2, 29) + timedelta(days=1)
    check_out = check_in + timedelta(days=1)
    reservation_id = hotel_reservation_system.book_room(1, 'John Doe', check_in, check_out)
    assert reservation_id in hotel_reservation_system.reservations

def test_total_price_calculation(hotel_reservation_system):
    hotel_reservation_system.add_room(1, 'single', 100.0)
    check_in = date.today() + timedelta(days=1)
    check_out = check_in + timedelta(days=3)
    reservation_id = hotel_reservation_system.book_room(1, 'John Doe', check_in, check_out)
    reservation = hotel_reservation_system.reservations[reservation_id]
    assert reservation.total_price == 300.0

def test_total_price_calculation_different_room_types(hotel_reservation_system):
    hotel_reservation_system.add_room(1, 'single', 100.0)
    hotel_reservation_system.add_room(2, 'double', 200.0)
    check_in = date.today() + timedelta(days=1)
    check_out = check_in + timedelta(days=3)
    reservation_id1 = hotel_reservation_system.book_room(1, 'John Doe', check_in, check_out)
    reservation_id2 = hotel_reservation_system.book_room(2, 'Jane Doe', check_in, check_out)
    reservation1 = hotel_reservation_system.reservations[reservation_id1]
    reservation2 = hotel_reservation_system.reservations[reservation_id2]
    assert reservation1.total_price == 300.0
    assert reservation2.total_price == 600.0

def test_total_price_calculation_different_lengths_of_stay(hotel_reservation_system):
    hotel_reservation_system.add_room(1, 'single', 100.0)
    check_in1 = date.today() + timedelta(days=1)
    check_out1 = check_in1 + timedelta(days=3)
    check_in2 = date.today() + timedelta(days=1)
    check_out2 = check_in2 + timedelta(days=5)
    reservation_id1 = hotel_reservation_system.book_room(1, 'John Doe', check_in1, check_out1)
    reservation_id2 = hotel_reservation_system.book_room(1, 'Jane Doe', check_in2, check_out2)
    reservation1 = hotel_reservation_system.reservations[reservation_id1]
    reservation2 = hotel_reservation_system.reservations[reservation_id2]
    assert reservation1.total_price == 300.0
    assert reservation2.total_price == 500.0

def test_cancel_reservation_multiple_bookings_for_same_room(hotel_reservation_system):
    hotel_reservation_system.add_room(1, 'single', 100.0)
    check_in1 = date.today() + timedelta(days=10)
    check_out1 = check_in1 + timedelta(days=1)
    check_in2 = date.today() + timedelta(days=15)
    check_out2 = check_in2 + timedelta(days=1)
    reservation_id1 = hotel_reservation_system.book_room(1, 'John Doe', check_in1, check_out1)
    reservation_id2 = hotel_reservation_system.book_room(1, 'Jane Doe', check_in2, check_out2)
    refund1 = hotel_reservation_system.cancel_reservation(reservation_id1)
    refund2 = hotel_reservation_system.cancel_reservation(reservation_id2)
    assert refund1 == 100.0
    assert refund2 == 100.0

def test_cancel_reservation_multiple_bookings_for_different_rooms(hotel_reservation_system):
    hotel_reservation_system.add_room(1, 'single', 100.0)
    hotel_reservation_system.add_room(2, 'double', 200.0)
    check_in1 = date.today() + timedelta(days=10)
    check_out1 = check_in1 + timedelta(days=1)
    check_in2 = date.today() + timedelta(days=15)
    check_out2 = check_in2 + timedelta(days=1)
    reservation_id1 = hotel_reservation_system.book_room(1, 'John Doe', check_in1, check_out1)
    reservation_id2 = hotel_reservation_system.book_room(2, 'Jane Doe', check_in2, check_out2)
    refund1 = hotel_reservation_system.cancel_reservation(reservation_id1)
    refund2 = hotel_reservation_system.cancel_reservation(reservation_id2)
    assert refund1 == 100.0
    assert refund2 == 200.0