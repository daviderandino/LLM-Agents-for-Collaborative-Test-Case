import pytest
from data.input_code.d06_complex_logic import *
from datetime import datetime
from unittest.mock import patch

# T1_WarehouseCheckNotFound
def test_T1_WarehouseCheckNotFound():
    warehouse = Warehouse({"itemA": 10})
    with pytest.raises(InventoryError):
        warehouse.check_stock("missing_item", 1)

# T2_WarehouseLockInsufficient
def test_T2_WarehouseLockInsufficient():
    warehouse = Warehouse({"itemB": 5})
    with pytest.raises(InventoryError):
        warehouse.lock_item("itemB", 10)

# T3_DiscountNightGoldPromo

# T4_DiscountPlatinumSuperPromo
@pytest.mark.parametrize("total_amount, user_tier, promo_code, expected", [
    (2000.0, "PLATINUM", "XYZ-999", 1000.0)
])
def test_T4_DiscountPlatinumSuperPromo(total_amount, user_tier, promo_code, expected):
    discount = DiscountEngine.calculate_discount(total_amount, user_tier, promo_code)
    assert discount == expected

# T5_DiscountInvalidPromo
def test_T5_DiscountInvalidPromo():
    with pytest.raises(ValueError):
        DiscountEngine.calculate_discount(50.0, "STANDARD", "badcode")

# T6_DiscountCap
@pytest.mark.parametrize("total_amount, user_tier, promo_code, mock_datetime_hour, expected", [
    (1500.0, "PLATINUM", "DEF-456", 3, 0.35)  
])
def test_T6_DiscountCap(total_amount, user_tier, promo_code, mock_datetime_hour, expected):
    # Mock datetime
    with patch('datetime.datetime') as mock_datetime:
        mock_datetime.now.return_value = datetime(2022, 1, 1, mock_datetime_hour)
        discount = DiscountEngine.calculate_discount(total_amount, user_tier, promo_code)
    assert round(discount, 2) == expected

# T7_ValidateUserBadEmail
def test_T7_ValidateUserBadEmail():
    order_processor = OrderProcessor(Warehouse({}))
    with pytest.raises(UserValidationError):
        order_processor.validate_user("invalid_email", 30)

# T8_ValidateUserUnderage
def test_T8_ValidateUserUnderage():
    order_processor = OrderProcessor(Warehouse({}))
    with pytest.raises(UserValidationError):
        order_processor.validate_user("test@example.com", 16)

# T9_ValidateUserOver100
def test_T9_ValidateUserOver100():
    order_processor = OrderProcessor(Warehouse({}))
    with pytest.raises(UserValidationError):
        order_processor.validate_user("senior@example.com", 101)

# T10_ProcessOrderFreeReturn
@pytest.mark.parametrize("warehouse_stock, order_id, user_data, items, expected", [
    ({"itemX": 10}, "ORD_FREE", {"email": "user@example.com", "age": 30}, [{"id": "itemX", "qty": -1, "price": 0.0}], "ValueError")
])
def test_T10_ProcessOrderFreeReturn(warehouse_stock, order_id, user_data, items, expected):
    warehouse = Warehouse(warehouse_stock)
    order_processor = OrderProcessor(warehouse)
    if expected == "ValueError":
        with pytest.raises(ValueError):
            order_processor.process_order(order_id, user_data, items)
    else:
        result = order_processor.process_order(order_id, user_data, items)
        assert result == expected

# T11_ProcessOrderOutOfStock
@pytest.mark.parametrize("warehouse_stock, order_id, user_data, items, expected", [
    ({"itemY": 3}, "ORD_OOS", {"email": "buyer@example.com", "age": 25}, [{"id": "itemY", "qty": 5, "price": 20.0}], {"status": "failed", "reason": "Out of stock: Insufficient stock for itemY"})
])
def test_T11_ProcessOrderOutOfStock(warehouse_stock, order_id, user_data, items, expected):
    warehouse = Warehouse(warehouse_stock)
    order_processor = OrderProcessor(warehouse)
    result = order_processor.process_order(order_id, user_data, items)
    assert result == expected

# T12_ProcessOrderInvalidPromo
@pytest.mark.parametrize("warehouse_stock, order_id, user_data, items, promo_code, expected", [
    ({"itemZ": 10}, "ORD_BADPROMO", {"email": "shopper@example.com", "age": 28}, [{"id": "itemZ", "qty": 2, "price": 15.0}], "WRONG-001", {"status": "error", "reason": "Promo Error: Invalid promo code format"})
])
def test_T12_ProcessOrderInvalidPromo(warehouse_stock, order_id, user_data, items, promo_code, expected):
    warehouse = Warehouse(warehouse_stock)
    order_processor = OrderProcessor(warehouse)
    result = order_processor.process_order(order_id, user_data, items, promo_code)
    assert result == expected

# T13_ProcessOrderFraudPayPal

# T14_ProcessOrderCryptoTooLow
@pytest.mark.parametrize("warehouse_stock, order_id, user_data, items, expected", [
    ({"itemC": 2}, "ORD_CRYPTO", {"email": "crypto@example.com", "age": 40, "payment_method": "CRYPTO"}, [{"id": "itemC", "qty": 2, "price": 20.0}], PaymentError)
])
def test_T14_ProcessOrderCryptoTooLow(warehouse_stock, order_id, user_data, items, expected):
    warehouse = Warehouse(warehouse_stock)
    order_processor = OrderProcessor(warehouse)
    with pytest.raises(expected):
        order_processor.process_order(order_id, user_data, items)

# T15_ProcessOrderSuccess
@pytest.mark.parametrize("warehouse_stock, order_id, user_data, items, expected", [
    ({"itemS": 5}, "ORD_SUCCESS", {"email": "good@example.com", "age": 45}, [{"id": "itemS", "qty": 2, "price": 50.0}], 
     {"status": "success", "order_id": "ORD_SUCCESS", "original_price": 100.0, "discount_applied": 0.0, "final_total": 122.0, "items_count": 1})
])
def test_T15_ProcessOrderSuccess(warehouse_stock, order_id, user_data, items, expected):
    warehouse = Warehouse(warehouse_stock)
    order_processor = OrderProcessor(warehouse)
    result = order_processor.process_order(order_id, user_data, items)
    assert result == expected