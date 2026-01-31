import pytest
import builtins
from unittest.mock import patch

from data.input_code.d06_complex_logic import (
    InventoryError,
    PaymentError,
    FraudDetectedError,
    UserValidationError,
    Warehouse,
    DiscountEngine,
    OrderProcessor,
)


# Helper to create a Warehouse with given stock
@pytest.fixture
def warehouse():
    return Warehouse(initial_stock={"item1": 10, "item2": 5, "item3": 1})


# -------------------- DiscountEngine Tests --------------------
















# -------------------- Warehouse Tests --------------------


def test_warehouse_check_stock_success():
    wh = Warehouse({"A": 5})
    assert wh.check_stock("A", 3) is True


def test_warehouse_check_stock_missing_item():
    wh = Warehouse({})
    with pytest.raises(InventoryError):
        wh.check_stock("missing", 1)


def test_warehouse_lock_and_release():
    wh = Warehouse({"B": 4})
    wh.lock_item("B", 2)
    assert wh._locked_stock["B"] == 2
    wh.release_item("B", 2)
    assert "B" not in wh._locked_stock


def test_warehouse_insufficient_stock_raises():
    wh = Warehouse({"C": 1})
    with pytest.raises(InventoryError):
        wh.lock_item("C", 2)


# -------------------- OrderProcessor Tests --------------------


def test_order_success_basic(warehouse):
    op = OrderProcessor(warehouse)
    user = {"email": "test@example.com", "age": 30, "tier": "GOLD", "payment_method": "CC"}
    items = [{"id": "item1", "qty": 2, "price": 50.0}]
    result = op.process_order("ORD123", user, items)
    assert result["status"] == "success"
    assert result["order_id"] == "ORD123"
    assert result["original_price"] == 100.0
    # Gold tier 0.10 discount, no night, no promo
    expected_discount = 0.10
    assert result["discount_applied"] == expected_discount
    # final = 100 * (1-0.10) * 1.22 = 109.8 rounded
    assert result["final_total"] == round(100 * (1 - expected_discount) * 1.22, 2)
    assert result["items_count"] == 1


def test_order_invalid_email_raises():
    op = OrderProcessor(Warehouse({}))
    user = {"email": "invalid-email", "age": 25}
    items = []
    with pytest.raises(UserValidationError):
        op.process_order("ORDX", user, items)


def test_order_underage_raises():
    op = OrderProcessor(Warehouse({}))
    user = {"email": "test@example.com", "age": 16}
    items = []
    with pytest.raises(UserValidationError):
        op.process_order("ORDX", user, items)


def test_order_overage_raises():
    op = OrderProcessor(Warehouse({}))
    user = {"email": "test@example.com", "age": 101}
    items = []
    with pytest.raises(UserValidationError):
        op.process_order("ORDX", user, items)


def test_order_insufficient_stock_handling(warehouse):
    op = OrderProcessor(warehouse)
    user = {"email": "test@example.com", "age": 30}
    items = [
        {"id": "item1", "qty": 5, "price": 10.0},
        {"id": "item2", "qty": 10, "price": 5.0},  # exceeds stock (only 5 available)
    ]
    result = op.process_order("ORDFAIL", user, items)
    assert result["status"] == "failed"
    assert "Out of stock" in result["reason"]
    # Ensure no locked stock remains
    assert warehouse._locked_stock == {}






def test_order_crypto_min_amount_error(warehouse):
    op = OrderProcessor(warehouse)
    user = {"email": "test@example.com", "age": 30, "payment_method": "CRYPTO"}
    items = [{"id": "item1", "qty": 1, "price": 30.0}]
    with pytest.raises(PaymentError):
        op.process_order("ORDCRYPTO", user, items)


def test_order_negative_qty_zero_price_raises():
    op = OrderProcessor(Warehouse({"itemX": 10}))
    user = {"email": "test@example.com", "age": 30}
    items = [{"id": "itemX", "qty": -1, "price": 0.0}]
    with pytest.raises(ValueError):
        op.process_order("ORDNEG", user, items)


