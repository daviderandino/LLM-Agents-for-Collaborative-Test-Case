import pytest
from data.input_code.hotel_reservation import *
import datetime

@pytest.fixture
def hotel_reservation_system():
    return HotelReservationSystem()

@pytest.mark.parametrize('room_number, room_type, price_per_night, expected', [
    (101, 'single', 100.0, None),
    (101, 'single', 0.0, ValueError)
])
def test_add_room(hotel_reservation_system, room_number, room_type, price_per_night, expected):
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            hotel_reservation_system.add_room(room_number, room_type, price_per_night)
    else:
        hotel_reservation_system.add_room(room_number, room_type, price_per_night)
        assert hotel_reservation_system.rooms[room_number]['price_per_night'] == price_per_night

@pytest.mark.parametrize('room_number, user_name, check_in, check_out, expected', [
    # Successful booking
    (101, 'John Doe', datetime.date.today() + datetime.timedelta(days=10),
     datetime.date.today() + datetime.timedelta(days=12), 'RES-0001'),
    # Room does not exist
    (102, 'John Doe', datetime.date.today() + datetime.timedelta(days=10),
     datetime.date.today() + datetime.timedelta(days=12), RoomNotFoundError),
    # Invalid date: check_in == check_out
    (101, 'John Doe', datetime.date.today() + datetime.timedelta(days=10),
     datetime.date.today() + datetime.timedelta(days=10), InvalidDateError),
    # Past date booking
    (101, 'John Doe', datetime.date.today() - datetime.timedelta(days=5),
     datetime.date.today() - datetime.timedelta(days=3), InvalidDateError),
    # Room unavailable (overlap)
    (101, 'John Doe', datetime.date.today() + datetime.timedelta(days=10),
     datetime.date.today() + datetime.timedelta(days=12), RoomUnavailableError)
])
def test_book_room(hotel_reservation_system, room_number, user_name, check_in, check_out, expected):
    # Ensure room 101 exists for relevant tests
    if room_number == 101:
        hotel_reservation_system.add_room(101, 'single', 100.0)

    # For the unavailable test, pre-book the same slot
    if expected is RoomUnavailableError:
        hotel_reservation_system.book_room(101, 'Existing Guest',
                                           check_in, check_out)

    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            hotel_reservation_system.book_room(room_number, user_name, check_in, check_out)
    else:
        res_id = hotel_reservation_system.book_room(room_number, user_name, check_in, check_out)
        assert res_id == expected

@pytest.mark.parametrize('reservation_id, expected', [
    ('RES-0001', 200.0),  
    ('RES-0002', ReservationNotFoundError)
])
def test_cancel_reservation(hotel_reservation_system, reservation_id, expected):
    # Add room and make a future reservation
    hotel_reservation_system.add_room(101, 'single', 100.0)
    future_check_in = datetime.date.today() + datetime.timedelta(days=10)
    future_check_out = future_check_in + datetime.timedelta(days=2)
    hotel_reservation_system.book_room(101, 'John Doe', future_check_in, future_check_out)

    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            hotel_reservation_system.cancel_reservation(reservation_id)
    else:
        refund = hotel_reservation_system.cancel_reservation(reservation_id)
        assert refund == expected

@pytest.mark.parametrize('date, expected', [
    (datetime.date.today() + datetime.timedelta(days=10), []),
])
def test_get_room_occupancy(hotel_reservation_system, date, expected):
    # No reservations yet for the given date
    assert hotel_reservation_system.get_room_occupancy(date) == expected

@pytest.mark.parametrize('room_number, check_in, check_out, expected', [
    (101, datetime.date.today() + datetime.timedelta(days=10),
     datetime.date.today() + datetime.timedelta(days=12), True),
])
def test_is_room_available(hotel_reservation_system, room_number, check_in, check_out, expected):
    hotel_reservation_system.add_room(101, 'single', 100.0)
    assert hotel_reservation_system._is_room_available(room_number, check_in, check_out) == expected

