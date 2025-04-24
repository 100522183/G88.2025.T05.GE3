"""Import all the needed from Attribute class and the exceptions"""
from uc3m_money.Data.attr.attributes import Attribute
from uc3m_money.account_management_exception import AccountManagementException


class DepositAmount(Attribute):
    """Manages the DepositAmount attribute"""
    def __init__(self, attr_value):
        self._error_message = "Error - Invalid deposit amount"
        self._validation_pattern = r"^EUR [0-9]{4}\.[0-9]{2}"
        self._attr_value = self._validate(attr_value)

    def _validate(self, attr_value):
        attr_value = super()._validate(attr_value)
        deposit_amount_as_float = float(attr_value[4:])
        if deposit_amount_as_float == 0:
            raise AccountManagementException("Error - Deposit must be greater than 0")
        return deposit_amount_as_float