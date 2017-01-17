import logging

from settings import TRANSACTION_CHARGE, CURRENCY_DENOMINATIONS, MINIMUM_WITHDRAWAL

logger = logging.getLogger(__name__)


class ATM(object):
    """
    Class for performing atm transaction

    Cash dispensing algorithm supposed to dispense minimum amount
    of notes for a withdrawal
    """

    # order of Currency denomination is DESC sorted
    currency_denominations = CURRENCY_DENOMINATIONS

    # no of notes of each currency denomination
    currency_numbers = (0, 0, 0)
    total_amount = 0

    def __init__(self):
        ATM.total_amount = sum([i * j for i, j in zip(ATM.currency_denominations, ATM.currency_numbers)])
        self.withdraw_amount = 0
        # Protected property
        # to keep track of no of notes of each currency denomination that will serve the withdraw request
        self._note_count = []

    def withdraw(self, amount, person):
        """
        Withdraw given amount
        :person: consumer instance
        :return: account balance
        """
        self.withdraw_amount = amount

        if amount % MINIMUM_WITHDRAWAL == 0 and self.is_enough_amount() and person.is_dispense_possible(amount):
            return self._withdraw(person)

        logging.debug('Pre conditioned failed to satisfy the given request ')
        return person.account_balance

    def _withdraw(self, person):
        """
        protected method to actually make a withdrawal
        :person: consumer whose making a withdrawal
        :return account balance:
        """
        withdraw_amount = self.withdraw_amount
        # trying to make right combination of notes
        for currency_denomination, no_of_notes in zip(ATM.currency_denominations, ATM.currency_numbers):
            if currency_denomination <= withdraw_amount:
                withdraw_amount = self._set_note_count(currency_denomination, no_of_notes, withdraw_amount)
            else:
                self._note_count.append(0)

        return self._perform_withdrawal(person)

    def _perform_withdrawal(self, person):
        """
        Check if withdrawal is possible with given notes and return deducted/undeducted account balance

        :person: consumer whose making a withdrawal
        :return: account balance
        """
        if sum([cur_denom * notes for cur_denom, notes in
                zip(ATM.currency_denominations, tuple(self._note_count))]) == self.withdraw_amount:
            person.account_balance -= (TRANSACTION_CHARGE + self.withdraw_amount)
            ATM.total_amount -= self.withdraw_amount
            # update the no of notes of each type
            ATM.currency_numbers = tuple(available_note - this_withdrawal for available_note, this_withdrawal in
                                         zip(ATM.currency_numbers, tuple(self._note_count)))
            logging.debug('Notes selected: {}'.format(self._note_count))
            logging.debug('Remaining Note count: {}'.format(ATM.currency_numbers))
            logging.debug('Remaining balance in ATM: {}'.format(ATM.total_amount))

        # clear note count for another transaction *if required
        self._note_count = []
        return person.account_balance

    def _set_note_count(self, cur_denom, no_of_notes, withdraw_amount):
        """
        update note_count to reflect that how many notes of a particular currency denomination will
        be required to make a withdraw
        :param cur_denom: integer showing one of currency denomination
        :param no_of_notes: number of notes of cur_denom
        :param withdraw_amount: amount to perform the check
        :return: remaining withdraw amount
        """
        note_count = int(withdraw_amount / cur_denom)
        if no_of_notes > 0:
            notes = no_of_notes if note_count >= no_of_notes else note_count
            self._note_count.append(notes)
            return withdraw_amount - (cur_denom * notes)
        return withdraw_amount

    def is_enough_amount(self):
        """
        check if atm or user have enough balance
        :return: boolean showing yes/no
        """
        return not self.is_out_of_cash() and ATM.total_amount > self.withdraw_amount + TRANSACTION_CHARGE

    def is_out_of_cash(self):
        """
        check if atm have any cash at all
        :return:
        """
        return self.total_amount < MINIMUM_WITHDRAWAL
