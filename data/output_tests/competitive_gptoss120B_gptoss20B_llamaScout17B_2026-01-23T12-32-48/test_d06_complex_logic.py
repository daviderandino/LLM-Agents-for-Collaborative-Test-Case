import pytest
from data.input_code.d06_complex_logic import *
from datetime import datetime
from unittest.mock import patch

# ------------------- Warehouse Tests -------------------

@pytest.mark.parametrize(
    "initial_stock, item_id, quantity, expected_exception",
    [
        # T1: missing item raises InventoryError
        ({ "item1": 5 }, "missing", 1, InventoryError),
        # T4: insufficient stock returns False (no exception)
        ({ "item1": 2 }, "item1", 5, None),
    ]
)
def test_warehouse_check_stock_exceptions(initial_stock, item_id, quantity, expected_exception):
    warehouse = Warehouse(initial_stock)
    if expected_exception:
        with pytest.raises(expected_exception):
            warehouse.check_stock(item_id, quantity)
    else:
        assert warehouse.check_stock(item_id, quantity) is False

@pytest.mark.parametrize(
    "initial_stock, item_id, quantity, expected_result",
    [
        # T2: sufficient stock returns True
        ({ "item1": 5 }, "item1", 3, True),
    ]
)
def test_warehouse_check_stock_success(initial_stock, item_id, quantity, expected_result):
    warehouse = Warehouse(initial_stock)
    assert warehouse.check_stock(item_id, quantity) == expected_result

def test_warehouse_lock_and_release():
    # T3: lock and release item
    warehouse = Warehouse({"item1": 5})
    # Lock 2 items
    warehouse.lock_item("item1", 2)
    # After locking, available stock should be 3
    assert warehouse.check_stock("item1", 3) is True
    # Release the locked items
    warehouse.release_item("item1", 2)
    # After release, full stock should be available again
    assert warehouse.check_stock("item1", 5) is True

# ------------------- DiscountEngine Tests -------------------

@pytest.mark.parametrize(
    "hour, total_amount, user_tier, promo_code, expected_discount",
    [
        # T5: Night hour discount
        (2, 100.0, "STANDARD", None, 0.05),
        # T6: Platinum tier with high amount
        (12, 1500.0, "PLATINUM", None, 0.25),
        # T7: Gold tier with valid promo
        (12, 100.0, "GOLD", "ABC-123", 0.20),
        # T8: Promo ending with 999 gives 50% off (returns amount, not percent)
        (12, 200.0, "STANDARD", "XYZ-999", 100.0),
    ]
)
def test_discount_engine_calculate_discount(hour, total_amount, user_tier, promo_code, expected_discount):
    # Patch the datetime used inside DiscountEngine
    with patch('data.input_code.06_complex_logic.datetime') as mock_datetime:
        mock_datetime.now.return_value = datetime(2023, 1, 1, hour, 0, 0)
        discount = DiscountEngine.calculate_discount(total_amount, user_tier, promo_code)
        assert discount == expected_discount

def test_discount_engine_invalid_promo():
    # T9: Invalid promo code raises ValueError
    with patch('data.input_code.06_complex_logic.datetime') as mock_datetime:
        mock_datetime.now.return_value = datetime(2023, 1, 1, 12, 0, 0)
        with pytest.raises(ValueError):
            DiscountEngine.calculate_discount(100.0, "STANDARD", "badcode")

# ------------------- OrderProcessor Tests -------------------

def test_order_processor_validate_user_invalid_email():
    # T10: Invalid email format
    processor = OrderProcessor(Warehouse({}))
    with pytest.raises(UserValidationError):
        processor.validate_user("invalid-email", 30)

def test_order_processor_validate_user_underage():
    # T11: Underage user
    processor = OrderProcessor(Warehouse({}))
    with pytest.raises(UserValidationError):
        processor.validate_user("test@example.com", 16)

def test_order_processor_validate_user_overage():
    # T12: Over 100 years old
    processor = OrderProcessor(Warehouse({}))
    with pytest.raises(UserValidationError):
        processor.validate_user("elder@example.com", 101)

def test_order_processor_process_success():
    # T13: Happy path
    warehouse = Warehouse({"item1": 10})
    processor = OrderProcessor(warehouse)
    result = processor.process_order(
        order_id="ORD123",
        user_data={
            "email": "buyer@example.com",
            "age": 30,
            "tier": "GOLD",
            "payment_method": "CC"
        },
        items=[
            {"id": "item1", "qty": 2, "price": 50.0}
        ],
        promo_code=None
    )
    expected = {
        "status": "success",
        "order_id": "ORD123",
        "original_price": 100.0,
        "discount_applied": 0.10,
        "final_total": 109.8,
        "items_count": 1
    }
    assert result == expected

def test_order_processor_process_inventory_failure():
    # T14: Inventory error leads to failed status
    warehouse = Warehouse({"item1": 1})
    processor = OrderProcessor(warehouse)
    result = processor.process_order(
        order_id="ORD124",
        user_data={
            "email": "buyer@example.com",
            "age": 30,
            "tier": "STANDARD",
            "payment_method": "CC"
        },
        items=[
            {"id": "item1", "qty": 2, "price": 20.0}
        ],
        promo_code=None
    )
    assert result["status"] == "failed"
    assert "Out of stock" in result["reason"]

def test_order_processor_hidden_division_error():
    # T15: Negative qty with zero price triggers ValueError
    warehouse = Warehouse({"item1": 5})
    processor = OrderProcessor(warehouse)
    with pytest.raises(ValueError):
        processor.process_order(
            order_id="ORD125",
            user_data={
                "email": "buyer@example.com",
                "age": 30,
                "tier": "STANDARD",
                "payment_method": "CC"
            },
            items=[
                {"id": "item1", "qty": -1, "price": 0.0}
            ],
            promo_code=None
        )

def test_order_processor_invalid_promo():
    # T16: Invalid promo code results in error status
    warehouse = Warehouse({"item1": 5})
    processor = OrderProcessor(warehouse)
    result = processor.process_order(
        order_id="ORD126",
        user_data={
            "email": "buyer@example.com",
            "age": 30,
            "tier": "STANDARD",
            "payment_method": "CC"
        },
        items=[
            {"id": "item1", "qty": 1, "price": 30.0}
        ],
        promo_code="XYZ-12A"
    )
    assert result["status"] == "error"
    assert "Promo Error" in result["reason"]

def test_order_processor_fraud_paypal():
    # T17: FraudDetectedError when final amount equals 666.66
    warehouse = Warehouse({"item1": 5})
    processor = OrderProcessor(warehouse)
    # Set tax rate to produce 666.66 final total
    processor.tax_rate = 5.6666  # (666.66/100)-1
    with pytest.raises(FraudDetectedError):
        processor.process_order(
            order_id="ORD127",
            user_data={
                "email": "buyer@example.com",
                "age": 30,
                "tier": "STANDARD",
                "payment_method": "PAYPAL"
            },
            items=[
                {"id": "item1", "qty": 1, "price": 100.0}
            ],
            promo_code=None
        )

def test_order_processor_crypto_min_amount():
    # T18: PaymentError for crypto below minimum amount
    warehouse = Warehouse({"item1": 5})
    processor = OrderProcessor(warehouse)
    with pytest.raises(PaymentError):
        processor.process_order(
            order_id="ORD128",
            user_data={
                "email": "buyer@example.com",
                "age": 30,
                "tier": "STANDARD",
                "payment_method": "CRYPTO"
            },
            items=[
                {"id": "item1", "qty": 1, "price": 40.0}
            ],
            promo_code=None
        )