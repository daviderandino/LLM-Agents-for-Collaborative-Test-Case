import pytest
from data.input_code.06_complex_logic import *

# Test Warehouse
@pytest.mark.parametrize("initial_stock, expected", [
    ({"item1": 10}, {"item1": 10}),
])
def test_warehouse_init(initial_stock, expected):
    warehouse = Warehouse(initial_stock)
    assert warehouse._stock == expected


def test_warehouse_check_stock_error():
    warehouse = Warehouse({"item1": 10})
    with pytest.raises(InventoryError):
        warehouse.check_stock("item2", 5)

@pytest.mark.parametrize("item, qty, expected", [
    ("item1", 5, {"item1": 5}),
])
def test_warehouse_lock_item_success(item, qty, expected):
    warehouse = Warehouse({"item1": 10})
    warehouse.lock_item(item, qty)
    assert warehouse._locked_stock == expected

def test_warehouse_lock_item_error():
    warehouse = Warehouse({"item1": 5})
    with pytest.raises(InventoryError):
        warehouse.lock_item("item1", 10)

# Test DiscountEngine

def test_discount_engine_calculate_discount_error():
    with pytest.raises(ValueError):
        DiscountEngine.calculate_discount(100.0, "STANDARD", "ABC")

# Test OrderProcessor
def test_order_processor_validate_user_success():
    order_processor = OrderProcessor(Warehouse({}))
    order_processor.validate_user("test@test.com", 25)

def test_order_processor_validate_user_error():
    order_processor = OrderProcessor(Warehouse({}))
    with pytest.raises(UserValidationError):
        order_processor.validate_user("test", 25)

@pytest.mark.parametrize("order_id, user_data, items, expected_status", [
    ("1", {"email": "test@test.com", "age": 25, "tier": "STANDARD"}, [{"id": "item1", "qty": 5, "price": 10.0}], "success"),
    ("1", {"email": "test@test.com", "age": 25, "tier": "STANDARD"}, [{"id": "item2", "qty": 5, "price": 10.0}], "failed"),
])
def test_order_processor_process_order(order_id, user_data, items, expected_status):
    warehouse = Warehouse({"item1": 10})
    order_processor = OrderProcessor(warehouse)
    result = order_processor.process_order(order_id, user_data, items)
    assert result["status"] == expected_status

def test_warehouse_check_stock_edge():
    warehouse = Warehouse({"item1": 0})
    assert not warehouse.check_stock("item1", 5)

def test_discount_engine_calculate_discount_platinum_cap():
    result = DiscountEngine.calculate_discount(500.0, "PLATINUM", None)
    assert result == 0.20

def test_discount_engine_calculate_discount_promo_code():
    result = DiscountEngine.calculate_discount(100.0, "STANDARD", "ABC-123")
    assert result == 0.10

