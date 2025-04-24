"""Account manager module """
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
        deposit_obj = AccountDeposit.load_deposit_from_file(input_file)
        deposit_store = DepositsJsonStore()
        deposit_store.add_item(deposit_obj)
        return deposit_obj.deposit_signature


    def calculate_balance(self, iban:str)->bool:
        """calculate the balance for a given iban"""
        iban_balance = IbanBalance(iban)

        balance_store = BalancesJsonStore()
        balance_store.add_item(iban_balance)
        return True
