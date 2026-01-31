import pytest
from data.input_code.d06_complex_logic import Warehouse, DiscountEngine, OrderProcessor, InventoryError, PaymentError, FraudDetectedError, UserValidationError

@pytest.fixture
def warehouse():
    return Warehouse({'item1': 10})

@pytest.mark.parametrize('item_id, quantity, expected', [
    ('item1', 1, True),
    ('item2', 1, False)
])
def test_warehouse_check_stock(warehouse, item_id, quantity, expected):
    if expected:
        assert warehouse.check_stock(item_id, quantity) == expected
    else:
        with pytest.raises(InventoryError):
            warehouse.check_stock(item_id, quantity)

def test_warehouse_lock_item(warehouse):
    warehouse.lock_item('item1', 1)
    assert warehouse._locked_stock['item1'] == 1

def test_warehouse_release_item(warehouse):
    warehouse.lock_item('item1', 1)
    warehouse.release_item('item1', 1)
    assert 'item1' not in warehouse._locked_stock

@pytest.mark.parametrize('total_amount, user_tier, promo_code, expected', [
    (100.0, 'GOLD', 'ABC-123', 0.2),
    (100.0, 'GOLD', 'ABC-1234', 'ValueError')
])
def test_discount_engine_calculate_discount(total_amount, user_tier, promo_code, expected):
    if expected == 'ValueError':
        with pytest.raises(ValueError):
            DiscountEngine.calculate_discount(total_amount, user_tier, promo_code)
    else:
        assert DiscountEngine.calculate_discount(total_amount, user_tier, promo_code) == expected

@pytest.mark.parametrize('email, age, expected', [
    ('test@example.com', 25, None),
    ('invalid', 25, 'UserValidationError'),
    ('test@example.com', 15, 'UserValidationError')
])
def test_order_processor_validate_user(email, age, expected):
    if expected:
        with pytest.raises(UserValidationError):
            OrderProcessor(Warehouse({})).validate_user(email, age)
    else:
        OrderProcessor(Warehouse({})).validate_user(email, age)


# Additional test to ensure the discount is correctly applied when promo code is 'ABC-999'

# Additional test to ensure the payment error is correctly raised when payment method is 'PAYPAL' and amount is 666.66

# Additional test to ensure the payment error is correctly raised when payment method is 'CRYPTO' and amount is less than 50.0
def test_order_processor_process_order_payment_error_crypto():
    order_id = 'order1'
    user_data = {'email': 'test@example.com', 'age': 25, 'tier': 'GOLD', 'payment_method': 'CRYPTO'}
    items = [{'id': 'item1', 'qty': 1, 'price': 10.0}]
    promo_code = 'ABC-123'
    with pytest.raises(PaymentError):
        OrderProcessor(Warehouse({'item1': 10})).process_order(order_id, user_data, items, promo_code)