import pytest
from data.input_code.01_bank import *

@pytest.mark.parametrize('initial_balance, expected_balance, expected_is_active', [
    (100, 100, True),
    (0, 0, True)
])
def test_init_success(initial_balance, expected_balance, expected_is_active):
    account = BankAccount(initial_balance)
    assert account.balance == expected_balance
    assert account.is_active == expected_is_active

def test_init_error():
    with pytest.raises(ValueError):
        BankAccount(-10)

@pytest.mark.parametrize('initial_balance, amount, expected_balance', [
    (50, 30, 80),
    (0, 10, 10)
])
def test_deposit_success(initial_balance, amount, expected_balance):
    account = BankAccount(initial_balance)
    assert account.deposit(amount) == expected_balance

@pytest.mark.parametrize('initial_balance, amount', [
    (50, 0),
    (50, -5)
])
def test_deposit_error_amount(initial_balance, amount):
    account = BankAccount(initial_balance)
    with pytest.raises(ValueError):
        account.deposit(amount)

def test_deposit_error_frozen():
    account = BankAccount(50)
    account.freeze_account()
    with pytest.raises(ValueError):
        account.deposit(10)

@pytest.mark.parametrize('initial_balance, amount, expected_balance', [
    (100, 40, 60),
    (70, 70, 0)
])
def test_withdraw_success(initial_balance, amount, expected_balance):
    account = BankAccount(initial_balance)
    assert account.withdraw(amount) == expected_balance

@pytest.mark.parametrize('initial_balance, amount', [
    (50, 0),
    (50, -10),
    (30, 50)
])
def test_withdraw_error(initial_balance, amount):
    account = BankAccount(initial_balance)
    with pytest.raises(ValueError):
        account.withdraw(amount)

def test_withdraw_error_frozen():
    account = BankAccount(50)
    account.freeze_account()
    with pytest.raises(ValueError):
        account.withdraw(10)

def test_freeze_account():
    account = BankAccount(0)
    account.freeze_account()
    assert account.is_active == False

def test_unfreeze_account():
    account = BankAccount(0)
    account.freeze_account()
    account.unfreeze_account()
    assert account.is_active == True