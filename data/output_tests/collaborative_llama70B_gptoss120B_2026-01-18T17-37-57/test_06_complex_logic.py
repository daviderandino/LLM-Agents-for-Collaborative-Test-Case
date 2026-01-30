import pytest
from unittest.mock import patch

from data.input_code.06_complex_logic import *

# ---------- Fixtures ----------
@pytest.fixture
def warehouse():
    # initial stock with enough for successful tests
    return Warehouse(initial_stock={"item1": 5})


@pytest.fixture
def order_processor(warehouse):
    return OrderProcessor(warehouse=warehouse)


# ---------- Helper to mock datetime ----------
def mock_datetime(target_hour):
    class MockedDatetime(datetime):
        @classmethod
        def now(cls):
            return datetime(2022, 1, 1, target_hour, 0, 0)
    return MockedDatetime


# ---------- Warehouse Tests ----------
@pytest.mark.parametrize(
    "item_id, qty, expected",
    [
        ("item1", 1, True),          # stock exists and sufficient
    ],
)
def test_warehouse_check_stock_ok(warehouse, item_id, qty, expected):
    assert warehouse.check_stock(item_id, qty) is expected


def test_warehouse_check_stock_not_found(warehouse):
    with pytest.raises(InventoryError):
        warehouse.check_stock("item2", 1)


@pytest.mark.parametrize(
    "item_id, qty",
    [
        ("item1", 1),   # sufficient stock
    ],
)
def test_warehouse_lock_item_ok(warehouse, item_id, qty):
    warehouse.lock_item(item_id, qty)  # should not raise
    # after locking, stock should be reduced for further checks
    assert not warehouse.check_stock(item_id, 5)  # only 4 left


def test_warehouse_lock_item_insufficient(warehouse):
    with pytest.raises(InventoryError):
        warehouse.lock_item("item1", 10)


def test_warehouse_release_item(warehouse):
    # lock first, then release
    warehouse.lock_item("item1", 2)
    warehouse.release_item("item1", 2)
    # after release, original stock should be fully available again
    assert warehouse.check_stock("item1", 5)


# ---------- DiscountEngine Tests ----------
@patch("data.input_code.06_complex_logic.datetime", mock_datetime(2))
def test_discount_engine_happy_path():
    # hour 2 -> night discount (0.05) + GOLD (0.10) + valid promo (0.10) = 0.25
    discount = DiscountEngine.calculate_discount(
        total_amount=100.0,
        user_tier="GOLD",
        promo_code="ABC-123",
    )
    assert discount == 0.25


def test_discount_engine_invalid_promo():
    with pytest.raises(ValueError):
        DiscountEngine.calculate_discount(
            total_amount=100.0,
            user_tier="GOLD",
            promo_code="ABC-1234",  # invalid format
        )


# ---------- OrderProcessor.validate_user Tests ----------
def test_validate_user_ok(order_processor):
    order_processor.validate_user(email="test@example.com", age=25)  # no exception


@pytest.mark.parametrize(
    "email, age, exc_msg",
    [
        ("test", 25, "Invalid email format"),
        ("test@example.com", 15, "User must be 18+"),
        ("test@example.com", 101, "Age verification required for 100+"),
    ],
)
def test_validate_user_errors(order_processor, email, age, exc_msg):
    with pytest.raises(UserValidationError) as ei:
        order_processor.validate_user(email=email, age=age)
    assert exc_msg in str(ei.value)


# ---------- OrderProcessor.process_order Tests ----------
@patch("data.input_code.06_complex_logic.datetime", mock_datetime(2))
def test_process_order_success(order_processor):
    result = order_processor.process_order(
        order_id="order1",
        user_data={
            "email": "test@example.com",
            "age": 25,
            "tier": "GOLD",
            "payment_method": "CC",
        },
        items=[{"id": "item1", "qty": 1, "price": 100.0}],
        promo_code="ABC-123",
    )
    # discount = 0.25 (night + GOLD + promo)
    assert result["status"] == "success"
    assert result["order_id"] == "order1"
    assert result["original_price"] == 100.0
    assert result["discount_applied"] == 0.25
    # final_total = round(100 * (1-0.25) * 1.22, 2) = 91.5
    assert result["final_total"] == 91.5
    assert result["items_count"] == 1


def test_process_order_out_of_stock(order_processor):
    # request more than available (warehouse has only 5)
    result = order_processor.process_order(
        order_id="order2",
        user_data={
            "email": "test@example.com",
            "age": 25,
            "tier": "GOLD",
            "payment_method": "CC",
        },
        items=[{"id": "item1", "qty": 10, "price": 100.0}],
        promo_code="ABC-123",
    )
    assert result["status"] == "failed"
    assert "Out of stock" in result["reason"]


