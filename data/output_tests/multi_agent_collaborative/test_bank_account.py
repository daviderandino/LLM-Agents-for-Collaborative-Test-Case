import pytest
from data.input_code.bank_account import BankAccount

@pytest.fixture
def bank_account():
    return BankAccount()

def test_create_new_bank_account_with_positive_initial_balance(bank_account):
    assert bank_account.balance == 0
    assert bank_account.is_active is True

def test_create_new_bank_account_with_negative_initial_balance():
    with pytest.raises(ValueError):
        BankAccount(-10)

def test_deposit_positive_amount_into_active_account(bank_account):
    bank_account.deposit(10)
    assert bank_account.balance == 10

def test_deposit_non_positive_amount_into_active_account():
    bank_account = BankAccount()
    with pytest.raises(ValueError):
        bank_account.deposit(-10)

def test_withdraw_positive_amount_from_active_account_with_sufficient_funds(bank_account):
    bank_account.deposit(10)
    bank_account.withdraw(5)
    assert bank_account.balance == 5

def test_withdraw_non_positive_amount_from_active_account():
    bank_account = BankAccount()
    with pytest.raises(ValueError):
        bank_account.withdraw(-10)

def test_withdraw_more_than_available_balance_from_active_account():
    bank_account = BankAccount()
    bank_account.deposit(10)
    with pytest.raises(ValueError):
        bank_account.withdraw(20)

def test_unfreeze_frozen_account(bank_account):
    bank_account.freeze_account()
    bank_account.unfreeze_account()
    assert bank_account.is_active is True

def test_deposit_into_frozen_account():
    bank_account = BankAccount()
    bank_account.freeze_account()
    with pytest.raises(ValueError):
        bank_account.deposit(10)

def test_withdraw_from_frozen_account():
    bank_account = BankAccount()
    bank_account.freeze_account()
    with pytest.raises(ValueError):
        bank_account.withdraw(10)

def test_unfreeze_already_active_account(bank_account):
    assert bank_account.is_active is True
    bank_account.unfreeze_account()
    assert bank_account.is_active is True