import pytest
from data.input_code.05_hotel import *
import datetime

# Ensure each test gets a fresh instance of the system
@pytest.fixture
def system():
    return HotelReservationSystem()

# ---------- add_room ----------
@pytest.mark.parametrize(
    "room_number, room_type, price, expect_exception",
    [
        (101, "single", 100.0, None),          # T1_OK
        (102, "double", 0.0, ValueError),     # T2_ERR
    ],
    ids=["T1_OK", "T2_ERR"]
)
def test_add_room(system, room_number, room_type, price, expect_exception):
    if expect_exception:
        with pytest.raises(expect_exception):
            system.add_room(room_number, room_type, price)
    else:
        system.add_room(room_number, room_type, price)
        assert room_number in system.rooms
        assert system.rooms[room_number]["type"] == room_type
        assert system.rooms[room_number]["price_per_night"] == price

# ---------- book_room ----------
@pytest.mark.parametrize(
    "room_number, user_name, check_in_args, check_out_args, expected, expect_exception, prebook",
    [
        # T3_OK – first successful booking
        (101, "John Doe", (2024, 9, 20), (2024, 9, 22), "RES-0001", None, None),

        # T4_ERR – room does not exist
        (103, "Jane Doe", (2024, 9, 20), (2024, 9, 22), None, RoomNotFoundError, None),

        # T5_ERR – checkout same day as check‑in
        (101, "John Doe", (2024, 9, 20), (2024, 9, 20), None, InvalidDateError, None),

        # T6_ERR – booking in the past (check‑in before today)
        (101, "John Doe", (2024, 9, 5), (2024, 9, 7), None, InvalidDateError, None),

        # T7_ERR – room already booked for those dates
        (101, "John Doe", (2024, 9, 20), (2024, 9, 22), None, RoomUnavailableError,
         {"room_number": 101, "user_name": "Jane Doe",
          "check_in": (2024, 9, 20), "check_out": (2024, 9, 22)}),
    ],
    ids=["T3_OK", "T4_ERR", "T5_ERR", "T6_ERR", "T7_ERR"]
)
def test_book_room(system, monkeypatch, room_number, user_name,
                   check_in_args, check_out_args, expected,
                   expect_exception, prebook):
    # Fix today's date for deterministic behaviour
    fake_today = datetime.date(2024, 9, 10)

    class FixedDate(datetime.date):
        @classmethod
        def today(cls):
            return fake_today

    monkeypatch.setattr(datetime, "date", FixedDate)

    # Add the room (skip for the not‑found case)
    if room_number != 103:
        system.add_room(room_number, "single", 100.0)

    # Pre‑book a reservation if required (T7_ERR)
    if prebook:
        system.add_room(prebook["room_number"], "single", 100.0)
        system.book_room(
            prebook["room_number"],
            prebook["user_name"],
            FixedDate(*prebook["check_in"]),
            FixedDate(*prebook["check_out"])
        )

    check_in = FixedDate(*check_in_args)
    check_out = FixedDate(*check_out_args)

    if expect_exception:
        with pytest.raises(expect_exception):
            system.book_room(room_number, user_name, check_in, check_out)
    else:
        reservation_id = system.book_room(room_number, user_name, check_in, check_out)
        assert reservation_id == expected
        assert reservation_id in system.reservations
        res = system.reservations[reservation_id]
        assert res.room_number == room_number
        assert res.user_name == user_name
        assert res.check_in == check_in
        assert res.check_out == check_out

# ---------- cancel_reservation ----------
def test_cancel_reservation_success(system, monkeypatch):
    fake_today = datetime.date(2024, 9, 10)

    class FixedDate(datetime.date):
        @classmethod
        def today(cls):
            return fake_today

    monkeypatch.setattr(datetime, "date", FixedDate)

    system.add_room(101, "single", 100.0)
    check_in = FixedDate(2024, 9, 20)
    check_out = FixedDate(2024, 9, 22)
    reservation_id = system.book_room(101, "John Doe", check_in, check_out)

    refund = system.cancel_reservation(reservation_id)
    assert refund == 200.0

def test_cancel_reservation_not_found(system):
    with pytest.raises(ReservationNotFoundError):
        system.cancel_reservation("RES-0002")

