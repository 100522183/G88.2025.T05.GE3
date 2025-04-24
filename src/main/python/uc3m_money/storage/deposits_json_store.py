"""Import all the needed from JsonStore class and account_management_config"""
from uc3m_money.storage.json_store import JsonStore
from uc3m_money.account_management_config import DEPOSITS_STORE_FILE

class DepositsJsonStore(JsonStore):
    """Manages the deposits json store"""
    _file_name = DEPOSITS_STORE_FILE