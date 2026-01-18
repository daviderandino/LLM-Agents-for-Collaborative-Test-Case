import pytest
from data.input_code.d01_bank_account import BankAccount

class TestBankAccount:
    def test_init_default(self):
        account = BankAccount()
        assert account.balance == 0
        assert account.is_active == True

    def test_init_custom(self):
        account = BankAccount(100)
        assert account.balance == 100
        assert account.is_active == True

    def test_init_negative(self):
        with pytest.raises(ValueError):
            BankAccount(-100)

    def test_deposit_positive(self):
        account = BankAccount()
        account.deposit(100)
        assert account.balance == 100


    def test_deposit_negative(self):
        account = BankAccount()
        with pytest.raises(ValueError):
            account.deposit(-100)

    def test_withdraw_positive(self):
        account = BankAccount(100)
        account.withdraw(50)
        assert account.balance == 50


    def test_withdraw_negative(self):
        account = BankAccount(100)
        with pytest.raises(ValueError):
            account.withdraw(-50)

    def test_withdraw_insufficient(self):
        account = BankAccount(100)
        with pytest.raises(ValueError):
            account.withdraw(150)

    def test_freeze_account(self):
        account = BankAccount()
        account.freeze_account()
        assert account.is_active == False

    def test_unfreeze_account(self):
        account = BankAccount()
        account.freeze_account()
        account.unfreeze_account()
        assert account.is_active == True

    def test_freeze_unfreeze_cycle(self):
        account = BankAccount()
        account.freeze_account()
        account.unfreeze_account()
        assert account.is_active == True
        account.freeze_account()
        assert account.is_active == False