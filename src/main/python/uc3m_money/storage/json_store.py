import json
from uc3m_money.account_management_exception import AccountManagementException


class JsonStore:
    _data_list = []
    _file_name = ""
    def __init__(self):
        self.load_list_from_file()

    def save_list_to_file(self):
        """saves the list in the store"""
        try:
            with open(self._file_name, "w", encoding = "utf-8", newline = "") as file:
                json.dump(self._data_list, file, indent = 2)
        except FileNotFoundError as ex:
            raise AccountManagementException("Wrong file or file path") from ex

    def load_list_from_file(self):
        """This method loads the json file and returns a list with its contents, if the file is empty,
                an empy list is returned"""
        try:
            with open(self._file_name, "r", encoding="utf-8", newline="") as file:
                self._data_list = json.load(file)
        except FileNotFoundError:
            self._data_list= []
        except json.JSONDecodeError as ex:
            raise AccountManagementException("JSON Decode Error - Wrong JSON Format") from ex

    def add_item(self, item):
        """Adds an item to the list
        :param item: The object whose json representation will be added to the list"""
        self.load_list_from_file()
        self._data_list.append(item.to_json())
        self.save_list_to_file()