def test_process_order_invalid_promo(order_processor):
    result = order_processor.process_order(
        order_id="order3",
        user_data={
            "email": "test@example.com",
            "age": 25,
            "tier": "GOLD",
            "payment_method": "CC",
        },
        items=[{"id": "item1", "qty": 1, "price": 100.0}],
        promo_code="ABC-1234",  # invalid format
    )
    assert result["status"] == "error"
    assert "Promo Error" in result["reason"]


@patch("data.input_code.06_complex_logic.datetime", mock_datetime(2))
def test_process_order_fraud_detected(order_processor):
    # price chosen so that after discount & tax we get exactly 666.66
    result = None
    with pytest.raises(FraudDetectedError):
        order_processor.process_order(
            order_id="order4",
            user_data={
                "email": "test@example.com",
                "age": 25,
                "tier": "GOLD",
                "payment_method": "PAYPAL",
            },
            items=[{"id": "item1", "qty": 1, "price": 728.59}],
            promo_code="ABC-123",
        )


@patch("data.input_code.06_complex_logic.datetime", mock_datetime(2))
def test_process_order_payment_error(order_processor):
    with pytest.raises(PaymentError):
        order_processor.process_order(
            order_id="order5",
            user_data={
                "email": "test@example.com",
                "age": 25,
                "tier": "GOLD",
                "payment_method": "CRYPTO",
            },
            items=[{"id": "item1", "qty": 1, "price": 10.0}],
            promo_code="ABC-123",
        )

import pytest
from unittest.mock import patch
from data.input_code.06_complex_logic import *

# Helper to mock datetime at a specific hour (no night discount)
def mock_datetime_no_night(target_hour=10):
    class MockedDatetime(datetime):
        @classmethod
        def now(cls):
            return datetime(2022, 1, 1, target_hour, 0, 0)
    return MockedDatetime


# ---------- DiscountEngine Additional Tests ----------
@patch("data.input_code.06_complex_logic.datetime", mock_datetime_no_night())
def test_discount_engine_night_owl_off():
    # hour 10 -> no night discount, STANDARD tier, no promo
    discount = DiscountEngine.calculate_discount(
        total_amount=100.0,
        user_tier="STANDARD",
        promo_code=None,
    )
    assert discount == 0.0


@patch("data.input_code.06_complex_logic.datetime", mock_datetime_no_night())
def test_discount_engine_platinum_tier():
    discount = DiscountEngine.calculate_discount(
        total_amount=100.0,
        user_tier="PLATINUM",
        promo_code=None,
    )
    assert discount == 0.20


@patch("data.input_code.06_complex_logic.datetime", mock_datetime_no_night())
def test_discount_engine_platinum_tier_high_amount():
    discount = DiscountEngine.calculate_discount(
        total_amount=1001.0,
        user_tier="PLATINUM",
        promo_code=None,
    )
    # 0.20 tier + 0.05 extra for amount > 1000 = 0.25
    assert discount == 0.25


def test_discount_engine_promo_code_50_percent():
    # Promo ending with 999 gives immediate 50% off (returns amount, not percent)
    result = DiscountEngine.calculate_discount(
        total_amount=100.0,
        user_tier="STANDARD",
        promo_code="ABC-999",
    )
    assert result == 50.0


# ---------- OrderProcessor.validate_user Additional Test ----------
def test_validate_user_email_simple_invalid(order_processor):
    with pytest.raises(UserValidationError) as exc:
        order_processor.validate_user(email="test@example", age=25)
    assert "Invalid email format" in str(exc.value)


# ---------- OrderProcessor.process_order Edge Cases ----------
@pytest.mark.parametrize(
    "item, expected_original, expected_final",
    [
        ({"id": "item1", "qty": 0, "price": 100.0}, 0.0, 0.0),
        ({"id": "item1", "qty": -1, "price": 100.0}, -100.0, -97.6),
        ({"id": "item1", "qty": 1, "price": 0.0}, 0.0, 0.0),
        ({"id": "item1", "qty": 1, "price": -100.0}, -100.0, -97.6),
    ],
)
@patch("data.input_code.06_complex_logic.datetime", mock_datetime_no_night())
def test_process_order_edge_cases(order_processor, item, expected_original, expected_final):
    result = order_processor.process_order(
        order_id="order_edge",
        user_data={
            "email": "test@example.com",
            "age": 25,
            "tier": "GOLD",
            "payment_method": "CC",
        },
        items=[item],
        promo_code="ABC-123",
    )
    assert result["status"] == "success"
    assert result["original_price"] == expected_original
    assert result["final_total"] == expected_final
    assert result["items_count"] == 1