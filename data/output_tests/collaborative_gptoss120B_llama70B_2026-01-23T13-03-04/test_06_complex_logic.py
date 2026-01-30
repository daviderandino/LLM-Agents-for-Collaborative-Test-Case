import pytest
from data.input_code.06_complex_logic import OrderProcessor, Warehouse, DiscountEngine, UserValidationError, FraudDetectedError, PaymentError
from datetime import datetime
import re

@pytest.fixture
def warehouse():
    return Warehouse({"item1": 10, "item2": 5, "item3": 10, "item5": 5, "item10": 5, "item11": 10, "item6": 10})

@pytest.fixture
def order_processor(warehouse):
    return OrderProcessor(warehouse)



def test_T3_PROMO_INVALID(order_processor):
    result = order_processor.process_order(
        "ORD003",
        {"email": "valid@domain.com", "age": 28, "tier": "STANDARD", "payment_method": "CC"},
        [{"id": "item3", "qty": 2, "price": 50.0}],
        "BAD123"
    )
    assert result == {
        "status": "error",
        "reason": "Promo Error: Invalid promo code format"
    }

def test_T4_INVENTORY_MISSING_ITEM(order_processor):
    result = order_processor.process_order(
        "ORD004",
        {"email": "shopper@site.com", "age": 35, "tier": "STANDARD", "payment_method": "CC"},
        [{"id": "missing_item", "qty": 1, "price": 10.0}],
        None
    )
    assert result == {
        "status": "failed",
        "reason": "Out of stock: Item missing_item not found in warehouse."
    }

def test_T5_INVENTORY_INSUFFICIENT(order_processor):
    result = order_processor.process_order(
        "ORD005",
        {"email": "buyer@shop.it", "age": 40, "tier": "STANDARD", "payment_method": "CC"},
        [{"id": "item5", "qty": 10, "price": 15.0}],
        None
    )
    assert result == {
        "status": "failed",
        "reason": "Out of stock: Insufficient stock for item5"
    }

def test_T6_NEGATIVE_QTY_ZERO_PRICE(order_processor):
    with pytest.raises(ValueError):
        order_processor.process_order(
            "ORD006",
            {"email": "return@shop.com", "age": 30, "tier": "STANDARD", "payment_method": "CC"},
            [{"id": "item6", "qty": -1, "price": 0.0}],
            None
        )

def test_T7_INVALID_EMAIL(order_processor):
    with pytest.raises(UserValidationError):
        order_processor.validate_user("invalid-email", 30)

def test_T8_AGE_UNDER_18(order_processor):
    with pytest.raises(UserValidationError):
        order_processor.validate_user("young@user.com", 16)

def test_T9_AGE_OVER_100(order_processor):
    with pytest.raises(UserValidationError):
        order_processor.validate_user("elder@user.com", 101)

def test_T10_PAYPAL_FRAUD(order_processor):
    with pytest.raises(FraudDetectedError):
        order_processor.process_order(
            "ORD010",
            {"email": "fraud@shop.com", "age": 45, "tier": "STANDARD", "payment_method": "PAYPAL"},
            [{"id": "item10", "qty": 1, "price": 666.66 / (1 + 0.22)}],
            None
        )

def test_T11_CRYPTO_MIN_AMOUNT(order_processor):
    with pytest.raises(PaymentError):
        order_processor.process_order(
            "ORD011",
            {"email": "crypto@shop.com", "age": 28, "tier": "STANDARD", "payment_method": "CRYPTO"},
            [{"id": "item11", "qty": 1, "price": 40.0}],
            None
        )