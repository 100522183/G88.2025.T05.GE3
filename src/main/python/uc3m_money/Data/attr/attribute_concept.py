"""Import all the needed from Attribute class"""
from uc3m_money.Data.attr.attributes import Attribute

class Concept(Attribute):
    """Manages the Concept attribute"""
    def __init__(self, attr_value):
        self._error_message = "Invalid concept format"
        self._validation_pattern = r"^(?=^.{10,30}$)([a-zA-Z]+(\s[a-zA-Z]+)+)$"
        self._attr_value = self._validate(attr_value)