@pytest.mark.parametrize("room_number, user_name, check_in, check_out, expected", [
    (101, 'John Doe', datetime.date.today() + datetime.timedelta(days=20), datetime.date.today() + datetime.timedelta(days=22), 'RES-0001'),
    (102, 'John Doe', datetime.date(2024, 9, 20), datetime.date(2024, 9, 22), RoomNotFoundError),
    (101, 'John Doe', datetime.date(2024, 9, 20), datetime.date(2024, 9, 20), InvalidDateError),
    (101, 'John Doe', datetime.date(2024, 8, 20), datetime.date(2024, 8, 22), InvalidDateError),
])
def test_book_room_new(hotel_reservation_system, room_number, user_name, check_in, check_out, expected):
    hotel_reservation_system.add_room(101, 'single', 100.0)
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            hotel_reservation_system.book_room(room_number, user_name, check_in, check_out)
    else:
        res_id = hotel_reservation_system.book_room(room_number, user_name, check_in, check_out)
        assert res_id == expected

@pytest.mark.parametrize("reservation_id, expected", [
    ('RES-0001', 200.0),
    ('RES-0002', ReservationNotFoundError)
])
def test_cancel_reservation_new(hotel_reservation_system, reservation_id, expected):
    hotel_reservation_system.add_room(101, 'single', 100.0)
    future_check_in = datetime.date.today() + datetime.timedelta(days=10)
    future_check_out = future_check_in + datetime.timedelta(days=2)
    res_id = hotel_reservation_system.book_room(101, 'John Doe', future_check_in, future_check_out)
    if reservation_id == 'RES-0001':
        reservation_id = res_id
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            hotel_reservation_system.cancel_reservation(reservation_id)
    else:
        refund = hotel_reservation_system.cancel_reservation(reservation_id)
        assert refund == expected

def test_cancel_reservation_refund_policy_2_days_before_checkin(hotel_reservation_system):
    hotel_reservation_system.add_room(101, 'single', 100.0)
    future_check_in = datetime.date.today() + datetime.timedelta(days=2)
    future_check_out = future_check_in + datetime.timedelta(days=1)
    res_id = hotel_reservation_system.book_room(101, 'John Doe', future_check_in, future_check_out)
    refund = hotel_reservation_system.cancel_reservation(res_id)
    assert refund == 50.0

def test_cancel_reservation_refund_policy_edge_case_today(hotel_reservation_system):
    hotel_reservation_system.add_room(101, 'single', 100.0)
    future_check_in = datetime.date.today()
    future_check_out = future_check_in + datetime.timedelta(days=1)
    res_id = hotel_reservation_system.book_room(101, 'John Doe', future_check_in, future_check_out)
    refund = hotel_reservation_system.cancel_reservation(res_id)
    assert refund == 0.0

@pytest.mark.parametrize(
    "check_in, check_out, expected",
    [
        (
            datetime.date.today() + datetime.timedelta(days=10),
            datetime.date.today() + datetime.timedelta(days=11),
            "RES-0001",
        ),
    ],
)
def test_book_room_partial_overlap(hotel_reservation_system, check_in, check_out, expected):
    hotel_reservation_system.add_room(101, "single", 100.0)
    res_id = hotel_reservation_system.book_room(101, "Jane Doe", check_in, check_out)
    assert res_id == expected

@pytest.mark.parametrize(
    "days_until_checkin, expected_refund",
    [
        (8, 200.0),  # > 7 days: full refund
    ],
)
def test_cancel_reservation_refund_policy_edge_cases(hotel_reservation_system, days_until_checkin, expected_refund):
    hotel_reservation_system.add_room(101, "single", 100.0)
    future_check_in = datetime.date.today() + datetime.timedelta(days=days_until_checkin)
    future_check_out = future_check_in + datetime.timedelta(days=2)
    res_id = hotel_reservation_system.book_room(101, "John Doe", future_check_in, future_check_out)
    refund = hotel_reservation_system.cancel_reservation(res_id)
    assert refund == expected_refund

@pytest.mark.parametrize(
    "date, expected",
    [
        (
            datetime.date.today() + datetime.timedelta(days=10),
            [101],
        ),
    ],
)
def test_get_room_occupancy_multiple_occupancies(hotel_reservation_system, date, expected):
    hotel_reservation_system.add_room(101, "single", 100.0)
    check_in = date
    check_out = date + datetime.timedelta(days=1)
    hotel_reservation_system.book_room(101, "John Doe", check_in, check_out)
    assert hotel_reservation_system.get_room_occupancy(date) == expected

