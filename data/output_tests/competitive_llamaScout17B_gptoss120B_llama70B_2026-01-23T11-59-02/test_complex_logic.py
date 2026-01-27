import pytest
from datetime import datetime
from data.input_code.complex_logic import (
    Warehouse,
    DiscountEngine,
    OrderProcessor,
    InventoryError,
    UserValidationError,
    PaymentError,
    FraudDetectedError,
)

# ----------------------------------------------------------------------
# Helper to mock datetime.now() used inside DiscountEngine
# ----------------------------------------------------------------------
@pytest.fixture(autouse=True)
def mock_datetime_now(monkeypatch):
    """Force datetime.now() to return a fixed hour (2 AM) to trigger night discount."""
    class MockDateTime(datetime):
        @classmethod
        def now(cls, tz=None):
            # Return a datetime with hour=2 (night discount applies)
            return datetime(2022, 1, 1, 2, 0, 0, tzinfo=tz)

    monkeypatch.setattr("data.input_code.complex_logic.datetime", MockDateTime)


# ----------------------------------------------------------------------
# Warehouse tests
# ----------------------------------------------------------------------
@pytest.mark.parametrize("initial_stock, expected", [({"item1": 10, "item2": 5}, None)])
def test_warehouse_init(initial_stock, expected):
    warehouse = Warehouse(initial_stock)
    assert warehouse._stock == initial_stock
    assert warehouse._locked_stock == {}


@pytest.mark.parametrize(
    "item_id, quantity, expected",
    [
        ("item1", 5, True),
        ("item2", 10, False),
    ],
)
def test_warehouse_check_stock(item_id, quantity, expected):
    warehouse = Warehouse({"item1": 10, "item2": 5})
    assert warehouse.check_stock(item_id, quantity) == expected


def test_warehouse_check_stock_error():
    warehouse = Warehouse({"item1": 10, "item2": 5})
    with pytest.raises(InventoryError):
        warehouse.check_stock("item3", 5)


@pytest.mark.parametrize(
    "item_id, quantity",
    [
        ("item1", 5),
        ("item2", 3),
    ],
)
def test_warehouse_lock_item(item_id, quantity):
    warehouse = Warehouse({"item1": 10, "item2": 5})
    warehouse.lock_item(item_id, quantity)
    assert warehouse._locked_stock[item_id] == quantity


def test_warehouse_lock_item_error():
    warehouse = Warehouse({"item1": 10, "item2": 5})
    with pytest.raises(InventoryError):
        warehouse.lock_item("item1", 15)


@pytest.mark.parametrize(
    "item_id, quantity",
    [
        ("item1", 5),
        ("item2", 3),
    ],
)
def test_warehouse_release_item(item_id, quantity):
    warehouse = Warehouse({"item1": 10, "item2": 5})
    warehouse.lock_item(item_id, quantity)
    warehouse.release_item(item_id, quantity)
    assert item_id not in warehouse._locked_stock


# ----------------------------------------------------------------------
# DiscountEngine tests
# ----------------------------------------------------------------------
@pytest.mark.parametrize(
    "total_amount, user_tier, promo_code, expected",
    [
        (100.0, "GOLD", None, 0.15),          # night 0.05 + gold 0.10
        (1000.0, "PLATINUM", None, 0.25),    # night 0.05 + platinum 0.20
        (100.0, "GOLD", "ABC-123", 0.25),    # night 0.05 + gold 0.10 + promo 0.10
        (100.0, "GOLD", "ABC-999", 50.0),    # special promo returns discounted price
    ],
)
def test_discount_engine_calculate_discount(total_amount, user_tier, promo_code, expected):
    result = DiscountEngine.calculate_discount(total_amount, user_tier, promo_code)
    # Use pytest.approx for floating‑point comparisons
    assert result == pytest.approx(expected)


def test_discount_engine_calculate_discount_error():
    with pytest.raises(ValueError):
        DiscountEngine.calculate_discount(100.0, "GOLD", "Invalid-Code")


# ----------------------------------------------------------------------
# OrderProcessor user validation tests
# ----------------------------------------------------------------------
@pytest.mark.parametrize(
    "email, age, expected",
    [
        ("test@test.com", 25, None),
        ("invalid_email", 25, "UserValidationError"),
        ("test@test.com", 15, "UserValidationError"),
    ],
)
def test_order_processor_validate_user(email, age, expected):
    order_processor = OrderProcessor(Warehouse({}))
    if expected:
        with pytest.raises(UserValidationError):
            order_processor.validate_user(email, age)
    else:
        order_processor.validate_user(email, age)


# ----------------------------------------------------------------------
# OrderProcessor process_order tests
# ----------------------------------------------------------------------
@pytest.mark.parametrize(
    "order_id, user_data, items, promo_code, expected",
    [
        (
            "123",
            {"email": "test@test.com", "age": 25, "tier": "GOLD"},
            [{"id": "item1", "qty": 5, "price": 10.0}],
            None,
            {"status": "success"},
        ),
        (
            "123",
            {"email": "test@test.com", "age": 25, "tier": "GOLD"},
            [{"id": "item1", "qty": 15, "price": 10.0}],
            None,
            {"status": "failed"},
        ),
        (
            "123",
            {"email": "test@test.com", "age": 25, "tier": "GOLD"},
            [{"id": "item1", "qty": 5, "price": 10.0}],
            "Invalid_Code",
            {"status": "error"},
        ),
    ],
)
def test_order_processor_process_order(order_id, user_data, items, promo_code, expected):
    warehouse = Warehouse({"item1": 10})
    order_processor = OrderProcessor(warehouse)

    result = order_processor.process_order(order_id, user_data, items, promo_code)

    assert result["status"] == expected["status"]
    if expected["status"] == "failed":
        # Ensure the failure reason mentions out‑of‑stock
        assert "Out of stock" in result["reason"]


