"""Import re and the exceptions"""
import re
from uc3m_money.account_management_exception import AccountManagementException


class Attribute():
    """Superclass for all attributes"""
    def __init__(self):
        self._attr_value = ""
        self._error_message = ""
        self._validation_pattern = r""

    def _validate(self, value):
        myregex = re.compile(self._validation_pattern)
        result = myregex.fullmatch(value)
        if not result:
            raise AccountManagementException(self._error_message)
        return value
    @property
    def value(self):
        return self._attr_value

    @value.setter
    def value(self, attr_value):
        self._attr_value = attr_value