@pytest.mark.parametrize(
    "check_in, check_out, expected",
    [
        (
            datetime.date.today() + datetime.timedelta(days=10),
            datetime.date.today() + datetime.timedelta(days=12),
            False,
        ),
    ],
)
def test_is_room_available_false_case(hotel_reservation_system, check_in, check_out, expected):
    hotel_reservation_system.add_room(101, "single", 100.0)
    # Pre-book the same slot
    hotel_reservation_system.book_room(101, "Existing Guest", check_in, check_out)
    assert hotel_reservation_system._is_room_available(101, check_in, check_out) == expected

@pytest.mark.parametrize(
    "days_until_checkin, expected_refund",
    [
        (1, 0.0),  # < 2 days: no refund
    ],
)
def test_cancel_reservation_2_days_before_checkin(hotel_reservation_system, days_until_checkin, expected_refund):
    hotel_reservation_system.add_room(101, "single", 100.0)
    future_check_in = datetime.date.today() + datetime.timedelta(days=days_until_checkin)
    future_check_out = future_check_in + datetime.timedelta(days=1)
    res_id = hotel_reservation_system.book_room(101, "John Doe", future_check_in, future_check_out)
    refund = hotel_reservation_system.cancel_reservation(res_id)
    assert refund == expected_refund

@pytest.mark.parametrize(
    "date, expected",
    [
        (
            datetime.date.today() + datetime.timedelta(days=12),
            [],
        ),
    ],
)
def test_get_room_occupancy_checkout_date(hotel_reservation_system, date, expected):
    hotel_reservation_system.add_room(101, "single", 100.0)
    check_in = datetime.date.today() + datetime.timedelta(days=10)
    check_out = datetime.date.today() + datetime.timedelta(days=12)
    hotel_reservation_system.book_room(101, "John Doe", check_in, check_out)
    assert hotel_reservation_system.get_room_occupancy(date) == expected

@pytest.mark.parametrize(
    "check_in, check_out, expected",
    [
        (
            datetime.date.today() + datetime.timedelta(days=10),
            datetime.date.today() + datetime.timedelta(days=11),
            "RES-0001",
        ),
    ],
)
def test_book_room_same_day_checkin_checkout_valid(hotel_reservation_system, check_in, check_out, expected):
    hotel_reservation_system.add_room(101, "single", 100.0)
    res_id = hotel_reservation_system.book_room(101, "Jane Doe", check_in, check_out)
    assert res_id == expected

@pytest.mark.parametrize(
    "check_in, check_out, expected",
    [
        (
            datetime.date.today() + datetime.timedelta(days=12),
            datetime.date.today() + datetime.timedelta(days=13),
            True,
        ),
    ],
)
def test_is_room_available_partial_overlap(hotel_reservation_system, check_in, check_out, expected):
    hotel_reservation_system.add_room(101, "single", 100.0)
    # Pre-book a slot that does not overlap with the test range
    pre_check_in = datetime.date.today() + datetime.timedelta(days=10)
    pre_check_out = datetime.date.today() + datetime.timedelta(days=12)
    hotel_reservation_system.book_room(101, "Existing Guest", pre_check_in, pre_check_out)
    assert hotel_reservation_system._is_room_available(101, check_in, check_out) == expected

@pytest.mark.parametrize(
    "days_until_checkin, expected_refund",
    [
        (7, 100.0),  # 7 days before check-in: 50% refund
    ],
)
def test_cancel_reservation_refund_policy_edge_case_7_days_before_checkin(hotel_reservation_system, days_until_checkin, expected_refund):
    hotel_reservation_system.add_room(101, "single", 100.0)
    future_check_in = datetime.date.today() + datetime.timedelta(days=days_until_checkin)
    future_check_out = future_check_in + datetime.timedelta(days=2)
    res_id = hotel_reservation_system.book_room(101, "John Doe", future_check_in, future_check_out)
    refund = hotel_reservation_system.cancel_reservation(res_id)
    assert refund == expected_refund

@pytest.mark.parametrize(
    "price_per_night, expected",
    [
        (0.01, "RES-0001"),
    ],
)
def test_book_room_edge_case_min_price(hotel_reservation_system, price_per_night, expected):
    hotel_reservation_system.add_room(101, "single", price_per_night)
    check_in = datetime.date.today() + datetime.timedelta(days=10)
    check_out = check_in + datetime.timedelta(days=2)
    res_id = hotel_reservation_system.book_room(101, "John Doe", check_in, check_out)
    assert res_id == expected