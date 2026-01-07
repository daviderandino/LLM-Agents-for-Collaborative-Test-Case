import datetime
from data.input_code.hotel_reservation import HotelReservationSystem, RoomNotFoundError, RoomUnavailableError, InvalidDateError, ReservationNotFoundError

def test_add_room_valid():
    hotel = HotelReservationSystem()
    hotel.add_room(101, 'Single', 100.0)
    assert hotel.rooms[101]['type'] == 'Single'
    assert hotel.rooms[101]['price_per_night'] == 100.0

def test_add_room_invalid_price():
    hotel = HotelReservationSystem()
    with pytest.raises(ValueError):
        hotel.add_room(101, 'Single', -100.0)

def test_book_room_valid():
    hotel = HotelReservationSystem()
    hotel.add_room(101, 'Single', 100.0)
    check_in = datetime.date.today() + datetime.timedelta(days=1)
    check_out = check_in + datetime.timedelta(days=2)
    res_id = hotel.book_room(101, 'John Doe', check_in, check_out)
    assert res_id.startswith('RES-')
    assert len(res_id) == 8

def test_book_room_non_existent():
    hotel = HotelReservationSystem()
    check_in = datetime.date.today() + datetime.timedelta(days=1)
    check_out = check_in + datetime.timedelta(days=2)
    with pytest.raises(RoomNotFoundError):
        hotel.book_room(101, 'John Doe', check_in, check_out)

def test_book_room_invalid_dates():
    hotel = HotelReservationSystem()
    hotel.add_room(101, 'Single', 100.0)
    check_in = datetime.date.today() + datetime.timedelta(days=2)
    check_out = check_in
    with pytest.raises(InvalidDateError):
        hotel.book_room(101, 'John Doe', check_in, check_out)

def test_book_room_past_date():
    hotel = HotelReservationSystem()
    hotel.add_room(101, 'Single', 100.0)
    check_in = datetime.date.today() - datetime.timedelta(days=1)
    check_out = check_in + datetime.timedelta(days=2)
    with pytest.raises(InvalidDateError):
        hotel.book_room(101, 'John Doe', check_in, check_out)

def test_book_room_unavailable():
    hotel = HotelReservationSystem()
    hotel.add_room(101, 'Single', 100.0)
    check_in = datetime.date.today() + datetime.timedelta(days=1)
    check_out = check_in + datetime.timedelta(days=2)
    hotel.book_room(101, 'John Doe', check_in, check_out)
    with pytest.raises(RoomUnavailableError):
        hotel.book_room(101, 'Jane Doe', check_in, check_out)

def test_cancel_reservation_valid():
    hotel = HotelReservationSystem()
    hotel.add_room(101, 'Single', 100.0)
    check_in = datetime.date.today() + datetime.timedelta(days=10)
    check_out = check_in + datetime.timedelta(days=2)
    res_id = hotel.book_room(101, 'John Doe', check_in, check_out)
    refund = hotel.cancel_reservation(res_id)
    assert refund == hotel.reservations[res_id].total_price

def test_cancel_reservation_non_existent():
    hotel = HotelReservationSystem()
    with pytest.raises(ReservationNotFoundError):
        hotel.cancel_reservation('RES-0001')

def test_cancel_reservation_refund_policy():
    hotel = HotelReservationSystem()
    hotel.add_room(101, 'Single', 100.0)
    
    # More than 7 days
    check_in = datetime.date.today() + datetime.timedelta(days=10)
    check_out = check_in + datetime.timedelta(days=2)
    res_id1 = hotel.book_room(101, 'John Doe', check_in, check_out)
    refund1 = hotel.cancel_reservation(res_id1)
    assert refund1 == hotel.reservations[res_id1].total_price
    
    # Between 2 and 7 days
    check_in = datetime.date.today() + datetime.timedelta(days=5)
    check_out = check_in + datetime.timedelta(days=2)
    res_id2 = hotel.book_room(101, 'Jane Doe', check_in, check_out)
    refund2 = hotel.cancel_reservation(res_id2)
    assert refund2 == round(hotel.reservations[res_id2].total_price * 0.5, 2)
    
    # Less than 2 days
    check_in = datetime.date.today() + datetime.timedelta(days=1)
    check_out = check_in + datetime.timedelta(days=2)
    res_id3 = hotel.book_room(101, 'Bob Smith', check_in, check_out)
    refund3 = hotel.cancel_reservation(res_id3)
    assert refund3 == 0.0

def test_get_room_occupancy():
    hotel = HotelReservationSystem()
    hotel.add_room(101, 'Single', 100.0)
    hotel.add_room(102, 'Double', 200.0)
    check_in = datetime.date.today() + datetime.timedelta(days=1)
    check_out = check_in + datetime.timedelta(days=2)
    hotel.book_room(101, 'John Doe', check_in, check_out)
    occupied_rooms = hotel.get_room_occupancy(check_in + datetime.timedelta(days=1))
    assert occupied_rooms == [101]