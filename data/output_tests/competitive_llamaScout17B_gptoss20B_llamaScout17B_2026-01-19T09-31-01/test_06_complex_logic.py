import pytest
from data.input_code.06_complex_logic import *
from datetime import datetime

# ------------------------------------------------------------------
# Warehouse tests
# ------------------------------------------------------------------
@pytest.fixture
def warehouse():
    return Warehouse(initial_stock={"item1": 10})

@pytest.mark.parametrize(
    "item_id, quantity, expected",
    [
        ("item1", 5, True),
        ("item1", 15, False),
    ],
)
def test_warehouse_check_stock(warehouse, item_id, quantity, expected):
    assert warehouse.check_stock(item_id, quantity) == expected

def test_warehouse_lock_and_release(warehouse):
    # Locking should succeed
    warehouse.lock_item("item1", 5)
    assert warehouse._locked_stock["item1"] == 5
    # Releasing should remove the lock
    warehouse.release_item("item1", 5)
    assert "item1" not in warehouse._locked_stock

# ------------------------------------------------------------------
# DiscountEngine tests
# ------------------------------------------------------------------
def test_discount_engine_night(monkeypatch):
    # Mock datetime.now() to return hour 3 (night)
    class DummyDateTime:
        @staticmethod
        def now():
            return datetime(2023, 1, 1, 3, 0, 0)
    monkeypatch.setattr("data.input_code.06_complex_logic.datetime", DummyDateTime)
    discount = DiscountEngine.calculate_discount(100.0, "STANDARD", None)
    assert discount == 0.05  # only night discount

def test_discount_engine_gold():
    discount = DiscountEngine.calculate_discount(100.0, "GOLD", None)
    assert discount == 0.10

def test_discount_engine_platinum():
    # Expected discount depends on current hour (night discount may apply)
    base_discount = 0.20
    if datetime.now().hour < 6:
        base_discount += 0.05
    # total_amount is 1000.0, not > 1000.00, so no extra 0.05
    expected = base_discount
    discount = DiscountEngine.calculate_discount(1000.0, "PLATINUM", None)
    assert discount == expected

def test_discount_engine_promo_code():
    # Expected discount depends on current hour (night discount may apply)
    base_discount = 0.10  # promo code discount
    if datetime.now().hour < 6:
        base_discount += 0.05  # night discount
    expected = base_discount
    discount = DiscountEngine.calculate_discount(100.0, "STANDARD", "ABC-123")
    assert discount == expected

def test_discount_engine_promo_code_999():
    discount = DiscountEngine.calculate_discount(100.0, "STANDARD", "ABC-999")
    assert discount == 50.0  # 50% off immediate

def test_discount_engine_invalid_promo():
    with pytest.raises(ValueError):
        DiscountEngine.calculate_discount(100.0, "STANDARD", "invalid_promo_code")

# ------------------------------------------------------------------
# OrderProcessor tests
# ------------------------------------------------------------------
@pytest.fixture
def order_processor(warehouse):
    return OrderProcessor(warehouse)

def test_validate_user_success(order_processor):
    # Should not raise
    order_processor.validate_user("test@test.com", 25)

def test_validate_user_invalid_email(order_processor):
    with pytest.raises(UserValidationError):
        order_processor.validate_user("invalid_email", 25)

def test_validate_user_invalid_age(order_processor):
    with pytest.raises(UserValidationError):
        order_processor.validate_user("test@test.com", 15)

def test_process_order_success(order_processor):
    result = order_processor.process_order(
        order_id="123",
        user_data={"email": "test@test.com", "age": 25, "tier": "STANDARD"},
        items=[{"id": "item1", "qty": 5, "price": 10.0}],
        promo_code=None,
    )
    assert result["status"] == "success"
    assert result["items_count"] == 1

def test_process_order_inventory_failure(order_processor):
    result = order_processor.process_order(
        order_id="123",
        user_data={"email": "test@test.com", "age": 25, "tier": "STANDARD"},
        items=[{"id": "item1", "qty": 15, "price": 10.0}],
        promo_code=None,
    )
    assert result["status"] == "failed"

def test_process_order_promo_error(order_processor):
    result = order_processor.process_order(
        order_id="123",
        user_data={"email": "test@test.com", "age": 25, "tier": "STANDARD"},
        items=[{"id": "item1", "qty": 5, "price": 10.0}],
        promo_code="invalid_promo_code",
    )
    assert result["status"] == "error"

def test_process_order_payment_error(order_processor, monkeypatch):
    # Ensure no night discount is applied
    class DummyDateTime:
        @staticmethod
        def now():
            return datetime(2023, 1, 1, 12, 0, 0)
    monkeypatch.setattr("data.input_code.06_complex_logic.datetime", DummyDateTime)
    # Monkeypatch tax_rate to 0 to make final_total equal to total_price
    monkeypatch.setattr(order_processor, "tax_rate", 0.0)
    # Items that sum to 666.66
    items = [{"id": "item1", "qty": 2, "price": 333.33}]
    with pytest.raises(FraudDetectedError):
        order_processor.process_order(
            order_id="123",
            user_data={
                "email": "test@test.com",
                "age": 25,
                "tier": "STANDARD",
                "payment_method": "PAYPAL",
            },
            items=items,
            promo_code=None,
        )

