import pytest
from data.input_code.complex_logic import *
import data.input_code.complex_logic as code


# ---------- Warehouse.check_stock ----------
@pytest.mark.parametrize(
    "initial_stock,item_id,quantity,expected",
    [
        ({"A1": 5}, "A1", 3, True),          # stock sufficient
        ({"A1": 5}, "B2", 1, InventoryError),  # item not found
    ],
)
def test_warehouse_check_stock(initial_stock, item_id, quantity, expected):
    wh = Warehouse(initial_stock)
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            wh.check_stock(item_id, quantity)
    else:
        assert wh.check_stock(item_id, quantity) == expected


# ---------- Warehouse.lock_item ----------
def test_warehouse_lock_item_insufficient():
    wh = Warehouse({"A1": 4})
    # pre‑lock 2 items
    wh._locked_stock = {"A1": 2}
    with pytest.raises(InventoryError):
        wh.lock_item("A1", 3)  # would leave only -1 available


# ---------- DiscountEngine.calculate_discount ----------
@pytest.mark.parametrize(
    "total_amount,user_tier,promo_code,mock_hour,expected",
    [
        (200.0, "GOLD", None, 2, 0.15),                     # night owl + GOLD
        (1500.0, "PLATINUM", None, 12, 0.25),               # PLATINUM >1000 adds extra 0.05
        (300.0, "STANDARD", "ABC-123", 14, 0.10),           # valid promo adds 0.10
        (800.0, "GOLD", "XYZ-999", 20, 0.50),               # super promo returns 50% of total
        (100.0, "STANDARD", "bad_code", 10, ValueError),   # malformed promo raises
    ],
)
def test_discount_engine(monkeypatch, total_amount, user_tier, promo_code, mock_hour, expected):
    # mock datetime.now().hour
    class _Now:
        @staticmethod
        def now():
            return type("dt", (), {"hour": mock_hour})()
    monkeypatch.setattr(code, "datetime", _Now)

    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            DiscountEngine.calculate_discount(total_amount, user_tier, promo_code)
    else:
        result = DiscountEngine.calculate_discount(total_amount, user_tier, promo_code)
        # For the super‑promo case the function returns a monetary value, not a percent
        if promo_code == "XYZ-999":
            assert result == total_amount * 0.50
        else:
            # Use approx for floating‑point comparisons
            if isinstance(expected, float):
                assert result == pytest.approx(expected)
            else:
                assert result == expected


# ---------- OrderProcessor.validate_user ----------
@pytest.mark.parametrize(
    "email,age,expected",
    [
        ("invalid_email", 25, UserValidationError),
        ("young@example.com", 16, UserValidationError),
        ("oldtimer@example.com", 101, UserValidationError),
    ],
)
def test_orderprocessor_validate_user(email, age, expected):
    op = OrderProcessor(Warehouse({}))
    with pytest.raises(expected):
        op.validate_user(email, age)


# ---------- OrderProcessor.process_order ----------
def test_orderprocessor_process_order_success(monkeypatch):
    # No time‑dependent discount, so mock any hour
    class _Now:
        @staticmethod
        def now():
            return type("dt", (), {"hour": 12})()
    monkeypatch.setattr(code, "datetime", _Now)

    wh = Warehouse({"P1": 10})
    op = OrderProcessor(wh)
    result = op.process_order(
        order_id="ORD-001",
        user_data={
            "email": "john.doe@example.com",
            "age": 30,
            "tier": "STANDARD",
            "payment_method": "CC",
        },
        items=[{"id": "P1", "qty": 2, "price": 50.0}],
        promo_code=None,
    )
    assert result == {
        "status": "success",
        "order_id": "ORD-001",
        "original_price": 100.0,
        "discount_applied": 0.0,
        "final_total": 122.0,
        "items_count": 1,
    }


def test_orderprocessor_process_order_inventory_failure():
    wh = Warehouse({"P2": 1})
    op = OrderProcessor(wh)
    result = op.process_order(
        order_id="ORD-002",
        user_data={
            "email": "alice@example.com",
            "age": 28,
            "tier": "GOLD",
            "payment_method": "CC",
        },
        items=[{"id": "P2", "qty": 3, "price": 20.0}],
        promo_code=None,
    )
    assert result == {
        "status": "failed",
        "reason": "Out of stock: Insufficient stock for P2",
    }


def test_orderprocessor_process_order_promo_error(monkeypatch):
    # Mock hour to avoid night discount interference
    class _Now:
        @staticmethod
        def now():
            return type("dt", (), {"hour": 12})()
    monkeypatch.setattr(code, "datetime", _Now)

    wh = Warehouse({"P3": 5})
    op = OrderProcessor(wh)
    result = op.process_order(
        order_id="ORD-003",
        user_data={
            "email": "bob@example.com",
            "age": 45,
            "tier": "STANDARD",
            "payment_method": "CC",
        },
        items=[{"id": "P3", "qty": 2, "price": 30.0}],
        promo_code="WRONG-12",
    )
    assert result == {
        "status": "error",
        "reason": "Promo Error: Invalid promo code format",
    }


def test_orderprocessor_process_order_zero_price_negative_qty():
    wh = Warehouse({"P4": 10})
    op = OrderProcessor(wh)
    with pytest.raises(ValueError):
        op.process_order(
            order_id="ORD-004",
            user_data={
                "email": "charlie@example.com",
                "age": 35,
                "tier": "STANDARD",
                "payment_method": "CC",
            },
            items=[{"id": "P4", "qty": -1, "price": 0.0}],
            promo_code=None,
        )


def test_orderprocessor_process_order_fraud_detected(monkeypatch):
    # Set hour to any value; discount not relevant for this edge case
    class _Now:
        @staticmethod
        def now():
            return type("dt", (), {"hour": 15})()
    monkeypatch.setattr(code, "datetime", _Now)

    wh = Warehouse({"P5": 10})
    op = OrderProcessor(wh)
    # Choose a price that yields a final total of 666.66 after tax (rounded)
    with pytest.raises(FraudDetectedError):
        op.process_order(
            order_id="ORD-005",
            user_data={
                "email": "dave@example.com",
                "age": 40,
                "tier": "STANDARD",
                "payment_method": "PAYPAL",
            },
            items=[{"id": "P5", "qty": 1, "price": 546.44}],
            promo_code=None,
        )


def test_orderprocessor_process_order_crypto_too_low(monkeypatch):
    # Mock hour to avoid night discount
    class _Now:
        @staticmethod
        def now():
            return type("dt", (), {"hour": 10})()
    monkeypatch.setattr(code, "datetime", _Now)

    wh = Warehouse({"P6": 5})
    op = OrderProcessor(wh)
    with pytest.raises(PaymentError):
        op.process_order(
            order_id="ORD-006",
            user_data={
                "email": "eve@example.com",
                "age": 29,
                "tier": "STANDARD",
                "payment_method": "CRYPTO",
            },
            items=[{"id": "P6", "qty": 1, "price": 30.0}],
            promo_code=None,
        )