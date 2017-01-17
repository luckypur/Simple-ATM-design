import unittest
from atm import ATM
from person import Person
from settings import MINIMUM_WITHDRAWAL, TRANSACTION_CHARGE

THOUSANDS, FIVE_HUNDREDS, HUNDREDS = (5, 5, 5)


class AtmAssertion:
    """
    custom class to check account balance dose not change
    """

    def assertAccountBalanceUnchanged(self):
        """
        check if given amount is same as account balance
        """
        if self.account_balance != self.person.account_balance:
            raise AssertionError()


class AtmTestCase(unittest.TestCase, AtmAssertion):
    """
    class to test all functionality of atm.
    """

    def setUp(self):
        """
        create initial instances on which all test will be performed
        :return:
        """
        self.account_balance = 15000
        self.person = Person(self.account_balance)
        ATM.currency_numbers = (THOUSANDS, FIVE_HUNDREDS, HUNDREDS)
        self.atm = ATM()
        self.atm_balance = self.atm.total_amount

    def test_unsufficient_balance(self):
        """
        test if person have sufficient balance
        :return:
        """
        self.person.dispense(self.account_balance + 10, self.atm)
        self.assertAccountBalanceUnchanged()

    def test_unsupported_amount(self):
        """
        test withdrawal amount should be multiple of/greater then MINIMUM_WITHDRAWAL
        :return:
        """
        self.person.dispense(MINIMUM_WITHDRAWAL - 50, self.atm)
        self.assertAccountBalanceUnchanged()
        self.person.dispense(MINIMUM_WITHDRAWAL + 50, self.atm)
        self.assertAccountBalanceUnchanged()

    def test_excess_amount(self):
        """
        test withdrawal with bigger amount then atm have
        :return:
        """
        self.person.dispense(self.atm.total_amount + 10, self.atm)
        self.assertAccountBalanceUnchanged()

    def test_all_money_withdrawal(self):
        """
        test withdrawal of all amount
        :return:
        """
        # then there will be no amount for transaction charge
        self.person.dispense(self.person.account_balance, self.atm)
        self.assertAccountBalanceUnchanged()

    def test_transaction_charge(self):
        """
        test if transaction charge is being deducted
        :return:
        """
        withdraw_amount = 100
        self.person.dispense(withdraw_amount, self.atm)
        self.assertEqual(self.person.account_balance,
                         self.account_balance - (withdraw_amount + TRANSACTION_CHARGE))

    def test_atm_balance(self):
        """
        test if transaction charge is being deducted
        :return:
        """
        withdraw_amount = 700
        self.person.dispense(withdraw_amount, self.atm)
        self.assertEqual(self.atm.total_amount, self.atm_balance - withdraw_amount)

    def test_availability_of_notes(self):
        """
        test if right combination of notes are present to serve the request
        :return:
        """
        ATM.currency_numbers = (THOUSANDS, FIVE_HUNDREDS, 3)
        self.atm = ATM()
        withdraw_amount = 400
        self.person.dispense(withdraw_amount, self.atm)
        self.assertAccountBalanceUnchanged()

    def test_note_count(self):
        """
        test if notes are being selected as expected
        :return:
        """
        withdraw_amount = 2800
        self.person.dispense(withdraw_amount, self.atm)
        self.assertEqual(ATM.currency_numbers, (THOUSANDS - 2, FIVE_HUNDREDS - 1, HUNDREDS - 3))


if __name__ == "__main__":
    unittest.main()
