import pytest
from data.input_code.d05_hotel import *
import datetime

# Helper function to create date objects from strings
def date_from_str(date_str):
    return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()

# Test data
test_data = [
    # T1_ADD_VALID
    {
        "target": "add_room",
        "input": {
            "room_number": 101,
            "room_type": "Deluxe",
            "price_per_night": 100
        },
        "expected": None
    },
    # T2_ADD_INVALID_PRICE
    {
        "target": "add_room",
        "input": {
            "room_number": 102,
            "room_type": "Standard",
            "price_per_night": 0
        },
        "expected": "ValueError"
    },
    # T3_BOOK_ROOM_NOT_FOUND
    {
        "target": "book_room",
        "input": {
            "room_number": 999,
            "user_name": "Alice",
            "check_in": date_from_str("2026-01-23"),
            "check_out": date_from_str("2026-01-26")
        },
        "expected": "RoomNotFoundError"
    },
    # T4_BOOK_ROOM_INVALID_DATE
    {
        "target": "book_room",
        "input": {
            "room_number": 101,
            "user_name": "Bob",
            "check_in": date_from_str("2026-01-23"),
            "check_out": date_from_str("2026-01-23")
        },
        "setup": [
            {"method": "add_room", "args": {"room_number": 101, "room_type": "Deluxe", "price_per_night": 120}},
        ],
        "expected": "InvalidDateError"
    },
    # T5_BOOK_ROOM_PAST_DATE
    {
        "target": "book_room",
        "input": {
            "room_number": 101,
            "user_name": "Carol",
            "check_in": date_from_str("2026-01-10"),
            "check_out": date_from_str("2026-01-23")
        },
        "setup": [
            {"method": "add_room", "args": {"room_number": 101, "room_type": "Deluxe", "price_per_night": 120}},
        ],
        "expected": "InvalidDateError"
    },
    # T6_BOOK_ROOM_UNAVAILABLE
    {
        "target": "book_room",
        "input": {
            "room_number": 101,
            "user_name": "Dave",
            "check_in": date_from_str("2026-01-24"),
            "check_out": date_from_str("2026-01-27")
        },
        "setup": [
            {"method": "add_room", "args": {"room_number": 101, "room_type": "Deluxe", "price_per_night": 120}},
            {"method": "book_room", "args": {"room_number": 101, "user_name": "Eve", "check_in": date_from_str("2026-01-23"), "check_out": date_from_str("2026-01-26")}},
        ],
        "expected": "RoomUnavailableError"
    },
    # T7_BOOK_ROOM_SUCCESS
    {
        "target": "book_room",
        "input": {
            "room_number": 102,
            "user_name": "Frank",
            "check_in": date_from_str("2026-01-23"),
            "check_out": date_from_str("2026-01-26")
        },
        "setup": [
            {"method": "add_room", "args": {"room_number": 102, "room_type": "Standard", "price_per_night": 120}},
        ],
        "expected": lambda res_id: res_id.startswith("RES-")
    },
    # T8_CANCEL_RESERVATION_NOT_FOUND
    {
        "target": "cancel_reservation",
        "input": {
            "reservation_id": "RES-9999"
        },
        "expected": "ReservationNotFoundError"
    },
    # T9_CANCEL_RESERVATION_FULL_REFUND
    {
        "target": "cancel_reservation",
        "input": {
            "reservation_id": "RES-0001"
        },
        "setup": [
            {"method": "add_room", "args": {"room_number": 103, "room_type": "Suite", "price_per_night": 150}},
            {"method": "book_room", "args": {"room_number": 103, "user_name": "Grace", "check_in": date_from_str("2026-01-28"), "check_out": date_from_str("2026-01-31")}},
        ],
        "expected": 450.0
    },
    # T10_CANCEL_RESERVATION_HALF_REFUND
    {
        "target": "cancel_reservation",
        "input": {
            "reservation_id": "RES-0001"
        },
        "setup": [
            {"method": "add_room", "args": {"room_number": 104, "room_type": "Standard", "price_per_night": 80}},
            {"method": "book_room", "args": {"room_number": 104, "user_name": "Heidi", "check_in": date_from_str("2026-01-23"), "check_out": date_from_str("2026-01-26")}},
        ],
        "expected": 120.0
    },
    # T11_CANCEL_RESERVATION_NO_REFUND
    {
        "target": "cancel_reservation",
        "input": {
            "reservation_id": "RES-0001"
        },
        "setup": [
            {"method": "add_room", "args": {"room_number": 105, "room_type": "Standard", "price_per_night": 90}},
            {"method": "book_room", "args": {"room_number": 105, "user_name": "Ivan", "check_in": date_from_str("2026-01-19"), "check_out": date_from_str("2026-01-20")}},
        ],
        "expected": 0.0
    },
    # T12_GET_OCCUPANCY_WITH_RESERVATIONS
    {
        "target": "get_room_occupancy",
        "input": {
            "date": date_from_str("2026-01-24")
        },
        "setup": [
            {"method": "add_room", "args": {"room_number": 106, "room_type": "Deluxe", "price_per_night": 110}},
            {"method": "book_room", "args": {"room_number": 106, "user_name": "Judy", "check_in": date_from_str("2026-01-23"), "check_out": date_from_str("2026-01-26")}},
            {"method": "add_room", "args": {"room_number": 107, "room_type": "Standard", "price_per_night": 100}},
            {"method": "book_room", "args": {"room_number": 107, "user_name": "Karl", "check_in": date_from_str("2026-01-24"), "check_out": date_from_str("2026-01-27")}},
        ],
        "expected": [106, 107]
    },
    # T13_GET_OCCUPANCY_EMPTY
    {
        "target": "get_room_occupancy",
        "input": {
            "date": date_from_str("2026-01-20")
        },
        "expected": []
    }
]

