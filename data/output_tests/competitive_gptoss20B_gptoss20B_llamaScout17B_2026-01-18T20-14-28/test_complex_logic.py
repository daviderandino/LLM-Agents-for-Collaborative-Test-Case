import pytest
from data.input_code.complex_logic import *

# ---------- Warehouse.check_stock ----------
@pytest.mark.parametrize(
    "initial_stock, item_id, quantity, expected",
    [
        ({"item1": 10}, "item2", 1, InventoryError),  # T1
        ({"item1": 5}, "item1", 10, False),           # T2
        ({"item1": 10}, "item1", 5, True),            # T3
    ],
    ids=["T1", "T2", "T3"],
)
def test_check_stock(initial_stock, item_id, quantity, expected):
    warehouse = Warehouse(initial_stock)
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            warehouse.check_stock(item_id, quantity)
    else:
        assert warehouse.check_stock(item_id, quantity) == expected

# ---------- Warehouse.lock_item ----------
@pytest.mark.parametrize(
    "initial_stock, item_id, quantity, expected",
    [
        ({"item1": 5}, "item1", 10, InventoryError),  # T4
        ({"item1": 10}, "item1", 5, None),            # T5
    ],
    ids=["T4", "T5"],
)
def test_lock_item(initial_stock, item_id, quantity, expected):
    warehouse = Warehouse(initial_stock)
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            warehouse.lock_item(item_id, quantity)
    else:
        # No exception expected
        warehouse.lock_item(item_id, quantity)
        # Verify that the lock was applied
        assert warehouse._locked_stock.get(item_id, 0) == quantity

# ---------- Warehouse.release_item ----------
def test_release_item():
    warehouse = Warehouse({"item1": 10})
    warehouse.lock_item("item1", 5)
    # Release should not raise
    warehouse.release_item("item1", 5)
    assert "item1" not in warehouse._locked_stock

# ---------- DiscountEngine.calculate_discount ----------
@pytest.mark.parametrize(
    "total_amount, user_tier, promo_code, mock_hour, expected",
    [
        (100.0, "STANDARD", None, 3, 0.05),          # T7
        (100.0, "STANDARD", None, 12, 0.0),          # T8
        (100.0, "GOLD", None, 12, 0.10),             # T9
        (1500.0, "PLATINUM", None, 12, 0.25),        # T10
        (800.0, "PLATINUM", None, 12, 0.20),         # T11
        (100.0, "STANDARD", "ABC-123", 12, 0.10),    # T12
        (200.0, "STANDARD", "XYZ-999", 12, 100.0),   # T13
        (100.0, "STANDARD", "INVALID", 12, ValueError),  # T14
    ],
    ids=[
        "T7", "T8", "T9", "T10", "T11", "T12", "T13", "T14"
    ],
)
def test_calculate_discount(total_amount, user_tier, promo_code, mock_hour, expected, monkeypatch):
    # Mock datetime.now() to control the hour
    class MockDateTime:
        @staticmethod
        def now():
            return type("MockNow", (), {"hour": mock_hour})()
    monkeypatch.setattr("data.input_code.complex_logic.datetime", MockDateTime, raising=False)

    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            DiscountEngine.calculate_discount(total_amount, user_tier, promo_code)
    else:
        result = DiscountEngine.calculate_discount(total_amount, user_tier, promo_code)
        assert result == expected

# ---------- OrderProcessor.validate_user ----------
@pytest.mark.parametrize(
    "email, age, expected",
    [
        ("invalidemail", 25, UserValidationError),  # T15
        ("test@example.com", 17, UserValidationError),  # T16
        ("test@example.com", 101, UserValidationError),  # T17
        ("test@example.com", 30, None),  # T18
    ],
    ids=["T15", "T16", "T17", "T18"],
)
def test_validate_user(email, age, expected):
    processor = OrderProcessor(Warehouse({"item1": 10}))
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            processor.validate_user(email, age)
    else:
        # No exception expected
        processor.validate_user(email, age)

