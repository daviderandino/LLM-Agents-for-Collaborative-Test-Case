import pytest
from data.input_code.d01_bank import *

@pytest.mark.parametrize('initial_balance, expected', [
    (100, None)
])
def test_bank_account_init_success(initial_balance, expected):
    account = BankAccount(initial_balance)
    assert account.balance == initial_balance
    assert account.is_active

def test_bank_account_init_error():
    with pytest.raises(ValueError):
        BankAccount(-1)

@pytest.mark.parametrize('amount, expected', [
    (50, 150)
])
def test_bank_account_deposit_success(amount, expected):
    account = BankAccount(100)
    assert account.deposit(amount) == expected

@pytest.mark.parametrize('amount', [
    0, -1
])
def test_bank_account_deposit_error(amount):
    account = BankAccount(100)
    with pytest.raises(ValueError):
        account.deposit(amount)

def test_bank_account_deposit_frozen():
    account = BankAccount(100)
    account.freeze_account()
    with pytest.raises(ValueError):
        account.deposit(50)

@pytest.mark.parametrize('amount, expected', [
    (20, 80)
])
def test_bank_account_withdraw_success(amount, expected):
    account = BankAccount(100)
    assert account.withdraw(amount) == expected

@pytest.mark.parametrize('amount', [
    0, -1
])
def test_bank_account_withdraw_error(amount):
    account = BankAccount(100)
    with pytest.raises(ValueError):
        account.withdraw(amount)

def test_bank_account_withdraw_insufficient_funds():
    account = BankAccount(100)
    with pytest.raises(ValueError):
        account.withdraw(200)

def test_bank_account_withdraw_frozen():
    account = BankAccount(100)
    account.freeze_account()
    with pytest.raises(ValueError):
        account.withdraw(50)

def test_bank_account_freeze_account():
    account = BankAccount(100)
    account.freeze_account()
    assert not account.is_active

def test_bank_account_unfreeze_account():
    account = BankAccount(100)
    account.freeze_account()
    account.unfreeze_account()
    assert account.is_active