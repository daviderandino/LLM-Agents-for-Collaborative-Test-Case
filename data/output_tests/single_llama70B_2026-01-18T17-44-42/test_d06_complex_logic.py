import pytest
from unittest.mock import patch, MagicMock
from data.input_code.d06_complex_logic import Warehouse, DiscountEngine, OrderProcessor, InventoryError, PaymentError, FraudDetectedError, UserValidationError

@pytest.fixture
def warehouse():
    return Warehouse({"item1": 10, "item2": 20})

@pytest.fixture
def order_processor(warehouse):
    return OrderProcessor(warehouse)

def test_warehouse_check_stock(warehouse):
    assert warehouse.check_stock("item1", 5) == True
    assert warehouse.check_stock("item1", 15) == False
    with pytest.raises(InventoryError):
        warehouse.check_stock("item3", 5)

def test_warehouse_lock_item(warehouse):
    warehouse.lock_item("item1", 5)
    assert warehouse._locked_stock["item1"] == 5
    with pytest.raises(InventoryError):
        warehouse.lock_item("item1", 10)

def test_warehouse_release_item(warehouse):
    warehouse.lock_item("item1", 5)
    warehouse.release_item("item1", 3)
    assert warehouse._locked_stock["item1"] == 2
    warehouse.release_item("item1", 2)
    assert "item1" not in warehouse._locked_stock


def test_order_processor_validate_user(order_processor):
    with pytest.raises(UserValidationError):
        order_processor.validate_user("invalid-email", 18)
    with pytest.raises(UserValidationError):
        order_processor.validate_user("test@example.com", 17)
    with pytest.raises(UserValidationError):
        order_processor.validate_user("test@example.com", 101)


def test_order_processor_process_order_out_of_stock(order_processor):
    user_data = {"email": "test@example.com", "age": 18, "tier": "GOLD", "payment_method": "CC"}
    items = [{"id": "item1", "qty": 15, "price": 10.0}, {"id": "item2", "qty": 3, "price": 20.0}]
    result = order_processor.process_order("order1", user_data, items)
    assert result["status"] == "failed"
    assert "Out of stock" in result["reason"]

def test_order_processor_process_order_invalid_promo_code(order_processor):
    user_data = {"email": "test@example.com", "age": 18, "tier": "GOLD", "payment_method": "CC"}
    items = [{"id": "item1", "qty": 2, "price": 10.0}, {"id": "item2", "qty": 3, "price": 20.0}]
    result = order_processor.process_order("order1", user_data, items, "invalid-promo-code")
    assert result["status"] == "error"
    assert "Promo Error" in result["reason"]


def test_order_processor_process_order_payment_error(order_processor):
    user_data = {"email": "test@example.com", "age": 18, "tier": "GOLD", "payment_method": "CRYPTO"}
    items = [{"id": "item1", "qty": 2, "price": 10.0}, {"id": "item2", "qty": 3, "price": 20.0}]
    with patch.object(DiscountEngine, "calculate_discount", return_value=0.50):
        with pytest.raises(PaymentError):
            order_processor.process_order("order1", user_data, items)

def test_order_processor_process_order_user_validation_error(order_processor):
    user_data = {"email": "invalid-email", "age": 18, "tier": "GOLD", "payment_method": "CC"}
    items = [{"id": "item1", "qty": 2, "price": 10.0}, {"id": "item2", "qty": 3, "price": 20.0}]
    with pytest.raises(UserValidationError):
        order_processor.process_order("order1", user_data, items)