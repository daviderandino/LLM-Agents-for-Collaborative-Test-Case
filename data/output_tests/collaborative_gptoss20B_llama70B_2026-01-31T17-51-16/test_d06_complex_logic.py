import pytest
from data.input_code.d06_complex_logic import *
from datetime import datetime
import re
from unittest.mock import patch

@pytest.mark.parametrize('warehouse_initial_stock, item_id, quantity, expected', [
    ({"A": 10}, "B", 1, "InventoryError"),
    ({"A": 10}, "A", 5, True),
    ({"A": 10}, "A", 15, False),
])
def test_warehouse_check_stock(warehouse_initial_stock, item_id, quantity, expected):
    warehouse = Warehouse(warehouse_initial_stock)
    if expected == "InventoryError":
        with pytest.raises(InventoryError):
            warehouse.check_stock(item_id, quantity)
    else:
        assert warehouse.check_stock(item_id, quantity) == expected

@pytest.mark.parametrize('warehouse_initial_stock, item_id, quantity, expected', [
    ({"A": 5}, "A", 10, "InventoryError"),
    ({"A": 10}, "A", 5, None),
])
def test_warehouse_lock_item(warehouse_initial_stock, item_id, quantity, expected):
    warehouse = Warehouse(warehouse_initial_stock)
    if expected == "InventoryError":
        with pytest.raises(InventoryError):
            warehouse.lock_item(item_id, quantity)
    else:
        warehouse.lock_item(item_id, quantity)
        assert warehouse._locked_stock.get(item_id, 0) == quantity


@pytest.mark.parametrize('total_amount, user_tier, promo_code, expected', [
    (200, "GOLD", None, 0.10),
    (1500, "PLATINUM", None, 0.25),
    (500, "PLATINUM", None, 0.20),
    (200, "STANDARD", "ABC-123", 0.10),
    (200, "STANDARD", "XYZ-999", 100.0),
    (200, "STANDARD", "abc-123", "ValueError"),
])
def test_discount_engine_calculate_discount(total_amount, user_tier, promo_code, expected, monkeypatch):
    with patch('datetime.datetime') as mock_datetime:
        mock_datetime.now.return_value = datetime(2022, 1, 1, 2, 0, 0)
        if expected == "ValueError":
            with pytest.raises(ValueError):
                DiscountEngine.calculate_discount(total_amount, user_tier, promo_code)
        else:
            assert DiscountEngine.calculate_discount(total_amount, user_tier, promo_code) == expected

@pytest.mark.parametrize('email, age, expected', [
    ("invalid", 30, "UserValidationError"),
    ("test@test.com", 17, "UserValidationError"),
    ("test@test.com", 101, "UserValidationError"),
    ("test@test.com", 30, None),
])
def test_order_processor_validate_user(email, age, expected):
    order_processor = OrderProcessor(Warehouse({}))
    if expected == "UserValidationError":
        with pytest.raises(UserValidationError):
            order_processor.validate_user(email, age)
    else:
        order_processor.validate_user(email, age)

