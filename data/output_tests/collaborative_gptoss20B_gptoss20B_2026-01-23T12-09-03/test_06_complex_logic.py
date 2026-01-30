import pytest
from data.input_code.06_complex_logic import *
import data.input_code.06_complex_logic as mod

# Helper to mock datetime.now() in the module
def mock_datetime_now(monkeypatch, hour):
    class DummyDateTime:
        @classmethod
        def now(cls):
            return DummyDateTime()
        @property
        def hour(self):
            return hour
    # Replace the datetime class in the module with DummyDateTime
    monkeypatch.setattr(mod, 'datetime', DummyDateTime)

# ----------------- Warehouse Tests -----------------
def test_warehouse_check_stock_item_not_found():
    warehouse = Warehouse(initial_stock={"A": 10})
    with pytest.raises(InventoryError):
        warehouse.check_stock("B", 1)

def test_warehouse_check_stock_insufficient():
    warehouse = Warehouse(initial_stock={"A": 5})
    # check_stock should return False, not raise
    assert warehouse.check_stock("A", 6) is False

def test_warehouse_check_stock_sufficient():
    warehouse = Warehouse(initial_stock={"A": 5})
    assert warehouse.check_stock("A", 3) is True

def test_warehouse_lock_item_success(monkeypatch):
    warehouse = Warehouse(initial_stock={"A": 5})
    mock_datetime_now(monkeypatch, 10)  # not needed but keep consistency
    # No exception should be raised
    warehouse.lock_item("A", 3)
    assert warehouse._locked_stock.get("A") == 3

def test_warehouse_lock_item_insufficient(monkeypatch):
    warehouse = Warehouse(initial_stock={"A": 5})
    mock_datetime_now(monkeypatch, 10)
    with pytest.raises(InventoryError):
        warehouse.lock_item("A", 6)

def test_warehouse_release_item_removes_key(monkeypatch):
    warehouse = Warehouse(initial_stock={"A": 5})
    mock_datetime_now(monkeypatch, 10)
    warehouse.lock_item("A", 3)
    warehouse.release_item("A", 3)
    assert "A" not in warehouse._locked_stock

# ----------------- DiscountEngine Tests -----------------
@pytest.mark.parametrize(
    "total_amount,user_tier,promo_code,expected_hour,expected",
    [
        (500.0, "GOLD", None, 3, 0.15),   # night hour + GOLD
        (1500.0, "PLATINUM", None, 10, 0.25),  # day + PLATINUM + >1000
        (800.0, "PLATINUM", None, 10, 0.20),   # day + PLATINUM + <=1000
        (200.0, "STANDARD", "ABC-123", 10, 0.10),  # valid promo
        (500.0, "STANDARD", "XYZ-999", 10, 250.0),  # promo ending 999
    ]
)
def test_discount_engine_success(monkeypatch, total_amount, user_tier, promo_code, expected_hour, expected):
    mock_datetime_now(monkeypatch, expected_hour)
    result = DiscountEngine.calculate_discount(total_amount, user_tier, promo_code)
    assert result == pytest.approx(expected)

@pytest.mark.parametrize(
    "total_amount,user_tier,promo_code,expected_hour,expected_exception",
    [
        (200.0, "STANDARD", "AB-123", 10, ValueError),  # invalid promo format
    ]
)
def test_discount_engine_invalid_promo(monkeypatch, total_amount, user_tier, promo_code, expected_hour, expected_exception):
    mock_datetime_now(monkeypatch, expected_hour)
    with pytest.raises(expected_exception):
        DiscountEngine.calculate_discount(total_amount, user_tier, promo_code)

# ----------------- OrderProcessor.validate_user Tests -----------------
@pytest.mark.parametrize(
    "email,age,expected_exception",
    [
        ("test@test", 30, UserValidationError),  # invalid email
        ("user@example.com", 17, UserValidationError),  # age below 18
        ("user@example.com", 101, UserValidationError),  # age above 100
    ]
)
def test_validate_user_errors(email, age, expected_exception):
    processor = OrderProcessor(Warehouse(initial_stock={}))
    with pytest.raises(expected_exception):
        processor.validate_user(email, age)

