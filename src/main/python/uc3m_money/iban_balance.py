import datetime

from uc3m_money.Data.attr.attribute_iban import Iban
from uc3m.money.account_management_exception import AccountManagementException
import json
from uc3m_money.account_management_config import BALANCES_STORE_FILE
import time

class IbanBalance:
    def __init__(self, iban):
        self._iban = Iban(iban).value

    def calculate_balance(self, iban: str) -> bool:
        """calculate the balance for a given iban"""
        iban = self.validate_iban(iban)
        balance = self.sum_account_transactions(iban)

        try:
            with open(BALANCES_STORE_FILE, "r", encoding="utf-8", newline="") as file:
                balance_list = json.load(file)
        except FileNotFoundError:
            balance_list = []
        except json.JSONDecodeError as ex:
            raise AccountManagementException("JSON Decode Error - Wrong JSON Format") from ex

        balance_list.append(last_balance)

        self.dump_data_into_json(BALANCES_STORE_FILE, balance_list)
        return True

    def sum_account_transactions(self, iban):
        transaction_history = self.read_transactions_file()
        iban_found = False
        balance = 0
        for transaction in transaction_history:
            # print(transaction["IBAN"] + " - " + iban)
            if transaction["IBAN"] == iban:
                balance += float(transaction["amount"])
                iban_found = True
        if not iban_found:
            raise AccountManagementException("IBAN not found")
        return balance

    def to_json(self, balance):
        last_balance = {"IBAN": self._iban,
                        "time": datetime.timestamp(datetime.now(timezone.utc)),
                        "BALANCE": balance}
        return last_balance