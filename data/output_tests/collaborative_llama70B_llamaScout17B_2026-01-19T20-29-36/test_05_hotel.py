import pytest
from data.input_code.05_hotel import *
import datetime

@pytest.fixture
def hotel_reservation_system():
    return HotelReservationSystem()

@pytest.mark.parametrize("room_number, room_type, price_per_night", [
    (1, "single", 100.0),
    (2, "double", 200.0),
])
def test_add_room(hotel_reservation_system, room_number, room_type, price_per_night):
    hotel_reservation_system.add_room(room_number, room_type, price_per_night)
    assert hotel_reservation_system.rooms[room_number]['type'] == room_type
    assert hotel_reservation_system.rooms[room_number]['price_per_night'] == price_per_night

def test_add_room_overwrite(hotel_reservation_system):
    hotel_reservation_system.add_room(1, "single", 100.0)
    hotel_reservation_system.add_room(1, "double", 200.0)
    assert hotel_reservation_system.rooms[1]['type'] == "double"
    assert hotel_reservation_system.rooms[1]['price_per_night'] == 200.0

def test_add_room_invalid_price(hotel_reservation_system):
    with pytest.raises(ValueError):
        hotel_reservation_system.add_room(1, "single", 0.0)

@pytest.mark.parametrize("reservation_id, expected", [
    ("RES-0001", 200.0),  # Assuming 2 nights
])
def test_cancel_reservation_success(hotel_reservation_system, reservation_id, expected):
    hotel_reservation_system.add_room(1, "single", 100.0)
    check_in = datetime.date.today() + datetime.timedelta(days=10)
    check_out = check_in + datetime.timedelta(days=2)
    res_id = hotel_reservation_system.book_room(1, "John Doe", check_in, check_out)
    result = hotel_reservation_system.cancel_reservation(res_id)
    assert result == expected

def test_cancel_reservation_already_cancelled(hotel_reservation_system):
    hotel_reservation_system.add_room(1, "single", 100.0)
    check_in = datetime.date.today() + datetime.timedelta(days=10)
    check_out = check_in + datetime.timedelta(days=2)
    res_id = hotel_reservation_system.book_room(1, "John Doe", check_in, check_out)
    hotel_reservation_system.cancel_reservation(res_id)
    with pytest.raises(ReservationNotFoundError):
        hotel_reservation_system.cancel_reservation(res_id)

def test_cancel_reservation_invalid_id(hotel_reservation_system):
    hotel_reservation_system.add_room(1, "single", 100.0)
    check_in = datetime.date.today() + datetime.timedelta(days=10)
    check_out = check_in + datetime.timedelta(days=2)
    hotel_reservation_system.book_room(1, "John Doe", check_in, check_out)
    with pytest.raises(ReservationNotFoundError):
        hotel_reservation_system.cancel_reservation("Invalid-ID")

@pytest.mark.parametrize("check_in, check_out, expected_error", [
    (datetime.date.today() + datetime.timedelta(days=1), datetime.date.today(), InvalidDateError),
    (datetime.date.today() - datetime.timedelta(days=1), datetime.date.today() + datetime.timedelta(days=1), InvalidDateError),
])
def test_book_room_invalid_dates(hotel_reservation_system, check_in, check_out, expected_error):
    hotel_reservation_system.add_room(1, "single", 100.0)
    with pytest.raises(expected_error):
        hotel_reservation_system.book_room(1, "John Doe", check_in, check_out)

def test_book_room_room_not_found(hotel_reservation_system):
    with pytest.raises(RoomNotFoundError):
        hotel_reservation_system.book_room(1, "John Doe", datetime.date.today() + datetime.timedelta(days=1), datetime.date.today() + datetime.timedelta(days=2))

def test_book_room_room_unavailable(hotel_reservation_system):
    hotel_reservation_system.add_room(1, "single", 100.0)
    hotel_reservation_system.book_room(1, "John Doe", datetime.date.today() + datetime.timedelta(days=1), datetime.date.today() + datetime.timedelta(days=2))
    with pytest.raises(RoomUnavailableError):
        hotel_reservation_system.book_room(1, "Jane Doe", datetime.date.today() + datetime.timedelta(days=1), datetime.date.today() + datetime.timedelta(days=2))

