"""Import all the needed from Attribute class"""
from uc3m_money.Data.attr.attributes import Attribute

class Type(Attribute):
    """Manages the Type attribute"""
    def __init__(self, attr_value):
        self._error_message = "Invalid transfer type"
        self._validation_pattern = r"(ORDINARY|INMEDIATE|URGENT)"
        self._attr_value = self._validate(attr_value)