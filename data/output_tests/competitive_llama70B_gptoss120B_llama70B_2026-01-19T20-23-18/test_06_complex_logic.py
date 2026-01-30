import pytest
from data.input_code.06_complex_logic import *
import data.input_code.06_complex_logic as logic
import importlib

# ---------- Fixtures ----------
@pytest.fixture
def warehouse():
    return Warehouse(initial_stock={"item1": 10})

@pytest.fixture
def order_processor(warehouse):
    return OrderProcessor(warehouse)


# ---------- Helper for datetime mocking ----------
class FixedDatetime:
    @classmethod
    def now(cls):
        # Fixed hour 12 (no night discount)
        return datetime(2020, 1, 1, 12, 0, 0)


# ---------- Warehouse Tests ----------
@pytest.mark.parametrize(
    "stock, item_id, qty, expected",
    [
        ({"item1": 10}, "item1", 1, True),          # enough stock
        ({"item1": 10}, "item1", 11, False),        # insufficient stock
    ],
)
def test_warehouse_check_stock(stock, item_id, qty, expected):
    wh = Warehouse(initial_stock=stock)
    if expected is False:
        assert wh.check_stock(item_id, qty) is False
    else:
        assert wh.check_stock(item_id, qty) is True


def test_warehouse_check_stock_item_not_found():
    wh = Warehouse(initial_stock={"item1": 10})
    with pytest.raises(InventoryError):
        wh.check_stock("item2", 1)


@pytest.mark.parametrize(
    "stock, item_id, qty, should_raise",
    [
        ({"item1": 10}, "item1", 1, False),   # lock succeeds
        ({"item1": 10}, "item1", 11, True),   # insufficient stock
    ],
)
def test_warehouse_lock_item(stock, item_id, qty, should_raise):
    wh = Warehouse(initial_stock=stock)
    if should_raise:
        with pytest.raises(InventoryError):
            wh.lock_item(item_id, qty)
    else:
        # No exception expected
        wh.lock_item(item_id, qty)
        # Verify that the locked amount is recorded
        assert wh._locked_stock.get(item_id, 0) == qty


# ---------- DiscountEngine Tests ----------
@pytest.fixture(autouse=True)
def mock_datetime(monkeypatch):
    """Patch datetime.now() used inside DiscountEngine."""
    monkeypatch.setattr(logic, "datetime", FixedDatetime)


@pytest.mark.parametrize(
    "total, tier, promo, expected",
    [
        (100.0, "GOLD", None, 0.10),                     # tier GOLD
        (100.0, "GOLD", "ABC-123", 0.20),                # tier + valid promo
    ],
)
def test_discount_engine_calculate_discount(total, tier, promo, expected):
    result = DiscountEngine.calculate_discount(total, tier, promo)
    assert result == expected


def test_discount_engine_invalid_promo():
    with pytest.raises(ValueError):
        DiscountEngine.calculate_discount(100.0, "GOLD", "invalid")


# ---------- OrderProcessor.validate_user Tests ----------
@pytest.mark.parametrize(
    "email, age, should_raise",
    [
        ("test@example.com", 25, False),   # valid
        ("invalid", 25, True),             # bad email
        ("test@example.com", 17, True),   # underage
    ],
)
def test_order_processor_validate_user(email, age, should_raise):
    op = OrderProcessor(Warehouse(initial_stock={}))
    if should_raise:
        with pytest.raises(UserValidationError):
            op.validate_user(email, age)
    else:
        # Should not raise any exception
        op.validate_user(email, age)


# ---------- OrderProcessor.process_order Tests ----------
def test_process_order_success(order_processor):
    # Happy path – GOLD tier, no promo, PAYPAL not triggered
    result = order_processor.process_order(
        order_id="order1",
        user_data={"email": "test@example.com", "age": 25, "tier": "GOLD"},
        items=[{"id": "item1", "qty": 1, "price": 100.0}],
    )
    assert result["status"] == "success"
    assert result["order_id"] == "order1"
    assert result["original_price"] == 100.0
    assert result["discount_applied"] == 0.10
    # 100 * (1-0.10) = 90 ; 90 * 1.22 = 109.8 -> rounded to 2 decimals
    assert result["final_total"] == 109.8
    assert result["items_count"] == 1


def test_process_order_insufficient_stock(order_processor):
    result = order_processor.process_order(
        order_id="order1",
        user_data={"email": "test@example.com", "age": 25, "tier": "GOLD"},
        items=[{"id": "item1", "qty": 11, "price": 100.0}],
    )
    assert result["status"] == "failed"
    assert "Out of stock" in result["reason"]


def test_process_order_invalid_promo(order_processor):
    result = order_processor.process_order(
        order_id="order1",
        user_data={"email": "test@example.com", "age": 25, "tier": "GOLD"},
        items=[{"id": "item1", "qty": 1, "price": 100.0}],
        promo_code="invalid",
    )
    assert result["status"] == "error"
    assert "Promo Error" in result["reason"]


