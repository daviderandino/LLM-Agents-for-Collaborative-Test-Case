import pytest
from data.input_code.d06_complex_logic import *
from datetime import datetime
import re

@pytest.fixture
def warehouse():
    return Warehouse({"item1": 10, "item2": 20})

def test_warehouse_init():
    warehouse = Warehouse({"item1": 10, "item2": 20})
    assert warehouse._stock == {"item1": 10, "item2": 20}

@pytest.mark.parametrize('item_id, quantity, expected', [
    ("item1", 5, True),
    ("item2", 25, False),
])
def test_warehouse_check_stock(warehouse, item_id, quantity, expected):
    assert warehouse.check_stock(item_id, quantity) == expected

def test_warehouse_lock_item(warehouse):
    warehouse.lock_item("item1", 5)
    assert warehouse._locked_stock == {"item1": 5}

def test_warehouse_release_item(warehouse):
    warehouse.lock_item("item1", 5)
    warehouse.release_item("item1", 5)
    assert warehouse._locked_stock == {}

@pytest.mark.parametrize('total_amount, user_tier, promo_code, expected', [
    (100.0, "STANDARD", None, 0.0),
    (100.0, "GOLD", None, 0.1),
    (1500.0, "PLATINUM", None, 0.25),
    (100.0, "STANDARD", "ABC-123", 0.1),
])
def test_discount_engine_calculate_discount(total_amount, user_tier, promo_code, expected):
    assert DiscountEngine.calculate_discount(total_amount, user_tier, promo_code) == expected

def test_discount_engine_calculate_discount_invalid_promo_code():
    with pytest.raises(ValueError):
        DiscountEngine.calculate_discount(100.0, "STANDARD", "Invalid-Code")

@pytest.mark.parametrize('email, age, expected', [
    ("test@example.com", 25, None),
    ("invalid_email", 25, "UserValidationError"),
    ("test@example.com", 15, "UserValidationError"),
])
def test_order_processor_validate_user(email, age, expected):
    if expected:
        with pytest.raises(UserValidationError):
            OrderProcessor(Warehouse({})).validate_user(email, age)
    else:
        OrderProcessor(Warehouse({})).validate_user(email, age)