# ---------- get_room_occupancy ----------
def test_get_room_occupancy(system, monkeypatch):
    fake_today = datetime.date(2024, 9, 10)

    class FixedDate(datetime.date):
        @classmethod
        def today(cls):
            return fake_today

    monkeypatch.setattr(datetime, "date", FixedDate)

    system.add_room(101, "single", 100.0)
    check_in = FixedDate(2024, 9, 20)
    check_out = FixedDate(2024, 9, 22)
    system.book_room(101, "John Doe", check_in, check_out)

    query_date = FixedDate(2024, 9, 21)
    occupied = system.get_room_occupancy(query_date)

    assert occupied == [101]

# ---------- cancel_reservation (50% refund) ----------
@pytest.mark.parametrize(
    "setup, expected_refund",
    [
        (
            {
                "add_room": [101, "single", 100.0],
                "book_room": [
                    101,
                    "John Doe",
                    {"year": 2024, "month": 9, "day": 17},
                    {"year": 2024, "month": 9, "day": 19},
                ],
                "today": {"year": 2024, "month": 9, "day": 10},
            },
            100.0,
        ),
    ],
    ids=["T_MISSING_CANCEL_REFUND_50PERCENT"],
)
def test_cancel_reservation_refund_50_percent(system, monkeypatch, setup, expected_refund):
    fake_today = datetime.date(**setup["today"])

    class FixedDate(datetime.date):
        @classmethod
        def today(cls):
            return fake_today

    monkeypatch.setattr(datetime, "date", FixedDate)

    system.add_room(*setup["add_room"])

    book_args = setup["book_room"]
    check_in = FixedDate(**book_args[2])
    check_out = FixedDate(**book_args[3])
    reservation_id = system.book_room(
        book_args[0], book_args[1], check_in, check_out
    )

    refund = system.cancel_reservation(reservation_id)
    assert refund == expected_refund

# ---------- cancel_reservation (0% refund) ----------
@pytest.mark.parametrize(
    "setup, expected_refund",
    [
        (
            {
                "add_room": [101, "single", 100.0],
                "book_room": [
                    101,
                    "John Doe",
                    {"year": 2024, "month": 9, "day": 12},
                    {"year": 2024, "month": 9, "day": 14},
                ],
                "today": {"year": 2024, "month": 9, "day": 10},
            },
            100.0,
        ),
    ],
    ids=["T_MISSING_CANCEL_REFUND_0PERCENT"],
)
def test_cancel_reservation_refund_0_percent(system, monkeypatch, setup, expected_refund):
    fake_today = datetime.date(**setup["today"])

    class FixedDate(datetime.date):
        @classmethod
        def today(cls):
            return fake_today

    monkeypatch.setattr(datetime, "date", FixedDate)

    system.add_room(*setup["add_room"])

    book_args = setup["book_room"]
    check_in = FixedDate(**book_args[2])
    check_out = FixedDate(**book_args[3])
    reservation_id = system.book_room(
        book_args[0], book_args[1], check_in, check_out
    )

    refund = system.cancel_reservation(reservation_id)
    assert refund == expected_refund

# ---------- get_room_occupancy (multiple rooms) ----------
@pytest.mark.parametrize(
    "setup, query_date, expected",
    [
        (
            {
                "add_room": [
                    [101, "single", 100.0],
                    [102, "double", 200.0],
                ],
                "book_room": [
                    [
                        101,
                        "John Doe",
                        {"year": 2024, "month": 9, "day": 20},
                        {"year": 2024, "month": 9, "day": 22},
                    ],
                    [
                        102,
                        "Jane Doe",
                        {"year": 2024, "month": 9, "day": 20},
                        {"year": 2024, "month": 9, "day": 22},
                    ],
                ],
            },
            {"year": 2024, "month": 9, "day": 21},
            [101, 102],
        ),
    ],
    ids=["T_MISSING_GET_OCCUPANCY_MULTIPLE_ROOMS"],
)
def test_get_room_occupancy_multiple_rooms(system, monkeypatch, setup, query_date, expected):
    fake_today = datetime.date(2024, 9, 10)

    class FixedDate(datetime.date):
        @classmethod
        def today(cls):
            return fake_today

    monkeypatch.setattr(datetime, "date", FixedDate)

    for room_args in setup["add_room"]:
        system.add_room(*room_args)

    for book_args in setup["book_room"]:
        check_in = FixedDate(**book_args[2])
        check_out = FixedDate(**book_args[3])
        system.book_room(
            book_args[0], book_args[1], check_in, check_out
        )

    query = FixedDate(**query_date)
    occupied = system.get_room_occupancy(query)
    assert occupied == expected

