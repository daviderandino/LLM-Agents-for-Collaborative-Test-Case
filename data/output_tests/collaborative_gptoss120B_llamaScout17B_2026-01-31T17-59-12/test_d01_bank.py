import pytest
from data.input_code.d01_bank import *

def test_init_default():
    account = BankAccount(0)
    assert account.balance == 0
    assert account.is_active

def test_init_positive():
    account = BankAccount(150)
    assert account.balance == 150
    assert account.is_active

@pytest.mark.parametrize("initial_balance", [-10, -5, -1])
def test_init_negative(initial_balance):
    with pytest.raises(ValueError):
        BankAccount(initial_balance)

@pytest.mark.parametrize('init_balance, amount, expected', [
    (100, 50, 150),
    (200, 20, 220),
])
def test_deposit_success(init_balance, amount, expected):
    account = BankAccount(init_balance)
    assert account.deposit(amount) == expected

@pytest.mark.parametrize('init_balance, amount', [
    (100, 0),
    (100, -10),
])
def test_deposit_nonpositive(init_balance, amount):
    account = BankAccount(init_balance)
    with pytest.raises(ValueError):
        account.deposit(amount)

def test_deposit_frozen():
    account = BankAccount(100)
    account.freeze_account()
    with pytest.raises(ValueError):
        account.deposit(30)

@pytest.mark.parametrize('init_balance, amount, expected', [
    (120, 40, 80),
    (150, 50, 100),
])
def test_withdraw_success(init_balance, amount, expected):
    account = BankAccount(init_balance)
    assert account.withdraw(amount) == expected

@pytest.mark.parametrize('init_balance, amount', [
    (80, 80),
    (100, 100),
])
def test_withdraw_equal_balance(init_balance, amount):
    account = BankAccount(init_balance)
    assert account.withdraw(amount) == 0

@pytest.mark.parametrize('init_balance, amount', [
    (50, 75),
    (20, 50),
])
def test_withdraw_insufficient(init_balance, amount):
    account = BankAccount(init_balance)
    with pytest.raises(ValueError):
        account.withdraw(amount)

@pytest.mark.parametrize('init_balance, amount', [
    (50, -5),
    (100, 0),
])
def test_withdraw_nonpositive(init_balance, amount):
    account = BankAccount(init_balance)
    with pytest.raises(ValueError):
        account.withdraw(amount)

def test_withdraw_frozen():
    account = BankAccount(70)
    account.freeze_account()
    with pytest.raises(ValueError):
        account.withdraw(20)

def test_freeze_unfreeze():
    account = BankAccount(30)
    account.freeze_account()
    assert not account.is_active
    account.unfreeze_account()
    assert account.is_active