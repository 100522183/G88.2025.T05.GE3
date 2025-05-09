"""Import all the needed from Attribute class the datetime and the exceptions"""
from uc3m_money.Data.attr.attributes import Attribute
from uc3m_money.account_management_exception import AccountManagementException
from datetime import datetime, timezone

class TransferDate(Attribute):
    """Manages the TransferDate attribute"""
    def __init__(self, attr_value):
        self._error_message = "Invalid date format"
        self._validation_pattern = r"^(([0-2]\d|3[0-1])\/(0\d|1[0-2])\/\d\d\d\d)$"
        self._attr_value = self._validate(attr_value)

    def _validate(self, attr_value):
        attr_value = super()._validate(attr_value)

        try:
            transfer_date = datetime.strptime(attr_value, "%d/%m/%Y").date()
        except ValueError as ex:
            raise AccountManagementException("Invalid date format") from ex

        if transfer_date < datetime.now(timezone.utc).date():
            raise AccountManagementException("Transfer date must be today or later.")

        if transfer_date.year < 2025 or transfer_date.year > 2050:
            raise AccountManagementException("Invalid date format")
        return attr_value
