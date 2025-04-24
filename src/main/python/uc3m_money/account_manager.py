"""Account manager module """
import json
from uc3m_money.account_management_exception import AccountManagementException
from uc3m_money.account_management_config import BALANCES_STORE_FILE

from uc3m_money.transfer_request import TransferRequest
from uc3m_money.account_deposit import AccountDeposit
from uc3m_money.iban_balance import IbanBalance
from uc3m_money.storage.transfers_json_store import TransfersJsonStore
from uc3m_money.storage.deposits_json_store import DepositsJsonStore


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

    @staticmethod
    def load_json_file(json_file:str)->list:
        """This method loads the json file and returns a list with its contents, if the file is empty,
        an empy list is returned
        :param json_file: the file that whose contents will be loaded"""
        try:
            with open(json_file, "r", encoding="utf-8", newline="") as file:
                transfer_history = json.load(file)
        except FileNotFoundError:
            transfer_history = []
        except json.JSONDecodeError as ex:
            raise AccountManagementException("JSON Decode Error - Wrong JSON Format") from ex
        return transfer_history

    def deposit_into_account(self, input_file:str)->str:
        """manages the deposits received for accounts"""
        try:
            with open(input_file, "r", encoding="utf-8", newline="") as file:
                deposit_data = json.load(file)
        except FileNotFoundError as ex:
            raise AccountManagementException("Error: file input not found") from ex
        except json.JSONDecodeError as ex:
            raise AccountManagementException("JSON Decode Error - Wrong JSON Format") from ex

        # comprobar valores del fichero
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
        try:
            with open(BALANCES_STORE_FILE, "r", encoding="utf-8", newline="") as file:
                balance_list = json.load(file)
        except FileNotFoundError:
            balance_list = []
        except json.JSONDecodeError as ex:
            raise AccountManagementException("JSON Decode Error - Wrong JSON Format") from ex

        balance_list.append(iban_balance.to_json())

        self.dump_data_into_json(BALANCES_STORE_FILE, balance_list)
        return True

    @staticmethod
    def dump_data_into_json(json_file:str, dump_data:list):
        """This method dumps the provided data into the specified json file
        :param json_file: the json file in which the data will be dumped
        :param dump_data: the data to be dumped"""
        try:
            with open(json_file, "w", encoding="utf-8", newline="") as file:
                json.dump(dump_data, file, indent=2)
        except FileNotFoundError as ex:
            raise AccountManagementException("Wrong file  or file path") from ex
        except json.JSONDecodeError as ex:
            raise AccountManagementException("JSON Decode Error - Wrong JSON Format") from ex