# ---------- get_room_occupancy (edge date – check‑in) ----------
@pytest.mark.parametrize(
    "setup, query_date, expected",
    [
        (
            {
                "add_room": [101, "single", 100.0],
                "book_room": [
                    101,
                    "John Doe",
                    {"year": 2024, "month": 9, "day": 20},
                    {"year": 2024, "month": 9, "day": 22},
                ],
            },
            {"year": 2024, "month": 9, "day": 20},
            [101],
        ),
    ],
    ids=["T_MISSING_GET_OCCUPANCY_EDGE_DATE"],
)
def test_get_room_occupancy_edge_date(system, monkeypatch, setup, query_date, expected):
    fake_today = datetime.date(2024, 9, 10)

    class FixedDate(datetime.date):
        @classmethod
        def today(cls):
            return fake_today

    monkeypatch.setattr(datetime, "date", FixedDate)

    system.add_room(*setup["add_room"])

    book_args = setup["book_room"]
    check_in = FixedDate(**book_args[2])
    check_out = FixedDate(**book_args[3])
    system.book_room(
        book_args[0], book_args[1], check_in, check_out
    )

    query = FixedDate(**query_date)
    occupied = system.get_room_occupancy(query)
    assert occupied == expected

import pytest
import datetime

# ---------- cancel_reservation (0% refund edge case) ----------
def test_cancel_reservation_refund_0_percent_edge(system, monkeypatch):
    # Setup fixed today as 2024-09-11
    fake_today = datetime.date(2024, 9, 11)

    class FixedDate(datetime.date):
        @classmethod
        def today(cls):
            return fake_today

    monkeypatch.setattr(datetime, "date", FixedDate)

    # Add room and create reservation (check‑in on 2024‑09‑11, checkout 2024‑09‑13)
    system.add_room(101, "single", 100.0)
    check_in = FixedDate(2024, 9, 11)   # same as today
    check_out = FixedDate(2024, 9, 13)
    reservation_id = system.book_room(101, "John Doe", check_in, check_out)

    # Cancel on 2024‑09‑11 (the day of check‑in) → 0 % refund
    refund = system.cancel_reservation(reservation_id)
    assert refund == 0.0


# ---------- get_room_occupancy (edge date – checkout) ----------
def test_get_room_occupancy_edge_date_checkout(system, monkeypatch):
    # Fix today's date (not directly used but kept for consistency)
    fake_today = datetime.date(2024, 9, 10)

    class FixedDate(datetime.date):
        @classmethod
        def today(cls):
            return fake_today

    monkeypatch.setattr(datetime, "date", FixedDate)

    # Add room and book it from 2024‑09‑20 to 2024‑09‑22
    system.add_room(101, "single", 100.0)
    check_in = FixedDate(2024, 9, 20)
    check_out = FixedDate(2024, 9, 22)
    system.book_room(101, "John Doe", check_in, check_out)

    # Query on the checkout date – should be empty
    query_date = FixedDate(2024, 9, 22)
    occupied = system.get_room_occupancy(query_date)
    assert occupied == []


# ---------- book_room (edge case – booking on today) ----------
def test_book_room_edge_date_today(system, monkeypatch):
    # Fix today's date to 2024‑09‑10
    fake_today = datetime.date(2024, 9, 10)

    class FixedDate(datetime.date):
        @classmethod
        def today(cls):
            return fake_today

    monkeypatch.setattr(datetime, "date", FixedDate)

    # Ensure the room exists
    system.add_room(101, "single", 100.0)

    check_in = FixedDate(2024, 9, 10)   # same as today
    check_out = FixedDate(2024, 9, 12)

    reservation_id = system.book_room(101, "John Doe", check_in, check_out)
    assert reservation_id == "RES-0001"
    assert reservation_id in system.reservations
    res = system.reservations[reservation_id]
    assert res.check_in == check_in
    assert res.check_out == check_out