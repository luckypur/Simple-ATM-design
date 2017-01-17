import logging
import argparse

from person import Person
from atm import ATM
from use_cases import use_cases

parser = argparse.ArgumentParser()
parser.add_argument('-l', '--log', type=str, help='Log level', required=False, default=logging.INFO)
args = parser.parse_args()

if __name__ == "__main__":

    logging.basicConfig(level=args.log, format='%(message)s')
    logger = logging.getLogger(__name__)
    print("Notes are ordered in DESC order (1000, 500, 100) \n\n")

    for use_case in use_cases:
        logger.info('Person account balance: {}'.format(use_case['account_balance']))
        logger.info('No. of notes for each denomination: {}'.format(use_case['currency_number']))
        logger.info('Withdraw amount: {}'.format(use_case['amount']))

        ATM.currency_numbers = use_case['currency_number']
        atm = ATM()
        person = Person(use_case['account_balance'])
        logger.info(person.dispense(use_case['amount'], atm))
        print('\n', '------------', '\n')
