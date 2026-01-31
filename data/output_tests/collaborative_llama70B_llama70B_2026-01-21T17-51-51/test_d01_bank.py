import pytest
from data.input_code.d01_bank import *

@pytest.mark.parametrize('initial_balance, expected', [
    (100, None)
])
def test_init_success(initial_balance, expected):
    account = BankAccount(initial_balance)
    assert account.balance == initial_balance

def test_init_error():
    with pytest.raises(ValueError):
        BankAccount(-100)

@pytest.mark.parametrize('amount, expected', [
    (50, 150)
])
def test_deposit_success(amount, expected):
    account = BankAccount(100)
    assert account.deposit(amount) == expected

@pytest.mark.parametrize('amount', [
    0
])
def test_deposit_error_nonpos(amount):
    account = BankAccount(100)
    with pytest.raises(ValueError):
        account.deposit(amount)

def test_deposit_error_frozen():
    account = BankAccount(100)
    account.freeze_account()
    with pytest.raises(ValueError):
        account.deposit(50)

@pytest.mark.parametrize('amount, expected', [
    (50, 50)
])
def test_withdraw_success(amount, expected):
    account = BankAccount(100)
    assert account.withdraw(amount) == expected

@pytest.mark.parametrize('amount', [
    0
])
def test_withdraw_error_nonpos(amount):
    account = BankAccount(100)
    with pytest.raises(ValueError):
        account.withdraw(amount)

def test_withdraw_error_frozen():
    account = BankAccount(100)
    account.freeze_account()
    with pytest.raises(ValueError):
        account.withdraw(50)

def test_withdraw_error_insuff():
    account = BankAccount(100)
    with pytest.raises(ValueError):
        account.withdraw(150)

def test_freeze_account():
    account = BankAccount(100)
    account.freeze_account()
    assert not account.is_active

def test_unfreeze_account():
    account = BankAccount(100)
    account.freeze_account()
    account.unfreeze_account()
    assert account.is_active