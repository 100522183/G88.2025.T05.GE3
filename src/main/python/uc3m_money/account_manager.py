"""Account manager module """
import json
from uc3m_money.account_management_exception import AccountManagementException
from uc3m_money.transfer_request import TransferRequest
from uc3m_money.account_deposit import AccountDeposit
from uc3m_money.iban_balance import IbanBalance
from uc3m_money.storage.transfers_json_store import TransfersJsonStore
from uc3m_money.storage.deposits_json_store import DepositsJsonStore
from uc3m_money.storage.balances_json_store import BalancesJsonStore


class AccountManager:
    """Class for providing the methods for managing the orders"""
    def __init__(self):
        pass

    #pylint: disable=too-many-arguments
    def transfer_request(self, from_iban: str,
                         to_iban: str,
                         concept: str,
                         transfer_type: str,
                         date: str,
                         amount: float)->str:
        """first method: receives transfer info and
        stores it into a file"""

        new_transfer_request = TransferRequest(from_iban=from_iban,
                                     to_iban=to_iban,
                                     transfer_concept=concept,
                                     transfer_type=transfer_type,
                                     transfer_date=date,
                                     transfer_amount=amount)

        transfer_store = TransfersJsonStore()
        transfer_store.add_item(new_transfer_request)
        return new_transfer_request.transfer_code


    def deposit_into_account(self, input_file:str)->str:
        """manages the deposits received for accounts"""
        try:
            with open(input_file, "r", encoding="utf-8", newline="") as file:
                deposit_data = json.load(file)
        except FileNotFoundError as ex:
            raise AccountManagementException("Error: file input not found") from ex
        except json.JSONDecodeError as ex:
            raise AccountManagementException("JSON Decode Error - Wrong JSON Format") from ex

        #check values of the file
        try:
            deposit_iban = deposit_data["IBAN"]
            deposit_amount = deposit_data["AMOUNT"]
        except KeyError as e:
            raise AccountManagementException("Error - Invalid Key in JSON") from e

        deposit_obj = AccountDeposit(to_iban=deposit_iban,
                                     deposit_amount=deposit_amount)

        deposit_store = DepositsJsonStore()
        deposit_store.add_item(deposit_obj)
        return deposit_obj.deposit_signature


    def calculate_balance(self, iban:str)->bool:
        """calculate the balance for a given iban"""
        iban_balance = IbanBalance(iban)

        balance_store = BalancesJsonStore()
        balance_store.add_item(iban_balance)
        return True
