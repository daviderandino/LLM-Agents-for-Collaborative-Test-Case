import pytest
from data.input_code.complex_logic import *

@pytest.fixture
def warehouse():
    return Warehouse({"item1": 10, "item2": 5})


@pytest.mark.parametrize("item_id, quantity, error", [
    ("item1", 11, InventoryError),
    ("item2", 6, InventoryError), 
    ("item3", 1, InventoryError),  # Item not in stock
])
def test_Warehouse_lock_item(warehouse, item_id, quantity, error):
    with pytest.raises(error):
        warehouse.lock_item(item_id, quantity)


@pytest.mark.parametrize("email, age, error", [
    ("invalid_email", 25, UserValidationError),
    ("test@example.com", 15, UserValidationError),
])
def test_OrderProcessor_validate_user(email, age, error):
    processor = OrderProcessor(Warehouse({}))
    with pytest.raises(error):
        processor.validate_user(email, age)

def test_OrderProcessor_process_order(warehouse):
    processor = OrderProcessor(warehouse)
    order_data = {
        "order_id": "order1",
        "user_data": {"email": "test@example.com", "age": 25, "tier": "GOLD"},
        "items": [{"id": "item1", "qty": 1, "price": 100}],
        "promo_code": "ABC-123"
    }
    result = processor.process_order(**order_data)
    assert result["status"] == "success"