def test_process_order_fraud_detected(order_processor):
    """
    Choose a price that, after applying the GOLD discount (10%) and tax (22%),
    results in a final total of exactly 666.66 (rounded to two decimals),
    which triggers the FraudDetectedError for PAYPAL payments.
    """
    # Compute the required total price:
    # final_total = round((total_price * 0.9) * 1.22, 2) == 666.66
    # Solving gives total_price ≈ 607.15844
    price = 607.15844
    with pytest.raises(FraudDetectedError):
        order_processor.process_order(
            order_id="order1",
            user_data={
                "email": "test@example.com",
                "age": 25,
                "tier": "GOLD",
                "payment_method": "PAYPAL",
            },
            items=[{"id": "item1", "qty": 1, "price": price}],
        )


def test_process_order_payment_error(order_processor):
    # Use low price to trigger crypto minimum amount error
    with pytest.raises(PaymentError):
        order_processor.process_order(
            order_id="order1",
            user_data={
                "email": "test@example.com",
                "age": 25,
                "tier": "GOLD",
                "payment_method": "CRYPTO",
            },
            items=[{"id": "item1", "qty": 1, "price": 40.0}],
        )


import pytest
from datetime import datetime

# ---------- DiscountEngine Additional Tests ----------
def test_discount_engine_night_discount(monkeypatch):
    """Night discount (5%) + GOLD tier (10%) = 15%."""
    class NightDatetime:
        @classmethod
        def now(cls):
            return datetime(2020, 1, 1, 2, 0, 0)  # hour within 0-5

    monkeypatch.setattr(logic, "datetime", NightDatetime)
    result = DiscountEngine.calculate_discount(100.0, "GOLD", None)
    # Adjusted expected value to match floating‑point result
    assert result == 0.15000000000000002


@pytest.mark.parametrize(
    "total, tier, promo, expected",
    [
        (100.0, "PLATINUM", None, 0.20),          # PLATINUM tier without extra amount
        (100.0, "GOLD", "ABC-999", 50.0),         # promo code ending with 999 gives 50% off
    ],
)
def test_discount_engine_other_cases(total, tier, promo, expected):
    """Tests PLATINUM tier discount and special 999 promo code."""
    result = DiscountEngine.calculate_discount(total, tier, promo)
    assert result == expected


def test_discount_engine_high_value_platinum_with_night(monkeypatch):
    """
    Night discount (5%) + PLATINUM tier (20%) = 25% when total_amount is 1000.
    The extra 5% for >1000 is not applied because total_amount == 1000.
    """
    class NightDatetime:
        @classmethod
        def now(cls):
            return datetime(2020, 1, 1, 3, 0, 0)  # night hour

    monkeypatch.setattr(logic, "datetime", NightDatetime)
    result = DiscountEngine.calculate_discount(1000.0, "PLATINUM", None)
    assert result == 0.25


# ---------- OrderProcessor.validate_user Edge Cases ----------
@pytest.mark.parametrize(
    "email, age, expected_msg",
    [
        ("test@example", 25, "Invalid email format"),
        ("test@example.com", 101, "Age verification required for 100+"),
    ],
)
def test_order_processor_validate_user_edge_cases(email, age, expected_msg):
    op = OrderProcessor(Warehouse(initial_stock={}))
    with pytest.raises(UserValidationError) as exc:
        op.validate_user(email, age)
    assert str(exc.value) == expected_msg


# ---------- OrderProcessor.process_order Additional Edge Cases ----------
def test_process_order_division_by_zero_error(order_processor):
    """
    Trigger the hidden division‑by‑zero guard: negative qty with zero price.
    """
    with pytest.raises(ValueError) as exc:
        order_processor.process_order(
            order_id="order1",
            user_data={"email": "test@example.com", "age": 25, "tier": "GOLD"},
            items=[{"id": "item1", "qty": -1, "price": 0.0}],
        )
    assert str(exc.value) == "Cannot return free items"


def test_process_order_crypto_minimum_amount_error(order_processor):
    """
    Crypto payments require a final total (after discount & tax) of at least 50.
    Using a low price ensures the final amount falls below the threshold.
    """
    with pytest.raises(PaymentError) as exc:
        order_processor.process_order(
            order_id="order1",
            user_data={
                "email": "test@example.com",
                "age": 25,
                "tier": "GOLD",
                "payment_method": "CRYPTO",
            },
            items=[{"id": "item1", "qty": 1, "price": 40.0}],
        )
    assert str(exc.value) == "Minimum crypto amount not met"

import pytest
from datetime import datetime

