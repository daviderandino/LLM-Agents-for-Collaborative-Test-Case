import pytest
from data.input_code.d06_complex_logic import *

# ------------------- Warehouse Tests ------------------- #

@pytest.fixture
def warehouse():
    return Warehouse(initial_stock={"item1": 10})


@pytest.mark.parametrize(
    "item_id, quantity, expected",
    [
        ("item1", 5, True),          # sufficient stock
    ],
)
def test_warehouse_check_stock_success(warehouse, item_id, quantity, expected):
    assert warehouse.check_stock(item_id, quantity) is expected


def test_warehouse_check_stock_missing_item(warehouse):
    with pytest.raises(InventoryError):
        warehouse.check_stock("item2", 5)


def test_warehouse_lock_item_success(warehouse):
    warehouse.lock_item("item1", 5)
    # after locking, available should be 5
    assert warehouse.check_stock("item1", 5) is True
    assert warehouse.check_stock("item1", 6) is False


def test_warehouse_lock_item_insufficient_stock(warehouse):
    with pytest.raises(InventoryError):
        warehouse.lock_item("item1", 15)


# ------------------- DiscountEngine Tests ------------------- #

def test_discount_engine_night_owl(monkeypatch):
    # Mock the datetime class used inside the module to control the hour
    class DummyDateTime:
        @staticmethod
        def now():
            class DummyNow:
                hour = 2  # night hour
            return DummyNow()
    monkeypatch.setattr("data.input_code.d06_complex_logic.datetime", DummyDateTime)

    # only night discount (5%) applied
    assert DiscountEngine.calculate_discount(100.0, "STANDARD") == 0.05


@pytest.mark.parametrize(
    "total, tier, expected",
    [
        (100.0, "GOLD", 0.10),          # gold tier
        (1000.0, "PLATINUM", 0.20),    # platinum without extra amount
        (1500.0, "PLATINUM", 0.25),    # platinum with extra amount >1000
    ],
)
def test_discount_engine_tier_logic(total, tier, expected):
    assert DiscountEngine.calculate_discount(total, tier) == expected


def test_discount_engine_promo_code_valid(monkeypatch):
    # mock datetime to avoid night discount interference
    class DummyDateTime:
        @staticmethod
        def now():
            class DummyNow:
                hour = 12
            return DummyNow()
    monkeypatch.setattr("data.input_code.d06_complex_logic.datetime", DummyDateTime)

    # regular promo code adds 10%
    assert DiscountEngine.calculate_discount(100.0, "STANDARD", "ABC-123") == 0.10


def test_discount_engine_promo_code_super(monkeypatch):
    class DummyDateTime:
        @staticmethod
        def now():
            class DummyNow:
                hour = 12
            return DummyNow()
    monkeypatch.setattr("data.input_code.d06_complex_logic.datetime", DummyDateTime)

    # super promo returns immediate 50% off (bypasses other discounts)
    result = DiscountEngine.calculate_discount(200.0, "GOLD", "XYZ-999")
    assert result == 100.0  # 50% of 200.0


def test_discount_engine_invalid_promo_code():
    with pytest.raises(ValueError):
        DiscountEngine.calculate_discount(100.0, "STANDARD", "invalid")  # not matching regex


# ------------------- OrderProcessor.validate_user Tests ------------------- #

@pytest.fixture
def order_processor(warehouse):
    return OrderProcessor(warehouse)


@pytest.mark.parametrize(
    "email, age",
    [
        ("test@test.com", 25),
        ("user.name+tag@sub.domain.co", 30),
    ],
)
def test_validate_user_success(order_processor, email, age):
    # should not raise
    order_processor.validate_user(email, age)


@pytest.mark.parametrize(
    "email, age, exc",
    [
        ("test", 25, UserValidationError),          # invalid email
        ("test@test.com", 15, UserValidationError),# underage
        ("test@test.com", 101, UserValidationError),# over 100
    ],
)
def test_validate_user_errors(order_processor, email, age, exc):
    with pytest.raises(exc):
        order_processor.validate_user(email, age)


# ------------------- OrderProcessor.process_order Tests ------------------- #

def test_process_order_success(order_processor):
    # warehouse already has item1 with 10 units
    order_id = "123"
    user_data = {"email": "test@test.com", "age": 25}
    items = [{"id": "item1", "qty": 5, "price": 10.0}]
    result = order_processor.process_order(order_id, user_data, items)

    assert result["status"] == "success"
    assert result["order_id"] == order_id
    assert result["original_price"] == 50.0  # 5 * 10
    # No discount, tax 22%
    expected_total = round(50.0 * 1.22, 2)
    assert result["final_total"] == expected_total
    assert result["items_count"] == 1


def test_process_order_out_of_stock(order_processor):
    order_id = "123"
    user_data = {"email": "test@test.com", "age": 25}
    items = [{"id": "item2", "qty": 5, "price": 10.0}]  # item2 not in stock
    result = order_processor.process_order(order_id, user_data, items)

    assert result["status"] == "failed"
    assert "Out of stock" in result["reason"]


def test_process_order_invalid_promo_code(order_processor):
    order_id = "123"
    user_data = {"email": "test@test.com", "age": 25}
    items = [{"id": "item1", "qty": 5, "price": 10.0}]
    # Use a promo code that does NOT match the required regex to trigger the error path
    result = order_processor.process_order(order_id, user_data, items, promo_code="BAD123")
    assert result["status"] == "error"
    assert "Promo Error" in result["reason"]


def test_process_order_negative_qty_zero_price(order_processor):
    order_id = "123"
    user_data = {"email": "test@test.com", "age": 25}
    items = [{"id": "item1", "qty": -5, "price": 0.0}]
    with pytest.raises(ValueError):
        order_processor.process_order(order_id, user_data, items)


def test_process_order_fraud_detected(monkeypatch, order_processor):
    # Force discount to 0% to control final amount
    monkeypatch.setattr(DiscountEngine, "calculate_discount", lambda total, tier, promo=None: 0.0)

    order_id = "123"
    user_data = {
        "email": "test@test.com",
        "age": 25,
        "payment_method": "PAYPAL"
    }
    # total_price such that total_price * 1.22 == 666.66
    total_price = round(666.66 / 1.22, 2)  # ≈ 546.0
    items = [{"id": "item1", "qty": 1, "price": total_price}]

    with pytest.raises(FraudDetectedError):
        order_processor.process_order(order_id, user_data, items)


def test_process_order_crypto_min_amount(monkeypatch, order_processor):
    # Force discount to 0% to keep price low
    monkeypatch.setattr(DiscountEngine, "calculate_discount", lambda total, tier, promo=None: 0.0)

    order_id = "123"
    user_data = {
        "email": "test@test.com",
        "age": 25,
        "payment_method": "CRYPTO"
    }
    items = [{"id": "item1", "qty": 1, "price": 30.0}]  # final total after tax will be < 50

    with pytest.raises(PaymentError):
        order_processor.process_order(order_id, user_data, items)