import json

import os

from object import Dialog


def get_dialog(user_id):
    with open('data.txt') as data_file:
        data = json.loads(data_file.read())
        if str(user_id) in data:
            dialog = Dialog()
            dialog.__dict__ = data[str(user_id)]
            return dialog
        else:
            return None


def store_dialog(dialog):
    with open('data.txt') as data_file:
        data = json.loads(data_file.read())
    data[str(dialog.user_id)] = dialog.__dict__
    with open('data_tmp.txt', 'w') as data_file:
        json.dump(data, data_file, sort_keys=True, indent=4)
    if os.path.exists('data.txt'):
        os.remove('data.txt')
    os.rename("data_tmp.txt", "data.txt")