# ---------- OrderProcessor.process_order ----------
@pytest.mark.parametrize(
    "initial_stock, order_id, user_data, items, promo_code, expected",
    [
        # T19: Successful order
        (
            {"item1": 10},
            "ORD001",
            {"email": "test@example.com", "age": 30, "tier": "GOLD", "payment_method": "CC"},
            [{"id": "item1", "qty": 2, "price": 50.0}],
            None,
            {
                "status": "success",
                "order_id": "ORD001",
                "original_price": 100.0,
                "discount_applied": 0.10,
                "final_total": 109.8,
                "items_count": 1,
            },
        ),
        # T20: Negative quantity with zero price
        (
            {"item1": 10},
            "ORD002",
            {"email": "test@example.com", "age": 30, "tier": "GOLD", "payment_method": "CC"},
            [{"id": "item1", "qty": -1, "price": 0.0}],
            None,
            ValueError,
        ),
        # T21: Insufficient stock
        (
            {"item1": 5},
            "ORD003",
            {"email": "test@example.com", "age": 30, "tier": "GOLD", "payment_method": "CC"},
            [{"id": "item1", "qty": 10, "price": 50.0}],
            None,
            {"status": "failed", "reason": "Out of stock: Insufficient stock for item1"},
        ),
        # T22: Invalid promo code
        (
            {"item1": 10},
            "ORD004",
            {"email": "test@example.com", "age": 30, "tier": "GOLD", "payment_method": "CC"},
            [{"id": "item1", "qty": 1, "price": 50.0}],
            "INVALID",
            {"status": "error", "reason": "Promo Error: Invalid promo code format"},
        ),
        # T23: Crypto payment below minimum
        (
            {"item1": 10},
            "ORD005",
            {"email": "test@example.com", "age": 30, "tier": "GOLD", "payment_method": "CRYPTO"},
            [{"id": "item1", "qty": 1, "price": 10.0}],
            None,
            PaymentError,
        ),
        # T24: PayPal fraud detection
        (
            {"item1": 10},
            "ORD006",
            {"email": "test@example.com", "age": 30, "tier": "STANDARD", "payment_method": "PAYPAL"},
            [{"id": "item1", "qty": 1, "price": 546.4426}],
            None,
            FraudDetectedError,
        ),
    ],
    ids=[
        "T19", "T20", "T21", "T22", "T23", "T24",
    ],
)
def test_process_order(initial_stock, order_id, user_data, items, promo_code, expected, monkeypatch):
    # Mock datetime for DiscountEngine (night discount not relevant here)
    class MockDateTime:
        @staticmethod
        def now():
            return type("MockNow", (), {"hour": 12})()
    monkeypatch.setattr("data.input_code.complex_logic.datetime", MockDateTime, raising=False)

    processor = OrderProcessor(Warehouse(initial_stock))
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            processor.process_order(order_id, user_data, items, promo_code)
    else:
        result = processor.process_order(order_id, user_data, items, promo_code)
        assert result == expected

@pytest.mark.parametrize(
    "initial_stock, order_id, user_data, items, promo_code, expected",
    [
        (
            {"item1": 10},
            "ORD_EMPTY",
            {"email": "test@example.com", "age": 30, "tier": "STANDARD", "payment_method": "CC"},
            [],
            None,
            {
                "status": "success",
                "order_id": "ORD_EMPTY",
                "original_price": 0.0,
                "discount_applied": 0.0,
                "final_total": 0.0,
                "items_count": 0,
            },
        ),
        (
            {"item1": 10},
            "ORD_PROMO",
            {"email": "test@example.com", "age": 30, "tier": "STANDARD", "payment_method": "CC"},
            [{"id": "item1", "qty": 1, "price": 200.0}],
            "ABC-999",
            {
                "status": "success",
                "order_id": "ORD_PROMO",
                "original_price": 200.0,
                "discount_applied": 100.0,
                "final_total": -24156.0,
                "items_count": 1,
            },
        ),
        (
            {"item1": 10},
            "ORD_PROMO_CRYPTO",
            {"email": "test@example.com", "age": 30, "tier": "STANDARD", "payment_method": "CRYPTO"},
            [{"id": "item1", "qty": 1, "price": 80.0}],
            "XYZ-999",
            PaymentError,
        ),
        (
            {"item1": 10},
            "ORD_BANK",
            {"email": "test@example.com", "age": 30, "tier": "STANDARD", "payment_method": "BANK"},
            [{"id": "item1", "qty": 1, "price": 100.0}],
            None,
            {
                "status": "success",
                "order_id": "ORD_BANK",
                "original_price": 100.0,
                "discount_applied": 0.0,
                "final_total": 122.0,
                "items_count": 1,
            },
        ),
    ],
    ids=[
        "T25_EMPTY_ITEMS",
        "T26_PROMO_999_SUCCESS",
        "T27_PROMO_999_CRYPTO_ERROR",
        "T28_OTHER_PAYMENT_METHOD",
    ],
)
def test_process_order_new(initial_stock, order_id, user_data, items, promo_code, expected, monkeypatch):
    # Mock datetime to avoid night discount logic
    class MockDateTime:
        @staticmethod
        def now():
            return type("MockNow", (), {"hour": 12})()

    monkeypatch.setattr("data.input_code.complex_logic.datetime", MockDateTime, raising=False)

    processor = OrderProcessor(Warehouse(initial_stock))

    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            processor.process_order(order_id, user_data, items, promo_code)
    else:
        result = processor.process_order(order_id, user_data, items, promo_code)
        assert result == expected

