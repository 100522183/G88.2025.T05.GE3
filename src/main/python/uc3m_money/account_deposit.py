"""Contains the class OrderShipping"""
import json
from datetime import datetime, timezone
import hashlib
from uc3m_money.Data.attr.attribute_iban import Iban
from uc3m_money.Data.attr.attribute_deposit_amount import DepositAmount
from uc3m_money.account_management_exception import AccountManagementException

class AccountDeposit():
    """Class representing the information required for shipping of an order"""

    def __init__(self,
                 to_iban: str,
                 deposit_amount: float):
        self.__algorithm = "SHA-256"
        self.__type = "DEPOSIT"
        self.__to_iban = Iban(to_iban).value
        self.__deposit_amount = DepositAmount(deposit_amount).value
        justnow = datetime.now(timezone.utc)
        self.__deposit_date = datetime.timestamp(justnow)

    def to_json(self):
        """returns the object data in json format"""
        return {"alg": self.__algorithm,
                "type": self.__type,
                "to_iban": self.__to_iban,
                "deposit_amount": self.__deposit_amount,
                "deposit_date": self.__deposit_date,
                "deposit_signature": self.deposit_signature}

    def __signature_string(self):
        """Composes the string to be used for generating the key for the date"""
        return "{alg:" + str(self.__algorithm) + ",typ:" + str(self.__type) + ",iban:" + \
               str(self.__to_iban) + ",amount:" + str(self.__deposit_amount) + \
               ",deposit_date:" + str(self.__deposit_date) + "}"

    @property
    def to_iban(self):
        """Property that represents the product_id of the patient"""
        return self.__to_iban

    @to_iban.setter
    def to_iban(self, value):
        self.__to_iban = value

    @property
    def deposit_amount(self):
        """Property that represents the order_id"""
        return self.__deposit_amount
    @deposit_amount.setter
    def deposit_amount(self, value):
        self.__deposit_amount = value

    @property
    def deposit_date(self):
        """Property that represents the phone number of the client"""
        return self.__deposit_date
    @deposit_date.setter
    def deposit_date( self, value ):
        self.__deposit_date = value


    @property
    def deposit_signature( self ):
        """Returns the sha256 signature of the date"""
        return hashlib.sha256(self.__signature_string().encode()).hexdigest()

    @classmethod
    def load_deposit_from_file(cls, input_file):
        """classmethod for loading the deposit from file"""
        try:
            with open(input_file, "r", encoding="utf-8", newline="") as file:
                deposit_data = json.load(file)
        except FileNotFoundError as ex:
            raise AccountManagementException("Error: file input not found") from ex
        except json.JSONDecodeError as ex:
            raise AccountManagementException("JSON Decode Error - Wrong JSON Format") from ex
        # check values of the file
        try:
            deposit_iban = deposit_data["IBAN"]
            deposit_amount = deposit_data["AMOUNT"]
        except KeyError as e:
            raise AccountManagementException("Error - Invalid Key in JSON") from e
        return cls(deposit_iban, deposit_amount)
