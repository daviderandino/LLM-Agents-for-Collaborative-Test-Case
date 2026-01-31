import pytest
from data.input_code.d01_bank import *

@pytest.mark.parametrize(
    "initial_balance, expected_balance, expected_is_active, expect_exception",
    [
        (0, 0, True, None),          # T1_INIT_DEFAULT
        (150, 150, True, None),      # T2_INIT_POSITIVE
        (-5, None, None, ValueError),# T3_INIT_NEGATIVE
    ],
)
def test_bank_account_init(initial_balance, expected_balance, expected_is_active, expect_exception):
    if expect_exception:
        with pytest.raises(expect_exception):
            BankAccount(initial_balance=initial_balance)
    else:
        account = BankAccount(initial_balance=initial_balance)
        assert account.balance == expected_balance
        assert account.is_active == expected_is_active

def test_deposit_success():
    account = BankAccount()
    result = account.deposit(40)  # T4_DEPOSIT_SUCCESS
    assert result == 40
    assert account.balance == 40

def test_deposit_zero():
    account = BankAccount()
    with pytest.raises(ValueError):  # T5_DEPOSIT_ZERO
        account.deposit(0)

def test_deposit_frozen():
    account = BankAccount()
    account.freeze_account()       # T6_DEPOSIT_FROZEN
    with pytest.raises(ValueError):
        account.deposit(10)

@pytest.mark.parametrize(
    "initial_balance, amount, expected_balance, expect_exception",
    [
        (80, 30, 50, None),          # T7_WITHDRAW_SUCCESS
        (60, 60, 0, None),           # T8_WITHDRAW_EQUAL_BALANCE
        (0, 0, None, ValueError),    # T9_WITHDRAW_ZERO
        (25, 50, None, ValueError),  # T10_WITHDRAW_INSUFFICIENT
        (40, 10, None, ValueError),  # T11_WITHDRAW_FROZEN
    ],
)
def test_withdraw(initial_balance, amount, expected_balance, expect_exception):
    account = BankAccount(initial_balance=initial_balance)
    if initial_balance == 40 and amount == 10:
        account.freeze_account()   # freeze before withdrawal for T11
    if expect_exception:
        with pytest.raises(expect_exception):
            account.withdraw(amount)
    else:
        result = account.withdraw(amount)
        assert result == expected_balance
        assert account.balance == expected_balance

def test_freeze_unfreeze():
    account = BankAccount()
    account.freeze_account()       # T12_FREEZE_UNFREEZE
    account.unfreeze_account()
    assert account.is_active is True