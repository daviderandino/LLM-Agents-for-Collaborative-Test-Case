import pytest
from unittest.mock import patch
from data.input_code.complex_logic import *

# ------------------- Warehouse Tests ------------------- #

@pytest.mark.parametrize(
    "initial_stock,item_id,quantity,expected",
    [
        ({"item1": 5}, "item2", 1, InventoryError),   # Item not found
        ({"item1": 5}, "item1", 6, False),            # Insufficient stock returns False
        ({"item1": 5}, "item1", 5, True),             # Sufficient stock
    ],
)
def test_warehouse_check_stock(initial_stock, item_id, quantity, expected):
    wh = Warehouse(initial_stock)
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            wh.check_stock(item_id, quantity)
    else:
        assert wh.check_stock(item_id, quantity) is expected


def test_warehouse_lock_item_success():
    wh = Warehouse({"item1": 5})
    wh.lock_item("item1", 3)
    assert wh._locked_stock["item1"] == 3


def test_warehouse_lock_item_insufficient():
    wh = Warehouse({"item1": 5})
    with pytest.raises(InventoryError):
        wh.lock_item("item1", 6)


def test_warehouse_release_item_reduce_to_zero():
    wh = Warehouse({"item1": 5})
    wh.lock_item("item1", 3)
    wh.release_item("item1", 3)
    assert "item1" not in wh._locked_stock


def test_warehouse_release_item_reduce_below_zero():
    wh = Warehouse({"item1": 5})
    wh.lock_item("item1", 3)
    wh.release_item("item1", 1)
    assert wh._locked_stock["item1"] == 2


# ------------------- DiscountEngine Tests ------------------- #

def mock_datetime(hour):
    class MockedDatetime:
        @classmethod
        def now(cls):
            return cls()
        @property
        def hour(self):
            return hour
    return MockedDatetime

@pytest.mark.parametrize(
    "hour,total_amount,user_tier,promo_code,expected",
    [
        (7, 100.0, "STANDARD", None, 0.0),                 # No discounts
        (3, 100.0, "STANDARD", None, 0.05),                # Night only
        (7, 100.0, "GOLD", None, 0.10),                    # Gold tier
        (7, 100.0, "PLATINUM", None, 0.20),                # Platinum tier
        (7, 1500.0, "PLATINUM", None, 0.25),               # Platinum high amount
        (7, 100.0, "STANDARD", "ABC-123", 0.10),           # Valid promo
        (7, 100.0, "STANDARD", "XYZ-999", 50.0),           # Promo ending 999 (returns amount)
        (7, 100.0, "STANDARD", "abc-123", ValueError),    # Invalid promo format
        (3, 1500.0, "PLATINUM", "ABC-123", 0.40),          # Cap at 40%
        (3, 1500.0, "PLATINUM", "XYZ-999", 750.0),         # Promo 999 overrides cap (returns amount)
    ],
)
def test_discount_engine_calculate_discount(hour, total_amount, user_tier, promo_code, expected):
    with patch('data.input_code.complex_logic.datetime', mock_datetime(hour)):
        if isinstance(expected, type) and issubclass(expected, Exception):
            with pytest.raises(expected):
                DiscountEngine.calculate_discount(total_amount, user_tier, promo_code)
        else:
            result = DiscountEngine.calculate_discount(total_amount, user_tier, promo_code)
            assert result == expected


# ------------------- OrderProcessor.validate_user Tests ------------------- #

@pytest.mark.parametrize(
    "email,age,expect_exception",
    [
        ("user@example.com", 18, None),                     # Valid
        ("userexample.com", 18, UserValidationError),      # Invalid email
        ("user@example.com", 17, UserValidationError),     # Underage
        ("user@example.com", 101, UserValidationError),    # Over 100
    ],
)
def test_order_processor_validate_user(email, age, expect_exception):
    op = OrderProcessor(Warehouse({}))
    if expect_exception:
        with pytest.raises(expect_exception):
            op.validate_user(email, age)
    else:
        op.validate_user(email, age)  # should not raise


# ------------------- OrderProcessor.process_order Tests ------------------- #

def test_process_order_happy_path(monkeypatch):
    wh = Warehouse({"item1": 5})
    op = OrderProcessor(wh)

    # Mock DiscountEngine to return 0.10 (10% discount) for simplicity
    monkeypatch.setattr(DiscountEngine, "calculate_discount", lambda total, tier, promo: 0.10)

    result = op.process_order(
        order_id="ORD123",
        user_data={"email": "user@example.com", "age": 25, "tier": "GOLD", "payment_method": "CC"},
        items=[{"id": "item1", "qty": 2, "price": 10.0}],
        promo_code=None,
    )
    assert result == {
        "status": "success",
        "order_id": "ORD123",
        "original_price": 20.0,
        "discount_applied": 0.10,
        "final_total": 21.96,
        "items_count": 1,
    }


