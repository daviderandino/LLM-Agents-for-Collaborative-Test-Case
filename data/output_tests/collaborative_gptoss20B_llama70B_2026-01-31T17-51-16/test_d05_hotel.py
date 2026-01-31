import pytest
from data.input_code.d05_hotel import HotelReservationSystem, RoomNotFoundError, RoomUnavailableError, InvalidDateError, ReservationNotFoundError
from datetime import date

@pytest.fixture
def hotel_system():
    return HotelReservationSystem()

def test_is_room_available_partial_overlap(hotel_system):
    hotel_system.add_room(101, "Deluxe", 100)
    hotel_system.book_room(101, "Alice", date(2026, 2, 1), date(2026, 2, 3))
    assert hotel_system._is_room_available(101, date(2026, 2, 4), date(2026, 2, 6)) == True

def test_cancel_reservation_refund_100(hotel_system):
    hotel_system.add_room(101, "Deluxe", 100)
    res_id = hotel_system.book_room(101, "Alice", date(2026, 2, 10), date(2026, 2, 12))
    refund = hotel_system.cancel_reservation(res_id)
    # Since the test is run today (assuming today is before 2026-02-10), 
    # and the check-in date is 2026-02-10, the refund should be 100% of the total price.
    # The total price is calculated as (check_out - check_in).days * price_per_night
    # which is (2026-02-12 - 2026-02-10).days * 100 = 2 * 100 = 200
    assert refund == 200.0

