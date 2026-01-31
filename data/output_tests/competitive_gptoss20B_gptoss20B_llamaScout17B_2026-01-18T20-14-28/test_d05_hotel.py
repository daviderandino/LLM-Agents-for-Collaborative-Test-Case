import pytest
import datetime
from data.input_code.d05_hotel import *

@pytest.fixture
def system(monkeypatch):
    # Freeze today's date to 2026-01-18 for deterministic tests
    class FixedDate(datetime.date):
        @classmethod
        def today(cls):
            return cls(2026, 1, 18)
    monkeypatch.setattr(datetime, 'date', FixedDate)
    return HotelReservationSystem()

# ---------- add_room ----------
@pytest.mark.parametrize(
    "room_number,room_type,price",
    [(101, "single", 100.0)]
)
def test_add_room_success(system, room_number, room_type, price):
    system.add_room(room_number, room_type, price)
    assert system.rooms[room_number]["price_per_night"] == price

@pytest.mark.parametrize(
    "room_number,room_type,price",
    [(102, "double", 0)]
)
def test_add_room_invalid_price(system, room_number, room_type, price):
    with pytest.raises(ValueError):
        system.add_room(room_number, room_type, price)

# ---------- _is_room_available ----------
@pytest.mark.parametrize(
    "room_number,check_in,check_out,expected",
    [(101, datetime.date(2026, 1, 19), datetime.date(2026, 1, 20), True)]
)
def test_is_room_available_no_reservations(system, room_number, check_in, check_out, expected):
    system.add_room(room_number, "single", 100.0)
    assert system._is_room_available(room_number, check_in, check_out) == expected

@pytest.mark.parametrize(
    "room_number,check_in,check_out,expected",
    [(101, datetime.date(2026, 1, 19), datetime.date(2026, 1, 21), False)]
)
def test_is_room_available_overlap(system, room_number, check_in, check_out, expected):
    system.add_room(room_number, "single", 100.0)
    # Existing reservation that overlaps
    system.book_room(room_number, "user", datetime.date(2026, 1, 20), datetime.date(2026, 1, 22))
    assert system._is_room_available(room_number, check_in, check_out) == expected

@pytest.mark.parametrize(
    "room_number,check_in,check_out,expected",
    [(101, datetime.date(2026, 1, 23), datetime.date(2026, 1, 24), True)]
)
def test_is_room_available_non_overlap(system, room_number, check_in, check_out, expected):
    system.add_room(room_number, "single", 100.0)
    system.book_room(room_number, "user", datetime.date(2026, 1, 20), datetime.date(2026, 1, 22))
    assert system._is_room_available(room_number, check_in, check_out) == expected

# ---------- book_room ----------
@pytest.mark.parametrize(
    "room_number,user_name,check_in,check_out",
    [(999, "Alice", datetime.date(2026, 1, 19), datetime.date(2026, 1, 20))]
)
def test_book_room_room_not_found(system, room_number, user_name, check_in, check_out):
    with pytest.raises(RoomNotFoundError):
        system.book_room(room_number, user_name, check_in, check_out)

@pytest.mark.parametrize(
    "room_number,user_name,check_in,check_out",
    [(101, "Bob", datetime.date(2026, 1, 20), datetime.date(2026, 1, 20))]
)
def test_book_room_invalid_dates_checkin_ge_checkout(system, room_number, user_name, check_in, check_out):
    system.add_room(room_number, "single", 100.0)
    with pytest.raises(InvalidDateError):
        system.book_room(room_number, user_name, check_in, check_out)

@pytest.mark.parametrize(
    "room_number,user_name,check_in,check_out",
    [(101, "Carol", datetime.date(2026, 1, 17), datetime.date(2026, 1, 20))]
)
def test_book_room_invalid_dates_past(system, room_number, user_name, check_in, check_out):
    system.add_room(room_number, "single", 100.0)
    with pytest.raises(InvalidDateError):
        system.book_room(room_number, user_name, check_in, check_out)

