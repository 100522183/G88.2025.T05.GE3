"""Import all the needed from JsonStore class and account_management_config"""
from uc3m_money.storage.json_store import JsonStore
from uc3m_money.account_management_config import BALANCES_STORE_FILE

class BalancesJsonStore(JsonStore._JsonStore):
    """Manages the balances json store"""
    _file_name = BALANCES_STORE_FILE