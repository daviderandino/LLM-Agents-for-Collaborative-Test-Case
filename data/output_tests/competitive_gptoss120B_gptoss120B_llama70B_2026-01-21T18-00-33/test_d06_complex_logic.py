import pytest
from data.input_code.d06_complex_logic import *
import data.input_code.06_complex_logic as logic
from datetime import datetime as real_datetime

# ---------- Warehouse Tests ----------
@pytest.mark.parametrize(
    "stock,item_id,quantity,expected_exception",
    [
        ({"itemA": 10}, "missing_item", 1, InventoryError),
        ({"itemB": 5}, "itemB", 10, InventoryError),
    ],
)
def test_warehouse_exceptions(stock, item_id, quantity, expected_exception):
    wh = Warehouse(stock)
    if expected_exception is InventoryError and item_id not in stock:
        with pytest.raises(InventoryError):
            wh.check_stock(item_id, quantity)
    else:
        with pytest.raises(InventoryError):
            wh.lock_item(item_id, quantity)


def test_warehouse_lock_and_release():
    wh = Warehouse({"itemC": 8})
    wh.lock_item("itemC", 3)
    assert wh._locked_stock == {"itemC": 3}
    wh.release_item("itemC", 3)
    assert wh._locked_stock == {}


# ---------- DiscountEngine Tests ----------
@pytest.mark.parametrize(
    "hour,total,user_tier,promo,expected",
    [
        (2, 200.0, "STANDARD", None, 0.05),          # night discount
        (12, 150.0, "GOLD", None, 0.10),             # gold tier
        (14, 1500.0, "PLATINUM", None, 0.25),        # platinum + amount >1000
        (14, 800.0, "PLATINUM", None, 0.20),         # platinum only
        (9, 300.0, "STANDARD", "ABC-123", 0.10),     # valid promo adds 10%
        (9, 400.0, "STANDARD", "XYZ-999", 200.0),    # super promo returns 50% amount
    ],
)
def test_discount_engine(monkeypatch, hour, total, user_tier, promo, expected):
    class MockDateTime:
        @classmethod
        def now(cls):
            return type("dt", (), {"hour": hour})()

    monkeypatch.setattr(logic, "datetime", MockDateTime)

    if isinstance(expected, float) and expected > 1.0:
        # super promo returns a monetary amount, not a percentage
        result = DiscountEngine.calculate_discount(total, user_tier, promo)
        assert result == expected
    else:
        result = DiscountEngine.calculate_discount(total, user_tier, promo)
        assert result == expected


def test_discount_engine_invalid_promo():
    with pytest.raises(ValueError):
        DiscountEngine.calculate_discount(250.0, "STANDARD", "bad-code")


# ---------- OrderProcessor.validate_user Tests ----------
@pytest.mark.parametrize(
    "email,age,expected_exception",
    [
        ("invalid_email", 30, UserValidationError),
        ("test@example.com", 16, UserValidationError),
        ("senior@example.com", 101, UserValidationError),
    ],
)
def test_validate_user_errors(email, age, expected_exception):
    op = OrderProcessor(Warehouse({}))
    with pytest.raises(expected_exception):
        op.validate_user(email, age)


# ---------- OrderProcessor.process_order Tests ----------
def test_order_success_cc(monkeypatch):
    # Mock datetime to a non‑night hour
    class MockDateTime:
        @classmethod
        def now(cls):
            return type("dt", (), {"hour": 10})()

    monkeypatch.setattr(logic, "datetime", MockDateTime)

    wh = Warehouse({"item1": 10})
    processor = OrderProcessor(wh)

    result = processor.process_order(
        order_id="ORD001",
        user_data={
            "email": "buyer@example.com",
            "age": 35,
            "tier": "GOLD",
            "payment_method": "CC",
        },
        items=[{"id": "item1", "qty": 2, "price": 50.0}],
        promo_code=None,
    )

    assert result == {
        "status": "success",
        "order_id": "ORD001",
        "original_price": 100.0,
        "discount_applied": 0.10,
        "final_total": 109.8,
        "items_count": 1,
    }


def test_order_inventory_fail():
    wh = Warehouse({"itemX": 1, "itemY": 5})
    processor = OrderProcessor(wh)

    result = processor.process_order(
        order_id="ORD002",
        user_data={
            "email": "shopper@example.com",
            "age": 28,
            "tier": "STANDARD",
            "payment_method": "CC",
        },
        items=[
            {"id": "itemX", "qty": 1, "price": 20.0},
            {"id": "itemY", "qty": 10, "price": 5.0},
        ],
        promo_code=None,
    )

    assert result["status"] == "failed"
    assert "Out of stock: Insufficient stock for itemY" in result["reason"]


def test_order_promo_invalid():
    wh = Warehouse({"itemZ": 3})
    processor = OrderProcessor(wh)

    result = processor.process_order(
        order_id="ORD003",
        user_data={
            "email": "promo@example.com",
            "age": 45,
            "tier": "STANDARD",
            "payment_method": "CC",
        },
        items=[{"id": "itemZ", "qty": 2, "price": 30.0}],
        promo_code="WRONG-01",
    )

    assert result["status"] == "error"
    assert "Promo Error: Invalid promo code format" in result["reason"]


def test_order_return_free_item():
    wh = Warehouse({"itemFree": 5})
    processor = OrderProcessor(wh)

    with pytest.raises(ValueError):
        processor.process_order(
            order_id="ORD004",
            user_data={
                "email": "returner@example.com",
                "age": 30,
                "tier": "STANDARD",
                "payment_method": "CC",
            },
            items=[{"id": "itemFree", "qty": -1, "price": 0.0}],
            promo_code=None,
        )


def test_order_paypal_fraud(monkeypatch):
    # Mock DiscountEngine to return 0% discount (no discount)
    class MockDiscountEngine:
        @staticmethod
        def calculate_discount(total_amount, user_tier, promo_code=None):
            return 0.0

    monkeypatch.setattr(logic, "DiscountEngine", MockDiscountEngine)

    # Use a price that, after tax (22%), yields exactly 666.66
    # price * 1.22 rounded to 2 decimals = 666.66  => price ≈ 546.44
    wh = Warehouse({"itemA": 10})
    processor = OrderProcessor(wh)

    with pytest.raises(FraudDetectedError):
        processor.process_order(
            order_id="ORD005",
            user_data={
                "email": "fraud@example.com",
                "age": 40,
                "tier": "STANDARD",
                "payment_method": "PAYPAL",
            },
            items=[{"id": "itemA", "qty": 1, "price": 546.44}],
            promo_code=None,
        )


def test_order_crypto_min(monkeypatch):
    # No discount, price 30 -> final with tax = 36.6 (<50) triggers PaymentError
    class MockDateTime:
        @classmethod
        def now(cls):
            return type("dt", (), {"hour": 9})()

    monkeypatch.setattr(logic, "datetime", MockDateTime)

    wh = Warehouse({"itemB": 5})
    processor = OrderProcessor(wh)

    with pytest.raises(PaymentError):
        processor.process_order(
            order_id="ORD006",
            user_data={
                "email": "crypto@example.com",
                "age": 29,
                "tier": "STANDARD",
                "payment_method": "CRYPTO",
            },
            items=[{"id": "itemB", "qty": 1, "price": 30.0}],
            promo_code=None,
        )