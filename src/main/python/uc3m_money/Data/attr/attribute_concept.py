from uc3m_money.Data.attr.attributes import Attribute

class Concept(Attribute):
    def __init__(self, attr_value):
        self._error_message = "Invalid concept format"
        self._validation_pattern = r"^(?=^.{10,30}$)([a-zA-Z]+(\s[a-zA-Z]+)+)$"
        self._attr_value = self._validate(attr_value)