"""Account manager module """
import re
import json
from datetime import datetime, timezone
from uc3m_money.account_management_exception import AccountManagementException
from uc3m_money.account_management_config import (TRANSFERS_STORE_FILE,
                                        DEPOSITS_STORE_FILE,
                                        TRANSACTIONS_STORE_FILE,
                                        BALANCES_STORE_FILE)

from uc3m_money.transfer_request import TransferRequest
from uc3m_money.account_deposit import AccountDeposit


class AccountManager:
    """Class for providing the methods for managing the orders"""
    def __init__(self):
        pass

    @staticmethod
    def validate_iban(iban_without_control_digits: str):
        """
    Calcula el dígito de control de un IBAN español.

    Args:
        iban_without_control_digits (str): El IBAN sin los dos últimos dígitos (dígito de control).

    Returns:
        str: El dígito de control calculado.
        """
        iban_regex = re.compile(r"^ES[0-9]{22}")
        result = iban_regex.fullmatch(iban_without_control_digits)
        if not result:
            raise AccountManagementException("Invalid IBAN format")
        iban = iban_without_control_digits
        original_code = iban[2:4]
        #replacing the control
        iban = iban[:2] + "00" + iban[4:]
        iban = iban[4:] + iban[:4]


        # Convertir el IBAN en una cadena numérica, reemplazando letras por números
        iban = (iban.replace('A', '10').replace('B', '11').
                replace('C', '12').replace('D', '13').replace('E', '14').
                replace('F', '15'))
        iban = (iban.replace('G', '16').replace('H', '17').
                replace('I', '18').replace('J', '19').replace('K', '20').
                replace('L', '21'))
        iban = (iban.replace('M', '22').replace('N', '23').
                replace('O', '24').replace('P', '25').replace('Q', '26').
                replace('R', '27'))
        iban = (iban.replace('S', '28').replace('T', '29').replace('U', '30').
                replace('V', '31').replace('W', '32').replace('X', '33'))
        iban = iban.replace('Y', '34').replace('Z', '35')

        # Mover los cuatro primeros caracteres al final

        # Convertir la cadena en un número entero
        calculated_int_from_string = int(iban)

        # Calcular el módulo 97
        mod = calculated_int_from_string % 97

        # Calcular el dígito de control (97 menos el módulo)
        calculated_control_digit = 98 - mod

        if int(original_code) != calculated_control_digit:
            #print(calculated_control_digit)
            raise AccountManagementException("Invalid IBAN control digit")

        return iban_without_control_digits

    @staticmethod
    def validate_concept(concept: str):
        """regular expression for checking the minimum and maximum length as well as
        the allowed characters and spaces restrictions
        there are other ways to check this"""
        conecept_regex = re.compile(r"^(?=^.{10,30}$)([a-zA-Z]+(\s[a-zA-Z]+)+)$")

        result = conecept_regex.fullmatch(concept)
        if not result:
            raise AccountManagementException ("Invalid concept format")

    @staticmethod
    def validate_transfer_date(transfer_date_string):
        """validates the arrival date format  using regex"""
        transfer_date_regex = re.compile(r"^(([0-2]\d|3[0-1])\/(0\d|1[0-2])\/\d\d\d\d)$")
        result = transfer_date_regex.fullmatch(transfer_date_string)
        if not result:
            raise AccountManagementException("Invalid date format")

        try:
            transfer_date = datetime.strptime(transfer_date_string, "%d/%m/%Y").date()
        except ValueError as ex:
            raise AccountManagementException("Invalid date format") from ex

        if transfer_date < datetime.now(timezone.utc).date():
            raise AccountManagementException("Transfer date must be today or later.")

        if transfer_date.year < 2025 or transfer_date.year > 2050:
            raise AccountManagementException("Invalid date format")
        return transfer_date_string

    @staticmethod
    def validate_amount(amount: str):
        """This method verifies that the provided amount is valid
        :param amount: Amount to be verified"""
        try:
            amount_as_float = float(amount)
        except ValueError as exc:
            raise AccountManagementException("Invalid transfer amount") from exc
        amount_as_string = str(amount_as_float)
        if '.' in amount_as_string:
            decimales = len(amount_as_string.split('.')[1])
            if decimales > 2:
                raise AccountManagementException("Invalid transfer amount")
        if amount_as_float < 10 or amount_as_float > 10000:
            raise AccountManagementException("Invalid transfer amount")

    @staticmethod
    def validate_type(transfer_type: str):
        """This method verifies if the type of a transfer is valid
        :param transfer_type; type to be verified"""
        transfer_type_regex = re.compile(r"(ORDINARY|INMEDIATE|URGENT)")
        result = transfer_type_regex.fullmatch(transfer_type)
        if not result:
            raise AccountManagementException("Invalid transfer type")

    #pylint: disable=too-many-arguments
    def transfer_request(self, from_iban: str,
                         to_iban: str,
                         concept: str,
                         transfer_type: str,
                         date: str,
                         amount: float)->str:
        """first method: receives transfer info and
        stores it into a file"""
        self.validate_type(transfer_type)
        self.validate_transfer_date(date)
        self.validate_amount(amount)

        new_transfer_request = TransferRequest(from_iban=from_iban,
                                     to_iban=to_iban,
                                     transfer_concept=concept,
                                     transfer_type=transfer_type,
                                     transfer_date=date,
                                     transfer_amount=amount)

        transfer_history = self.load_json_file(TRANSFERS_STORE_FILE)

        for transfer in transfer_history:
            if ((transfer["from_iban"] == new_transfer_request.from_iban and
                    transfer["to_iban"] == new_transfer_request.to_iban and
                    transfer["transfer_date"] == new_transfer_request.transfer_date)):
                    if (transfer["transfer_amount"] == new_transfer_request.transfer_amount and
                    transfer["transfer_concept"] == new_transfer_request.transfer_concept and
                    transfer["transfer_type"] == new_transfer_request.transfer_type):
                        raise AccountManagementException("Duplicated transfer in transfer list")

        transfer_history.append(new_transfer_request.to_json())
        self.dump_data_into_json(TRANSFERS_STORE_FILE, transfer_history)
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


        deposit_iban = self.validate_iban(deposit_iban)
        amount_regex = re.compile(r"^EUR [0-9]{4}\.[0-9]{2}")
        result = amount_regex.fullmatch(deposit_amount)
        if not result:
            raise AccountManagementException("Error - Invalid deposit amount")

        deposit_amount_as_float = float(deposit_amount[4:])
        if deposit_amount_as_float == 0:
            raise AccountManagementException("Error - Deposit must be greater than 0")

        deposit_obj = AccountDeposit(to_iban=deposit_iban,
                                     deposit_amount=deposit_amount_as_float)

        deposits_history = self.load_json_file(DEPOSITS_STORE_FILE)
        deposits_history.append(deposit_obj.to_json())

        self.dump_data_into_json(DEPOSITS_STORE_FILE, deposits_history)

        return deposit_obj.deposit_signature

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


    def calculate_balance(self, iban:str)->bool:
        """calculate the balance for a given iban"""
        iban = self.validate_iban(iban)
        transaction_history = self.read_transactions_file()
        iban_found = False
        balance = 0
        for transaction in transaction_history:
            #print(transaction["IBAN"] + " - " + iban)
            if transaction["IBAN"] == iban:
                balance += float(transaction["amount"])
                iban_found = True
        if not iban_found:
            raise AccountManagementException("IBAN not found")

        last_balance = {"IBAN": iban,
                        "time": datetime.timestamp(datetime.now(timezone.utc)),
                        "BALANCE": balance}

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
