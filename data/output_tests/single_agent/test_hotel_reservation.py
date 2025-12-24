import datetime
import pytest
from data.input_code.hotel_reservation import (
    HotelReservationSystem,
    RoomNotFoundError,
    RoomUnavailableError,
    InvalidDateError,
    ReservationNotFoundError,
    Reservation,
)

@pytest.fixture
def system():
    return HotelReservationSystem()

def test_add_room_success(system):
    system.add_room(101, "Deluxe", 150.0)
    assert 101 in system.rooms
    assert system.rooms[101]["type"] == "Deluxe"
    assert system.rooms[101]["price_per_night"] == 150.0

def test_add_room_invalid_price(system):
    with pytest.raises(ValueError):
        system.add_room(102, "Standard", 0)
    with pytest.raises(ValueError):
        system.add_room(103, "Standard", -50)

def test_book_room_success(system):
    system.add_room(201, "Suite", 200.0)
    today = datetime.date.today()
    check_in = today + datetime.timedelta(days=1)
    check_out = check_in + datetime.timedelta(days=3)
    res_id = system.book_room(201, "Alice", check_in, check_out)
    assert res_id.startswith("RES-")
    assert res_id in system.reservations
    res = system.reservations[res_id]
    assert res.room_number == 201
    assert res.user_name == "Alice"
    assert res.check_in == check_in
    assert res.check_out == check_out
    assert res.total_price == round(3 * 200.0, 2)

def test_book_room_room_not_found(system):
    today = datetime.date.today()
    check_in = today + datetime.timedelta(days=1)
    check_out = check_in + datetime.timedelta(days=2)
    with pytest.raises(RoomNotFoundError):
        system.book_room(999, "Bob", check_in, check_out)

def test_book_room_invalid_dates(system):
    system.add_room(301, "Standard", 100.0)
    today = datetime.date.today()
    check_in = today + datetime.timedelta(days=5)
    check_out = check_in - datetime.timedelta(days=1)  # checkout before checkin
    with pytest.raises(InvalidDateError):
        system.book_room(301, "Carol", check_in, check_out)

def test_book_room_past_date(system):
    system.add_room(302, "Standard", 100.0)
    past = datetime.date.today() - datetime.timedelta(days=1)
    future = datetime.date.today() + datetime.timedelta(days=2)
    with pytest.raises(InvalidDateError):
        system.book_room(302, "Dave", past, future)

def test_book_room_overlapping(system):
    system.add_room(401, "Deluxe", 120.0)
    today = datetime.date.today()
    check_in1 = today + datetime.timedelta(days=2)
    check_out1 = check_in1 + datetime.timedelta(days=3)
    system.book_room(401, "Eve", check_in1, check_out1)

    # Overlap: starts before previous ends
    check_in2 = check_in1 + datetime.timedelta(days=1)
    check_out2 = check_in2 + datetime.timedelta(days=2)
    with pytest.raises(RoomUnavailableError):
        system.book_room(401, "Frank", check_in2, check_out2)

    # Non-overlap: after previous ends
    check_in3 = check_out1
    check_out3 = check_in3 + datetime.timedelta(days=2)
    res_id = system.book_room(401, "Grace", check_in3, check_out3)
    assert res_id in system.reservations

def test_cancel_reservation_not_found(system):
    with pytest.raises(ReservationNotFoundError):
        system.cancel_reservation("NON-EXISTENT")

def test_cancel_reservation_refund(monkeypatch):
    system = HotelReservationSystem()
    system.add_room(501, "Suite", 250.0)
    today = datetime.date(2025, 1, 1)
    monkeypatch.setattr(datetime, "date", lambda *args, **kwargs: today)

    # Helper to create reservation
    def book(days_from_today, nights):
        check_in = today + datetime.timedelta(days=days_from_today)
        check_out = check_in + datetime.timedelta(days=nights)
        return system.book_room(501, "Hank", check_in, check_out)

    # >7 days before check-in: full refund
    res1 = book(10, 2)
    refund1 = system.cancel_reservation(res1)
    assert refund1 == round(2 * 250.0, 2)

    # 5 days before check-in: 50% refund
    res2 = book(5, 3)
    refund2 = system.cancel_reservation(res2)
    assert refund2 == round(3 * 250.0 * 0.5, 2)

    # 1 day before check-in: no refund
    res3 = book(1, 1)
    refund3 = system.cancel_reservation(res3)
    assert refund3 == 0.0

def test_get_room_occupancy(system):
    system.add_room(601, "Standard", 80.0)
    system.add_room(602, "Standard", 80.0)
    today = datetime.date.today()
    # Booking 601 for 2 days
    system.book_room(601, "Ivy", today, today + datetime.timedelta(days=2))
    # Booking 602 for 1 day
    system.book_room(602, "Jack", today + datetime.timedelta(days=1), today + datetime.timedelta(days=2))

    # Occupancy on today: only 601
    occ_today = system.get_room_occupancy(today)
    assert occ_today == [601]

    # Occupancy on tomorrow: both 601 and 602
    occ_tomorrow = system.get_room_occupancy(today + datetime.timedelta(days=1))
    assert occ_tomorrow == [601, 602]

    # Occupancy after check-out: none
    occ_after = system.get_room_occupancy(today + datetime.timedelta(days=2))
    assert occ_after == []

def test_reservation_id_uniqueness(system):
    system.add_room(701, "Deluxe", 180.0)
    today = datetime.date.today()
    check_in = today + datetime.timedelta(days=3)
    check_out = check_in + datetime.timedelta(days=2)
    ids = set()
    for _ in range(5):
        res_id = system.book_room(701, "User", check_in, check_out)
        assert res_id not in ids
        ids.add(res_id)
    assert len(ids) == 5

def test_price_calculation_rounding(system):
    system.add_room(801, "Suite", 99.99)
    today = datetime.date.today()
    check_in = today + datetime.timedelta(days=1)
    check_out = check_in + datetime.timedelta(days=3)  # 3 nights
    res_id = system.book_room(801, "Kate", check_in, check_out)
    res = system.reservations[res_id]
    expected = round(3 * 99.99, 2)
    assert res.total_price == expected
    assert res.total_price == pytest.approx(expected, rel=1e-9)