import pytest
from data.input_code.d01_bank import *

@pytest.mark.parametrize('initial_balance, expected', [
    (0, {"balance": 0, "is_active": True}),
    (100, {"balance": 100, "is_active": True})
])
def test_init_success(initial_balance, expected):
    account = BankAccount(initial_balance)
    assert account.balance == expected["balance"]
    assert account.is_active == expected["is_active"]

def test_init_error():
    with pytest.raises(ValueError):
        BankAccount(-10)

@pytest.mark.parametrize('initial_balance, amount, expected', [
    (100, 50, 150),
    (0, 10, 10)
])
def test_deposit_success(initial_balance, amount, expected):
    account = BankAccount(initial_balance)
    assert account.deposit(amount) == expected

@pytest.mark.parametrize('initial_balance, amount', [
    (100, 0),
    (0, 0)
])
def test_deposit_error_zero(initial_balance, amount):
    account = BankAccount(initial_balance)
    with pytest.raises(ValueError):
        account.deposit(amount)

def test_deposit_error_frozen():
    account = BankAccount(100)
    account.freeze_account()
    with pytest.raises(ValueError):
        account.deposit(50)

@pytest.mark.parametrize('initial_balance, amount, expected', [
    (100, 30, 70),
    (50, 10, 40)
])
def test_withdraw_success(initial_balance, amount, expected):
    account = BankAccount(initial_balance)
    assert account.withdraw(amount) == expected

@pytest.mark.parametrize('initial_balance, amount', [
    (100, 0),
    (100, -10),
    (100, 150)
])
def test_withdraw_error(initial_balance, amount):
    account = BankAccount(initial_balance)
    with pytest.raises(ValueError):
        account.withdraw(amount)

def test_withdraw_error_frozen():
    account = BankAccount(100)
    account.freeze_account()
    with pytest.raises(ValueError):
        account.withdraw(10)

def test_freeze_account():
    account = BankAccount(100)
    account.freeze_account()
    assert account.is_active == False

def test_unfreeze_account():
    account = BankAccount(100)
    account.freeze_account()
    account.unfreeze_account()
    assert account.is_active == True

def test_deposit_after_unfreeze():
    account = BankAccount(100)
    account.freeze_account()
    account.unfreeze_account()
    assert account.deposit(20) == 120