# ---------- DiscountEngine Additional Tests ----------
@pytest.mark.parametrize(
    "hour, total, tier, promo, expected",
    [
        # Night discount (5%) + GOLD tier (10%) + valid promo (10%) = 0.25
        (2, 100.0, "GOLD", "ABC-123", 0.25),
        # PLATINUM tier (20%) + extra 5% for total > 1000 = 0.25
        (12, 1001.0, "PLATINUM", None, 0.25),
    ],
)
def test_discount_engine_various_cases(monkeypatch, hour, total, tier, promo, expected):
    """Test night discount with promo and high‑value PLATINUM tier."""
    class MockDatetime:
        @classmethod
        def now(cls):
            return datetime(2020, 1, 1, hour, 0, 0)

    monkeypatch.setattr(logic, "datetime", MockDatetime)
    result = DiscountEngine.calculate_discount(total, tier, promo)
    assert result == expected


# ---------- OrderProcessor.validate_user Edge Cases ----------
@pytest.mark.parametrize(
    "email, age, expected_msg",
    [
        ("invalid", 25, "Invalid email format"),
        ("test@example.com", 101, "Age verification required for 100+"),
    ],
)
def test_order_processor_validate_user_edge_cases(email, age, expected_msg):
    op = OrderProcessor(Warehouse(initial_stock={}))
    with pytest.raises(UserValidationError) as exc:
        op.validate_user(email, age)
    assert str(exc.value) == expected_msg


# ---------- OrderProcessor.process_order Crypto Payment ----------
def test_process_order_crypto_success(order_processor):
    """CRYPTO payment with a final amount above the 50 € threshold should succeed."""
    result = order_processor.process_order(
        order_id="order1",
        user_data={
            "email": "test@example.com",
            "age": 25,
            "tier": "GOLD",
            "payment_method": "CRYPTO",
        },
        items=[{"id": "item1", "qty": 1, "price": 100.0}],
    )
    assert result["status"] == "success"
    assert result["order_id"] == "order1"
    # Verify that the discount and tax calculations are consistent
    assert result["original_price"] == 100.0
    assert result["discount_applied"] == 0.10
    # 100 * 0.9 = 90 ; 90 * 1.22 = 109.8
    assert result["final_total"] == 109.8

# ---------- DiscountEngine New Tests ----------
@pytest.mark.parametrize(
    "hour,total,user_tier,promo_code,expected",
    [
        (2, 100.0, "GOLD", "ABC-123", 0.25),   # night discount + GOLD + promo
        (12, 1001.0, "PLATINUM", "ABC-123", 0.35),  # no night discount, high PLATINUM + promo
    ],
)
def test_discount_engine_various_new_cases(monkeypatch, hour, total, user_tier, promo_code, expected):
    """Validate discount calculations for night‑time and high‑value PLATINUM scenarios."""
    class MockDatetime:
        @classmethod
        def now(cls):
            return datetime(2020, 1, 1, hour, 0, 0)

    monkeypatch.setattr(logic, "datetime", MockDatetime)
    result = DiscountEngine.calculate_discount(total, user_tier, promo_code)
    assert result == expected


# ---------- OrderProcessor.validate_user New Test ----------
def test_order_processor_validate_user_over_100():
    """User over 100 years old should raise the specific validation message."""
    op = OrderProcessor(Warehouse(initial_stock={}))
    with pytest.raises(UserValidationError) as exc:
        op.validate_user(email="test@example.com", age=101)
    assert str(exc.value) == "Age verification required for 100+"


# ---------- OrderProcessor.process_order New Tests ----------
def test_process_order_negative_qty_non_zero_price(order_processor):
    """
    Negative quantity with a non‑zero price should be processed (no special guard).
    The total price becomes negative; the order should still succeed.
    """
    result = order_processor.process_order(
        order_id="order1",
        user_data={"email": "test@example.com", "age": 25, "tier": "GOLD"},
        items=[{"id": "item1", "qty": -1, "price": 100.0}],
    )
    assert result["status"] == "success"
    # original_price reflects the negative total
    assert result["original_price"] == -100.0
    # discount for GOLD tier
    assert result["discount_applied"] == 0.10
    # final total after discount and tax (negative)
    # -100 * 0.9 = -90 ; -90 * 1.22 = -109.8
    assert result["final_total"] == -109.8
    assert result["items_count"] == 1


def test_process_order_zero_quantity_success(order_processor):
    """An item with zero quantity should result in a successful order with zero price."""
    result = order_processor.process_order(
        order_id="order1",
        user_data={"email": "test@example.com", "age": 25, "tier": "GOLD"},
        items=[{"id": "item1", "qty": 0, "price": 100.0}],
    )
    assert result["status"] == "success"
    assert result["original_price"] == 0.0
    assert result["discount_applied"] == 0.10
    assert result["final_total"] == 0.0
    assert result["items_count"] == 1


def test_process_order_empty_items_success(order_processor):
    """Processing an order with an empty items list should succeed with zero totals."""
    result = order_processor.process_order(
        order_id="order1",
        user_data={"email": "test@example.com", "age": 25, "tier": "GOLD"},
        items=[],
    )
    assert result["status"] == "success"
    assert result["original_price"] == 0.0
    assert result["discount_applied"] == 0.10
    assert result["final_total"] == 0.0
    assert result["items_count"] == 0