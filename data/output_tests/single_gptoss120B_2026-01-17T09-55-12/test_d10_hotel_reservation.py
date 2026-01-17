import datetime
import pytest
from data.input_code.d10_hotel_reservation import (
    HotelReservationSystem,
    RoomNotFoundError,
    RoomUnavailableError,
    InvalidDateError,
    ReservationNotFoundError,
)


@pytest.fixture(autouse=True)
def fixed_today(monkeypatch):
    """Monkeypatch datetime.date.today to return a fixed date for deterministic tests."""
    fixed = datetime.date(2023, 1, 1)

    class FixedDate(datetime.date):
        @classmethod
        def today(cls):
            return fixed

    monkeypatch.setattr(datetime, "date", FixedDate)
    return fixed


@pytest.fixture
def system():
    return HotelReservationSystem()


def test_add_room_success_and_overwrite(system):
    system.add_room(101, "single", 80.0)
    assert system.rooms[101]["type"] == "single"
    assert system.rooms[101]["price_per_night"] == 80.0

    # Overwrite same room
    system.add_room(101, "double", 120.0)
    assert system.rooms[101]["type"] == "double"
    assert system.rooms[101]["price_per_night"] == 120.0


def test_add_room_invalid_price_raises(system):
    with pytest.raises(ValueError):
        system.add_room(102, "suite", -50.0)


def test_book_room_successful_reservation(system):
    system.add_room(201, "double", 100.0)
    check_in = datetime.date.today() + datetime.timedelta(days=2)
    check_out = check_in + datetime.timedelta(days=3)  # 3 nights
    res_id = system.book_room(201, "Alice", check_in, check_out)

    assert res_id == "RES-0001"
    reservation = system.reservations[res_id]
    assert reservation.room_number == 201
    assert reservation.user_name == "Alice"
    assert reservation.check_in == check_in
    assert reservation.check_out == check_out
    assert reservation.total_price == 300.0  # 3 nights * 100


def test_book_room_nonexistent_room_raises(system):
    check_in = datetime.date.today() + datetime.timedelta(days=2)
    check_out = check_in + datetime.timedelta(days=1)
    with pytest.raises(RoomNotFoundError):
        system.book_room(999, "Bob", check_in, check_out)


def test_book_room_invalid_dates_raises(system):
    system.add_room(301, "single", 50.0)
    today = datetime.date.today()
    # check_in >= check_out
    with pytest.raises(InvalidDateError):
        system.book_room(301, "Carol", today + datetime.timedelta(days=5), today + datetime.timedelta(days=5))
    # check_in in the past
    with pytest.raises(InvalidDateError):
        system.book_room(301, "Carol", today - datetime.timedelta(days=1), today + datetime.timedelta(days=1))


def test_book_room_unavailable_raises(system):
    system.add_room(401, "suite", 200.0)
    check_in = datetime.date.today() + datetime.timedelta(days=10)
    check_out = check_in + datetime.timedelta(days=5)
    # First reservation succeeds
    system.book_room(401, "Dave", check_in, check_out)

    # Overlapping reservation should fail
    overlapping_check_in = check_in + datetime.timedelta(days=2)
    overlapping_check_out = overlapping_check_in + datetime.timedelta(days=3)
    with pytest.raises(RoomUnavailableError):
        system.book_room(401, "Eve", overlapping_check_in, overlapping_check_out)


def test_cancel_reservation_refund_policies(system):
    system.add_room(501, "deluxe", 150.0)
    today = datetime.date.today()

    # >7 days until check-in: full refund
    check_in_far = today + datetime.timedelta(days=10)
    check_out_far = check_in_far + datetime.timedelta(days=2)
    res_id_far = system.book_room(501, "Frank", check_in_far, check_out_far)
    refund_far = system.cancel_reservation(res_id_far)
    assert refund_far == 300.0  # 2 nights * 150

    # 2-7 days until check-in: 50% refund
    check_in_mid = today + datetime.timedelta(days=5)
    check_out_mid = check_in_mid + datetime.timedelta(days=4)
    res_id_mid = system.book_room(501, "Grace", check_in_mid, check_out_mid)
    refund_mid = system.cancel_reservation(res_id_mid)
    assert refund_mid == round(4 * 150.0 * 0.5, 2)

    # <2 days until check-in: no refund
    check_in_near = today + datetime.timedelta(days=1)
    check_out_near = check_in_near + datetime.timedelta(days=3)
    res_id_near = system.book_room(501, "Heidi", check_in_near, check_out_near)
    refund_near = system.cancel_reservation(res_id_near)
    assert refund_near == 0.0


def test_cancel_reservation_not_found_raises(system):
    with pytest.raises(ReservationNotFoundError):
        system.cancel_reservation("NON-EXISTENT")


def test_get_room_occupancy(system):
    system.add_room(601, "standard", 80.0)
    system.add_room(602, "standard", 80.0)
    today = datetime.date.today()
    # Reservation for room 601 from day 3 to day 6
    check_in = today + datetime.timedelta(days=3)
    check_out = check_in + datetime.timedelta(days=3)
    system.book_room(601, "Ivan", check_in, check_out)

    # Reservation for room 602 from day 5 to day 8
    check_in2 = today + datetime.timedelta(days=5)
    check_out2 = check_in2 + datetime.timedelta(days=3)
    system.book_room(602, "Judy", check_in2, check_out2)

    # Date within first reservation only
    occupied_day4 = system.get_room_occupancy(today + datetime.timedelta(days=4))
    assert occupied_day4 == [601]

    # Date overlapping both reservations
    occupied_day5 = system.get_room_occupancy(today + datetime.timedelta(days=5))
    assert occupied_day5 == [601, 602]

    # Date after all reservations
    occupied_day9 = system.get_room_occupancy(today + datetime.timedelta(days=9))
    assert occupied_day9 == []