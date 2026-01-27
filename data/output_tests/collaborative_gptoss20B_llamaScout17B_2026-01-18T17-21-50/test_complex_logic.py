import pytest
from data.input_code.complex_logic import Warehouse, DiscountEngine, OrderProcessor, InventoryError, PaymentError, FraudDetectedError, UserValidationError
from datetime import datetime
from unittest import mock

# Helper to mock datetime for testing
@pytest.fixture
def mock_datetime():
    with mock.patch('datetime.datetime') as mock_dt:
        yield mock_dt

@pytest.mark.parametrize("initial_stock, expected_stock, expected_locked_stock", [
    ({"item1": 10, "item2": 5}, {"item1": 10, "item2": 5}, {}),
])
def test_warehouse_init(initial_stock, expected_stock, expected_locked_stock):
    warehouse = Warehouse(initial_stock)
    assert warehouse._stock == expected_stock
    assert warehouse._locked_stock == expected_locked_stock

@pytest.mark.parametrize("item, qty, stock, expected", [
    ("item1", 5, {"item1": 10}, True),
    ("item1", 15, {"item1": 10}, False),
])
def test_check_stock(item, qty, stock, expected):
    warehouse = Warehouse(stock)
    assert warehouse.check_stock(item, qty) == expected

@pytest.mark.parametrize("item, qty, stock", [
    ("item1", 5, {"item1": 10}),
])
def test_lock_item(item, qty, stock):
    warehouse = Warehouse(stock)
    warehouse.lock_item(item, qty)
    assert warehouse._locked_stock[item] == qty

@pytest.mark.parametrize("item, qty_locked, qty_released, expected", [
    ("item1", 5, 3, 2),
])
def test_release_item(item, qty_locked, qty_released, expected):
    warehouse = Warehouse({"item1": 10})
    warehouse.lock_item(item, qty_locked)
    warehouse.release_item(item, qty_released)
    assert warehouse._locked_stock[item] == expected


@pytest.mark.parametrize("email, age, expected_error", [
    ("test@example.com", 25, None),
    ("invalid_email", 25, UserValidationError),
    ("test@example.com", 17, UserValidationError),
    ("test@example.com", 101, UserValidationError),
])
def test_order_processor_validate_user(email, age, expected_error):
    order_processor = OrderProcessor(Warehouse({}))
    if expected_error:
        with pytest.raises(expected_error):
            order_processor.validate_user(email, age)
    else:
        order_processor.validate_user(email, age)

@pytest.mark.parametrize("warehouse_stock, order_items, expected_status", [
    ({"item1": 10}, [{"id": "item1", "qty": 5, "price": 10.0}], "success"),
    ({"item1": 3}, [{"id": "item1", "qty": 5, "price": 10.0}], "failed"),
])
def test_order_processor_process_order(warehouse_stock, order_items, expected_status):
    warehouse = Warehouse(warehouse_stock)
    order_processor = OrderProcessor(warehouse)
    order_data = {
        "email": "test@example.com",
        "age": 25,
        "tier": "STANDARD"
    }
    result = order_processor.process_order("order1", order_data, order_items)
    assert result["status"] == expected_status

