import pytest
from data.input_code.01_bank import *

@pytest.mark.parametrize('initial_balance', [100, 0])
def test_init_ok(initial_balance):
    account = BankAccount(initial_balance)
    assert account.balance == initial_balance

def test_init_neg():
    with pytest.raises(ValueError):
        BankAccount(-10)

@pytest.mark.parametrize('amount, expected', [
    (50, 150),
])
def test_deposit_ok(amount, expected):
    account = BankAccount(100)
    assert account.deposit(amount) == expected

@pytest.mark.parametrize('amount, error', [
    (50, ValueError),
])
def test_deposit_frozen(amount, error):
    account = BankAccount(100)
    account.freeze_account()
    with pytest.raises(error):
        account.deposit(amount)

@pytest.mark.parametrize('amount, error', [
    (0, ValueError),
    (-20, ValueError),
])
def test_deposit_invalid(amount, error):
    account = BankAccount(100)
    with pytest.raises(error):
        account.deposit(amount)

@pytest.mark.parametrize('amount, expected', [
    (20, 80),
])
def test_withdraw_ok(amount, expected):
    account = BankAccount(100)
    assert account.withdraw(amount) == expected

@pytest.mark.parametrize('amount, error', [
    (0, ValueError),
    (-10, ValueError),
    (200, ValueError),
])
def test_withdraw_invalid(amount, error):
    account = BankAccount(100)
    with pytest.raises(error):
        account.withdraw(amount)

def test_freeze_account():
    account = BankAccount(100)
    account.freeze_account()
    assert account.is_active == False

def test_unfreeze_account():
    account = BankAccount(100)
    account.freeze_account()
    account.unfreeze_account()
    assert account.is_active == True

@pytest.mark.parametrize('initial_balance, amount, expected', [
    (0, 50, 50),
])
def test_deposit_zero_balance(initial_balance, amount, expected):
    account = BankAccount(initial_balance)
    assert account.deposit(amount) == expected

@pytest.mark.parametrize('amount', [
    20,
])
def test_withdraw_frozen(amount):
    account = BankAccount(100)
    account.freeze_account()
    with pytest.raises(ValueError):
        account.withdraw(amount)