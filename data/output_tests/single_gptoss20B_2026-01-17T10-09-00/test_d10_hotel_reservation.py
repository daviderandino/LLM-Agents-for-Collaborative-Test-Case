import datetime
import pytest

from data.input_code.d10_hotel_reservation import (
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


def test_add_room_and_overwrite(system):
    system.add_room(101, "single", 100.0)
    assert system.rooms[101]["type"] == "single"
    assert system.rooms[101]["price_per_night"] == 100.0

    # Overwrite existing room
    system.add_room(101, "double", 150.0)
    assert system.rooms[101]["type"] == "double"
    assert system.rooms[101]["price_per_night"] == 150.0


def test_add_room_invalid_price(system):
    with pytest.raises(ValueError):
        system.add_room(102, "single", 0.0)
    with pytest.raises(ValueError):
        system.add_room(103, "single", -10.0)


def test_is_room_available_overlap(system, monkeypatch):
    # Freeze today's date
    fixed_today = datetime.date(2023, 1, 1)
    monkeypatch.setattr(
        "data.input_code.d10_hotel_reservation.datetime.date",
        type(
            "FakeDate",
            (datetime.date,),
            {"today": staticmethod(lambda: fixed_today)},
        ),
    )

    # Add a room and book it
    system.add_room(101, "single", 100.0)
    res_id = system.book_room(
        101, "Alice", datetime.date(2023, 1, 10), datetime.date(2023, 1, 15)
    )
    assert res_id in system.reservations

    # Non-overlapping before
    assert system._is_room_available(101, datetime.date(2023, 1, 5), datetime.date(2023, 1, 10))
    # Non-overlapping after
    assert system._is_room_available(101, datetime.date(2023, 1, 15), datetime.date(2023, 1, 20))
    # Overlapping start
    assert not system._is_room_available(101, datetime.date(2023, 1, 8), datetime.date(2023, 1, 12))
    # Overlapping end
    assert not system._is_room_available(101, datetime.date(2023, 1, 12), datetime.date(2023, 1, 18))
    # Fully inside
    assert not system._is_room_available(101, datetime.date(2023, 1, 11), datetime.date(2023, 1, 13))
    # Fully contains
    assert not system._is_room_available(101, datetime.date(2023, 1, 9), datetime.date(2023, 1, 16))
    # Edge case: check_in == existing check_out
    assert system._is_room_available(101, datetime.date(2023, 1, 15), datetime.date(2023, 1, 18))
    # Edge case: check_out == existing check_in
    assert system._is_room_available(101, datetime.date(2023, 1, 5), datetime.date(2023, 1, 10))


def test_book_room_success(system, monkeypatch):
    fixed_today = datetime.date(2023, 1, 1)
    monkeypatch.setattr(
        "data.input_code.d10_hotel_reservation.datetime.date",
        type(
            "FakeDate",
            (datetime.date,),
            {"today": staticmethod(lambda: fixed_today)},
        ),
    )

    system.add_room(101, "single", 100.0)
    res_id = system.book_room(
        101, "Bob", datetime.date(2023, 1, 10), datetime.date(2023, 1, 12)
    )
    assert res_id == "RES-0001"
    reservation = system.reservations[res_id]
    assert reservation.room_number == 101
    assert reservation.user_name == "Bob"
    assert reservation.check_in == datetime.date(2023, 1, 10)
    assert reservation.check_out == datetime.date(2023, 1, 12)
    assert reservation.total_price == 200.0  # 2 nights * 100


def test_book_room_errors(system, monkeypatch):
    fixed_today = datetime.date(2023, 1, 1)
    monkeypatch.setattr(
        "data.input_code.d10_hotel_reservation.datetime.date",
        type(
            "FakeDate",
            (datetime.date,),
            {"today": staticmethod(lambda: fixed_today)},
        ),
    )

    system.add_room(101, "single", 100.0)

    # Room not found
    with pytest.raises(RoomNotFoundError):
        system.book_room(999, "Charlie", datetime.date(2023, 1, 10), datetime.date(2023, 1, 12))

    # Invalid date: check_in >= check_out
    with pytest.raises(InvalidDateError):
        system.book_room(101, "Charlie", datetime.date(2023, 1, 12), datetime.date(2023, 1, 12))

    # Past date
    with pytest.raises(InvalidDateError):
        system.book_room(101, "Charlie", datetime.date(2022, 12, 31), datetime.date(2023, 1, 2))

    # Room unavailable
    system.book_room(101, "Alice", datetime.date(2023, 1, 10), datetime.date(2023, 1, 15))
    with pytest.raises(RoomUnavailableError):
        system.book_room(101, "Bob", datetime.date(2023, 1, 12), datetime.date(2023, 1, 18))


def test_cancel_reservation_refund(system, monkeypatch):
    # Set a fixed today date
    fixed_today = datetime.date(2023, 1, 1)
    monkeypatch.setattr(
        "data.input_code.d10_hotel_reservation.datetime.date",
        type(
            "FakeDate",
            (datetime.date,),
            {"today": staticmethod(lambda: fixed_today)},
        ),
    )

    system.add_room(101, "single", 100.0)

    # Reservation 10 days from today -> full refund
    res_id_full = system.book_room(
        101, "Alice", datetime.date(2023, 1, 11), datetime.date(2023, 1, 13)
    )
    refund_full = system.cancel_reservation(res_id_full)
    assert refund_full == 200.0

    # Reservation 5 days from today -> 50% refund
    res_id_half = system.book_room(
        101, "Bob", datetime.date(2023, 1, 6), datetime.date(2023, 1, 8)
    )
    refund_half = system.cancel_reservation(res_id_half)
    assert refund_half == 100.0  # 200 * 0.5

    # Reservation 1 day from today -> no refund
    res_id_none = system.book_room(
        101, "Charlie", datetime.date(2023, 1, 2), datetime.date(2023, 1, 3)
    )
    refund_none = system.cancel_reservation(res_id_none)
    assert refund_none == 0.0

    # Cancel non-existent reservation
    with pytest.raises(ReservationNotFoundError):
        system.cancel_reservation("NON-EXISTENT")


