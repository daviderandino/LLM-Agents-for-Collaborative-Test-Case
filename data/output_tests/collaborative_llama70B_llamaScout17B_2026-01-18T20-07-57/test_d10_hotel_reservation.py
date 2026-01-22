import pytest
from data.input_code.d10_hotel_reservation import *
import datetime

@pytest.mark.parametrize("room_number, guest_name, check_in_date, check_out_date, expected", [
    (1, "John Doe", datetime.date.today() + datetime.timedelta(days=2), datetime.date.today() + datetime.timedelta(days=4), "RES-0001"),
    (2, "Jane Doe", datetime.date.today() + datetime.timedelta(days=1), datetime.date.today() + datetime.timedelta(days=3), "RES-0002"),
    (1, "John Doe", datetime.date.today() + datetime.timedelta(days=2), datetime.date.today() + datetime.timedelta(days=4), RoomUnavailableError),
])
def test_book_room(room_number, guest_name, check_in_date, check_out_date, expected):
    hotel_reservation_system = HotelReservationSystem()
    hotel_reservation_system.add_room(1, "Single", 100.0)
    hotel_reservation_system.add_room(2, "Double", 200.0)
    
    if isinstance(expected, str) and expected.startswith("RES-"):
        result = hotel_reservation_system.book_room(room_number, guest_name, check_in_date, check_out_date)
        assert result == expected
    elif expected == RoomUnavailableError:
        with pytest.raises(RoomUnavailableError):
            hotel_reservation_system.book_room(room_number, guest_name, check_in_date, check_out_date)
    else:
        with pytest.raises(expected):
            hotel_reservation_system.book_room(room_number, guest_name, check_in_date, check_out_date)

@pytest.mark.parametrize("reservation_id, expected", [
    (101, ReservationNotFoundError),
    ("RES-0001", {'reservation_id': "RES-0001", 'room_number': 1, 'user_name': 'John Doe', 'check_in': (datetime.date.today() + datetime.timedelta(days=2)), 'check_out': (datetime.date.today() + datetime.timedelta(days=4)), 'total_price': 200.0}),
    ("RES-0002", {'reservation_id': "RES-0002", 'room_number': 2, 'user_name': 'Jane Doe', 'check_in': (datetime.date.today() + datetime.timedelta(days=1)), 'check_out': (datetime.date.today() + datetime.timedelta(days=3)), 'total_price': 400.0}),
])
def test_get_reservation(reservation_id, expected):
    hotel_reservation_system = HotelReservationSystem()
    hotel_reservation_system.add_room(1, "Single", 100.0)
    hotel_reservation_system.add_room(2, "Double", 200.0)
    hotel_reservation_system.book_room(1, "John Doe", datetime.date.today() + datetime.timedelta(days=2), datetime.date.today() + datetime.timedelta(days=4))
    hotel_reservation_system.book_room(2, "Jane Doe", datetime.date.today() + datetime.timedelta(days=1), datetime.date.today() + datetime.timedelta(days=3))
    
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            hotel_reservation_system.get_reservation(reservation_id)
    else:
        result = hotel_reservation_system.get_reservation(reservation_id)
        assert result.reservation_id == expected['reservation_id']
        assert result.room_number == expected['room_number']
        assert result.user_name == expected['user_name']
        assert result.check_in == expected['check_in']
        assert result.check_out == expected['check_out']
        assert result.total_price == expected['total_price']

@pytest.mark.parametrize("reservation_id, new_check_out_date, expected", [
    ("RES-0001", datetime.date.today() + datetime.timedelta(days=5), "RES-0001"),
    ("RES-0002", datetime.date.today() + datetime.timedelta(days=2), "RES-0002"),
    (103, ReservationNotFoundError),
])
def test_update_reservation(reservation_id, new_check_out_date, expected):
    hotel_reservation_system = HotelReservationSystem()
    hotel_reservation_system.add_room(1, "Single", 100.0)
    hotel_reservation_system.add_room(2, "Double", 200.0)
    res1 = hotel_reservation_system.book_room(1, "John Doe", datetime.date.today() + datetime.timedelta(days=2), datetime.date.today() + datetime.timedelta(days=4))
    res2 = hotel_reservation_system.book_room(2, "Jane Doe", datetime.date.today() + datetime.timedelta(days=1), datetime.date.today() + datetime.timedelta(days=3))
    
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            hotel_reservation_system.update_reservation(reservation_id, new_check_out_date)
    else:
        result = hotel_reservation_system.update_reservation(reservation_id, new_check_out_date)
        assert result == expected

@pytest.mark.parametrize("reservation_id, expected", [
    ("RES-0001", None),
    ("RES-0002", None),
    (103, ReservationNotFoundError),
])
def test_cancel_reservation(reservation_id, expected):
    hotel_reservation_system = HotelReservationSystem()
    hotel_reservation_system.add_room(1, "Single", 100.0)
    hotel_reservation_system.add_room(2, "Double", 200.0)
    hotel_reservation_system.book_room(1, "John Doe", datetime.date.today() + datetime.timedelta(days=2), datetime.date.today() + datetime.timedelta(days=4))
    hotel_reservation_system.book_room(2, "Jane Doe", datetime.date.today() + datetime.timedelta(days=1), datetime.date.today() + datetime.timedelta(days=3))
    
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            hotel_reservation_system.cancel_reservation(reservation_id)
    else:
        result = hotel_reservation_system.cancel_reservation(reservation_id)
        assert result == expected