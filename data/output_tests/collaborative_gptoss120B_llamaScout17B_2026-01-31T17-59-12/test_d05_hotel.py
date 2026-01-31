import pytest
from data.input_code.d05_hotel import *
from datetime import date, timedelta

@pytest.mark.parametrize("days_until_checkin, expected_percent, expected_price", [
    (10, 100, 800.0),  # 10 days before check-in, 100% refund
    (5, 50, 400.0),   # 5 days before check-in, 50% 
    (1, 0, 0.0),     # 1 day before check-in, 0% 
])
def test_cancel_reservation(days_until_checkin, expected_percent, expected_price):
    hrs = HotelReservationSystem()  
    hrs.add_room(101, "Deluxe", 400.0)  
    today = date.today()
    check_in = today + timedelta(days=days_until_checkin)
    check_out = check_in + timedelta(days=2)
    reservation_id = hrs.book_room(101, "Grace", check_in, check_out)
    refund = hrs.cancel_reservation(reservation_id)
    assert refund == expected_price

# For nicer output on failed assertions 
def test_get_room_occupancy_today():
    hrs = HotelReservationSystem()
    hrs.add_room(101, "Deluxe", 400)
    today = date.today()
    res_id = hrs.book_room(101, "John", today + timedelta(days=2), today + timedelta(days=5))
    assert sorted(hrs.get_room_occupancy(today + timedelta(days=3))) == [101]

def test_book_room():
    hrs = HotelReservationSystem()
    hrs.add_room(101, "Deluxe", 400)
    today = date.today()
    res_id = hrs.book_room(101, "John", today + timedelta(days=2), today + timedelta(days=5))
    assert res_id is not None


def test_get_room_occupancy_future_date():
    hrs = HotelReservationSystem()
    hrs.add_room(101, "Deluxe", 400)
    today = date.today()
    res_id = hrs.book_room(101, "John", today + timedelta(days=2), today + timedelta(days=5))
    assert sorted(hrs.get_room_occupancy(today + timedelta(days=6))) == []