def test_process_order_item_not_found():
    wh = Warehouse({})
    op = OrderProcessor(wh)
    result = op.process_order(
        order_id="ORD124",
        user_data={"email": "user@example.com", "age": 25, "tier": "STANDARD", "payment_method": "CC"},
        items=[{"id": "item1", "qty": 1, "price": 10.0}],
        promo_code=None,
    )
    assert result["status"] == "failed"
    assert "Out of stock" in result["reason"]


def test_process_order_insufficient_stock():
    wh = Warehouse({"item1": 1})
    op = OrderProcessor(wh)
    result = op.process_order(
        order_id="ORD125",
        user_data={"email": "user@example.com", "age": 25, "tier": "STANDARD", "payment_method": "CC"},
        items=[{"id": "item1", "qty": 2, "price": 10.0}],
        promo_code=None,
    )
    assert result["status"] == "failed"
    assert "Insufficient stock" in result["reason"]


def test_process_order_invalid_promo(monkeypatch):
    wh = Warehouse({"item1": 5})
    op = OrderProcessor(wh)

    # Ensure DiscountEngine raises ValueError for invalid promo
    def raise_value_error(*args, **kwargs):
        raise ValueError("Invalid promo code format")
    monkeypatch.setattr(DiscountEngine, "calculate_discount", raise_value_error)

    result = op.process_order(
        order_id="ORD126",
        user_data={"email": "user@example.com", "age": 25, "tier": "STANDARD", "payment_method": "CC"},
        items=[{"id": "item1", "qty": 1, "price": 10.0}],
        promo_code="abc-123",
    )
    assert result["status"] == "error"
    assert "Promo Error" in result["reason"]


def test_process_order_div_zero_hidden():
    wh = Warehouse({"item1": 5})
    op = OrderProcessor(wh)
    with pytest.raises(ValueError):
        op.process_order(
            order_id="ORD127",
            user_data={"email": "user@example.com", "age": 25, "tier": "STANDARD", "payment_method": "CC"},
            items=[{"id": "item1", "qty": -1, "price": 0.0}],
            promo_code=None,
        )


def test_process_order_crypto_payment_error():
    wh = Warehouse({"item1": 5})
    op = OrderProcessor(wh)
    with pytest.raises(PaymentError):
        op.process_order(
            order_id="ORD128",
            user_data={"email": "user@example.com", "age": 25, "tier": "STANDARD", "payment_method": "CRYPTO"},
            items=[{"id": "item1", "qty": 1, "price": 10.0}],
            promo_code=None,
        )


def test_process_order_fraud_detected_error():
    wh = Warehouse({"item1": 5})
    op = OrderProcessor(wh)

    # Use a price that after tax rounds to 666.66, triggering FraudDetectedError
    with pytest.raises(FraudDetectedError):
        op.process_order(
            order_id="ORD129",
            user_data={"email": "user@example.com", "age": 25, "tier": "STANDARD", "payment_method": "PAYPAL"},
            items=[{"id": "item1", "qty": 1, "price": 546.44}],
            promo_code=None,
        )


def test_process_order_rounding():
    wh = Warehouse({"item1": 5})
    op = OrderProcessor(wh)

    # No discount (default behavior)
    result = op.process_order(
        order_id="ORD130",
        user_data={"email": "user@example.com", "age": 25, "tier": "STANDARD", "payment_method": "CC"},
        items=[{"id": "item1", "qty": 1, "price": 9.3333}],
        promo_code=None,
    )
    assert result == {
        "status": "success",
        "order_id": "ORD130",
        "original_price": 9.3333,
        "discount_applied": 0.0,
        "final_total": 11.39,
        "items_count": 1,
    }


def test_process_order_promo_999_discount(monkeypatch):
    wh = Warehouse({"item1": 5})
    op = OrderProcessor(wh)

    # Patch DiscountEngine to return 0.5 for promo ending with 999 (correct behavior)
    monkeypatch.setattr(DiscountEngine, "calculate_discount", lambda total, tier, promo: 0.5)

    result = op.process_order(
        order_id="ORD131",
        user_data={"email": "user@example.com", "age": 25, "tier": "STANDARD", "payment_method": "CC"},
        items=[{"id": "item1", "qty": 1, "price": 100.0}],
        promo_code="ABC-999",
    )
    assert result == {
        "status": "success",
        "order_id": "ORD131",
        "original_price": 100.0,
        "discount_applied": 0.5,
        "final_total": 61.0,
        "items_count": 1,
    }