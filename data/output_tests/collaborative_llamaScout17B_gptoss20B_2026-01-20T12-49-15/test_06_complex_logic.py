import pytest
import datetime as dt
from data.input_code.06_complex_logic import *

# ---------- Warehouse Edge Case Tests ----------
def test_warehouse_lock_item_zero_quantity():
    warehouse = Warehouse({"test_item": 10})
    # Locking zero quantity should not raise and should set locked stock to 0
    warehouse.lock_item("test_item", 0)
    assert warehouse._locked_stock == {"test_item": 0}

def test_warehouse_release_item_zero_quantity():
    warehouse = Warehouse({"test_item": 10})
    # Release zero quantity should not raise and should not alter locked stock
    warehouse.release_item("test_item", 0)
    assert warehouse._locked_stock == {}

# ---------- DiscountEngine Night Owl Discount ----------
@pytest.mark.parametrize(
    "total_amount, user_tier, promo_code, expected",
    [
        (100.0, "STANDARD", None, 0.05),
    ],
)
def test_discount_engine_night_owl_discount(total_amount, user_tier, promo_code, expected, monkeypatch):
    # Mock datetime to 02:00 (night window)
    monkeypatch.setattr(
        "data.input_code.06_complex_logic.datetime",
        type(
            "MockDateTime",
            (),
            {"now": staticmethod(lambda: dt.datetime(2023, 1, 1, 2))},
        ),
        raising=False,
    )
    result = DiscountEngine.calculate_discount(total_amount, user_tier, promo_code)
    assert result == expected

# ---------- DiscountEngine Platinum Max Discount ----------
@pytest.mark.parametrize(
    "total_amount, user_tier, promo_code, expected",
    [
        (1001.0, "PLATINUM", None, 0.25),
    ],
)
def test_discount_engine_platinum_max_discount(total_amount, user_tier, promo_code, expected, monkeypatch):
    # Ensure we are not in the night window
    monkeypatch.setattr(
        "data.input_code.06_complex_logic.datetime",
        type(
            "MockDateTime",
            (),
            {"now": staticmethod(lambda: dt.datetime(2023, 1, 1, 12))},
        ),
        raising=False,
    )
    result = DiscountEngine.calculate_discount(total_amount, user_tier, promo_code)
    assert result == expected

# ---------- DiscountEngine Super Promo Code ----------
@pytest.mark.parametrize(
    "total_amount, user_tier, promo_code, expected",
    [
        (100.0, "STANDARD", "ABC-999", 50.0),
    ],
)
def test_discount_engine_super_promo_code(total_amount, user_tier, promo_code, expected, monkeypatch):
    # Mock datetime to avoid night discount
    monkeypatch.setattr(
        "data.input_code.06_complex_logic.datetime",
        type(
            "MockDateTime",
            (),
            {"now": staticmethod(lambda: dt.datetime(2023, 1, 1, 12))},
        ),
        raising=False,
    )
    result = DiscountEngine.calculate_discount(total_amount, user_tier, promo_code)
    assert result == expected

# ---------- OrderProcessor.validate_user Age Over 100 ----------
def test_order_processor_validate_user_age_over_100():
    processor = OrderProcessor(Warehouse({"test_item": 10}))
    with pytest.raises(UserValidationError):
        processor.validate_user("test@example.com", 101)

# ---------- OrderProcessor.process_order Crypto Minimum Amount ----------
def test_order_processor_process_order_crypto_min_amount(monkeypatch):
    warehouse = Warehouse({"test_item": 10})
    processor = OrderProcessor(warehouse)

    # Mock datetime to avoid night discount
    monkeypatch.setattr(
        "data.input_code.06_complex_logic.datetime",
        type(
            "MockDateTime",
            (),
            {"now": staticmethod(lambda: dt.datetime(2023, 1, 1, 12))},
        ),
        raising=False,
    )

    with pytest.raises(PaymentError):
        processor.process_order(
            "test_order",
            {"email": "test@example.com", "age": 25, "tier": "STANDARD", "payment_method": "CRYPTO"},
            [{"id": "test_item", "qty": 1, "price": 40.0}],
            None,
        )

# ---------- OrderProcessor.process_order Credit Card Success ----------
def test_order_processor_process_order_credit_card_success(monkeypatch):
    warehouse = Warehouse({"test_item": 10})
    processor = OrderProcessor(warehouse)

    # Mock datetime to avoid night discount
    monkeypatch.setattr(
        "data.input_code.06_complex_logic.datetime",
        type(
            "MockDateTime",
            (),
            {"now": staticmethod(lambda: dt.datetime(2023, 1, 1, 12))},
        ),
        raising=False,
    )

    result = processor.process_order(
        "test_order",
        {"email": "test@example.com", "age": 25, "tier": "STANDARD", "payment_method": "CC"},
        [{"id": "test_item", "qty": 1, "price": 100.0}],
        None,
    )
    assert result["status"] == "success"
    # Final total should be 100 * 1.22 = 122.0
    assert result["final_total"] == 122.0

import pytest
import datetime as dt
from data.input_code.06_complex_logic import *

# ---------- Warehouse Initialization Edge Case ----------
def test_warehouse_initial_stock_zero():
    warehouse = Warehouse({})
    assert warehouse._stock == {}
    assert warehouse._locked_stock == {}

# ---------- DiscountEngine Zero Amount ----------
@pytest.mark.parametrize(
    "total_amount, user_tier, promo_code, expected",
    [
        (0.0, "STANDARD", None, 0.0),
    ],
)
def test_discount_engine_zero_amount(total_amount, user_tier, promo_code, expected, monkeypatch):
    # Ensure we are not in the night window
    monkeypatch.setattr(
        "data.input_code.06_complex_logic.datetime",
        type(
            "MockDateTime",
            (),
            {"now": staticmethod(lambda: dt.datetime(2023, 1, 1, 12))},
        ),
        raising=False,
    )
    result = DiscountEngine.calculate_discount(total_amount, user_tier, promo_code)
    assert result == expected

# ---------- OrderProcessor.validate_user Empty Email ----------
def test_order_processor_validate_user_empty_email():
    processor = OrderProcessor(Warehouse({"test_item": 10}))
    with pytest.raises(UserValidationError):
        processor.validate_user("", 25)

# ---------- OrderProcessor PayPal Fraud Detected ----------

# ---------- OrderProcessor Crypto Minimum Amount ----------
@pytest.mark.parametrize(
    "price, expected_exception",
    [
        (40.0, PaymentError),  # price chosen so that final_price_with_tax < 50
    ],
)
def test_order_processor_crypto_min_amount(price, expected_exception, monkeypatch):
    warehouse = Warehouse({"test_item": 10})
    processor = OrderProcessor(warehouse)

    # Mock datetime to avoid night discount
    monkeypatch.setattr(
        "data.input_code.06_complex_logic.datetime",
        type(
            "MockDateTime",
            (),
            {"now": staticmethod(lambda: dt.datetime(2023, 1, 1, 12))},
        ),
        raising=False,
    )

    with pytest.raises(expected_exception):
        processor.process_order(
            "test_order",
            {"email": "test@example.com", "age": 25, "tier": "STANDARD", "payment_method": "CRYPTO"},
            [{"id": "test_item", "qty": 1, "price": price}],
            None,
        )

# ---------- DiscountEngine Night Owl and Gold Tier ----------