@pytest.mark.parametrize("test_case", test_data, ids=lambda x: f"T{test_data.index(x)+1}_{x.get('target')}")
def test_hotel_reservation_system(test_case):
    hotel = HotelReservationSystem()
    try:
        for setup_step in test_case.get("setup", []):
            method_name = setup_step["method"]
            args = setup_step["args"]
            getattr(hotel, method_name)(**args)

        target_method = getattr(hotel, test_case["target"])
        input_args = test_case["input"]
        result = target_method(**input_args)

        expected = test_case["expected"]
        if isinstance(expected, str) and expected.endswith("Error"):
            exception_map = {
                "ValueError": pytest.raises(ValueError),
                "RoomNotFoundError": pytest.raises(RoomNotFoundError),
                "RoomUnavailableError": pytest.raises(RoomUnavailableError),
                "InvalidDateError": pytest.raises(InvalidDateError),
                "ReservationNotFoundError": pytest.raises(ReservationNotFoundError)
            }
            with exception_map[expected]:
                pass
        elif callable(expected):
            assert expected(result)
        else:
            assert result == expected
    except Exception as e:
        if 'Price per night must be positive' in str(e):
            assert test_case['target'] == 'add_room' and test_case['input']['price_per_night'] == 0
        elif 'does not exist' in str(e):
            assert test_case['target'] == 'book_room' and test_case['input']['room_number'] == 999
        elif 'Check-out date must be after check-in date' in str(e):
            assert test_case['target'] == 'book_room' and test_case['input']['check_in'] == test_case['input']['check_out']
        elif 'Cannot book in the past' in str(e):
            assert test_case['target'] == 'book_room' and (test_case['input']['check_in'] < datetime.date.today())
        elif 'is not available for these dates' in str(e):
            assert test_case['target'] == 'book_room' and test_case['input']['room_number'] == 101
        elif 'Reservation not found' in str(e):
            assert test_case['target'] == 'cancel_reservation' and test_case['input']['reservation_id'] == 'RES-9999'
        else:
            pytest.fail(f"Test failed with exception: {str(e)}")