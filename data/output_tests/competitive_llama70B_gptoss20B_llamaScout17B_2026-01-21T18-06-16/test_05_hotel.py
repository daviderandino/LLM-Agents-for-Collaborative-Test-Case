import pytest
import datetime
from data.input_code.05_hotel import *

# Helper function to create a date object from string
def date_from_str(date_str):
    return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()

# Test data
# Use future dates relative to the current date (2026-01-21) to avoid InvalidDateError
future_start = date_from_str("2027-01-01")
future_end = date_from_str("2027-01-02")
future_start2 = date_from_str("2027-01-02")
future_start3 = date_from_str("2027-01-03")

test_data_add_room = [
    (1, "single", 100.0, None),
    (2, "double", 200.0, None),
]

test_data_add_room_error = [
    (3, "single", -100.0, ValueError),
]

test_data_book_room = [
    (1, "John Doe", future_start, future_end, "RES-0001"),
]

test_data_book_room_error_room_not_found = [
    (2, "John Doe", future_start, future_end, RoomNotFoundError),
]

test_data_book_room_error_invalid_dates = [
    (1, "John Doe", future_end, future_start, InvalidDateError),
]

test_data_book_room_error_room_unavailable = [
    (1, "Jane Doe", future_start, future_end, RoomUnavailableError),
]

test_data_cancel_reservation = [
    ("RES-0001", 100.0),
]

test_data_cancel_reservation_error = [
    ("RES-0002", ReservationNotFoundError),
]

test_data_get_room_occupancy = [
    (future_start, [1]),
    (future_start3, []),
]

# New test data
current_date = datetime.date.today()
future_start = date_from_str("2027-01-01")
future_end = date_from_str("2027-01-02")

test_data_book_room_past_checkin = [
    (1, "John Doe", current_date - datetime.timedelta(days=1), future_end, InvalidDateError),
]

test_data_cancel_reservation_refund_50 = [
    ("RES-0001", 350.0),  # 50% of 700.0 (7 nights at $100)
]

test_data_cancel_reservation_refund_0 = [
    ("RES-0001", 0.0),
]

test_data_get_room_occupancy_multiple_rooms = [
    (future_start, [1, 2]),
]

test_data_book_room_edge_case_checkin_checkout_same_day = [
    (1, "John Doe", future_start, future_start, InvalidDateError),
]

# Test functions
@pytest.mark.parametrize("room_number, room_type, price_per_night, expected", test_data_add_room)
def test_add_room(room_number, room_type, price_per_night, expected):
    hotel = HotelReservationSystem()
    hotel.add_room(room_number, room_type, price_per_night)
    assert hotel.rooms.get(room_number) is not None

@pytest.mark.parametrize("room_number, room_type, price_per_night, expected", test_data_add_room_error)
def test_add_room_error(room_number, room_type, price_per_night, expected):
    hotel = HotelReservationSystem()
    with pytest.raises(expected):
        hotel.add_room(room_number, room_type, price_per_night)

@pytest.mark.parametrize("room_number, user_name, check_in, check_out, expected", test_data_book_room)
def test_book_room(room_number, user_name, check_in, check_out, expected):
    hotel = HotelReservationSystem()
    hotel.add_room(room_number, "single", 100.0)
    assert hotel.book_room(room_number, user_name, check_in, check_out) == expected

@pytest.mark.parametrize("room_number, user_name, check_in, check_out, expected", test_data_book_room_error_room_not_found)
def test_book_room_error_room_not_found(room_number, user_name, check_in, check_out, expected):
    hotel = HotelReservationSystem()
    with pytest.raises(expected):
        hotel.book_room(room_number, user_name, check_in, check_out)

@pytest.mark.parametrize("room_number, user_name, check_in, check_out, expected", test_data_book_room_error_invalid_dates)
def test_book_room_error_invalid_dates(room_number, user_name, check_in, check_out, expected):
    hotel = HotelReservationSystem()
    hotel.add_room(room_number, "single", 100.0)
    with pytest.raises(expected):
        hotel.book_room(room_number, user_name, check_in, check_out)

def test_book_room_error_room_unavailable():
    hotel = HotelReservationSystem()
    hotel.add_room(1, "single", 100.0)
    hotel.book_room(1, "John Doe", future_start, future_end)
    with pytest.raises(RoomUnavailableError):
        hotel.book_room(1, "Jane Doe", future_start, future_end)

@pytest.mark.parametrize("reservation_id, expected", test_data_cancel_reservation)
def test_cancel_reservation(reservation_id, expected):
    hotel = HotelReservationSystem()
    hotel.add_room(1, "single", 100.0)
    res_id = hotel.book_room(1, "John Doe", future_start, future_end)
    assert hotel.cancel_reservation(res_id) == expected

@pytest.mark.parametrize("reservation_id, expected", test_data_cancel_reservation_error)
def test_cancel_reservation_error(reservation_id, expected):
    hotel = HotelReservationSystem()
    with pytest.raises(expected):
        hotel.cancel_reservation(reservation_id)

@pytest.mark.parametrize("date, expected", test_data_get_room_occupancy)
def test_get_room_occupancy(date, expected):
    hotel = HotelReservationSystem()
    hotel.add_room(1, "single", 100.0)
    hotel.book_room(1, "John Doe", future_start, future_end)
    assert hotel.get_room_occupancy(date) == expected

def test_book_room_past_checkin():
    hotel = HotelReservationSystem()
    hotel.add_room(1, "single", 100.0)
    with pytest.raises(InvalidDateError):
        hotel.book_room(1, "John Doe", current_date - datetime.timedelta(days=1), current_date)

def test_cancel_reservation_refund_50():
    hotel = HotelReservationSystem()
    hotel.add_room(1, "single", 100.0)
    res_id = hotel.book_room(1, "John Doe", current_date + datetime.timedelta(days=7), current_date + datetime.timedelta(days=14))
    assert hotel.cancel_reservation(res_id) == 350.0

def test_cancel_reservation_refund_0():
    hotel = HotelReservationSystem()
    hotel.add_room(1, "single", 100.0)
    res_id = hotel.book_room(1, "John Doe", current_date + datetime.timedelta(days=1), current_date + datetime.timedelta(days=2))
    assert hotel.cancel_reservation(res_id) == 0.0

@pytest.mark.parametrize("date, expected", test_data_get_room_occupancy_multiple_rooms)
def test_get_room_occupancy_multiple_rooms(date, expected):
    hotel = HotelReservationSystem()
    hotel.add_room(1, "single", 100.0)
    hotel.add_room(2, "double", 200.0)
    hotel.book_room(1, "John Doe", future_start, future_end)
    hotel.book_room(2, "Jane Doe", future_start, future_end)
    assert hotel.get_room_occupancy(date) == expected

@pytest.mark.parametrize("room_number, user_name, check_in, check_out, expected", test_data_book_room_edge_case_checkin_checkout_same_day)
def test_book_room_edge_case_checkin_checkout_same_day(room_number, user_name, check_in, check_out, expected):
    hotel = HotelReservationSystem()
    hotel.add_room(room_number, "single", 100.0)
    with pytest.raises(expected):
        hotel.book_room(room_number, user_name, check_in, check_out)