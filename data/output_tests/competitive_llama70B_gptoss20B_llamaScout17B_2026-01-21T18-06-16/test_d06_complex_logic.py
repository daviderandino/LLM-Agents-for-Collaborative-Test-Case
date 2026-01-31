import pytest
import re
import unittest
from datetime import datetime
from data.input_code.d06_complex_logic import *

# ---------- Warehouse Tests ----------
@pytest.mark.parametrize(
    "item_id, quantity, initial_stock, expected",
    [
        ("item1", 1, {"item1": 10}, True),
        ("item2", 1, {"item1": 10}, InventoryError),
    ],
)
def test_warehouse_check_stock(item_id, quantity, initial_stock, expected):
    warehouse = Warehouse(initial_stock)
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            warehouse.check_stock(item_id, quantity)
    else:
        assert warehouse.check_stock(item_id, quantity) is expected


@pytest.mark.parametrize(
    "item_id, quantity, initial_stock, expected",
    [
        ("item1", 1, {"item1": 10}, None),
        ("item1", 11, {"item1": 10}, InventoryError),
    ],
)
def test_warehouse_lock_item(item_id, quantity, initial_stock, expected):
    warehouse = Warehouse(initial_stock)
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            warehouse.lock_item(item_id, quantity)
    else:
        # No exception expected
        warehouse.lock_item(item_id, quantity)


def test_warehouse_release_item():
    warehouse = Warehouse({"item1": 10})
    warehouse.lock_item("item1", 1)
    # No exception expected
    warehouse.release_item("item1", 1)


# ---------- DiscountEngine Tests ----------
@pytest.mark.parametrize(
    "total_amount, user_tier, promo_code, expected",
    [
        (100.0, "GOLD", None, 0.10),
        (100.0, "GOLD", "ABC-123", 0.20),
        (100.0, "GOLD", "invalid", ValueError),
    ],
)
def test_discount_engine(total_amount, user_tier, promo_code, expected):
    # Compute expected discount including possible night discount
    base_discount = 0.0
    current_hour = datetime.now().hour
    if 0 <= current_hour < 6:
        base_discount += 0.05

    if user_tier == "GOLD":
        base_discount += 0.10
    elif user_tier == "PLATINUM":
        base_discount += 0.20
        if total_amount > 1000.00:
            base_discount += 0.05

    if promo_code:
        if re.match(r"^[A-Z]{3}-\d{3}$", promo_code):
            if promo_code.endswith("999"):
                # 50% off immediate
                base_discount = 0.5
            else:
                base_discount += 0.10
        else:
            base_discount = ValueError

    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            DiscountEngine.calculate_discount(total_amount, user_tier, promo_code)
    else:
        discount = DiscountEngine.calculate_discount(total_amount, user_tier, promo_code)
        assert discount == expected


# ---------- OrderProcessor.validate_user Tests ----------
@pytest.mark.parametrize(
    "email, age, expected",
    [
        ("test@example.com", 25, None),
        ("invalid", 25, UserValidationError),
        ("test@example.com", 17, UserValidationError),
    ],
)
def test_order_processor_validate_user(email, age, expected):
    processor = OrderProcessor(Warehouse({}))
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            processor.validate_user(email, age)
    else:
        processor.validate_user(email, age)  # No exception expected


# ---------- OrderProcessor.process_order Tests ----------
@pytest.mark.parametrize(
    "order_id, user_data, items, promo_code, expected_status",
    [
        # Successful order
        (
            "order1",
            {"email": "test@example.com", "age": 25, "tier": "GOLD"},
            [{"id": "item1", "qty": 1, "price": 100.0}],
            None,
            "success",
        ),
        # Out of stock
        (
            "order1",
            {"email": "test@example.com", "age": 25, "tier": "GOLD"},
            [{"id": "item1", "qty": 11, "price": 100.0}],
            None,
            "failed",
        ),
        # Order with promo code
        (
            "order1",
            {"email": "test@example.com", "age": 25, "tier": "GOLD"},
            [{"id": "item1", "qty": 1, "price": 100.0}],
            "ABC-123",
            "success",
        ),
        # Invalid promo code
        (
            "order1",
            {"email": "test@example.com", "age": 25, "tier": "GOLD"},
            [{"id": "item1", "qty": 1, "price": 100.0}],
            "invalid",
            "error",
        ),
        # Payment error with crypto
        (
            "order1",
            {"email": "test@example.com", "age": 25, "tier": "GOLD", "payment_method": "CRYPTO"},
            [{"id": "item1", "qty": 1, "price": 40.0}],
            None,
            PaymentError,
        ),
    ],
)
def test_order_processor_process_order(order_id, user_data, items, promo_code, expected_status):
    warehouse = Warehouse({"item1": 10})
    processor = OrderProcessor(warehouse)

    if isinstance(expected_status, type) and issubclass(expected_status, Exception):
        with pytest.raises(expected_status):
            processor.process_order(order_id, user_data, items, promo_code)
    else:
        result = processor.process_order(order_id, user_data, items, promo_code)

        assert result["status"] == expected_status

        if expected_status == "success":
            assert "order_id" in result
            assert "original_price" in result
            assert "discount_applied" in result
            assert "final_total" in result
            assert "items_count" in result
        elif expected_status == "failed":
            assert "reason" in result
        elif expected_status == "error":
            assert "reason" in result


# ---------- New DiscountEngine Tests ----------


@pytest.mark.parametrize(
    "total_amount, user_tier, promo_code, expected",
    [
        (1000.1, "PLATINUM", None, 0.25),  # Platinum tier over 1000
    ],
)
def test_discount_engine_platinum_tier(total_amount, user_tier, promo_code, expected):
    discount = DiscountEngine.calculate_discount(total_amount, user_tier, promo_code)
    assert discount == expected


@pytest.mark.parametrize(
    "total_amount, user_tier, promo_code, expected",
    [
        (100.0, "GOLD", "ABC-999", 50.0),  # Promo code 999
    ],
)
def test_discount_engine_promo_999(total_amount, user_tier, promo_code, expected):
    discount = DiscountEngine.calculate_discount(total_amount, user_tier, promo_code)
    assert discount == expected


# ---------- New OrderProcessor.validate_user Tests ----------
@pytest.mark.parametrize(
    "email, age, expected",
    [
        ("test@example.com", 101, UserValidationError),  # Age over 100
    ],
)
def test_order_processor_validate_user_age_100(email, age, expected):
    processor = OrderProcessor(Warehouse({}))
    with pytest.raises(expected):
        processor.validate_user(email, age)


# ---------- New OrderProcessor.process_order Tests ----------
@pytest.mark.parametrize(
    "order_id, user_data, items, promo_code, expected",
    [
        (
            "order1",
            {"email": "test@example.com", "age": 25, "tier": "GOLD", "payment_method": "PAYPAL"},
            [{"id": "item1", "qty": 1, "price": 666.66}],
            None,
            "success",
        ),  # Payment fraud detection
        (
            "order1",
            {"email": "test@example.com", "age": 25, "tier": "GOLD"},
            [{"id": "item1", "qty": -1, "price": 0.0}],
            None,
            ValueError,
        ),  # Return item with price 0
    ],
)
def test_order_processor_process_order_new_cases(order_id, user_data, items, promo_code, expected):
    warehouse = Warehouse({"item1": 10})
    processor = OrderProcessor(warehouse)

    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            processor.process_order(order_id, user_data, items, promo_code)
    else:
        result = processor.process_order(order_id, user_data, items, promo_code)
        assert result["status"] == expected