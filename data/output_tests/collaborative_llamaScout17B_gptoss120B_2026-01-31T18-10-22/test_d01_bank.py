import pytest
from data.input_code.d01_bank import *

@pytest.fixture
def account():
    """Provides a fresh BankAccount with a balance of 100 for each test."""
    return BankAccount(initial_balance=100)

# -------------------- __init__ --------------------
@pytest.mark.parametrize(
    "initial_balance, expected_balance",
    [
        (100, 100),
        (0, 0),
    ],
    ids=["positive", "zero"],
)
def test_init_success(initial_balance, expected_balance):
    acc = BankAccount(initial_balance=initial_balance)
    assert acc.balance == expected_balance
    assert acc.is_active is True


@pytest.mark.parametrize(
    "initial_balance",
    [-10, -1],
    ids=["neg10", "neg1"],
)
def test_init_negative_raises(initial_balance):
    with pytest.raises(ValueError):
        BankAccount(initial_balance=initial_balance)


# -------------------- deposit --------------------
@pytest.mark.parametrize(
    "deposit_amount, expected_balance",
    [
        (50, 150),
        (1, 101),
    ],
    ids=["deposit_50", "deposit_1"],
)
def test_deposit_success(account, deposit_amount, expected_balance):
    result = account.deposit(deposit_amount)
    assert result == expected_balance
    assert account.balance == expected_balance


@pytest.mark.parametrize(
    "deposit_amount",
    [50],
    ids=["deposit_frozen"],
)
def test_deposit_frozen_raises(account, deposit_amount):
    account.freeze_account()
    with pytest.raises(ValueError):
        account.deposit(deposit_amount)


@pytest.mark.parametrize(
    "deposit_amount",
    [0, -5],
    ids=["deposit_zero", "deposit_negative"],
)
def test_deposit_nonpositive_raises(account, deposit_amount):
    with pytest.raises(ValueError):
        account.deposit(deposit_amount)


# -------------------- withdraw --------------------
@pytest.mark.parametrize(
    "withdraw_amount, expected_balance",
    [
        (20, 80),
        (100, 0),
    ],
    ids=["withdraw_20", "withdraw_100"],
)
def test_withdraw_success(account, withdraw_amount, expected_balance):
    result = account.withdraw(withdraw_amount)
    assert result == expected_balance
    assert account.balance == expected_balance


@pytest.mark.parametrize(
    "withdraw_amount",
    [20],
    ids=["withdraw_frozen"],
)
def test_withdraw_frozen_raises(account, withdraw_amount):
    account.freeze_account()
    with pytest.raises(ValueError):
        account.withdraw(withdraw_amount)


@pytest.mark.parametrize(
    "withdraw_amount",
    [0, -10],
    ids=["withdraw_zero", "withdraw_negative"],
)
def test_withdraw_nonpositive_raises(account, withdraw_amount):
    with pytest.raises(ValueError):
        account.withdraw(withdraw_amount)


def test_withdraw_insufficient_funds(account):
    with pytest.raises(ValueError):
        account.withdraw(200)


# -------------------- freeze / unfreeze --------------------
def test_freeze_and_unfreeze(account):
    account.freeze_account()
    assert account.is_active is False
    account.unfreeze_account()
    assert account.is_active is True