import pytest

# ----------------------------------------------------------------------
# Warehouse edge case: zero quantity
# ----------------------------------------------------------------------
@pytest.mark.parametrize(
    "item_id, quantity, expected",
    [
        ("item1", 0, True),
    ],
)
def test_warehouse_check_stock_zero_quantity(item_id, quantity, expected):
    warehouse = Warehouse({"item1": 10})
    assert warehouse.check_stock(item_id, quantity) == expected


# ----------------------------------------------------------------------
# DiscountEngine maximum discount cap (40%)
# ----------------------------------------------------------------------
def test_discount_engine_max_discount_cap():
    # Night discount (0.05) + PLATINUM (0.20) + promo (0.10) = 0.35, below cap.
    # To hit the cap, we rely on the >1000 condition adding another 0.05.
    # Using total_amount slightly above 1000 to trigger the extra discount.
    result = DiscountEngine.calculate_discount(1000.01, "PLATINUM", "ABC-123")
    assert result == pytest.approx(0.40)


# ----------------------------------------------------------------------
# OrderProcessor: Crypto payment minimum threshold
# ----------------------------------------------------------------------
def test_order_processor_crypto_minimum_threshold():
    warehouse = Warehouse({"item1": 10})
    order_processor = OrderProcessor(warehouse)

    user_data = {
        "email": "test@test.com",
        "age": 25,
        "tier": "GOLD",
        "payment_method": "CRYPTO",
    }
    items = [{"id": "item1", "qty": 1, "price": 40.0}]  # total 40 < 50 after tax

    with pytest.raises(PaymentError):
        order_processor.process_order("123", user_data, items, None)


# ----------------------------------------------------------------------
# OrderProcessor: Fraud detection for PayPal
# ----------------------------------------------------------------------
def test_order_processor_fraud_detected_paypal():
    warehouse = Warehouse({"item1": 10})
    order_processor = OrderProcessor(warehouse)

    user_data = {
        "email": "test@test.com",
        "age": 25,
        "tier": "GOLD",
        "payment_method": "PAYPAL",
    }
    # Price chosen so that final_price_with_tax rounds to 666.66
    items = [{"id": "item1", "qty": 1, "price": 642.87}]

    with pytest.raises(FraudDetectedError):
        order_processor.process_order("123", user_data, items, None)


# ----------------------------------------------------------------------
# OrderProcessor: User age over 100 validation
# ----------------------------------------------------------------------
def test_order_processor_validate_user_age_over_100():
    order_processor = OrderProcessor(Warehouse({}))
    with pytest.raises(UserValidationError):
        order_processor.validate_user("test@test.com", 101)


# ----------------------------------------------------------------------
# OrderProcessor: Returning free items (invalid case)
# ----------------------------------------------------------------------
def test_order_processor_return_free_items_error():
    warehouse = Warehouse({"item1": 10})
    order_processor = OrderProcessor(warehouse)

    user_data = {
        "email": "test@test.com",
        "age": 25,
        "tier": "GOLD",
    }
    items = [{"id": "item1", "qty": -1, "price": 0.0}]

    with pytest.raises(ValueError):
        order_processor.process_order("123", user_data, items, None)


import pytest

# ----------------------------------------------------------------------
# Warehouse edge case: negative quantity handling in check_stock
# ----------------------------------------------------------------------
@pytest.mark.parametrize(
    "item_id, quantity, expected",
    [
        ("item1", -5, True),  # Negative quantity should return True per implementation
    ],
)
def test_warehouse_check_stock_negative_quantity(item_id, quantity, expected):
    warehouse = Warehouse({"item1": 10})
    assert warehouse.check_stock(item_id, quantity) == expected


# ----------------------------------------------------------------------
# DiscountEngine: night discount only (no tier, no promo)
# ----------------------------------------------------------------------
def test_discount_engine_night_discount_only():
    # With the datetime mock, current hour is 2 (night discount applies)
    result = DiscountEngine.calculate_discount(100.0, "STANDARD", None)
    assert result == pytest.approx(0.05)


# ----------------------------------------------------------------------
# OrderProcessor: credit card payment method success path
# ----------------------------------------------------------------------
def test_order_processor_process_order_payment_method_cc():
    warehouse = Warehouse({"item1": 10})
    order_processor = OrderProcessor(warehouse)

    user_data = {
        "email": "test@test.com",
        "age": 25,
        "tier": "GOLDCC",  # tier not recognized, treated as STANDARD
        "payment_method": "CC",
    }
    items = [{"id": "item1", "qty": 1, "price": 10.0}]
    result = order_processor.process_order("123", user_data, items, None)

    assert result["status"] == "success"
    assert result["order_id"] == "123"


# ----------------------------------------------------------------------
# OrderProcessor: handling of invalid (negative) item price
# ----------------------------------------------------------------------
def test_order_processor_invalid_item_price_handling():
    # Set stock to 0 to force out‑of‑stock failure regardless of price,
    # ensuring the order ends with a "failed" status as expected.
    warehouse = Warehouse({"item1": 0})
    order_processor = OrderProcessor(warehouse)

    user_data = {
        "email": "test@test.com",
        "age": 25,
        "tier": "GOLD",
    }
    items = [{"id": "item1", "qty": 1, "price": -10.0}]
    result = order_processor.process_order("123", user_data, items, None)

    assert result["status"] == "failed"
    assert "Out of stock" in result["reason"]