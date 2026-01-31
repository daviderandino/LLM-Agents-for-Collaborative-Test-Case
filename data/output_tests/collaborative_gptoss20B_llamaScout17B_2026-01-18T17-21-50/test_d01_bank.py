import pytest
from data.input_code.d01_bank import BankAccount

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
        BankAccount(-1)

@pytest.mark.parametrize('initial_balance, amount, expected', [
    (0, 50, 50),
    (100, 20, 120)
])
def test_deposit_success(initial_balance, amount, expected):
    account = BankAccount(initial_balance)
    assert account.deposit(amount) == expected

@pytest.mark.parametrize('initial_balance, amount, expected', [
    (0, 0, ValueError),
    (0, -10, ValueError),
    (0, None, TypeError),
    (0, "", TypeError),
    (0, [], TypeError)
])
def test_deposit_error(initial_balance, amount, expected):
    account = BankAccount(initial_balance)
    if expected == TypeError:
        with pytest.raises(TypeError):
            account.deposit(amount)
    else:
        with pytest.raises(ValueError):
            account.deposit(amount)

@pytest.mark.parametrize('initial_balance, amount, expected', [
    (50, 20, 30),
    (100, 50, 50)
])
def test_withdraw_success(initial_balance, amount, expected):
    account = BankAccount(initial_balance)
    assert account.withdraw(amount) == expected

@pytest.mark.parametrize('initial_balance, amount, expected', [
    (50, 0, ValueError),
    (50, -5, ValueError),
    (50, None, TypeError),
    (50, "", TypeError),
    (50, [], TypeError),
    (50, 100, ValueError)
])
def test_withdraw_error(initial_balance, amount, expected):
    account = BankAccount(initial_balance)
    if expected == TypeError:
        with pytest.raises(TypeError):
            account.withdraw(amount)
    else:
        with pytest.raises(ValueError):
            account.withdraw(amount)

def test_freeze_account():
    account = BankAccount(0)
    account.freeze_account()
    assert account.is_active == False

def test_unfreeze_account():
    account = BankAccount(0)
    account.freeze_account()
    account.unfreeze_account()
    assert account.is_active == True

def test_deposit_on_frozen_account():
    account = BankAccount(0)
    account.freeze_account()
    with pytest.raises(ValueError):
        account.deposit(50)

def test_withdraw_on_frozen_account():
    account = BankAccount(50)
    account.freeze_account()
    with pytest.raises(ValueError):
        account.withdraw(20)