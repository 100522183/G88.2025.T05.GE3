from uc3m_money.Data.attr.attributes import Attribute
from uc3m_money.account_management_exception import AccountManagementException


class TransferAmount(Attribute):
    def __init__(self, attr_value):
        self._error_message = "Invalid transfer amount"
        self._validation_pattern = None
        self._attr_value = self._validate(attr_value)

    def _validate(self, attr_value):
        try:
            amount_as_float = float(attr_value)
        except ValueError as exc:
            raise AccountManagementException(self._error_message) from exc
        amount_as_string = str(amount_as_float)
        if '.' in amount_as_string:
            decimales = len(amount_as_string.split('.')[1])
            if decimales > 2:
                raise AccountManagementException(self._error_message)
        if amount_as_float < 10 or amount_as_float > 10000:
            raise AccountManagementException(self._error_message)
        return attr_value