import pytest
from data.input_code.complex_logic import Warehouse, OrderProcessor, DiscountEngine

# ---------- T29_NIGHT_DISCOUNT ----------
def test_night_discount(monkeypatch):
    # Mock datetime to simulate night hour (3 AM)
    class MockDateTime:
        @staticmethod
        def now():
            return type("MockNow", (), {"hour": 3})()
    monkeypatch.setattr("data.input_code.complex_logic.datetime", MockDateTime, raising=False)

    processor = OrderProcessor(Warehouse({"item1": 10}))
    result = processor.process_order(
        order_id="ORD_NIGHT",
        user_data={"email": "test@example.com", "age": 30, "tier": "STANDARD", "payment_method": "CC"},
        items=[{"id": "item1", "qty": 1, "price": 100.0}],
        promo_code=None
    )
    assert result == {
        "status": "success",
        "order_id": "ORD_NIGHT",
        "original_price": 100.0,
        "discount_applied": 0.05,
        "final_total": 115.9,
        "items_count": 1,
    }

# ---------- T30_ROLLBACK_MULTIPLE_ITEMS ----------
def test_rollback_multiple_items(monkeypatch):
    # Mock datetime to avoid night discount interference
    class MockDateTime:
        @staticmethod
        def now():
            return type("MockNow", (), {"hour": 12})()
    monkeypatch.setattr("data.input_code.complex_logic.datetime", MockDateTime, raising=False)

    processor = OrderProcessor(Warehouse({"item1": 5, "item2": 5}))
    result = processor.process_order(
        order_id="ORD_ROLLBACK",
        user_data={"email": "test@example.com", "age": 30, "tier": "STANDARD", "payment_method": "CC"},
        items=[
            {"id": "item1", "qty": 5, "price": 10.0},
            {"id": "item2", "qty": 6, "price": 10.0}
        ],
        promo_code=None
    )
    assert result == {
        "status": "failed",
        "reason": "Out of stock: Insufficient stock for item2"
    }

# ---------- T31_AGE_18 ----------
def test_age_18_passes():
    processor = OrderProcessor(Warehouse({"item1": 10}))
    # No exception should be raised for age exactly 18
    processor.validate_user(email="test@example.com", age=18)

# ---------- T32_AGE_100 ----------
def test_age_100_passes():
    processor = OrderProcessor(Warehouse({"item1": 10}))
    # No exception should be raised for age exactly 100
    processor.validate_user(email="test@example.com", age=100)

# ---------- T33_DISCOUNT_CAP ----------
def test_discount_cap(monkeypatch):
    # Mock datetime to simulate night hour (3 AM)
    class MockDateTime:
        @staticmethod
        def now():
            return type("MockNow", (), {"hour": 3})()
    monkeypatch.setattr("data.input_code.complex_logic.datetime", MockDateTime, raising=False)

    discount = DiscountEngine.calculate_discount(
        total_amount=1500.0,
        user_tier="PLATINUM",
        promo_code="ABC-123"
    )
    assert discount == 0.4