@pytest.mark.parametrize(
    "room_number,user_name,check_in,check_out",
    [(101, "Dave", datetime.date(2026, 1, 20), datetime.date(2026, 1, 22))]
)
def test_book_room_unavailable(system, room_number, user_name, check_in, check_out):
    system.add_room(room_number, "single", 100.0)
    system.book_room(room_number, "existing", datetime.date(2026, 1, 20), datetime.date(2026, 1, 22))
    with pytest.raises(RoomUnavailableError):
        system.book_room(room_number, user_name, check_in, check_out)

@pytest.mark.parametrize(
    "room_number,user_name,check_in,check_out,expected_id",
    [(101, "Eve", datetime.date(2026, 1, 23), datetime.date(2026, 1, 25), "RES-0001")]
)
def test_book_room_success(system, room_number, user_name, check_in, check_out, expected_id):
    system.add_room(room_number, "single", 100.0)
    res_id = system.book_room(room_number, user_name, check_in, check_out)
    assert res_id == expected_id

# ---------- cancel_reservation ----------
@pytest.mark.parametrize(
    "reservation_id",
    ["RES-9999"]
)
def test_cancel_reservation_not_found(system, reservation_id):
    with pytest.raises(ReservationNotFoundError):
        system.cancel_reservation(reservation_id)

@pytest.mark.parametrize(
    "room_number,user_name,check_in,check_out,expected_refund",
    [(101, "User", datetime.date(2026, 1, 26), datetime.date(2026, 1, 28), 200.0)]
)
def test_cancel_reservation_full_refund(system, room_number, user_name, check_in, check_out, expected_refund):
    system.add_room(room_number, "single", 100.0)
    res_id = system.book_room(room_number, user_name, check_in, check_out)
    assert res_id == "RES-0001"
    refund = system.cancel_reservation(res_id)
    assert refund == expected_refund

@pytest.mark.parametrize(
    "room_number,user_name,check_in,check_out,expected_refund",
    [(101, "User", datetime.date(2026, 1, 23), datetime.date(2026, 1, 25), 100.0)]
)
def test_cancel_reservation_half_refund(system, room_number, user_name, check_in, check_out, expected_refund):
    system.add_room(room_number, "single", 100.0)
    res_id = system.book_room(room_number, user_name, check_in, check_out)
    assert res_id == "RES-0001"
    refund = system.cancel_reservation(res_id)
    assert refund == expected_refund

@pytest.mark.parametrize(
    "room_number,user_name,check_in,check_out,expected_refund",
    [(101, "User", datetime.date(2026, 1, 19), datetime.date(2026, 1, 20), 0.0)]
)
def test_cancel_reservation_no_refund(system, room_number, user_name, check_in, check_out, expected_refund):
    system.add_room(room_number, "single", 100.0)
    res_id = system.book_room(room_number, user_name, check_in, check_out)
    assert res_id == "RES-0001"
    refund = system.cancel_reservation(res_id)
    assert refund == expected_refund

# ---------- get_room_occupancy ----------
@pytest.mark.parametrize(
    "date,expected",
    [(datetime.date(2026, 1, 19), [])]
)
def test_get_room_occupancy_no_reservations(system, date, expected):
    assert system.get_room_occupancy(date) == expected

@pytest.mark.parametrize(
    "date,expected",
    [(datetime.date(2026, 1, 20), [101])]
)
def test_get_room_occupancy_single(system, date, expected):
    system.add_room(101, "single", 100.0)
    system.book_room(101, "user", datetime.date(2026, 1, 20), datetime.date(2026, 1, 22))
    assert system.get_room_occupancy(date) == expected

@pytest.mark.parametrize(
    "date,expected",
    [(datetime.date(2026, 1, 20), [101, 102])]
)
def test_get_room_occupancy_multiple(system, date, expected):
    system.add_room(101, "single", 100.0)
    system.add_room(102, "double", 150.0)
    system.book_room(101, "user1", datetime.date(2026, 1, 20), datetime.date(2026, 1, 22))
    system.book_room(102, "user2", datetime.date(2026, 1, 20), datetime.date(2026, 1, 22))
    assert system.get_room_occupancy(date) == expected