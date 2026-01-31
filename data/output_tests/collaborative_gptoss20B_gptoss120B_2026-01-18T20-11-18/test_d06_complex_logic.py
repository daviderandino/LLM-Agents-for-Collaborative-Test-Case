import pytest
from data.input_code.d06_complex_logic import *
from unittest.mock import MagicMock

# ------------------------------------------------------------------
# Warehouse tests
# ------------------------------------------------------------------
def test_T_WAREHOUSE_MISSING_ITEM():
    warehouse = Warehouse(initial_stock={"A": 10})
    with pytest.raises(InventoryError):
        warehouse.check_stock("B", 1)

def test_T_WAREHOUSE_INSUFFICIENT():
    warehouse = Warehouse(initial_stock={"A": 5})
    with pytest.raises(InventoryError):
        warehouse.lock_item("A", 6)

def test_T_WAREHOUSE_LOCK_RELEASE():
    warehouse = Warehouse(initial_stock={"A": 10})
    warehouse.lock_item("A", 3)
    assert warehouse._locked_stock.get("A") == 3
    warehouse.release_item("A", 3)
    assert warehouse._locked_stock == {}

# ------------------------------------------------------------------
# DiscountEngine tests
# ------------------------------------------------------------------
def mock_datetime(hour):
    class MockDateTime:
        @classmethod
        def now(cls):
            mock_now = MagicMock()
            mock_now.hour = hour
            return mock_now
    return MockDateTime

def test_T_DISCOUNT_NIGHT_OWL(monkeypatch):
    monkeypatch.setattr("data.input_code.06_complex_logic.datetime", mock_datetime(2))
    discount = DiscountEngine.calculate_discount(100.0, "STANDARD", None)
    assert discount == 0.05

def test_T_DISCOUNT_PLATINUM_HIGH(monkeypatch):
    monkeypatch.setattr("data.input_code.06_complex_logic.datetime", mock_datetime(12))
    discount = DiscountEngine.calculate_discount(1500.0, "PLATINUM", None)
    assert discount == 0.25

def test_T_DISCOUNT_PLATINUM_LOW(monkeypatch):
    monkeypatch.setattr("data.input_code.06_complex_logic.datetime", mock_datetime(12))
    discount = DiscountEngine.calculate_discount(800.0, "PLATINUM", None)
    assert discount == 0.20

def test_T_DISCOUNT_PROMO_VALID(monkeypatch):
    monkeypatch.setattr("data.input_code.06_complex_logic.datetime", mock_datetime(12))
    discount = DiscountEngine.calculate_discount(500.0, "GOLD", "ABC-123")
    # The discount should be 0.20 (10% tier + 10% promo), capped at 0.40
    assert discount == 0.20

def test_T_DISCOUNT_PROMO_SUPER(monkeypatch):
    monkeypatch.setattr("data.input_code.06_complex_logic.datetime", mock_datetime(12))
    discount = DiscountEngine.calculate_discount(200.0, "STANDARD", "XYZ-999")
    assert discount == 100.0

def test_T_DISCOUNT_PROMO_INVALID(monkeypatch):
    monkeypatch.setattr("data.input_code.06_complex_logic.datetime", mock_datetime(12))
    with pytest.raises(ValueError):
        DiscountEngine.calculate_discount(100.0, "STANDARD", "bad_code")

# ------------------------------------------------------------------
# OrderProcessor validation tests
# ------------------------------------------------------------------
def test_T_ORDER_VALIDATION_EMAIL():
    processor = OrderProcessor(Warehouse({}))
    with pytest.raises(UserValidationError):
        processor.validate_user("invalid-email", 30)

def test_T_ORDER_VALIDATION_AGE_UNDER():
    processor = OrderProcessor(Warehouse({}))
    with pytest.raises(UserValidationError):
        processor.validate_user("test@example.com", 16)

