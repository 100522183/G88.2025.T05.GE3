from uc3m_money.Data.attr.attributes import Attribute
from uc3m_money.account_management_exception import AccountManagementException


class Iban(Attribute):
    def __init__(self, attr_value):
        self._error_message = "Invalid IBAN format"
        self._validation_pattern = r"^ES[0-9]{22}"
        self._attr_value = self._validate(attr_value)

    def _validate(self, attr_value:str )->str:
        attr_value = super()._validate(attr_value)
        iban = attr_value
        original_code = iban[2:4]
        # replacing the control
        iban = iban[:2] + "00" + iban[4:]
        iban = iban[4:] + iban[:4]

        # Convertir el IBAN en una cadena numérica, reemplazando letras por números

        iban_replacements = {
            'A': '10', 'B': '11', 'C': '12', 'D': '13', 'E': '14',
            'F': '15', 'G': '16', 'H': '17', 'I': '18', 'J': '19',
            'K': '20', 'L': '21', 'M': '22', 'N': '23', 'O': '24',
            'P': '25', 'Q': '26', 'R': '27', 'S': '28', 'T': '29',
            'U': '30', 'V': '31', 'W': '32', 'X': '33', 'Y': '34',
            'Z': '35'
        }
        for letter in iban_replacements.keys():
            iban = iban.replace(letter, iban_replacements[letter])
        # Mover los cuatro primeros caracteres al final

        # Convertir la cadena en un número entero
        calculated_int_from_string = int(iban)

        # Calcular el módulo 97
        mod = calculated_int_from_string % 97

        # Calcular el dígito de control (97 menos el módulo)
        calculated_control_digit = 98 - mod

        if int(original_code) != calculated_control_digit:
            # print(calculated_control_digit)
            raise AccountManagementException("Invalid IBAN control digit")

        return attr_value