@pytest.mark.parametrize("check_in, check_out, expected_error", [
    (datetime.date.today() + datetime.timedelta(days=1), datetime.date.today() + datetime.timedelta(days=1), InvalidDateError),
])
def test_book_room_checkin_checkout_same_day(hotel_reservation_system, check_in, check_out, expected_error):
    hotel_reservation_system.add_room(1, "single", 100.0)
    with pytest.raises(expected_error):
        hotel_reservation_system.book_room(1, "John Doe", check_in, check_out)



def test_cancel_reservation_exactly_2_days(hotel_reservation_system):
    hotel_reservation_system.add_room(1, "single", 100.0)
    check_in = datetime.date.today() + datetime.timedelta(days=2)
    check_out = check_in + datetime.timedelta(days=2)
    res_id = hotel_reservation_system.book_room(1, "John Doe", check_in, check_out)
    result = hotel_reservation_system.cancel_reservation(res_id)
    # Refund policy: 50% refund if 2-7 days from check-in
    assert result == 100.0  # 2 nights * 100 per night * 0.5 

def test_get_room_occupancy_no_reservations(hotel_reservation_system):
    result = hotel_reservation_system.get_room_occupancy(datetime.date.today())
    assert result == []

def test_get_room_occupancy_checkin_date(hotel_reservation_system):
    hotel_reservation_system.add_room(1, "single", 100.0)
    check_in = datetime.date.today() + datetime.timedelta(days=1)
    check_out = check_in + datetime.timedelta(days=2)
    hotel_reservation_system.book_room(1, "John Doe", check_in, check_out)
    result = hotel_reservation_system.get_room_occupancy(check_in)
    assert result == [1]

def test_get_room_occupancy_checkout_date(hotel_reservation_system):
    hotel_reservation_system.add_room(1, "single", 100.0)
    check_in = datetime.date.today() + datetime.timedelta(days=1)
    check_out = check_in + datetime.timedelta(days=2)
    hotel_reservation_system.book_room(1, "John Doe", check_in, check_out)
    result = hotel_reservation_system.get_room_occupancy(check_out)
    assert result == []

def test_book_room_with_multiple_reservations(hotel_reservation_system):
    hotel_reservation_system.add_room(1, "single", 100.0)
    check_in1 = datetime.date.today() + datetime.timedelta(days=1)
    check_out1 = check_in1 + datetime.timedelta(days=2)
    res_id1 = hotel_reservation_system.book_room(1, "John Doe", check_in1, check_out1)
    check_in2 = datetime.date.today() + datetime.timedelta(days=3)
    check_out2 = check_in2 + datetime.timedelta(days=2)
    res_id2 = hotel_reservation_system.book_room(1, "Jane Doe", check_in2, check_out2)
    assert res_id2 == "RES-0002"

def test_cancel_reservation_between_2_7_days(hotel_reservation_system):
    hotel_reservation_system.add_room(1, "single", 100.0)
    check_in = datetime.date.today() + datetime.timedelta(days=4)
    check_out = check_in + datetime.timedelta(days=2)
    res_id = hotel_reservation_system.book_room(1, "John Doe", check_in, check_out)
    result = hotel_reservation_system.cancel_reservation(res_id)
    # Refund policy: 50% refund if 2-7 days from check-in
    assert result == 100.0 

def test_cancel_reservation_more_than_7_days(hotel_reservation_system):
    hotel_reservation_system.add_room(1, "single", 100.0)
    check_in = datetime.date.today() + datetime.timedelta(days=10)
    check_out = check_in + datetime.timedelta(days=2)
    res_id = hotel_reservation_system.book_room(1, "John Doe", check_in, check_out)
    result = hotel_reservation_system.cancel_reservation(res_id)
    # Refund policy: 100% refund if > 7 days from check-in
    assert result == 200.0