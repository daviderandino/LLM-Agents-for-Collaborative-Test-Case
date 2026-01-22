import pytest
from data.input_code.d01_bank_account import *

@pytest.mark.parametrize(
    "initial_balance, expected_balance, expected_active",
    [
        (0, 0, True),          # TC01_INIT_DEFAULT
    ]
)
def test_init_default(initial_balance, expected_balance, expected_active):
    account = BankAccount(initial_balance)
    assert account.balance == expected_balance
    assert account.is_active == expected_active

def test_init_negative():
    with pytest.raises(ValueError):
        BankAccount(-10)          # TC02_INIT_NEGATIVE

@pytest.mark.parametrize(
    "initial_balance, amount, expected_balance",
    [
        (50, 20, 70),            # TC03_DEPOSIT_SUCCESS
    ]
)
def test_deposit_success(initial_balance, amount, expected_balance):
    account = BankAccount(initial_balance)
    assert account.deposit(amount) == expected_balance

def test_deposit_nonpositive():
    account = BankAccount(0)
    with pytest.raises(ValueError):
        account.deposit(0)        # TC04_DEPOSIT_NONPOSITIVE

def test_deposit_frozen():
    account = BankAccount(0)
    account.freeze_account()
    with pytest.raises(ValueError):
        account.deposit(10)       # TC05_DEPOSIT_FROZEN

@pytest.mark.parametrize(
    "initial_balance, amount, expected_balance",
    [
        (100, 30, 70),           # TC06_WITHDRAW_SUCCESS
    ]
)
def test_withdraw_success(initial_balance, amount, expected_balance):
    account = BankAccount(initial_balance)
    assert account.withdraw(amount) == expected_balance

def test_withdraw_nonpositive():
    account = BankAccount(100)
    with pytest.raises(ValueError):
        account.withdraw(0)       # TC07_WITHDRAW_NONPOSITIVE

def test_withdraw_insufficient():
    account = BankAccount(50)
    with pytest.raises(ValueError):
        account.withdraw(60)      # TC08_WITHDRAW_INSUFFICIENT

def test_withdraw_frozen():
    account = BankAccount(100)
    account.freeze_account()
    with pytest.raises(ValueError):
        account.withdraw(10)      # TC09_WITHDRAW_FROZEN

def test_freeze_account():
    account = BankAccount(0)
    account.freeze_account()
    assert account.is_active is False   # TC10_FREEZE_ACCOUNT

def test_unfreeze_account():
    account = BankAccount(0)
    account.freeze_account()
    account.unfreeze_account()
    assert account.is_active is True    # TC11_UNFREEZE_ACCOUNT