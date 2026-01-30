import pytest
from data.input_code.01_bank import *

# -------------------- __init__ --------------------
@pytest.mark.parametrize(
    "initial_balance, expected_balance, expected_active, expect_exception",
    [
        (0, 0, True, None),          # default initialization
        (-10, None, None, ValueError)  # negative balance raises
    ]
)
def test_bank_account_init(initial_balance, expected_balance, expected_active, expect_exception):
    if expect_exception:
        with pytest.raises(expect_exception):
            BankAccount(initial_balance=initial_balance)
    else:
        acct = BankAccount(initial_balance=initial_balance)
        assert acct.balance == expected_balance
        assert acct.is_active is expected_active


# -------------------- deposit --------------------
@pytest.mark.parametrize(
    "init_balance, pre_action, amount, expected_balance, expect_exception",
    [
        (0, None, 50, 50, None),                     # normal deposit
        (0, None, 0, None, ValueError),              # zero amount
        (0, "freeze_account", 10, None, ValueError)  # frozen account
    ]
)
def test_bank_account_deposit(init_balance, pre_action, amount, expected_balance, expect_exception):
    acct = BankAccount(initial_balance=init_balance)
    if pre_action == "freeze_account":
        acct.freeze_account()
    if expect_exception:
        with pytest.raises(expect_exception):
            acct.deposit(amount)
    else:
        result = acct.deposit(amount)
        assert result == expected_balance
        assert acct.balance == expected_balance


# -------------------- withdraw --------------------
@pytest.mark.parametrize(
    "init_balance, pre_action, amount, expected_balance, expect_exception",
    [
        (100, None, 40, 60, None),                     # normal withdrawal
        (30, None, 50, None, ValueError),              # insufficient funds
        (30, None, 0, None, ValueError),               # zero amount
        (30, "freeze_account", 10, None, ValueError)   # frozen account
    ]
)
def test_bank_account_withdraw(init_balance, pre_action, amount, expected_balance, expect_exception):
    acct = BankAccount(initial_balance=init_balance)
    if pre_action == "freeze_account":
        acct.freeze_account()
    if expect_exception:
        with pytest.raises(expect_exception):
            acct.withdraw(amount)
    else:
        result = acct.withdraw(amount)
        assert result == expected_balance
        assert acct.balance == expected_balance


# -------------------- freeze / unfreeze --------------------
def test_freeze_and_unfreeze_account():
    acct = BankAccount(initial_balance=0)

    # freeze
    acct.freeze_account()
    assert acct.is_active is False

    # unfreeze
    acct.unfreeze_account()
    assert acct.is_active is True