def test_T_ORDER_VALIDATION_AGE_OVER():
    processor = OrderProcessor(Warehouse({}))
    with pytest.raises(UserValidationError):
        processor.validate_user("elder@example.com", 101)

# ------------------------------------------------------------------
# OrderProcessor process_order tests
# ------------------------------------------------------------------
def test_T_ORDER_SUCCESS_STANDARD():
    warehouse = Warehouse({"A": 5})
    processor = OrderProcessor(warehouse)
    result = processor.process_order(
        order_id="ORD123",
        user_data={
            "email": "buyer@example.com",
            "age": 30,
            "tier": "GOLD",
            "payment_method": "CC"
        },
        items=[{"id": "A", "qty": 2, "price": 50.0}],
        promo_code=None
    )
    assert result["status"] == "success"
    assert result["order_id"] == "ORD123"
    assert result["original_price"] == 100.0
    assert result["discount_applied"] == 0.10
    assert result["items_count"] == 1

def test_T_ORDER_INVENTORY_FAIL():
    warehouse = Warehouse({"B": 1, "C": 3})
    processor = OrderProcessor(warehouse)
    result = processor.process_order(
        order_id="ORD124",
        user_data={
            "email": "buyer2@example.com",
            "age": 25,
            "tier": "STANDARD",
            "payment_method": "CC"
        },
        items=[
            {"id": "B", "qty": 1, "price": 20.0},
            {"id": "C", "qty": 5, "price": 10.0}
        ],
        promo_code=None
    )
    assert result["status"] == "failed"
    assert result["reason"] == "Out of stock: Insufficient stock for C"

def test_T_ORDER_PROMO_ERROR():
    warehouse = Warehouse({"D": 10})
    processor = OrderProcessor(warehouse)
    result = processor.process_order(
        order_id="ORD125",
        user_data={
            "email": "buyer3@example.com",
            "age": 40,
            "tier": "STANDARD",
            "payment_method": "CC"
        },
        items=[{"id": "D", "qty": 1, "price": 30.0}],
        promo_code="bad-promo"
    )
    assert result["status"] == "error"
    assert result["reason"] == "Promo Error: Invalid promo code format"

def test_T_ORDER_PAYPAL_FRAUD():
    warehouse = Warehouse({"E": 5})
    processor = OrderProcessor(warehouse)
    # Adjust price so that final_total equals 666.66 to trigger fraud
    # final_total = round(total_price * (1 + tax_rate), 2)
    # Solve for total_price: total_price * 1.22 = 666.66 => total_price = 666.66 / 1.22
    total_price_needed = 666.66 / 1.22
    with pytest.raises(FraudDetectedError) as exc:
        processor.process_order(
            order_id="ORD126",
            user_data={
                "email": "fraud@example.com",
                "age": 35,
                "tier": "STANDARD",
                "payment_method": "PAYPAL"
            },
            items=[{"id": "E", "qty": 1, "price": total_price_needed}],
            promo_code=None
        )
    assert str(exc.value) == "Suspicious transaction amount"

def test_T_ORDER_CRYPTO_MIN():
    warehouse = Warehouse({"F": 10})
    processor = OrderProcessor(warehouse)
    with pytest.raises(PaymentError):
        processor.process_order(
            order_id="ORD127",
            user_data={
                "email": "crypto@example.com",
                "age": 28,
                "tier": "STANDARD",
                "payment_method": "CRYPTO"
            },
            items=[{"id": "F", "qty": 1, "price": 40.0}],
            promo_code=None
        )

def test_T_ORDER_RETURN_FREE_ERROR():
    warehouse = Warehouse({"G": 5})
    processor = OrderProcessor(warehouse)
    with pytest.raises(ValueError):
        processor.process_order(
            order_id="ORD128",
            user_data={
                "email": "return@example.com",
                "age": 45,
                "tier": "STANDARD",
                "payment_method": "CC"
            },
            items=[{"id": "G", "qty": -1, "price": 0.0}],
            promo_code=None
        )