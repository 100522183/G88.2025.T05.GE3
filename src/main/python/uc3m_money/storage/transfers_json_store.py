"""Import all the needed from JsonStore class, account_management_config and the exceptions"""
from uc3m_money.storage.json_store import JsonStore
from uc3m_money.account_management_config import TRANSFERS_STORE_FILE
from uc3m_money.account_management_exception import AccountManagementException


class TransfersJsonStore(JsonStore._JsonStore):
    """Manages the transfers json store"""
    _file_name = TRANSFERS_STORE_FILE

    def add_item(self, item):
        """Adds an item to the list and checks if the item is already in the file
        :param item: The object whose json representation will be added to the list"""
        for transfer in self._data_list:
            if transfer == item.to_json():
                raise AccountManagementException("Duplicated transfer in transfer list")
        super().add_item(item)