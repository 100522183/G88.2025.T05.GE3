import datetime

from uc3m_money.Data.attr.attribute_iban import Iban
from uc3m_money.account_management_exception import AccountManagementException
import json
from uc3m_money.account_management_config import BALANCES_STORE_FILE, TRANSACTIONS_STORE_FILE
from datetime import datetime, timezone

class IbanBalance:
    def __init__(self, iban):
        self._iban = Iban(iban).value
        self.__last_balance_time = datetime.timestamp(datetime.now(timezone.utc))
        self.__balance = self.calculate_iban_balance()

    def calculate_iban_balance(self) -> bool:
        """calculate the balance for a given iban"""
        transaction_history = self.read_transactions_file()
        iban_found = False
        balance = 0
        for transaction in transaction_history:
            # print(transaction["IBAN"] + " - " + iban)
            if transaction["IBAN"] == self._iban:
                balance += float(transaction["amount"])
                iban_found = True
        if not iban_found:
            raise AccountManagementException("IBAN not found")
        return balance

    @staticmethod
    def read_transactions_file():
        """loads the content of the transactions file
        and returns a list"""
        try:
            with open(TRANSACTIONS_STORE_FILE, "r", encoding="utf-8", newline="") as file:
                input_list = json.load(file)
        except FileNotFoundError as ex:
            raise AccountManagementException("Wrong file  or file path") from ex
        except json.JSONDecodeError as ex:
            raise AccountManagementException("JSON Decode Error - Wrong JSON Format") from ex
        return input_list

    def to_json(self):
        return {"IBAN": self._iban,
                        "time": self.__last_balance_time,
                        "BALANCE": self.__balance}