import pytest
from data.input_code.d01_bank_account import BankAccount

@pytest.mark.parametrize('initial_balance, expected', [
    (100, None),
    (0, None)
])
def test_bank_account_init_success(initial_balance, expected):
    if expected is None:
        account = BankAccount(initial_balance)
        assert account.balance == initial_balance
    else:
        assert False, "Expected should be None for successful initialization"

def test_bank_account_init_error():
    with pytest.raises(ValueError):
        BankAccount(-10)

@pytest.mark.parametrize('initial_balance, amount, expected', [
    (100, 50, 150)
])
def test_bank_account_deposit_success(initial_balance, amount, expected):
    account = BankAccount(initial_balance)
    assert account.deposit(amount) == expected

@pytest.mark.parametrize('initial_balance, amount, expected_exception', [
    (100, 0, ValueError),
    (100, -20, ValueError)
])
def test_bank_account_deposit_error(initial_balance, amount, expected_exception):
    account = BankAccount(initial_balance)
    with pytest.raises(expected_exception):
        account.deposit(amount)

def test_bank_account_deposit_frozen():
    account = BankAccount(100)
    account.freeze_account()
    with pytest.raises(ValueError):
        account.deposit(50)

@pytest.mark.parametrize('initial_balance, amount, expected', [
    (100, 20, 80)
])
def test_bank_account_withdraw_success(initial_balance, amount, expected):
    account = BankAccount(initial_balance)
    assert account.withdraw(amount) == expected

@pytest.mark.parametrize('initial_balance, amount, expected_exception', [
    (100, 0, ValueError),
    (100, -10, ValueError),
    (100, 200, ValueError)
])
def test_bank_account_withdraw_error(initial_balance, amount, expected_exception):
    account = BankAccount(initial_balance)
    with pytest.raises(expected_exception):
        account.withdraw(amount)

def test_bank_account_withdraw_frozen():
    account = BankAccount(100)
    account.freeze_account()
    with pytest.raises(ValueError):
        account.withdraw(20)

def test_bank_account_freeze_unfreeze():
    account = BankAccount(100)
    account.freeze_account()
    assert not account.is_active
    account.unfreeze_account()
    assert account.is_active