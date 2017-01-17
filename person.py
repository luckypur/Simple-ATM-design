from settings import TRANSACTION_CHARGE


class Person(object):
    """
    Class to represent a Consumer

    this class will use atm object to interact with ATM
    """

    def __init__(self, account_balance):
        self.account_balance = account_balance

    def dispense(self, amount, atm):
        """
        dispense the amount from atm
        :param amount: amount that need to be dispensed
        :return: account balance
        """
        return atm.withdraw(amount, self)

    def is_dispense_possible(self, amount):
        """
        check if user have enough balance to perform a dispense
        :amount:
        :return: boolean showing yes/no
        """
        return self.account_balance > amount + TRANSACTION_CHARGE
