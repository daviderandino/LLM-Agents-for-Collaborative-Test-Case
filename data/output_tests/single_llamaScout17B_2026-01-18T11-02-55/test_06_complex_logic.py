import pytest
from datetime import datetime
from data.input_code.06_complex_logic import Warehouse, DiscountEngine, OrderProcessor, InventoryError, PaymentError, FraudDetectedError, UserValidationError

# --- Test Setup ---
@pytest.fixture
def warehouse():
    return Warehouse({"item1": 100, "item2": 50})

@pytest.fixture
def order_processor(warehouse):
    return OrderProcessor(warehouse)

# --- Test Warehouse ---
def test_warehouse_init():
    warehouse = Warehouse({"item1": 100})
    assert warehouse._stock == {"item1": 100}
    assert warehouse._locked_stock == {}

def test_warehouse_check_stock(warehouse):
    assert warehouse.check_stock("item1", 50) == True
    assert warehouse.check_stock("item1", 100) == True
    assert warehouse.check_stock("item1", 150) == False
    with pytest.raises(InventoryError):
        warehouse.check_stock("item3", 50)

def test_warehouse_lock_item(warehouse):
    warehouse.lock_item("item1", 50)
    assert warehouse._locked_stock == {"item1": 50}
    with pytest.raises(InventoryError):
        warehouse.lock_item("item1", 60)

def test_warehouse_release_item(warehouse):
    warehouse.lock_item("item1", 50)
    warehouse.release_item("item1", 20)
    assert warehouse._locked_stock == {"item1": 30}

# --- Test DiscountEngine ---
def test_discount_engine_calculate_discount():
    assert DiscountEngine.calculate_discount(100, "STANDARD") == 0
    assert DiscountEngine.calculate_discount(100, "GOLD") == 0.10
    assert DiscountEngine.calculate_discount(100, "PLATINUM") == 0.20
    assert DiscountEngine.calculate_discount(1500, "PLATINUM") == 0.25

def test_discount_engine_promo_code():
    assert DiscountEngine.calculate_discount(100, "STANDARD", "ABC-123") == 0.10
    assert DiscountEngine.calculate_discount(100, "STANDARD", "ABC-999") == 50
    with pytest.raises(ValueError):
        DiscountEngine.calculate_discount(100, "STANDARD", "invalid")

# --- Test OrderProcessor ---
def test_order_processor_validate_user(order_processor):
    order_processor.validate_user("test@example.com", 25)
    with pytest.raises(UserValidationError):
        order_processor.validate_user("invalid_email", 25)
    with pytest.raises(UserValidationError):
        order_processor.validate_user("test@example.com", 15)
    with pytest.raises(UserValidationError):
        order_processor.validate_user("test@example.com", 150)

def test_order_processor_process_order(order_processor):
    order_data = {
        "email": "test@example.com",
        "age": 25,
        "tier": "GOLD"
    }
    items = [
        {"id": "item1", "qty": 2, "price": 10.0},
        {"id": "item2", "qty": 1, "price": 20.0}
    ]
    result = order_processor.process_order("order1", order_data, items)
    assert result["status"] == "success"

def test_order_processor_process_order_insufficient_stock(order_processor):
    order_data = {
        "email": "test@example.com",
        "age": 25,
        "tier": "GOLD"
    }
    items = [
        {"id": "item1", "qty": 200, "price": 10.0}
    ]
    result = order_processor.process_order("order1", order_data, items)
    assert result["status"] == "failed"


def test_order_processor_process_order_payment_error(order_processor):
    order_data = {
        "email": "test@example.com",
        "age": 25,
        "tier": "GOLD",
        "payment_method": "CRYPTO"
    }
    items = [
        {"id": "item1", "qty": 2, "price": 10.0}
    ]
    with pytest.raises(PaymentError):
        order_processor.process_order("order1", order_data, items)

def test_order_processor_process_order_user_validation_error(order_processor):
    order_data = {
        "email": "invalid_email",
        "age": 15
    }
    items = [
        {"id": "item1", "qty": 2, "price": 10.0}
    ]
    with pytest.raises(UserValidationError):
        order_processor.process_order("order1", order_data, items)