def test_validate_user_success():
    processor = OrderProcessor(Warehouse(initial_stock={}))
    # No exception should be raised
    processor.validate_user("user@example.com", 30)

# ----------------- OrderProcessor.process_order Tests -----------------
@pytest.fixture
def warehouse_success():
    return Warehouse(initial_stock={"A": 10, "B": 10, "C": 10, "D": 10, "E": 2, "F": 3, "G": 5})

def test_process_order_success(monkeypatch, warehouse_success):
    mock_datetime_now(monkeypatch, 10)
    processor = OrderProcessor(warehouse_success)
    result = processor.process_order(
        order_id="ORD001",
        user_data={
            "email": "user@example.com",
            "age": 30,
            "tier": "GOLD",
            "payment_method": "CC"
        },
        items=[{"id": "A", "qty": 2, "price": 100.0}],
        promo_code=None
    )
    expected = {
        "status": "success",
        "order_id": "ORD001",
        "original_price": 200.0,
        "discount_applied": 0.1,
        "final_total": 219.6,
        "items_count": 1
    }
    assert result == expected

def test_process_order_fraud_detected(monkeypatch, warehouse_success):
    mock_datetime_now(monkeypatch, 10)
    processor = OrderProcessor(warehouse_success)
    # Use a price that makes final_total == 666.66 after rounding
    price = 546.4426  # 546.4426 * 1.22 = 666.659972 -> rounded to 666.66
    with pytest.raises(FraudDetectedError):
        processor.process_order(
            order_id="ORD002",
            user_data={
                "email": "user@example.com",
                "age": 30,
                "tier": "STANDARD",
                "payment_method": "PAYPAL"
            },
            items=[{"id": "B", "qty": 1, "price": price}],
            promo_code=None
        )

def test_process_order_crypto_payment_error(monkeypatch, warehouse_success):
    mock_datetime_now(monkeypatch, 10)
    processor = OrderProcessor(warehouse_success)
    with pytest.raises(PaymentError):
        processor.process_order(
            order_id="ORD003",
            user_data={
                "email": "user@example.com",
                "age": 30,
                "tier": "STANDARD",
                "payment_method": "CRYPTO"
            },
            items=[{"id": "C", "qty": 3, "price": 10.0}],
            promo_code=None
        )

def test_process_order_hidden_division_error(monkeypatch, warehouse_success):
    mock_datetime_now(monkeypatch, 10)
    processor = OrderProcessor(warehouse_success)
    with pytest.raises(ValueError):
        processor.process_order(
            order_id="ORD004",
            user_data={
                "email": "user@example.com",
                "age": 30,
                "tier": "STANDARD",
                "payment_method": "CC"
            },
            items=[{"id": "D", "qty": -1, "price": 0.0}],
            promo_code=None
        )

def test_process_order_inventory_error(monkeypatch, warehouse_success):
    mock_datetime_now(monkeypatch, 10)
    processor = OrderProcessor(warehouse_success)
    result = processor.process_order(
        order_id="ORD005",
        user_data={
            "email": "user@example.com",
            "age": 30,
            "tier": "STANDARD",
            "payment_method": "CC"
        },
        items=[
            {"id": "E", "qty": 2, "price": 50.0},
            {"id": "F", "qty": 5, "price": 20.0}
        ],
        promo_code=None
    )
    expected = {
        "status": "failed",
        "reason": "Out of stock: Insufficient stock for F"
    }
    assert result == expected

def test_process_order_invalid_promo(monkeypatch, warehouse_success):
    mock_datetime_now(monkeypatch, 10)
    processor = OrderProcessor(warehouse_success)
    result = processor.process_order(
        order_id="ORD006",
        user_data={
            "email": "user@example.com",
            "age": 30,
            "tier": "STANDARD",
            "payment_method": "CC"
        },
        items=[{"id": "G", "qty": 1, "price": 100.0}],
        promo_code="AB-123"
    )
    expected = {
        "status": "error",
        "reason": "Promo Error: Invalid promo code format"
    }
    assert result == expected