# ------------------------------------------------------------------
# New tests for missing edge cases
# ------------------------------------------------------------------

def test_warehouse_check_stock_missing_item(warehouse):
    with pytest.raises(InventoryError) as excinfo:
        warehouse.check_stock("item2", 5)
    assert str(excinfo.value) == "Item item2 not found in warehouse."

def test_discount_engine_cap(monkeypatch):
    # Force night hour to trigger the 5% night discount
    class DummyDateTime:
        @staticmethod
        def now():
            return datetime(2023, 1, 1, 3, 0, 0)
    monkeypatch.setattr("data.input_code.06_complex_logic.datetime", DummyDateTime)

    discount = DiscountEngine.calculate_discount(
        total_amount=1000.0,
        user_tier="PLATINUM",
        promo_code="ABC-123",
    )
    # Night (0.05) + Platinum (0.20) + Promo (0.10) = 0.35, capped at 0.40
    assert discount == 0.35

def test_process_order_crypto_min(order_processor):
    with pytest.raises(PaymentError) as excinfo:
        order_processor.process_order(
            order_id="123",
            user_data={
                "email": "test@test.com",
                "age": 25,
                "tier": "STANDARD",
                "payment_method": "CRYPTO",
            },
            items=[{"id": "item1", "qty": 1, "price": 10.0}],
            promo_code=None,
        )
    assert str(excinfo.value) == "Minimum crypto amount not met"

def test_validate_user_age_100(order_processor):
    with pytest.raises(UserValidationError) as excinfo:
        order_processor.validate_user("test@test.com", 101)
    assert str(excinfo.value) == "Age verification required for 100+"

def test_process_order_item_return(order_processor):
    with pytest.raises(ValueError) as excinfo:
        order_processor.process_order(
            order_id="123",
            user_data={"email": "test@test.com", "age": 25, "tier": "STANDARD"},
            items=[{"id": "item1", "qty": -1, "price": 0.0}],
            promo_code=None,
        )
    assert str(excinfo.value) == "Cannot return free items"

import pytest
from datetime import datetime

# ------------------------------------------------------------------
# New tests for missing edge cases
# ------------------------------------------------------------------

def test_warehouse_release_item_negative(warehouse):
    """
    Releasing a negative quantity should not raise an error and should leave
    the locked stock unchanged if the item was not previously locked.
    """
    # Ensure the item is not locked initially
    assert "item1" not in warehouse._locked_stock
    # Release a negative quantity
    warehouse.release_item("item1", -5)
    # No exception should be raised and the locked stock remains unchanged
    assert "item1" not in warehouse._locked_stock


def test_discount_engine_zero_amount(monkeypatch):
    """
    Discount calculation with a zero total amount and no promo code should
    return 0.0, regardless of the current hour.  We monkeypatch datetime
    to avoid the night discount.
    """
    class DummyDateTime:
        @staticmethod
        def now():
            return datetime(2023, 1, 1, 12, 0, 0)  # 12:00 PM

    monkeypatch.setattr("data.input_code.06_complex_logic.datetime", DummyDateTime)
    discount = DiscountEngine.calculate_discount(0.0, "STANDARD", None)
    assert discount == 0.0


def test_process_order_unknown_payment_method(order_processor):
    """
    An unknown payment method is not explicitly handled in the code, so the
    order should still succeed with the default payment flow.
    """
    result = order_processor.process_order(
        order_id="123",
        user_data={
            "email": "test@test.com",
            "age": 25,
            "tier": "STANDARD",
            "payment_method": "UNKNOWN",
        },
        items=[{"id": "item1", "qty": 1, "price": 10.0}],
        promo_code=None,
    )
    assert result["status"] == "success"
    assert result["order_id"] == "123"
    assert result["items_count"] == 1


def test_process_order_item_price_zero(order_processor):
    """
    An item with a price of zero should be processed successfully, resulting
    in a final total of zero after tax.
    """
    result = order_processor.process_order(
        order_id="123",
        user_data={"email": "test@test.com", "age": 25, "tier": "STANDARD"},
        items=[{"id": "item1", "qty": 1, "price": 0.0}],
        promo_code=None,
    )
    assert result["status"] == "success"
    assert result["final_total"] == 0.0
    assert result["items_count"] == 1


def test_process_order_user_tier_unknown(order_processor):
    """
    An unknown user tier should not affect the order processing; the
    discount logic simply ignores unrecognized tiers.
    """
    result = order_processor.process_order(
        order_id="123",
        user_data={"email": "test@test.com", "age": 25, "tier": "UNKNOWN"},
        items=[{"id": "item1", "qty": 1, "price": 10.0}],
        promo_code=None,
    )
    assert result["status"] == "success"
    assert result["items_count"] == 1